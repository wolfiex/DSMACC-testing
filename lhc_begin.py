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

n_runs = 300
duration = 24*60*60*2
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
available_cores = 30 
pre_formatted_style=False #slower

run_simulate = True

n_runs = 150

duration = 24*60*60*2
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

###################################################

#concat resutls
#########################################################################################
print '\n Calculations complete! \n Concatenating results. \n '

ic_string= '\n'.join(tuple(open(ic_file)))

filename= ic_file.split('/')[-1].split('.')[0]+'_'+ time.strftime("%y%m%d%H%M")+'.nc'
ncfile = Dataset(filename,'w')
print 'add to results folder'
ncfile.initial_conditions_str = ic_string
ncfile.date = time.strftime("Completion time:%A %d %B %Y at %H:%M")
ncfile.description = 'Multiple LHC runs'

spec = ncfile.createDimension('spec', None)
time = ncfile.createDimension('time', None)
rate = ncfile.createDimension('rate', None) 


#for each simulation

l = 0 

for group_name in xrange(n_runs):
    print group_name
    
    group = ncfile.createGroup(str(group_name))
    group.WALL_time= 9999
    specvar = group.createVariable( 'Spec' , "f8"  ,('time','spec',))
    ratevar = group.createVariable( 'Rate' , "f8"  ,('time','rate',))

    specvar[:] = read_fbin('./Outputs/machine%05d_.spec'%group_name)
    ratevar[:] = read_fbin('./Outputs/machine%05d_.rate'%group_name)


    l += len(specvar[:])    

    print group
    specvar.head = ''.join(tuple(open('./Outputs/spec.names'))).replace(' ','').replace('\n','')
    ratevar.head = ''.join(tuple(open('./Outputs/rate.names'))).replace(' ','').replace('\n','')
    


# close the file.
ncfile.close()

if l <= 1 :
    os.system('rm '+filename)
    print 'Failed!'
else:
    print '*** SUCCESS writing %s!'%filename
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



os.system('find . -size +100M | cat >> .gitignore')



