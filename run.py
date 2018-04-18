#
import argparse,os

parser = argparse.ArgumentParser(description='create an ics')
parser.add_argument('-d','--dev', dest='dev', action='store_true', default=False, help='add a watch relaod for dev')
parser.add_argument('-s','--start', dest='start', action='store_true', default=False, help='run code')
parser.add_argument('-c','--ics', dest='ics', action='store_true', default=False, help='create new ics h5')
#parser.add_argument('--version', dest='vers', action='store_true', default=False, help='add a watch relaod for dev')
parser.add_argument('--version', dest='vers', action='store_true', default=False, help='add a watch relaod for dev')
args = parser.parse_args()

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

print args


if args.ics:
    import zics



if args.start:
    if ncores>1:
        cmd = 'mpiexec -n %d python zmpiout.py '%ncores
        print cmd
        os.system(cmd)
    else:
        cmd = 'mpiexec -n 2 --oversubscribe python zmpiout.py'
        print cmd
        os.system(cmd)


        
