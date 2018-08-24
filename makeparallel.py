import os,multiprocessing,glob

cmd = 'ifort -cpp -mcmodel large -O0 -fpp -traceback   -heap-arrays  -ftz -implicitnone -fp-model strict '
tuv = 'TUV_5.2.1'

try:
    cores = int(sys.argv[1])
except:
    cores=4

def make(f):
    print 'making',f
    os.system(' %s -c %s'%(cmd,f))

precom = glob.glob('model_*.f90')+glob.glob(tuv+'/*.f*')

multiprocessing.Pool(cores).map(make,precom)

os.system('%s -o model1 *.o %s/*.o'%(cmd,tuv))

print 'model is ready'
