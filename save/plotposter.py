import pandas as pd
import numpy as np
import netCDF4
from netCDF4 import Dataset
import glob,sys,os

file_list = glob.glob('*.nc')
file_list.sort(key=os.path.getctime)#getmtime - modified getctime-created




spc='NOx'

import numpy as np
import matplotlib.pyplot as plt

      

for myfile in file_list[:2]:      
    nc = Dataset(myfile,'r')
    print nc.date, '\n', nc.description,'\n'


    if len(nc.groups) > 1: 
        print 'Select Simulation: \n\n'
        for i,g in enumerate(nc.groups): print i , ' - ', g
        group = tuple(nc.groups)[int(input('Enter Number \n'))]
    else:
        group = list(nc.groups)[0]


    print group, 'took', nc.groups[group].WALL_time, 'seconds to compute.'

    if 'mcm' in group:grp='MCM 3.3.1'
    else: grp= 'CRI 2.1'    
    
    specs = pd.DataFrame(nc.groups[group].variables['Spec'][:])
    specs.columns = nc.groups[group].variables['Spec'].head.split(',')
    specs.index = pd.to_datetime(specs.TIME, unit='s') 

    specs = specs/(specs.M.mean())
    
          
    specs = specs.iloc[1:-1]#remove nan row
    specs = specs*1e9
    
    selection = specs['NO']+specs['NO2']#.ix[int(144/2):int(144/2)+144]#+specs['NO'].ix[int(144/2):int(144/2)+144]
    selection.plot(label=grp) 
    
    plt.ylabel('[%s]/ppb'%spc)
    plt.legend()
        
      
plt.savefig(spc+'.png')
