'''
This script reads a csv (or excel) file from a field campaign and then applies a feed forward (simple) neural network to generate a mean MONTHly diurnal for the entirety of the data. 

Input arguments: <Str:filename(s)> <Bool:all columns>

File structure:
 1. Species must contain 'ppbv' or 'pptv' after their names to be considered unless the optional second argument to the script is supplied, and set to 'True'
 2. A 'date' column must be supplied with the format of xxxx/mm/xxxx hh:mm:xx or 
xxxx-mm-xxxx hh:mm:xx, where x is not considered in the parsing. 

Missing/data with gaps works is fine - and is why this program was created!

Requirements:
- sklearn
- pandas
- matplotlib
- xlrd (if using excel)

###############

This script was developed as part of the PhD of Daniel Ellis at the university of York. An aim to make it universal (for all experimental data) has been taken, and it is yet to be tidied. If any tweaks are required feel free to update it and submit a pull request detailing any of the changes made. 

If used please cite the DSMACC repository doi <insert here> to which the script belongs and my thesis itself <insert link here>. 

##############

Author: daniel.ellis@york.ac.uk

'''

import sys,os,re
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
np.random.seed(42)
mpl.use('Agg')#headless

df = pd.DataFrame()

f = list(filter(lambda x : x != 'True',sys.argv[1:]))

for entry in f:
    try:
        newdf = pd.read_csv(entry)
    except:
        newdf = pd.read_excel(entry)
        
    # make everything upper case    
    newdf.columns = [str(i).upper() for i in newdf.columns]

        
    newdf = newdf[newdf.columns[newdf.count() > 0]]
        
    if len(df)<1: 
        df = newdf.copy()
    elif newdf.shape[1] == df.shape[1]:
        print('concat')
        df = pd.concat([df,newdf],axis=0) 
    elif newdf.shape[0] == df.shape[0]:
        print ('merge')
        temp = df.merge(newdf, on='DATE')
        if len(temp)> 0:
            df = temp.copy()
        else:
            print ('WARNING: column concat - may produce incorrect results')
            df = pd.concat([df,newdf],axis=1) 
            

#duplicate columns - rare but it occasionally happens

try:
    for dc in [i[0] for i in (df.columns.value_counts()>1).iteritems() if i[1]]   :
        
        if dc == 'DATE':
            str(input("Force ignoring duplicate DATES. Hit enter to continue, or kill the run."))
            print('Taking first column of ',dc)
            merge = np.array(df[dc])[:,0]
        else:
            print('nan_mean merge of columns',dc)
            merge = np.nanmean(df[dc])
        df = df.drop(dc,1)
        df[dc] = merge
except AttributeError as e:
    print (e)  

df.drop_duplicates(inplace = True) 
#df = df.groupby(list(set(df.columns)),as_index = False).mean()
df.reset_index(inplace=True)


dr = '_'.join([i.split('.')[0] for i in f])

# create the data folder for required plots
os.system('mkdir data')
os.system('cd data && mkdir '+dr)
os.system('rm data/'+dr+'/*')

# date formatting
df.DATE = df.DATE.astype(str)
df  = df[ df.DATE != 'nan'].reset_index()
df.DATE=[str(i).replace('-','/') for i in  df.DATE]
#  df = df[ df.DATE>'']
df['HOUR'] = df.DATE.apply(lambda x: float(str(x).split(':')[0].split(' ')[-1]) )*60.
df['HOUR'] += df.DATE.apply(lambda x: float(str(x).split(':')[1] )+ np.random.random()*1e-7 )
df['HOUR']/=(24*60.)
df['MONTH'] = df.DATE.apply(lambda x: float(str(x).split(' ')[0].split('/')[-2]) )/12 

print(set(df.MONTH*12))
thismonth = int(input('Enter month to save:\n'))
    

# parse each item 
for item in df.columns:    
    #rescale variable
    scale = None
    if ('PPTV' in item):
        scale = 1e-12
    elif 'PPBV' in item:
        scale = 1e-9
    elif sys.argv[-1]=='True':
        scale = 1


    try:# rm int column names
        fail = float(item)
    except:
        fail = False
        
    if (scale == None) or (item in ['DATE','INDEX','HOUR','MONTH']) or fail: 
        print('skipping',item)
        continue
    else: print(item)

    # grab only columns of interest
    df1 = df[['HOUR','MONTH',item]].dropna().astype(float)
    if len(df1)<1 : 
        print(item, ' contains no data')
        continue
    df1 = df1[df1[item]>0]
    X = df1['HOUR MONTH'.split()].values#.reshape(-1, 1)
    Y = np.log10(df1[item]*scale).values 
    X = np.array(X,dtype=float).reshape(-1, 2)

    


    # make the Neural Network
    nn = MLPRegressor(
        hidden_layer_sizes=(10,),  activation='tanh', solver='lbfgs', alpha=0.001, batch_size='auto',
        learning_rate='adaptive', learning_rate_init=0.005, power_t=0.5, max_iter=2000, shuffle=True,
        random_state=9, tol=1e-4, verbose=False , warm_start=False, momentum=0.9, nesterovs_momentum=True,
        early_stopping=False, validation_fraction=0.4, beta_1=0.9, beta_2=0.999, epsilon=1e-08)

    # Fit our data to the NN
    nn.fit(X,Y)

    mname = 'January February March April May June July August September October November December'.split()


# plotting
    mpl.rcParams['axes.spines.left'] = False   
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['axes.spines.top'] = False
    mpl.rcParams['axes.spines.bottom'] = False
    mpl.rcParams['lines.markersize'] = 0
    plt.clf()

    entries = np.array(list(set(df1.MONTH)))*12
    #print(entries)
    plt.clf()

    
    fig = plt.figure(figsize=(16.*((max(entries)-min(entries)+1)/12),8))
    fig.patch.set_visible(False)
    start = min(entries)
    

    # for each MONTH
    for m1 in range(1,13):
        m=m1/12
        
        s = df1[df1.MONTH==m]
        if len(s)<10: continue
        
        plt.scatter(m1 + s.HOUR.values*.9,np.log10(s[item]*scale).values,alpha=.25,s=.5)
        
        h = 0.9*np.array(range(24))/24.
        plt.plot(m1+h,nn.predict([[i,m] for i in h]))
        
        if m1 != thismonth: col= '#666666'
        else: col = 'red'
        
        s = np.log10(scale*s[item])
        bp = plt.boxplot(s.values, positions=[m1+.935],showmeans=True,showfliers=False,notch=True,widths=[.05], meanprops={"marker":"_"})
        
        for a in bp:
            for b in bp[a]:
                b.set_alpha(0.4)
                b.set_color('black')

        bp['means'][0].set_alpha(0.9)        
        
        
        #plt.errorbar(m1+0.5, s.quantile(.5), yerr=np.vstack([s.quantile(.5) - s.quantile(.25),s.quantile(.75)-s.quantile(.5)]),capthick=2, c = '#222222',fmt='x',lw=1.2,mec=col,alpha=.8)
        
        #plt.scatter(m1+0.5, s.quantile(.5), c = col, s=2,marker='x',alpha = .9)
        
    plt.xticks(np.arange(1.5, 13.5, step=1),mname)
    plt.locator_params(axis='x', nbins=12)
    plt.locator_params(axis='y', nbins=5)
     
    plt.tight_layout(rect=(.2,0,1,1), w_pad = 20)
    #plt.show()
    ax = fig.gca()

    labels = [re.sub(r'[^\x00-\x7F]+','-',iteml.get_text()) for iteml in ax.get_yticklabels()]


    labels = [(r'$%s}$'%('%.2e'%(10**float(iteml))).replace('e',r'\times 10^{')) for iteml in labels]

    ax.set_yticklabels(labels)
    ax.tick_params(axis=u'both', which=u'both',length=0)
    #ax.xaxis.tick_top()
    ax.spines['left'].set_position(('data', start))
    
    os.system('echo "%15s,%e" >> %sdata.txt'%(item.replace(',','.'),10**nn.predict([[0.5,thismonth]])[0],'./data/'+dr+'/'))
    item = re.findall(r'[A-z0-9_\.-]+',re.sub(r',+','',item))[0]
    print(item)
    plt.savefig('./data/'+dr+'/'+item+'.pdf')
    plt.close()