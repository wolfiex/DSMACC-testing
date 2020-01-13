from uf90 import readfun
from mpi4py import MPI
import os,sys,time,re
import numpy as np

comm  = MPI.COMM_WORLD
rank = comm.rank  # The process ID (integer 0-3 for 4-process run)

#universe_size=comm.Get_attr(MPI.UNIVERSE_SIZE)

try:
    soft=int(MPI.INFO_ENV.get("soft"))
except:
    print('cant find MPI soft, using 2 cores')
    soft = 2
#maxprocs= int(MPI.INFO_ENV.get("maxprocs"))

#if sys.argv[1] != 'ignore':
'''
try:
        ncores = int(os.popen('echo $NCPUS').read())
except:
    sys.exit('MPI_DSMACC:Use a Queue')

'''

ncpus = soft# int(comm.Get_attr(MPI.UNIVERSE_SIZE)) #int(os.popen('echo $NCPUS').read())

print(('ncpu rank', ncpus , rank , soft))

if ncpus <2 :
    ncpus = 2
    #sys.exit('MPI_DSMACC needs more cores: Use a Queue')

if ncpus > 130:
        sys.exit('I dont believe you are running DSMACC on %s cores, use a queue'%ncpus)


#if (not os.path.exists('./model') & runsaved==0): sys.exit('No model file found. Please run "make kpp" followed by "make"')


#filename = sys.argv[1]

obs=False
groups = None
debug=None #'for boradcast'
savelist = ['spec','rate','flux','vdot','jacsp']


for i in sys.argv[1:]:
    if i=='--obs':
        if rank==0:
            obs = int(tuple(open('include.obs'))[0].strip().replace('!obs:',''))
            print('observations being used, number of obs: ',int(obs))
    elif i == '--spinup':
            obs = -1
            print('Spinup period active')
    if '.h5' in i :
        filename = i.strip()
    if '--debug' in i:
        debug = True

#print ('dsfds',__file__,os.popen('pwd').read())

try:
    
    if rank == 0:
        ###read args
        extend = True
        rewind = False
        print("\033]0; running dsmacc...  \007")

        #### jacheader ###

        import h5py
        hf = h5py.File(filename, 'a')
        
        
        ids = ''.join( reversed(list(open('model_Parameters.f90').readlines() ) )).replace(' ','')
        ids = re.findall('ind_([\w\d]+)=(\d+)',ids)
        ids = dict(([key,value] for value,key in ids))

        jacfile = ''.join( open('model_Jacobian.f90').readlines()  ).replace(' ','')
        edges = re.findall('JVS\(\d+\)=Jac_FULL\((\d+),(\d+)\)\\n*JVS\(\d+\)',jacfile)
        edges = ['->'.join([ids[i[1]],ids[i[0]]]) for i in edges]


        print('edges:',len(edges))
        ### end jacheader ###

        if not debug:
            os.system(' touch temp.txt && rm temp.txt')
            debug = '>>temp.txt'

        head= hf.attrs['ictime'] + '\n' + '!'.join(['%15s'%i.decode('utf-8') for i in hf['icspecs']])+ '\n' + '!'.join(['%15s'%i for i in hf['icconst']])


        ############################################
        ###hf.attrs['ictime']=1000
        ##################### DEL

        print('duration' , hf.attrs['ictime'])
        
        
        #print (np.array(head))
        
        np.savetxt('Init_cons.dat', hf['icruns'], fmt='%15e', delimiter='!', newline='\n', header= head,comments='')
        
        #print(os.popen('less Init_cons.dat').read())

        groups = [[int(item.attrs['id']),item.name] for item in list(hf.values()) if isinstance(item, h5py.Group)]

        
        
        
    sys.stdout.flush()
    comm.Barrier()
    #print ('barrier')

    debug = comm.bcast(debug,root=0)
    groups = comm.bcast(groups,root=0)
    obs = comm.bcast(obs,root=0)
    lgroups = len(groups)

    #sys.stdout.flush()
    #print ('barrier:bcast')
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
                run ='./%s %d %d %s'%(model,int(g[0]),obs,debug)
                print('\n'+ run, ' of version ' , version) ;

                ##the actual run
                start = time.strftime("%s");os.system(run)
                wall = int(time.strftime("%s")) - int(start)


                #return data
                data = {'wall':wall,'group':g[1],'vers':version.strip(),'id':g[0]}
                comm.isend(data, 0,tag=n)

                #next task
                n+=(ncpus-1)


    else:

        for i in range(lgroups):
                
                print('Progress: %02d '%((float(i)/lgroups)*100.))
                
                req = comm.recv(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG)
                #req.Wait()
                g = hf[req['group']]
                
                print('Finished' , req, '. Cleaning and Saving.')

                

                g.attrs['version'] = req['vers']
                g.attrs['wall']= req['wall']


                
                for dataset in savelist:
                    data = readfun('Outputs/%s.%s'%(req['id'],dataset))
                    
                    if data[1].shape[0] == 0:
                        print(( 'no values found, skipping: ',  dataset))
                        continue
                    

                    if dataset == 'jacsp':
                        dataarr = ['TIME']
                        dataarr.extend(edges)
                    elif dataset == 'vdot':
                        dataarr = [ids[str(i+1)] for i in range(len(data[1][1]))]

                    else:
                        dataarr = data[0].split(',')


                    print(data[1].shape,len(dataarr),dataset)#remove non/
                    #zero results through mask

                    mask = np.array(data[1].sum(axis=0))
                    if dataset == 'spec':
                        mask[:12] = 1.
                    elif dataset == 'rate':
                        #only save reaction which contain species
                        match = re.compile(r'\b[\d\.]*(\w+)\b')
                        fltr=set(fltr)
                        keep = [len(set(match.findall(i))-fltr)==0 for i in dataarr]

                        try: mask *= np.array(keep)
                        except:None


                    mask = np.where(mask)

                    fltr = np.array(dataarr)[mask]


                    g.attrs[dataset + 'head']  = ','.join(fltr)
                    data[1]  = np.squeeze(data[1][...,mask],axis = 1)
                    print(data[1].shape,dataset)






                    try: g[dataset]
                    except:extend=False

                    if not extend :
                        g.create_dataset(dataset, data=data[1] , chunks=True,maxshape=(None,None))
                    else:
                        print('already saved')
                        #print g[dataset]
                        #g[dataset] = g[dataset].extend(data[1])     ### if exists extend this

                        #use lines below
                        #g[dataset].resize((g[dataset].shape[0] + data[1].shape[0]),axis=0)
                        #g[dataset][-data[1].shape[0]:] = data[1]
                    ### move status bar to here !!!
                    #print g[dataset]



            #print req,g.items()

        sys.stderr.flush()



    ## Catch Everything Up!
    sys.stdout.flush()
    comm.Barrier()

    if rank ==0 :
        print("\033]0; Simulation Finished \007")
        hf.close()
        print('written' , filename)




except Exception as e:

    #if rank ==0 :
      #  hf.close()
    print('Failed run',e)

    import traceback
    sys.stdout.flush()
    traceback.print_exc()

    comm.Abort()


