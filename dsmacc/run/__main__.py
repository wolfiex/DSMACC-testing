#
import argparse,os,sys

print __file__

parser = argparse.ArgumentParser(description='create an ics')
parser.add_argument('-d','--dev', dest='dev', action='store_true', default=False, help='add a watch reload for dev')
parser.add_argument('-o','--obs', dest='obs', action='store_true', default=False, help='run with obs')
parser.add_argument('-s','--spinup', dest='spinup', action='store_true', default=False, help='run with spinup')
parser.add_argument('-k','--kill', dest='kill', action='store_true', default=False, help='kill session at end of run')
parser.add_argument('--createobs', dest='createobs', action='store_true', default=False, help='create obs')
parser.add_argument('-r','--run', dest='run',nargs='?', action='store', default=False, help='run code')
#parser.add_argument('-c','--ics', dest='ics', action='store_true', default=False, help='create new ics h5')
parser.add_argument('-c','--ics', dest='ics',nargs='?', action='store', default=False, help='create new ics h5')
parser.add_argument('-l','--last', dest='last', action='store_true', default=False, help='run last ics')
#parser.add_argument('--version', dest='vers', action='store_true', default=False, help='add a watch relaod for dev')
parser.add_argument('--version', dest='vers', action='store_true', default=False, help='add a watch relaod for dev')
parser.add_argument('-v','--verbose', dest='verbose',nargs='?', action='store',     default=False, help='print temp')
args = parser.parse_args()

print 'initialisation arguments:'
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
    ncores=2

print 'cpus' ,ncores




if args.ics != False:
    import ics
    filename = ics.create_ics(fileic=args.ics, postime = args.obs,last = args.last)
    if args.run==None:args.start = filename

#if args.run==None:
#    sys.exit('You have not specified a runfile, or created one with --ics')


if args.run!=False:

    print 'Clearing Output dir'
    os.system('rm Outputs/* && mkdir Outputs')


    obs =''
    if args.obs: obs = '--obs'
    if args.spinup: obs = '--spinup'

    if ncores>1:
        cmd = 'mpiexec -n %d python zmpiout.py %s %s'%(ncores,args.start,obs)
        print cmd
        os.system(cmd)
    else:
        cmd = 'mpiexec -n %d python zmpiout.py %s %s'%(ncores,args.start,obs)
        print cmd
        os.system(cmd)
        '''
        cmd = 'python zserialout.py %s %s'%(args.start,obs)
        print cmd
        os.system(cmd)
        '''
    if args.kill:
        os.system('/opt/pbs/bin/qdel $PBS_JOBID')
        os.system('pkill screen')

if args.verbose:
     a = tuple(open('temp.txt'))
     for i in a:
         print i


print 'End of dsmacc.run'

#path to module os.path.dirname(amodule.__file__)
#if name is main run main
