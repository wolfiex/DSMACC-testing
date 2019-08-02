import pandas as pd
import re,datetime,os
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv('aphh_summer.csv',index_col=0)
col = df.columns = ' '.join(df.columns).upper().split()
df.index = pd.to_datetime(df.index)

ground = re.findall(r'\b([\w\d\.]+_PPBV)[^_]',','.join(df.columns).upper())

df = df[ground]


df.drop(columns = [
 'NOX_PPBV',
 'NOY_PPBV',
 'NOZ_PPBV',
 'SO2_PPBV'
])


#remove duplicates
#there are 620
df = df.groupby(df.index).mean()


os.system('rm figs/*')
#remove nanrows
#df.dropna(axis=0, inplace = True)


for i in df.index:
    if '00:00:00' in str(i):
        start = i
        break



end = start+datetime.timedelta(1)


keep ={}

day = []
while end<df.index[-1] :
    end = start+datetime.timedelta(1)
    ddf=df.loc[start:end]

    #col
    ddf = ddf[ddf.columns[np.isnan(ddf).sum() < 0.8*len(ddf)]]

    ddf = ddf.loc[ddf.index[np.isnan(ddf).sum(axis=1) != len(ddf)]]

    day.append(ddf)

    if len(ddf.columns)>30:
        plt.clf()
        sdf = ddf - ddf.mean()
        sdf/=sdf.max()
        sdf.plot(subplots=False,legend=False)
        plt.tight_layout()
        plt.savefig('figs/'+str(start)+'.png')
        plt.clf()
        plt.close()
        keep[str(start.date())] = ddf

    day.append(ddf)
    print len(ddf),len(ddf.columns),np.isnan(ddf).sum().sum(),np.isnan(ddf).sum().min(),np.isnan(ddf).sum().max()


    start = end






def s ():
    plt.tight_layout()
    plt.show()



drop = [u'NOY_PPBV', u'NOZ_PPBV', u'SO2_PPBV',u'CYCLOPENTANE_PPBV' , 'NO2_PPBV']# u'NOX_PPBV'

rename = [
['ISO.PENTANE','IC5H12'],
['N.PENTANE','NC5H12'],
['X1.3.BUTADIENE','C4H6'],
['O.XYLENE','OXYL'],
['ETHYL.BENZENE','EBENZ'],
[u'TRANS.2.BUTENE',   'TBUT2ENE' ],
[u'X1.BUTENE',  'BUT1ENE'],
[u'ISO.BUTENE',  'MEPROPENE'],
[u'CIS.2.BUTENE', 'CBUT2ENE'],
[u'TRANS.2.PENTENE', 'TPENT2ENE'],
[u'X2.3.METHYLPENTANE', 'M2PE'+'|'+ 'M3PE'],
[u'ETHANE','C2H6'],
[u'ETHENE','C2H4'],
[u'PROPANE','C3H8'],
[u'PROPENE','C3H6'],
['ISO.BUTANE','IC4H10'],
['N.BUTANE','NC4H10'],
['ACETYLENE','C2H2'],
['N.HEXANE','NC6H14'],
['N.HEPTANE','NC7H16'],
['ACETALDEHYDE','CH3CHO'],
['ETHANOL','C2H5OH'],
['METHANOL','CH3OH']
]


for id in  ['2017-06-17','2017-06-11']:
    select = keep[id]
    select.drop(drop,axis=1,inplace=True)
    names = ';'.join(select.columns)
    # rename
    for i in rename:

        names = re.sub(r'([^\.\w\d_-])('+i[0]+')_',r'\1'+i[1]+'_',names)


    select.columns = names.split(';')
    for i in select.columns:
        if '|' in i:
            j = i.split('|')
            for k in j:
                select[k]= select[i]/float(len(j))

            select.drop([i],axis=1,inplace=True)


    ## hack to get no2 (as missing on some )
    #select['NO2_PPBV'] = select['NOX_PPBV']-select['NO_PPBV']
    #select.drop(['NOX_PPBV'],axis=1,inplace=True)
    ## hack to have the same emissions in all for comparison
    select = select[[i+'_PPBV' for i in 'O3,CO,NO,C2H6,C2H4,C3H8,IC4H10,NC4H10,C2H2,TBUT2ENE,BUT1ENE,MEPROPENE,CBUT2ENE,IC5H12,NC5H12,C4H6,NC6H14,NC7H16,BENZENE,TOLUENE,EBENZ,OXYL,CH3CHO,CH3OH,C2H5OH,M3PE,NOX'.split(',')]]

    print ','.join([i.replace('_PPBV','') for i in select.columns])



    select.to_csv(id+'.csv')
