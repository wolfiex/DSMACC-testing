import lhsmdu,sys
import pandas as pd
import numpy as np

nruns = 300

specs='APINENE BENZAL BENZENE BOX2PROL BPINENE BUOX2ETOH BUT1ENE BUT2OL C2H2 C2H4 C2H5CHO C2H5CO3 C2H5NO3 C2H5O2 C2H5OH C2H5OOH C2H6 C3H6 C3H7CHO C3H8 C4H6 C4H9CHO C5H8 CBUT2ENE CH3CHO CH3CO2H CH3CO3 CH3CO3H CH3COCH3 CH3NO3 CH3O2 CH3OCH3 CH3OCHO CH3OH CH3OOH CH4 CHEX CHEX2ENE CO CPENT2ENE CYHEXOL CYHEXONE DIEK DIET35TOL DIETETHER DIIPRETHER DIME35EB DMC DMM EBENZ EOX2EOL ETBE ETHACET ETHGLY H2O2 HCHO HCOOH HEX1ENE HEX2ONE HEX3ONE HMML HNO3 HO2NO2 HOCH2CH2O2 HOCH2CHO HOCH2CO3 HOCH2CO3H HONO IBUTOL IC3H7NO3 IC3H7O2 IC3H7OOH IC4H10 IC5H12 IPBENZ IPEAOH IPEBOH IPECOH IPRCHO IPROACET IPROPOL M22C4 M23C4 M2HEX M2PE M3HEX M3PE MACO3 ME2BUT1ENE ME2BUT2ENE ME3BUOL ME3BUT1ENE MEK MEPROPENE METHACET METHTOL MIBK MIBKAOH MIPK MO2EOL MPAN MPRK MTBE MTBK MXYL N2O5 NBUTACET NBUTOL NC10H22 NC11H24 NC12H26 NC4H10 NC5H12 NC6H14 NC7H16 NC8H18 NC9H20 NEOP NO NO2 NO3 NOA NPROACET NPROPOL O3 OETHTOL OXYL PAN PBENZ PECOH PENT1ENE PETHTOL PHAN PPN PR2OHMOX PROPACID PROPGLY PXYL SBUTACET STYRENE TBUACET TBUT2ENE TBUTOL THEX2ENE TM123B TM124B TM135B TOLUENE TPENT2ENE'

specs= specs.split()
#specs.extend(['NO','NO2'])

specs=list(set(specs))


# may be slow.
lhs = lhsmdu.sample(len(specs),nruns)
#lhs = lhsmdu.createRandomStandardUniformMatrix(df.shape[1],nruns)#monte carlo
np.save('lhs.npy',lhs)
print 'lhs ready'


'''
If using file use new ics, we are just creating a new one
'''
##ics = newics.newics(h5file ='clfo.h5',timestep=int(25*60*60))

ics = pd.DataFrame(
    [
           ['ii', 'TIME', '0',str(24*60*60*3)],
           ['ii', 'TEMP', '0', '298'],
           ['ii', 'LAT', '0', '51.5074'],
           ['ii', 'LON', '0', '0.1278'],
           ['ii', 'JDAY', '0', '173.5'],
           ['ii', 'H2O', '0', '0.02'],
           ['ii', 'ALBEDO', '0', '0'],
           ['ii', 'PRESS', '0', '1013'],
           ['ii', 'NOx', '0', '0'],
           ['ii', 'DEPOS', '1', '1'],
           ['ii', 'FEMISS', '1', '0'],
           ['s', 'SPINUP', '0', '1e99']

           ]
    )

ics.columns =  ['Index', 'Species', 'Constrain', 'base']


### END ICS SETUP

myarray = []
for i,s in enumerate(specs):

    if specs in ['NO NO2 O3']:

        #limit range
        min = -13
        max = -7
    else:
        #limit range
        min = -13
        max = -8
    range = max - min
    valcol = lhs[i]


    print max,min

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
with open('./InitCons/'+'lhs_general'+'.csv','w') as f:
    f.write('A continuation ics file'+','*(combined.shape[1]-1))
    f.write('\n')
    f.write(','*(combined.shape[1]-1))
    f.write('\n')
    f.write(','.join(combined.columns.astype(str)))
    f.write('\n')
    f.write('\n'.join([','.join(i) for i in combined.values.astype(str)]))
