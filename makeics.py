'''
A program to ensure the correct format of the Init_cons file for DSMACC. It should also allow an easier comparison between values used and the quick alterations of each. 

Species and variables are defined by the conditons list, and simulation time is set by the seconds varaible. 
'''
import sys

seconds = 157680000

#CV
#'LAT    , 0 , 1.6510e+01',
#'LON    , 0 , -2.452e+01',

#York
# 'LAT    , 0 , 5.3960e+01',
# 'LON    , 0 , 1.0800e+01',

conditions= [
'TEMP   , 0 , 2.9800e+02',
'LAT    , 0 , 1.6510e+01',
'LON    , 0 , -2.452e+01',
'JDAY   , 0 , 0.0000e+00', 
'PRESS  , 0 , 1013.0e+00',
'NO2    , 0 , 2.0000e-11',
'O3     , 0 , 30.000e-09',
'C2H6   , 1 , 5.1590e-10',
'C3H8   , 1 , 2.5500e-11',
'IC4H10 , 1 , 1.2000e-12',
'NC4H10 , 1 , 2.6000e-12',
'C2H2   , 1 , 5.2800e-11',
'C2H4   , 1 , 1.6200e-11',
'C3H6   , 1 , 1.7300e-11',
'CH3OH  , 1 , 1.0468e-09',
'CH3COCH3 , 1 , 5.5500e-10',
'NOx    , 1 , 1.0000e+00',
'O3FT   , 1 , 3.0000e-08',
'CO     , 0 , 8.1500e-08',
'H2O    , 1 , 1.0000e-02',
'CH4    , 1 , 1.8540e-06',
]#number of spaces here does not matter 
#'NO2     , 0 , %s'%(sys.argv[1]),


#splits list elelments and removes whitespace
reformat =  [line.replace(' ','').split(',') for line in conditions]

#write to the file
ic = open('Init_cons.dat','w')

ic.write('%s\n'%seconds) # write simulation time

# go through items and write to file.
for i in [0,1,2]:
    for item in reformat:
        if i == 0:
            ic.write('%15s!'%item[0])
        elif i == 1:
            ic.write('%15s!'%item[1])
        else:
            ic.write('%15s!'%('%.5e'%float(item[2])))
    ic.write('\n')
        

ic.close()


