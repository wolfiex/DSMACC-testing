#!/usr/bin/python
import multiprocessing,os,subprocess,pickle,sys,time
import pandas as pd
import numpy as np
import netCDF4
from netCDF4 import Dataset
from scipy.io import FortranFile
#from StringIO import StringIO

'''options'''
available_cores = 16
ic_file= sys.argv[1]
pre_formatted_style=False #slower


#run simulations
#########################################################################################
ncores= available_cores # - 6 #if 6 used from openmp?
start = (time.strftime("%Y%m%d%H%M"))


# make ics 
if ('.csv' not in ic_file):  ic_file += '.csv' 
print ic_file
os.system("rm Init_cons.dat")
os.system("./makeics.pl %s"%ic_file)
ic_open= tuple(open(ic_file))
numbered = np.array([i for i in enumerate(ic_open[2].strip().split(',')[3:])])
n_runs=len(numbered)
if (ncores > n_runs): ncores = n_runs




global tuv_run,a,p,t,tuv_version
t,a,p,tuv_version=[],[],[],[]

o3col = 260 #set same as in dsmacc
for i in ic_open: 
    if 'TEMP' in i: t = i.replace('\n','').split(',')[3:]
    elif 'ALBEDO' in i: a = i.replace('\n','').split(',')[3:]
    elif 'PRESS' in i: p = i.replace('\n','').split(',')[3:]
    elif 'TUV' in i: tuv_version = i.replace('\n','').split(',')[3:]    #tuv folder


def tuv(i): #checks of the required tuv files are available, and if not generates them. 
    temp = float(t[i]);albedo=float(a[i]);press=float(p[i])
    name = '%.3e_%.3e_%.3e_%.3e'%(temp,press,albedo,260)
    name = name.replace('_','-').replace('.','_')+'.bin' #at max len 50 .replace('e','')

    alt = (1-(press/1013.25)**0.190263)*288.15/0.00198122*0.304800/1000.
    pathname = '%s/run_bin/%s'%(tuv_version[i],name)
    if (not os.path.isfile(pathname)):
        print os.system('cd %s/ && ./tuv %s %f %f %f %f'%(tuv_version[i],'run_bin/'+name,alt,albedo,o3col,temp))
    else:
        print 'using saved', pathname
    return pathname



def read_fbin(filename):
    ''' this reads each written binary instance itteratively'''
    f = FortranFile(filename, 'r')
    array = []
    while True:
        try: 
            array.append(f.read_reals(dtype=np.float_))
        except TypeError: 
            break
    #array = np.reshape(array, (nspecs,-1))
    
    f.close()
    return array
    








# run dsmacc
def simulate (arg_in):
    try:     #each system call has to be on a new line        
        start = time.strftime("%s")
        description="%s_%s"%('run',arg_in[1])
        linenumber = "%s"%(int(arg_in[0])+1) 
        print './model %s %s %s'%(description,int(linenumber), tuv_run[int(arg_in[0])])
        os.system('./model %s %s %s'%(description,int(linenumber), tuv_run[int(arg_in[0])]))
        return int(time.strftime("%s")) - int(start)
                
    except: 
        return 'Failed'








#do runs
#########################################################################################


tuv_run = multiprocessing.Pool(ncores).map( tuv , range(len(t))) 
del t,a,p    

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
    
    
    
    group = ncfile.createGroup(group_name[1])
    group.tuv = tuv_run[int(group_name[0])]
    
    specvar = group.createVariable( 'Spec' , "f8"  ,('time','spec',))
    ratevar = group.createVariable( 'Rate' , "f8"  ,('time','rate',))
    
    specvar[:] = read_fbin('run_%s_.spec'%group_name[1]) 
    ratevar[:] = read_fbin('run_%s_.rate'%group_name[1])
    
    print group
    specvar.head = ''.join(tuple(open('spec.names'))).replace(' ','').replace('\n','')
    ratevar.head = ''.join(tuple(open('rate.names'))).replace(' ','').replace('\n','')
    group.WALL_time = out[int(group_name[0])]


# close the file.
ncfile.close()
print '*** SUCCESS writing %s!'%filename



os.system('find . -size +100M | cat >> .gitignore')
