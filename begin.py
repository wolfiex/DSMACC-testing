#!/usr/local/anaconda/bin/python 
#/usr/bin/python
import multiprocessing,os,subprocess,pickle,sys,time
#import pandas as pd
import numpy as np
import glob,sys,os

# options
available_cores = 16
pre_formatted_style=False #slower


runsaved = False
if '--saved' in sys.argv: runsaved=True #runs model using saved versions when -modelname is provided
keepx = False
if '--keepx' in sys.argv: keepx=True # does not ignore runs marked with an X in the begining
icsonly = False
if '--icsonly' in sys.argv: icsonly=True # does not ignore runs marked with an X in the begining
obs= 0
if '--obs' in sys.argv: 
    obs=int(tuple(open('include.obs'))[0].strip().replace('!obs:','')) # does not ignore runs marked with an X in the begining
    print 'running with %s observations, with %s lines'%((obs-1.)/4.,obs)
last = False    
if '--last' in sys.argv: last = -1
if '--run' in sys.argv: 
    for i in sys.argv:
        try:
            last=int(i)
        except: None

print 'if obs unconstrain species where obs is used'


print sys.argv,last
 ##################
 ####read files####

file_list = glob.glob('InitCons/*.csv')
file_list.sort(key=os.path.getmtime)#getmtime - modified getctime-created

if (not os.path.exists('./model') & runsaved==0): sys.exit('No model file found. Please run "make kpp" followed by "make"')



print 'Select file to open: \n\n'
for i,f in enumerate(file_list): print i , ' - ', f.replace('InitCons/','').replace('.csv','')
if (last) : ic_file = file_list[last]
else : ic_file = file_list[int(raw_input('Enter Number \n'))]


#run simulations
#########################################################################################
ncores= available_cores # - 6 #if 6 used from openmp?
start = (time.strftime("%Y%m%d%H%M"))


# make ics
if ('.csv' not in ic_file):  ic_file += '.csv'
print ic_file
os.system("touch Init_cons.dat")
os.system("rm Init_cons.dat")
os.system("./InitCons/makeics.pl %s"%ic_file)

if icsonly: sys.exit('icsonly flag is on, Initi_cons.dat file made - only. Exiting.')



import netCDF4
from netCDF4 import Dataset
from scipy.io import FortranFile







ic_open= tuple(open(ic_file))
numbered = np.array([i for i in enumerate(ic_open[2].strip().split(',')[3:])])

if not keepx: numbered = filter(lambda x: x[1][0] not in 'xX', numbered)



n_runs=len(numbered)
if (ncores > n_runs): ncores = n_runs


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
        #os.system("touch Outputs/s_%s.empty"%('run',arg_in[1]))
        #os.system("rm Outputs/s_%s.*"%('run',arg_in[1]))
        start = time.strftime("%s")

        description="%s_%s"%('run',arg_in[1])
        model='model'
        if '-' in description: 
            if runsaved: model='save/exec/%s/model'%(description.split('-')[-1])
            else:  description = description.split('-')[0]
            
        print 'aaaa'    
        linenumber = "%s"%(int(arg_in[0])+1)
        run ='./%s %s %s %d'%(model, description,int(linenumber),obs)
        print run ;       os.system(run)
        return int(time.strftime("%s")) - int(start)
    except Exception as e:
        return 'Failed on '+ arg_in + e





#do runs
#########################################################################################

out = multiprocessing.Pool(ncores).map( simulate , numbered )
os.system('rm fort*')


#concat resutls
#########################################################################################
print '\n Calculations complete! \n Concatenating results. \n '

ic_string='' # get a string format of the intial conditions file
for line in ic_open[1:]: ic_string+=line

filename= ic_file.split('/')[-1].split('.')[0]+'_'+ time.strftime("%y%m%d%H%M")+'.nc'
ncfile = Dataset(filename,'w')
print 'add to results folder'
ncfile.initial_conditions_str = ic_string
ncfile.date = time.strftime("Completion time:%A %d %B %Y at %H:%M")
ncfile.description = ic_open[0].strip()

spec = ncfile.createDimension('spec', None)
time = ncfile.createDimension('time', None)
rate = ncfile.createDimension('rate', None) 


#for each simulation

l = 0 

for group_name in numbered:
    print group_name
    
    if not runsaved: group_name[1] = group_name[1].split('-')[0]
    
    group = ncfile.createGroup(group_name[1])

    specvar = group.createVariable( 'Spec' , "f8"  ,('time','spec',))
    ratevar = group.createVariable( 'Rate' , "f8"  ,('time','rate',))

    specvar[:] = read_fbin('./Outputs/run_%s_.spec'%group_name[1])
    ratevar[:] = read_fbin('./Outputs/run_%s_.rate'%group_name[1])


    l += len(specvar[:])    

    print group
    specvar.head = ''.join(tuple(open('./Outputs/spec.names'))).replace(' ','').replace('\n','')
    ratevar.head = ''.join(tuple(open('./Outputs/rate.names'))).replace(' ','').replace('\n','')
    group.WALL_time = out[int(group_name[0])]


# close the file.
ncfile.close()a

if l <= 1 :
    os.system('rm '+filename)
    print 'Failed!'
else:
    print '*** SUCCESS writing %s!'%filename



os.system('find . -size +100M | cat >> .gitignore')
