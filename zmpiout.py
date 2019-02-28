from mpi4py import MPI
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
    sys.exit('MPI_DSMACC:Use a Queue')



ncpus = soft# int(comm.Get_attr(MPI.UNIVERSE_SIZE)) #int(os.popen('echo $NCPUS').read())

print 'ncpu rank', ncpus , rank , soft

if ncpus <2 :
    sys.exit('MPI_DSMACC needs more cores: Use a Queue')

if ncpus > 80:
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
            print 'observations being used, number of obs: ',int(obs)
    elif i == '--spinup':
            obs = -1
            print 'Spinup period active'
    if '.h5' in i :
        filename = i.strip()
    if '--debug' in i:
        debug = True




try:

    if rank == 0:
        ###read args
        extend = True
        rewind = False
        print "\033]0; running dsmacc...  \007"

        #### jacheader ###


        ids = ''.join( reversed(list(open('model_Parameters.f90').readlines() ) )).replace(' ','')
        ids = re.findall('ind_([\w\d]+)=(\d+)',ids)
        ids = dict(([key,value] for value,key in ids))

        jacfile = ''.join( open('model_Jacobian.f90').readlines()  ).replace(' ','')
        edges = re.findall('JVS\(\d+\)=Jac_FULL\((\d+),(\d+)\)\\n*JVS\(\d+\)',jacfile)
        edges = ['->'.join([ids[i[1]],ids[i[0]]]) for i in edges]


        print len(edges)
        ### end jacheader ###

        if not debug:
            os.system(' touch temp.txt && rm temp.txt')
            debug = '>>temp.txt'

        from zuf90 import*
        from progressbar import ProgressBar,Bar


        pbar = ProgressBar(widgets=[Bar()])



        import h5py
        hf = h5py.File(filename, 'a')
        #ics = []
        #ics.extend([hf['icspecs'],hf['icconst']])



        ###extend????
        #[ics.append(i) for i in hf['icruns']]


        #ics = np.array(ics)

        head= hf.attrs['ictime'] + '\n' + '!'.join(['%15s'%i for i in hf['icspecs']])+ '\n' + '!'.join(['%15s'%i for i in hf['icconst']])


        ############################################
        ###hf.attrs['ictime']=1000
        ##################### DEL

        print 'duration' , hf.attrs['ictime']

        np.savetxt('Init_cons.dat', hf['icruns'], fmt='%15e', delimiter='!', newline='\n', header= head,comments='')

        groups = [[int(item.attrs['id']),item.name] for item in hf.values() if isinstance(item, h5py.Group)]


    sys.stdout.flush()
    comm.Barrier()


    debug = comm.bcast(debug,root=0)
    groups = comm.bcast(groups,root=0)
    obs = comm.bcast(obs,root=0)
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
                run ='./%s %d %d %s'%(model,int(g[0]),obs,debug)
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
                #clear flash
                #pbar.fd.write('\033[5m')
                #blocking recieve!
                req = comm.recv(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG)
                #req.Wait()
                g = hf[req['group']]

                print 'Finished' , req, '. Cleaning and Saving.'

                g.attrs['version'] = req['vers']
                g.attrs['wall']= req['wall']



                for dataset in savelist:
                    data = readfun('Outputs/%s.%s'%(req['id'],dataset))



                    if dataset == 'jacsp':
                        dataarr = ['TIME']
                        dataarr.extend(edges)
                    elif dataset == 'vdot':
                        dataarr = [ids[str(i+1)] for i in range(len(data[1][1]))]

                    else:
                        dataarr = data[0].split(',')


                    print data[1].shape,len(dataarr),dataset#remove non/zero results through mask


                    mask = data[1].sum(axis=0)
                    
                    if dataset == 'rate':
                        #only save reaction which contain species
                        match = re.compile(r'\b[\d\.]*(\w+)\b')
                        fltr=set(fltr)
                        keep = [len(set(match.findall(i))-fltr)==0 for i in dataarr]

                        try: mask *= np.array(keep)
                        except:None


                    mask = np.where(mask**0)

                    fltr = np.array(dataarr)[mask]
                    

                    g.attrs[dataset + u'head']  = ','.join(fltr)
                    data[1]  = np.squeeze(data[1][...,mask],axis = 1)
                    print data[1].shape,dataset






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

        import sys
        sys.stderr.flush()



    ## Catch Everything Up!
    sys.stdout.flush()
    comm.Barrier()

    if rank ==0 :
        print "\033]0; Simulation Finished \007"
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
