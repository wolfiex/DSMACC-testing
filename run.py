#
import argparse,os,sys

parser = argparse.ArgumentParser(description='create an ics')
parser.add_argument('-d','--dev', dest='dev', action='store_true', default=False, help='add a watch reload for dev')
parser.add_argument('-o','--obs', dest='obs', action='store_true', default=False, help='run with obs')
parser.add_argument('--createobs', dest='createobs', action='store_true', default=False, help='create obs')
parser.add_argument('-s','--start', dest='start',nargs='?', action='store', default=False, help='run code')
#parser.add_argument('-c','--ics', dest='ics', action='store_true', default=False, help='create new ics h5')
parser.add_argument('-c','--ics', dest='ics',nargs='?', action='store', default=False, help='create new ics h5')
#parser.add_argument('--version', dest='vers', action='store_true', default=False, help='add a watch relaod for dev')
parser.add_argument('--version', dest='vers', action='store_true', default=False, help='add a watch relaod for dev')
args = parser.parse_args()

print args



#for debugging#
#args.dev=True
if args.dev: 
    import ipyReload as ipr   
    
    def fn(): 
    
    
        import os 
        print 'alternative command', 
        print os.system('mpirun -np 3 python zmpiout.py')   
        import time
        #time.sleep(10)    
            
    ipr.watch('zmpiout.py',fn)    
    
    print 'watching'
    

try:
    ncores = int(os.popen('echo $NCPUS').read())
except:
    ncores=1

print 'cpus' ,ncores   

if args.ics != False:
    import zics
    filename = zics.create_ics(fileic=args.ics)
    if args.start==None:args.start = filename

if args.start==None:
    sys.exit('You have not specified a runfile, or created one with --ics')
    
    
if args.start!=False:
    if ncores>1:
        cmd = 'mpiexec -n %d python zmpiout.py %s'%(ncores,args.start)
        print cmd
        os.system(cmd)
    else:
        cmd = 'python zserialout.py %s'%(args.start)
        print cmd
        os.system(cmd)


 
#if name is main run main 