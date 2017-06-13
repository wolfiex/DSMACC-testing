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


r = np.arange(144)
theta = 2. * np.pi * r/144.

ax = plt.subplot(111, projection='polar')

      

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

    specs = pd.DataFrame(nc.groups[group].variables['Spec'][:])
    specs.columns = nc.groups[group].variables['Spec'].head.split(',')
    specs.index = pd.to_datetime(specs.TIME, unit='s') 

    specs = specs/(specs.M.mean())
          
          
    specs = specs.iloc[1:-1]#remove nan row
    selection = specs[spc].ix[int(144/2):int(144/2)+144]#+specs['NO'].ix[int(144/2):int(144/2)+144]
    ax.plot(np.array(list(theta)), np.array(selection) ,label=myfile)     
            
#ax.set_xticks(range(4))      
ax.set_xticklabels([])  
#ax.legend(loc='bottom')
##ax.plot(theta, r)
#ax.set_rmax()
#ax.set_rticks([min(selection),max(selection)])  # less radial ticks
ax.set_rlabel_position(+np.pi/12.)  # get radial labels away from plotted line
ax.grid(True)
ax.set_theta_zero_location('N')
ax.set_title(spc, va='bottom')
#plt.show()
plt.savefig(spc+'.png')
