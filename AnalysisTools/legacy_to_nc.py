import pandas as pd
import numpy as np
import netCDF4
from netCDF4 import Dataset
import glob,sys,os,time
import multiprocessing as mp 
 
#if len(sys.argv) == 1: sys.argv.append('1')

ic_file = sys.argv[1:][0]
os.system("./makeics.pl %s"%ic_file)
ic_open= tuple(open(ic_file))
names =  ic_open[2].strip().split(',')[3:]


ncfile = Dataset('%s_legacy.nc'%ic_file,'w')
   
ncfile.initial_conditions_str = ''.join(tuple(open('Init_cons.dat')))
ncfile.date = time.strftime("processing time :%A %d %B %Y at %H:%M")
#ncfile.description = ic_open[0].strip() 

spec = ncfile.createDimension('spec', None)
time = ncfile.createDimension('time', None)
rate = ncfile.createDimension('rate', None)
    
    
def fix_fort (dat):
    dat = dat.strip().split('!')
    #print dat   
    dummy = []
    for y in dat:
        y= y.replace('!','').replace(' ','')
        try: dummy.append(float(y)) 
        except:
            y = y.replace('-','E-').replace('+','E+')
            if y != '':
                if y[0] == 'E': y = y[1:]
                dummy.append(float(y))
 
    return dummy
    
    
 
for i in names:
    
    print i 
    
    spc = tuple(open('run_%s_def.spec'%i))
    rte = tuple(open('run_%s_def.rate'%i))
    
    s_head = [i for i in spc[0].strip().replace(' ','').split('!')][:-1]
    r_head = [i for i in rte[0].strip().replace(' ','').split('!')][:-1]
   
    spc = mp.Pool(16).map(fix_fort, spc[1:])
    rte = mp.Pool(16).map(fix_fort, rte[1:])
    
    
    group = ncfile.createGroup('group_%s'%i)
    specvar = group.createVariable( 'Spec' , "f8"  ,('time','spec',))
    ratevar = group.createVariable( 'Rate' , "f8"  ,('time','rate',))
    

    specvar[:] = spc
    ratevar[:] = rte

    specvar.head = ','.join([''.join(x).strip(' ') for x in s_head])
    ratevar.head = ','.join([''.join(x).strip(' ') for x in r_head])

    
ncfile.close()

