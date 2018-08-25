'''
A script to reduce compilation time of DSMACC by doing some files in parallel
This header must not be removed

Daniel Ells
daniel.ellis@york.ac.uk
'''
import os,multiprocessing,glob,time
global cmd,tuv
cmd = 'ifort -cpp -mcmodel large -O0 -fpp -traceback   -heap-arrays  -ftz -implicitnone -fp-model strict '
tuv = 'TUV_5.2.1'


def make(f):
    ''' sys call to run compiler'''
    global cmd
    print 'making',f
    os.system(' %s -c %s'%(cmd,f))
    #debug print 'done',f


def make_all():
    ''' main make function '''
    global cmd,tuv
    start_time = time.time()

    p1= ['model_Parameters.f90','model_Global.f90','model_Monitor.f90','model_Precision.f90']#jacsp can be here
    p2= ['model_Global.f90','model_Function.f90','model_JacobianSP.f90']
    p3= ['model_constants.f90','model_Initialize.f90','model_Util.f90','model_Rates.f90']
    p4= ['model_Jacobian.f90','model_LinearAlgebra.f90']
    p5= ['model_Integrator.f90']
    p6= ['model_Main.f90', 'model_Model.f90']

    cores=4 # only ever 4 files at a time based on workflow



    pool = multiprocessing.Pool(cores)
    counter = 0
    for p in [p1,p2,p3,p4,p5,p6]:
        counter += 1
        print "\033]0; compiling... %d/6 \007"%counter
        pool.map(make,p)

    print "\033]0; It all comes together \007"
    print 'Putting it all together now.'
    os.system('%s -o model *.o %s/*.o'%(cmd,tuv))

    print "--- %s seconds ---" % (time.time() - start_time)

    print "\033]0; Your model is ready \007"
    print 'Model is ready!'


if __name__ == '__main__':
    make_all()
