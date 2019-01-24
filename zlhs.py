import lhsmdu
import pandas as pd
import numpy as np
import zruntoics as newics
'''https://github.com/sahilm89/lhsmdu'''
df = np.log10(pd.read_csv('src/examples/clfo_describe.csv',index_col=0))


ignorecontinue = True

ignore = ['PXYL+MXYL','NO2','NOY','R','RO2','M','HO2','CH3O2','OH','TRICLETH','HONO','BUT2CHO', 'C3ME3CHO', 'C5H11CHO', 'CH2CL2', 'LIMONENE', 'MACR', 'MVK']
#'NO','NO2'


df = df[filter(lambda x: x not in ignore, df.columns)]


nruns = 500#df.shape[1]**2

print nruns

lhs = lhsmdu.sample(df.shape[1],nruns)
#lhs = lhsmdu.createRandomStandardUniformMatrix(df.shape[1],nruns)#monte carlo
np.save('lhs.npy',lhs)

print 'lhs ready'

ics = newics.newics(h5file='clfo.h5',timestep=int(144*1.5))
if ignorecontinue:
    keep = ['TIME', 'TEMP', 'LAT', 'LON', 'JDAY', 'H2O', 'ALBEDO', 'PRESS',
       'NOx', 'DEPOS', 'FEMISS', 'SPINUP']
    ics = ics[keep]


myarray = []

for i,s in enumerate(df):
    max = df[s].ix['max'] #+ df[s].ix['std']
    min = df[s].ix['min'] #- df[s].ix['std']
    try: int(min)
    except:min = -13
    if min<-13: min = -13
    if max>-5: max = -5
    range = max - min
    valcol = lhs[i]
    print max,min,df.columns
    valcol*= range
    valcol+= min



    try:
        const = ics[s].ix['Constrain']
        ics.drop(s,axis = 1,inplace = True)
    except:
        const = 0

    dummy = ['lhs',s,const]
    dummy.extend(list(10**np.array(valcol)[0]))

    myarray.append(dummy)

data = list(np.array(ics))
for i in xrange(nruns-1):
    data.append(data[3])

combined = pd.concat([pd.DataFrame(data),pd.DataFrame(myarray).T],axis=1).T

print combined

with open('InitCons/'+'lhs'+'.csv','w') as f:
    f.write('A continuation ics file'+','*(combined.shape[1]-1))
    f.write('\n')
    f.write(','*(combined.shape[1]-1))
    f.write('\n')
    f.write(','.join(combined.columns.astype(str)))
    f.write('\n')
    f.write('\n'.join([','.join(i) for i in combined.values.astype(str)]))
