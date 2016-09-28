#!/usr/bin/python
import multiprocessing,os,subprocess,pickle,sys,time
import pandas as pd
import numpy as np
import netCDF4
from netCDF4 import Dataset
#from StringIO import StringIO

print 'RENAME INITIATE'

'''options'''
available_cores = 16
ic_file= sys.argv[1]
pre_formatted_style=True #slower


#run simulations
#########################################################################################
ncores= available_cores # - 6 #if 6 used from openmp?
start = (time.strftime("%Y%m%d%H%M"))


# make ics 

if ('.csv' not in ic_file):  ic_file += '.csv' 
print ic_file
print 'makefile DISABLED'
#os.system("./makeics.pl %s"%ic_file)
ic_open= tuple(open(ic_file))
numbered = np.array([i for i in enumerate(ic_open[2].strip().split(',')[3:])])
n_runs=len(numbered)
if (ncores > n_runs): ncores = n_runs


# run dsmacc
def simulate (arg_in):
    try:     #each system call has to be on a new line        
        start = time.strftime("%s")
        description="%s_%s"%('run',arg_in[1])
        linenumber =  "%s"%(int(arg_in[0])+1) 
        os.system('./model %s %s'%(description,int(linenumber)))
        return int(time.strftime("%s")) - int(start)
                
    except: 
        return 'Failed'


out = multiprocessing.Pool(ncores).map( simulate , numbered ) 
os.system('rm fort*') 


#concat resutls
#########################################################################################
print '\n Calculations complete! \n Concatenating results. \n '  

ic_string='' # get a string format of the intial conditions file
for line in ic_open[1:]: ic_string+=line

filename= ic_file.split('.')[0]+'_'+ time.strftime("%y%m%d%H%M")+'.nc'
ncfile = Dataset(filename,'w')
print 'add to results folder'
ncfile.initial_conditions_str = ic_string
ncfile.date = time.strftime("Completion time:%A %d %B %Y at %H:%M")
ncfile.description = ic_open[0].strip() 

spec = ncfile.createDimension('spec', None)
time = ncfile.createDimension('time', None)
rate = ncfile.createDimension('rate', None)


#for each simulation


for group_name in numbered:
    print group_name
    nc = Dataset( 'run_'+group_name[1]+'.nc' , mode='r')
    group = ncfile.createGroup(group_name[1])
    specvar = group.createVariable( 'Spec' , "f8"  ,('time','spec',))
    ratevar = group.createVariable( 'Rate' , "f8"  ,('time','rate',))
    specvar[:] = nc.variables['Spec'][:].T
    ratevar[:] = nc.variables['Rate'][:].T
    print group
    specvar.head = ','.join([''.join(x).strip(' ') for x in nc.variables['species'][:]])
    ratevar.head = ','.join([''.join(x).strip(' ') for x in nc.variables['reactions'][:]])
    group.WALL_time = out[int(group_name[0])]
    
    nc.close()



# close the file.
ncfile.close()
print '*** SUCCESS writing %s!'%filename



os.system('find . -size +100M | cat >> .gitignore')
