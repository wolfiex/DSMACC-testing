#!/usr/local/anaconda/bin/python
#!/usr/bin/python
import numpy as np
import glob,sys,os,re

from pyDOE import lhs
#install pydoe using pip from pypi/packages.pyDOE


nruns = 700
duration = 24*60*60*5


#lhs_out = lhs(len(latin),n_runs)#,criterion='maximin')

o3 = ''

# name, const, val
repeat = [
['TIME',0,86400],
['NOx',1,1],
['OH',0,1e-6],
['TEMP',0,298],
['LAT',0,39.9],
['LON',0,116.4],
['H2O',0,0.02],
['JDAY',0,173.5],
['SPINUP',0,0],
['PRESS',0,1013],
['FEMISS',0,0],
['ALBEDO',0,0],
['DEPOS',0,0],
['O3' , 0,20e-9],
['CO' , 0,0],
]

# name,const,  min, max,10
iso = [
['NOX', 0,-15, -6],
['CH4' , 0,-15, -6],

]

lhs_out = lhs(len(iso),nruns).T#,criterion='maximin')

o3 += 'Description,,,'+','.join(['' for i in range(nruns)])+'\n'
o3 += ',,,'+','.join(['' for i in range(nruns)])+'\n'

o3 += 'Index,Species,Constrain,'+','.join([str(i) for i in range(nruns)])+'\n'

for i in repeat:
    o3+= 'c,%s,%s,'%(i[0],i[1]) +','.join([str(i[-1])]*nruns)+'\n'

for i,j in enumerate(iso):
    if j[0] == 'NOX':
        o3+= 'lh,NO,0,' +','.join([str( .5 *10 ** (((k *(j[2]-j[3])) + j[3]))  ) for k in lhs_out[i]])+'\n'
        o3+= 'lh,NO2,0,' +','.join([str(.5* 10 ** (((k *(j[2]-j[3])) + j[3]))  ) for k in lhs_out[i]])+'\n'

    else:
        o3+= 'lh,%s,%s,'%(j[0],j[1]) +','.join([str( 10 ** ((k *(j[2]-j[3])) + j[3])  ) for k in lhs_out[i]])+'\n'

print o3

with open('InitCons/grid.csv','w') as f:
    f.write(o3)
