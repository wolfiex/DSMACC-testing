from mpi4py import MPI
from scipy.io import FortranFile

import os,sys,time,re
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



ncpus = soft# int(comm.Get_attr(MPI.UNIVERSE_SIZE)) #int(os.popen('echo $NCPUS').read())

print 'ncpu rank', ncpus , rank , soft

if ncpus <2 :
        sys.exit('Use a Queue')

if ncpus > 80:
        sys.exit('I dont believe you are running DSMACC on %s cores, use a queue'%ncpus)


#if (not os.path.exists('./model') & runsaved==0): sys.exit('No model file found. Please run "make kpp" followed by "make"')


filename = 'BaseRun_init.h5'

obs = int(tuple(open('include.obs'))[0].strip().replace('!obs:',''))


'''
for i in sys.argv[1:]:
    if i=='--obs':
        if rank==0:print 'observations being used' 
        obs = True
    if '.h5' in i :
        filename = i.strip()    
'''


groups = None
debug=None #'for boradcast'


try:

    if rank == 0: 
        ###read args 
        extend = True 
        rewind = False
        debug = 1 
        
        if not debug: 
            os.system(' touch temp.txt && rm temp.txt')
            debug = '>>temp.txt'
            
            
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
        pbar = ProgressBar()

        import h5py
        hf = h5py.File(filename, 'a')
        ics = []
        ics.extend([hf['icspecs'],hf['icconst']])           
        
        
        
        ###extend????
        [ics.append(i) for i in hf['icruns']]
        ics = np.array(ics)
        
        ############################################            
        ###hf.attrs['ictime']=1000
        ##################### DEL
        print 'duration' , hf.attrs['ictime']
        
        np.savetxt('Init_cons.dat', ics, fmt='%15s', delimiter='!', newline='\n', header='%s'% hf.attrs['ictime'],comments='')  

        groups = [[int(item.attrs['id']),item.name] for item in hf.values() if isinstance(item, h5py.Group)]
       

    sys.stdout.flush()
    comm.Barrier()    
        

    debug = comm.bcast(debug,root=0)
    groups = comm.bcast(groups,root=0)
    lgroups = len(groups)
       


    #sys.stdout.flush()
    comm.Barrier() 
        
    n=rank-1




    if rank>0:

        
        while n < lgroups:
                
                g = groups[n]
                
                
                          
                #set the model
                model='model'
                if '-' in g[1]: 
                    if runsaved: model='save/exec/%s/model'%(g[1].split('-')[-1])
                    else:  description = g[1].split('-')[0]
                    
                
                #run cmd
                version = os.popen('./%s 0 0 --version'%(model)).read()
                run ='./%s %s %d %s'%(model,int(g[0]),obs,debug)
                print '\n'+ run, ' of version ' , version ;
                
                ##the actual run
                start = time.strftime("%s");os.system(run)
                wall = int(time.strftime("%s")) - int(start)

                
                #return data
                data = {'wall':wall,'group':g[1],'vers':version.strip(),'id':g[0]}
                comm.isend(data, 0,tag=n)       

                #next task        
                n+=(ncpus-1)


    else:
        
        for i in pbar(xrange(lgroups)):
        
                #blocking recieve! 
                req = comm.recv(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG)      
                #req.Wait()
                g = hf[req['group']]

                print 'Finished' , req, '. Cleaning and Saving.'
                
                g.attrs['version'] = req['vers']
                
                for dataset in ['spec','rate','flux']:
                    data = readfun('%s.%s'%(req['id'],dataset))     
                    
                    print data[1].shape,len(data[
                    0].split(','))#remove non/zero results through mask 
                 
                    dataarr = data[0].split(',')
                    mask = data[1].sum(axis=0)
                    if dataset != 'spec':
                        #only save reaction which contain species 
                        match = re.compile(r'\b(\w+)\b')
                        fltr=set(fltr)
                        keep = [len(set(match.findall(i))-fltr)==0 for i in dataarr]
                        
                        mask *= np.array(keep)
                    
                    mask = np.where(mask)
  
                    fltr = np.array(dataarr)[mask]
                    
                    
                    g.attrs[dataset + u'head']  = ','.join(fltr)
                    data[1]  = np.squeeze(data[1][...,mask],axis = 1)

                    try: g[dataset]
                    except:extend=False
                    
                    if not extend :
                        g.create_dataset(dataset, data=data[1] , chunks=True,maxshape=(None,None))
                    else:    
                        print 'already saved'
                        #print g[dataset]
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
            
    if rank ==0 :
        hf.close()
        print 'written' , filename
         



except Exception as e:
     
        
    #if rank ==0 :
      #  hf.close()
   
    import traceback
    sys.stdout.flush()
    traceback.print_exc() 
    
    comm.Abort()



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

