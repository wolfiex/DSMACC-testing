'''
A tool to calculate the fluxes from DSMACC
D.Ellis 2016
'''


#functions
global specs,reactants



xlen = lambda x: xrange(len(x))

import numpy as np
import pandas as pd
import sys,os,re,multiprocessing,netCDF4
from netCDF4 import Dataset
import matplotlib.pyplot as plt
#netcdf file path
ncfile = sys.argv[1]
ncores = 16


########### read dsmacc data
myfile = 'nheptane_1612091358.nc'


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



nc.close()
########################
specs['TIME'] = pd.to_datetime(specs.TIME, unit='s')
rates['TIME'] = specs['TIME']


''' 1 remove dummy and non-reactions'''
rates = rates[[r for r in rates.columns[6:] if ('DUMMY' not in r) & ('EMISS' not in r)]]

''' 2 remove species if not present (shrink data) '''
#specs = specs[specs.columns[specs.sum()>=0]]
rates = rates[rates.columns[rates.sum()>=0]]

''' 3 get conversion factor from molcm-3 to mixing ratio'''
M = specs['M'].mean()

''' 4 convert concentrations to mixing ratio '''
specs /= M

''' 5 generate reactants and products list '''
#no nead to clear whitespace as begin.py should take care of that.
rate_head = '\n'+'\n'.join(rates.columns)+'\n'
products = [i.split('+') for i in re.findall(r'-->([A-z0-9+]*)',rate_head)]
reactants = [j.split('+') for j in re.findall(r'\n([A-z0-9+]{1,60})[-->]{0,1}',rate_head)]
if len(reactants) != len(products) : print 'reactants and poducts differing lengths'


''' 6 trip to only timesteps required '''


print 'getconc'

''' Fluxes '''

flux = []

for i in xlen(reactants):
    rcol = []
    for j in reactants[i]:
        
 
        dummy = specs[re.sub(r'([\.\d\s]*)(\D[\d\D]*)', r'\2', j)]
    
        try: rcol.append( float(re.sub(r'([\.\d]*)\s*\D[\d\D]*', r'\1', j) * dummy ))
        except: rcol.append(dummy) # coeff = 1 if not yet specified
        
    prod = 1
    for k in rcol: prod *= k
    flux.append(prod * rates[rates.columns[i]])










''' 
force graphs 

'''












