import pandas as pd
import numpy as np
import netCDF4
from netCDF4 import Dataset
import glob,sys,os
 
file_list = glob.glob('*.nc')

print 'Select file to open: \n\n'
for i,f in enumerate(file_list): print i , ' - ', f
myfile = file_list[int(input('Enter Number \n'))]     

nc = Dataset(myfile,'r')
print nc.date, '\n', nc.description,'\n'

print 'Select Simulation: \n\n'
for i,g in enumerate(nc.groups): print i , ' - ', g
group = tuple(nc.groups)[int(input('Enter Number \n'))]     

print group, 'took', nc.groups[group].WALL_time, 'seconds to compute.'

specs = pd.DataFrame(nc.groups[group].variables['Spec'][:])
specs.columns = nc.groups[group].variables['Spec'].head.split(',')

rates = pd.DataFrame(nc.groups[group].variables['Rate'][:])
rates.columns = nc.groups[group].variables['Rate'].head.split(',')

print 'Spec and Rate files loaded'

from matplotlib.pyplot import *



nc.close()
