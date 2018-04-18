#!/usr/local/anaconda/bin/python
#!/usr/bin/python
from mpi4py import MPI
import multiprocessing,os,subprocess,pickle,sys,time
import numpy as np
import glob,sys,os,re
import netCDF4
from netCDF4 import Dataset
from scipy.io import FortranFile
from pyDOE import lhs
#install pydoe using pip from pypi/packages.pyDOE



# options
available_cores = 20 
pre_formatted_style=False #slower

run_simulate = True

n_runs = 1
duration = 2400#24*60*60*2/10
 ##################
 ####read files####

ic_file = 'machine.ssv'


#get input grid
#########################################################################################
ncores= available_cores # - 6 #if 6 used from openmp?
start = (time.strftime("%Y%m%d%H%M"))

const = False
latin = False
for i in tuple(open(ic_file)):
    print i
    if type(latin)!=list:
        if type(const)!=list:
            if '!CONST' in i:
                const =[]
                continue
        else:
            if '!RANGE' in i:
                latin = []
                continue
            const.append(i.replace('\n','').split(' '))
    elif type(const)==list:
        latin.append(i.replace('\n','').split(' '))

print latin


lhs_out = lhs(len(latin),n_runs)#,criterion='maximin')

namelist = [i[0] for i in const]
constlist = [i[2] for i in const]
constval = '!'.join(['%15e'%float(i[1]) for i in const])+'!'

for i,j in enumerate(latin):
    value = lhs_out[:,i]
    value *= float(j[2])-float(j[1])
    lhs_out[:,i] = value + float(j[1])
    namelist.append(j[0])
    constlist.append(j[3])

f =open('Init_cons.dat','w')
f.write(str(duration)+"\n")
f.write('!'.join(['%15s'%i for i in namelist])+'!'+"\n")
f.write('!'.join(['%15d'%int(i) for i in constlist])+'!'+"\n")

for j in lhs_out:
    f.write(constval+'!'.join(['%15e'%float(i) for i in j])+'!'+"\n")

f.close()


################################

if (ncores > n_runs): ncores = n_runs

#################################

# run dsmacc
def simulate (arg_in):

    try:     #each system call has to be on a new line
        start = time.strftime("%s")
        description = 'machine%05d'%arg_in
        model='model'

        linenumber = "%s"%(int(arg_in)+1)
        run ='./%s %s %s 1'%(model, description,int(linenumber))
        print run ;       os.system(run)
        return int(time.strftime("%s")) - int(start)
    except Exception as e:
        return 'Failed on '+ str(arg_in) + str(e)

  


if run_simulate:
    out = multiprocessing.Pool(ncores).map( simulate , xrange(n_runs) )
os.system('rm fort*')

##############################



global read_fbin

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
    
    
    #newdata = np.array(array)[:,selected_index]
    
    #indices = xrange(0,len(array)-sets_of,sets_of)
    
    
    #newdata = newdata[indices,:]
    #return newdata
    return array
    
    
   
    
import xarray as xa
import dask.dataframe as dd
import datetime
       
specs = np.array(''.join(tuple(open('Outputs/spec.names','r'))).replace('\n','').replace(' ','').split(','))
speccol = dict(zip(specs,range(len(specs))))


selected_specs = set(specs) - set(['DUMMY','EMISS','R','LAT','LON','M','RO2','O1D'])

    
    
    
def dt (d): 
        return datetime.datetime(datetime.datetime.today().year,1,1,0,0) + datetime.timedelta(seconds= d) 
        

    
time = np.vectorize(dt)(np.array(read_fbin('Outputs/machine00000_.spec'))[:,0])    
    

import explore_dsmacc as exp































t = exp.new(filename= 'Outputs/machine00000_')

'''
    
    
import pandas as pd

specs = np.array(''.join(tuple(open('Outputs/spec.names','r'))).replace('\n','').replace(' ','').split(','))

speccol = dict(zip(specs,range(len(specs))))


selected_specs = set(specs) - set(['DUMMY','EMISS','R','LAT','LON','M','RO2','O1D'])

#selected_specs = 'TIME,CH4,N2O5,NO3,OH,NO,HO2,NO2,O3,CH3OOH,CH3O2,HONO,CO,CH3OH,HO2NO2,CH3O'.split(',')
selected_index = [speccol[i] for i in selected_specs]

sets_of = 1 # 1 = 10 minutes 
readdata = multiprocessing.Pool(ncores).map( read_fbin , ['Outputs/machine%05d_.spec'%(i) for i in xrange(n_runs)] )



time = pd.to_datetime(np.array(readdata[0])[:,0], unit='s')
hours = [t.hour for t in time]








import xarray as xa







newgroups = [[i,i+1] for i in xrange(0,len(readdata[0])-1)]


readresults = []
readgroups=[]
for j,i in enumerate(readdata):
    i[:,0]=hours
    readresults.extend(i)
    readgroups.extend(np.array(newgroups)+(len(newgroups)+1)*j)


df = pd.DataFrame(readresults)
df.columns = selected_specs
df.to_csv('readres.csv')

df1=pd.DataFrame(readgroups)
df1.to_csv('groups.csv')


'''

'''

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


for group_name in numbered:
    print group_name

    if not runsaved: group_name[1] = group_name[1].split('-')[0]

    group = ncfile.createGroup(group_name[1])

    specvar = group.createVariable( 'Spec' , "f8"  ,('time','spec',))
    ratevar = group.createVariable( 'Rate' , "f8"  ,('time','rate',))

    specvar[:] = read_fbin('./Outputs/run_%s_.spec'%group_name[1])
    ratevar[:] = read_fbin('./Outputs/run_%s_.rate'%group_name[1])

    print group
    specvar.head = ''.join(tuple(open('./Outputs/spec.names'))).replace(' ','').replace('\n','')
    ratevar.head = ''.join(tuple(open('./Outputs/rate.names'))).replace(' ','').replace('\n','')
    group.WALL_time = out[int(group_name[0])]


# close the file.
ncfile.close()
print '*** Possible-SUCCESS writing %s!'%filename

'''

os.system('find . -size +100M | cat >> .gitignore')
