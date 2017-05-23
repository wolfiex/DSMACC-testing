import pandas as pd
import numpy as np
import netCDF4
from netCDF4 import Dataset
import glob,sys,os

file_list = glob.glob('*.nc')
file_list.sort(key=os.path.getctime)#getmtime - modified getctime-created

print 'Select file to open: \n\n'
for i,f in enumerate(file_list): print i , ' - ', f
myfile = file_list[int(input('Enter Number \n'))]

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

rates = pd.DataFrame(nc.groups[group].variables['Rate'][:])
rates.columns = nc.groups[group].variables['Rate'].head.split(',')[:]

print 'IGNORING LAST 2 RATES!!!!!!!!!!!!!!!!!!!!!!'

print 'Spec and Rate files loaded'

from matplotlib.pyplot import *


    
M= specs['M'].mean()

   
specs = specs.iloc[1:-1]#remove nan row


def compare(spc,skip=0):
    for group in nc.groups:
            
        specs = pd.DataFrame(nc.groups[group].variables['Spec'][:])
        specs.columns = nc.groups[group].variables['Spec'].head.split(',')
        specs.index = pd.to_datetime(specs.TIME, unit='s') 

        M= specs['M'].mean()
        specs = specs/M
        
        specs = specs.iloc[1:-1]#remove nan row
        specs[spc].ix[skip:].plot(label=group)
    title=spc
    legend()
    show()


#nc.close()

# Format x-axis for plots
time = (specs['TIME']-specs['TIME'][0]+600.)/3600.
xm = int(time.iloc[-1])+1

# Useful python command for formatting plots
# (Have to be used after plot command, can therefore not be included in scrpit.)
# xticks(np.arange(0,xm,12))
# xlabel('Model time / hours')
# ylabel('c / cm$^{-3}$\n(F / cm$^{-3}$ s$^{-1}$)')
# tight_layout()
# legend()
