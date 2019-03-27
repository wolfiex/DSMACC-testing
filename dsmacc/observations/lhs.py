import lhsmdu,sys
import pandas as pd
import numpy as np
#import zruntoics as newics
'''
lhsmdu lib:
https://github.com/sahilm89/lhsmdu

A dirty script to create our LHS input for a mass ML training dataset using CLFO data 

CMD line argvs : observation describe file, number of runs 
usage: 

    python -m dsmacc.observations.lhs ./src/examples/clfo_describe.csv 200

'''

location = sys.argv[1] #the describe file
nruns = int(sys.argv[2])

########## READ DATA
ignorecontinue = True
ignore = ['CO2','PXYL+MXYL','NO2','NOY','R','RO2','M','HO2','CH3O2','OH','TRICLETH','HONO','BUT2CHO', 'C3ME3CHO', 'C5H11CHO', 'CH2CL2', 'LIMONENE', 'MACR', 'MVK']
df = np.log10(pd.read_csv(location,index_col=0))#'../src/examples/clfo_describe.csv'
df = df[filter(lambda x: x not in ignore, df.columns)]

print(nruns)

# may be slow. 
lhs = lhsmdu.sample(df.shape[1],nruns)
#lhs = lhsmdu.createRandomStandardUniformMatrix(df.shape[1],nruns)#monte carlo
np.save('lhs.npy',lhs)
print 'lhs ready'

#### END LHS

#### set ics BASE
'''
If using file use new ics, we are just creating a new one 
'''
##ics = newics.newics(h5file ='clfo.h5',timestep=int(25*60*60))

ics = pd.DataFrame(
    [
           ['ii', 'TIME', '0',str(-24*60*60*1)],
           ['ii', 'TEMP', '0', '298'],
           ['ii', 'LAT', '0', '51.5074'],
           ['ii', 'LON', '0', '0.1278'],
           ['ii', 'JDAY', '0', '173.5'],
           ['ii', 'H2O', '0', '0.02'],
           ['ii', 'ALBEDO', '0', '0'],
           ['ii', 'PRESS', '0', '1013'],
           ['ii', 'NOx', '1', '0'],
           ['ii', 'DEPOS', '1', '1'],
           ['ii', 'FEMISS', '1', '0'],
           ['s', 'SPINUP', '0', '1e99']

           ]
    )
    
ics.columns =  ['Index', 'Species', 'Constrain', 'base']


### END ICS SETUP

### ICS CREATE
'''
if ignorecontinue:
    keep = ['TIME', 'TEMP', 'LAT', 'LON', 'JDAY', 'H2O', 'ALBEDO', 'PRESS',
       'NOx', 'DEPOS', 'FEMISS', 'SPINUP']
    ics = ics[keep]
'''
myarray = []
for i,s in enumerate(df):
    # median +- 2 orders of magnitude
    max = df[s].ix['50%']-2 #+ df[s].ix['std']
    min = df[s].ix['50%']+2 #- df[s].ix['std']
    try: int(min)
    except:min = -13
    
    #limit range
    if min<-13: min = -13
    if max>-6: max = -6
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




data = list(np.array(ics.T))
for i in xrange(nruns-1):
    data.append(data[3])

combined = pd.concat([pd.DataFrame(data),pd.DataFrame(myarray).T],axis=1).T


print combined
##### Write File lhs.csv
with open('./InitCons/'+'lhs_spinup'+'.csv','w') as f:
    f.write('A continuation ics file'+','*(combined.shape[1]-1))
    f.write('\n')
    f.write(','*(combined.shape[1]-1))
    f.write('\n')
    f.write(','.join(combined.columns.astype(str)))
    f.write('\n')
    f.write('\n'.join([','.join(i) for i in combined.values.astype(str)]))
