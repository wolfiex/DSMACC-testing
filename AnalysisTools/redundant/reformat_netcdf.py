''' 
Slow but neater formatting for netcdf: seperates results into columns.
D. Ellis
'''

import numpy as np
import netCDF4,sys
from netCDF4 import Dataset

group_name = sys.argv[1] 
nc = Dataset( group_name+'.nc' , mode='r')
ncf = Dataset('del.'+group_name,'w')

group =  ncf.createGroup('del')
spec = group.createGroup('Spec')
time = ncf.createDimension('time', None)
rate = group.createGroup('Rate')

specs= [''.join(x).strip(' ') for x in nc.variables['species'][:]]
for i,s in enumerate(specs):
    var = spec.createVariable( s , "f8"  ,('time',))
    var[:] = np.array(nc.variables['Spec'][i])
    
    if (i%100 == 0):
        print '%3d'%(float(i)/len(specs)*100), '% species from', group_name , 'saved'

reactions = [''.join(x).strip(' ') for x in nc.variables['reactions'][:]]
for i,r in enumerate(reactions):
    var = rate.createVariable( r , "f8"  ,('time',))
    var[:] = np.array(nc.variables['Rate'][i])
    
    if (i%100 == 0):
        print '%3d'%(float(i)/len(reactions)*100), '% reactions from', group_name , 'saved'
    
    
nc.close()
ncf.close()
