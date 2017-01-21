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
ncores = 4


########### read dsmacc data
myfile = 'geckonhep_1701050054.nc'


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
#specs['TIME'] = pd.to_datetime(specs.TIME, unit='s')
rates['TIME'] = specs['TIME']



## need atleast two timesteps here 
#specs = specs.ix[[99,100]]
#rates = rates.ix[[99,100]]

''' 1 remove dummy and non-reactions'''
specs = specs[[r for r in specs.columns if ('DUMMY' not in r) & ('EMISS' not in r)]]
rates = rates[[r for r in rates.columns[6:] if ('DUMMY' not in r) & ('EMISS' not in r)]]
rates = rates.loc[:, (rates > 0).any(axis=0)]





''' 2 remove species if not present (shrink data) '''
#rates = rates[rates.columns[rates.sum()>=0.]]

''' 3 get conversion factor from molcm-3 to mixing ratio'''
M = specs['M'].mean(),





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

''' 4 convert concentrations to mixing ratio '''

 #assign number for species, used later



#clean array if not making graph 
specs = specs.loc[:, (specs > 0).any(axis=0)]
specs /= M



flux = np.array(np.array(flux).tolist()).T



''' 
force graphs 

'''

''' 4 normalise concentrations '''
conc = np.array(specs[specs.columns[7:]])
conc_adjust = []

''' Define spec locations '''
locs2 = dict(enumerate(specs.columns[7:]))
locs = {v: k for k, v in locs2.iteritems()}
locs_json = str(locs).replace("u'",'"').replace("\'",'"') 



''' 1 get all species interaction '''
def combine(ln): return  [[[re.sub(r'([\.\d\s]*)(\D[\d\D]*)', r'\2',r),re.sub(r'([\.\d\s]*)(\D[\d\D]*)', r'\2',p)],ln] for p in 
products[ln] for r in reactants[ln]]

dummy = np.vectorize(combine)(xlen(reactants))
edges = [] ; [edges.extend(i) for i in dummy] ; edges.sort() #because why not 

''' 2 extract non duplicated list of reactions '''
individual = list(set(frozenset(i[0]) for i in edges))




''' 3 Normalise fluxes per timestep'''

minmax = []


'''
for i in xlen(specs):
    row = np.log10(flux[i,:])
    mn = row[row>-1e99].min()
    row = row+abs(mn)
    mx = row.max()
    flux[i,:] = 1-((row+1e-6)/abs(mx)) # large fluxes small
    minmax.extend([mn,mx])
  '''  
    
    


''' 4 Make a combination of these '''

flux_data = []

for i in individual:
    fp , fm =[],[]
    st = list(i)
    try:
    #if True:   
        d0, d1 = locs[st[0]],locs[st[1]]
        
        dummy  = [j for j in xlen(edges) if i == set(edges[j][0])]   
        for k in dummy:
            edge = edges[k]
            
            if st[0] == edge[0][0]: fp.append(edge[1])
            else:                   fm.append(edge[1])

        flux_data.append([[fp,fm] ,d0,d1])
    except IndexError as e: print e, st # if self reaction
    except KeyError as e : print 'no concentration for', e  #no specie concentration 






flux_data = np.array(flux_data)


#ncdf info 
combinations = str(list(flux_data[:,0]))
src = np.array(flux_data[:,1])
tar = np.array(flux_data[:,2])

times =  np.array(specs.TIME*M).astype(int)


#rateheaders = [x.strip() for x in rate_head.split('\n') if x.strip()]
#rates = np.array([i.split('-->') for i in rateheaders])


rate_head = '[' + rate_head.replace('\n','","').replace('-->','>')[2:-2] +']'


from netCDF4 import Dataset

 
nrows = conc.shape[0]

 
info_file = Dataset('volcano.nc', 'w', format='NETCDF3_CLASSIC')
 
info_file.createDimension('time', nrows)
info_file.createDimension('specs', conc.shape[1])
info_file.createDimension('fluxes', flux.shape[1])
info_file.createDimension('sourcetarget', len(src))
info_file.createDimension('dict', len(locs_json))
info_file.createDimension('comb', len(combinations))
info_file.createDimension('timestr', len(times))
info_file.createDimension('rateheader', len(rate_head))



 
cnc  = info_file.createVariable('concentration', 'f8', ('time', 'specs'))
cnc[:,:] = conc

flx  = info_file.createVariable('edge-length', 'f8', ('time', 'fluxes'))
flx[:,:] = flux

rt  = info_file.createVariable('rate', 'c', 'rateheader')
rt[:] = rate_head

sources  = info_file.createVariable('source', 'i4', 'sourcetarget')
sources[:] = src

targets  = info_file.createVariable('target', 'i4', 'sourcetarget')
targets[:] = tar

dictn  = info_file.createVariable('nodes', 'c', 'dict')
dictn[:] = locs_json

comb  = info_file.createVariable('combinations', 'c', 'comb')
comb[:] = combinations

stime  = info_file.createVariable('timeseconds', 'f8', 'time')
stime[:] = times


print 'PRIMARY SPECS'

print 'LOCAT~ION ARRAY'

print 'TIME ARRAY NOT HERE YET'
 
info_file.close()

print 'nc write'


#https://github.com/wolfiex/netcdfjs reader



