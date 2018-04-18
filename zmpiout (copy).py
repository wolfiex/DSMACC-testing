from mpi4py import MPI
from scipy.io import FortranFile

import os,sys,time
import numpy as np

comm  = MPI.COMM_WORLD
rank = comm.rank  # The process ID (integer 0-3 for 4-process run)

#universe_size=comm.Get_attr(MPI.UNIVERSE_SIZE)
soft=int(MPI.INFO_ENV.get("soft"))
#maxprocs= int(MPI.INFO_ENV.get("maxprocs"))

#if sys.argv[1] != 'ignore':
    
try:
        ncores = int(os.popen('echo $NCPUS').read())
except:
        sys.exit('Use a Queue')



ncpus = int(comm.Get_attr(MPI.UNIVERSE_SIZE)) #int(os.popen('echo $NCPUS').read())

print 'ncpu rank', ncpus , rank , soft

if soft <2 :
        sys.exit('Use a Queue')

if soft > 80:
        sys.exit('I dont believe you are running DSMACC on %s cores, use a queue'%soft)


#if (not os.path.exists('./model') & runsaved==0): sys.exit('No model file found. Please run "make kpp" followed by "make"')


filename = 'test.h5'




groups = None

if rank == 0: 
    counter =0 
    def readfun(filename):
        '''
        reads unformatted fortran files 
        ''' 
        f = FortranFile('Outputs/'+filename, 'r')
        names = ''.join(f.read_reals('c'))
        data = []
        while True:
                try:
                    data.append(f.read_reals(dtype=np.float_))
                except TypeError:
                    break
            #array = np.reshape(array, (nspecs,-1))

        f.close()
        return [names.replace(' ',''),np.array(data)]
    
    
    from progressbar import ProgressBar
    pbar = ProgressBar().start()

    import h5py
    hf = h5py.File(filename, 'a')
    ics = []
    ics.extend([hf['icspecs'],hf['icconst']])
    [ics.append(i) for i in hf['icruns']]
    ics = np.array(ics)
    
    ############################################            
    hf.attrs['ictime']=1000
    ##################### DEL
    
    np.savetxt('Init_cons.dat', ics, fmt='%15s', delimiter='!', newline='\n', header='%s'% hf.attrs['ictime'],comments='')  

    groups = [[int(item.attrs['id']),item.name] for item in hf.values() if isinstance(item, h5py.Group)]
   

sys.stdout.flush()
comm.Barrier()    
    


groups = comm.bcast(groups,root=0)
lgroups = len(groups)
   


sys.stdout.flush()
comm.Barrier() 
    
n=rank-1
if rank>0:
    while n < lgroups:
        
        g = groups[n]
        
        obs = False
        
        print ' '
        print n, lgroups
                  
        #set the model
        model='model'
        if '-' in g[1]: 
            if runsaved: model='save/exec/%s/model'%(g[1].split('-')[-1])
            else:  description = g[1].split('-')[0]
            
        
        #run cmd
        run ='./%s %s %s %d'%(model, g[1].strip('/'),int(g[0]),obs)
        print run ;
        
        ##the actual run
        start = time.strftime("%s");os.system(run)
        wall = int(time.strftime("%s")) - int(start)

        
        #return data
        data = {'wall':wall,'group':g[1]}
        comm.isend(data, 0,tag=n)       

        #next task        
        n+=(ncpus-1)
              


if rank == 0:
   
    for i in xrange(lgroups):
    
        if counter < lgroups:
            #blocking recieve! 
            req = comm.irecv(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG)      
            req.Wait()
            g = hf[req['group']]
            
            counter+=1
            pbar.update(100*(counter/lgroups))
            
            
            print 'Finished' , req
            
            for dataset in ['spec','rate']:
                data = readfun('%s.%s'%(req['group'],dataset))
                g.attrs[dataset + u'head']  = data[0]
                
                try:
                    g.create_dataset(dataset, data=data[1], chunks=True,maxshape=(None,None))
                except:    
                    print type(g[dataset])
                    #g[dataset] = g[dataset].extend(data[1])     ### if exists extend this 
                    
                    #use lines below
                    #g[dataset].resize((g[dataset].shape[0] + data[1].shape[0]),axis=0)
                    #g[dataset][-data[1].shape[0]:] = data[1]
            ### move status bar to here !!! 
            #print g[dataset]
            
        
        
        #print req,g.items()
        
        
        
        
## Catch Everything Up!        
sys.stdout.flush()
comm.Barrier()    
    





'''
parser = argparse.ArgumentParser(description='create an ics')
parser.add_argument('-d','--dev', dest='dev', action='store_false',                     default=False, help='add a watch relaod for dev')
args = parser.parse_args()

#for debugging#
#args.dev=True
if args.dev: 
    #import ipyReload as ipr    
    #pr.watch('zics.py')
    #print 'watching'



hf = h5py.File(filename, 'a', driver='mpio', comm=comm)

if rank == 0: 
    ics = []
    ics.extend([hf['icspecs'],hf['icconst']])
    [ics.append(i) for i in hf['icruns']]
    ics = np.array(ics)
    np.savetxt('Init_cons.dat', ics, fmt='%15s', delimiter='!', newline='\n', header='%s'% hf.attrs['ictime'],comments='')


groups = [[int(item.attrs['id']),item.name] for item in hf.values() if isinstance(item, h5py.Group)]

sys.stdout.flush()
comm.Barrier()
#### CREATE MUST BE DONE BY ALL ~~~~~~~~~~~ moved ot ics now just append


for g in groups: 
    #run append= n rankn 
    
    #g = hf.create_group('%d'%n)
    
    #hf[g[1]].create_dataset('req%s'%g[0], [])
    n=1
n = rank

while n < len(groups)-1:
    print n , rank
    #g = groups[n]
    #hf[g[1]]['rank']=[rank]
    #print n, rank , hf.items()
    #g = hf.create_group('%d'%n)
    #dset = g.create_dataset('rank', 4, dtype='i')
    #dset[n]=rank
    ##hf.items()[n]
    
    #time.sleep(1)
    n += q#maxprocs
        

        



  
    #dset = hf.create_dataset(  name = str(100*n),data = [2,3,4,5], dtype='i')#,shuffle=True, chunks=True, compression="gzip", compression_opts=9)



#-l ncpus --oversubscribe


hf.close()# needs to be in main body <

'''

