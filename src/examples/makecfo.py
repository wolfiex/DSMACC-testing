import pandas as pd
import os,re
import numpy as np

filen = 'clfo/ClearFlo_SUMMER_iop_15_min_merges_sep_2014.xls'
path = ''+ filen.split('.')[0]
df  = pd.read_excel(filen)

os.system('mkdir '+path)
os.system('touch '+path+'/empty')
os.system('rm '+path+'/*')

df = df[df.columns[:list(df.columns).index('Leicester spec rad photolysis rates (all s-1)')]]

cols = [i.replace(' / ','_') for i in df.columns]
df.columns = cols

remove = [
"total RO2_molec cm-3",
"RO2i_molec cm-3",
"OH reactivity_s-1",
"C6 alip",
"C7 alip",
"C8 alip",
"C9 alip",
"C10 alip",
"C11 alip",
"C12 alip",
"C13 alip",
"C4 mono aro",
"monoterpenes",
"2dgc (all ppbv)",
"U-3",
"U-4",
"t-2 pentene",
"U-5",
"1  pentene",
"U-6",
"U-7",
"U-8",
"U-9",
"U-10",
"U2",
"U-1",
"DP_oC",
"Press_mbar",
"Wind sp (local)_ms-1",
"Solar_Wm-2",
"WindDir (local)",
"Wind dir (BT tower)",
"GCFID (All ppb)",
#"total NOy_ppbv"
]


df = df[list(set(df.columns)-set(remove))]



mcm = pd.read_csv('../../mechanisms/useful/smiles_mined.csv')

test = lambda x :  mcm[mcm.name==x]


mcmd ={}
for i in mcm.iterrows():
    i=dict(i[1])
    mcmd[i['name']]=i['name']
    try:

            for j in i['synonyms'].replace(' ','').split(';'):
                mcmd[j.upper()]=i['name']
    except Exception as e:
        #print e
        None

mcmd['Formaldehydeppbv'.upper()]='HCHO'
mcmd['Acetate,ethyl-'.upper()]='ETHACET'
mcmd['cis-2-butene'.upper()]='BUT1ENE'
mcmd['TRANS-2-butene'.upper()]='BUT1ENE'




keep=[['PXYL+MXYL','m+p-xylene'],['NOY','total NOy_ppbv']]
dismiss=[]

for i in df.columns:
    try:
        keep.append([mcmd[i.replace(' ','').split('_')[0].split('.')[0].upper()],i])

    except Exception as e:
        print e

        try:
                v = i.upper().replace(' ','').split(',')
                bt =len(re.findall(r'-',','.join(v[1:])))

                if len(v)>1:
                    if bt>1:
                        keep.append([mcmd[','.join(v[1:])[:-1]+v[0]],i])
                    else:
                        keep.append([mcmd[v[1]+v[0]],i])
                else:
                    keep.append([mcmd[v[0].replace('-','').replace('ppbv','')],i])

        except Exception as e:
                print e
                dismiss.append(i)


keep = np.array(keep)

index = df['start time of averaging period_UTC'].iloc[:]
df.set_index(['start time of averaging period_UTC'])
df = df._get_numeric_data()

#merge columns after matcyh
keepcol = keep[:,1]
df = df[filter(lambda x: x in keep, df.columns)]

keepcol = dict(zip(keep[:,1],keep[:,0]))
df.columns = df.columns.map(lambda x: keepcol[x])



df = df.groupby(by=df.columns, axis=1).mean()
df['index'] = pd.to_datetime(index).map(lambda x: int(x.hour))

'''
steps = 4

def even (x):
    if x>0: return x
    elif(x%steps==0): return x
    else: return x+1
    
for i in xrange(steps):    
    df['index'] = df['index'].map(even)
    
'''    
    
print df['index']

df = df.groupby(['index']).mean()


##### SMoothing
for repeat in xrange(5):
    for i in range(len(df)):
        df.iloc[i] = df.iloc[[i-1,i,1+1]].mean(axis = 0)









correctorvalue = {'ppbv':1,'pptv':1e-12*1e+9,'molec cm-3':1e+9}
multiply=[]
for i in cols:
    if '_' in i:
        try:
            j = i.split('_')
            multiply.append([mcmd[j[0].upper()],j[-1]])
        except:None

#molecules cm3
df = df*1e-9
for i in multiply:
    j=i[0]
    df[j] = df[j]*correctorvalue[i[1]]


df.to_csv('ClearFloDiurnal.csv')
for i in df.columns:
    df[i].to_csv(path+'/'+i+'_units.csv')

print 'done',df.mean()
