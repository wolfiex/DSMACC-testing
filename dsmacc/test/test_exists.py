

def test_imports():
    '''
    Check if we are able to import the required libraries.
    '''
    imports = 'sys os hdf5 scipy mpi4py pandas dask dsmacc time re numpy'.split()
    for i in imports:
        __import__(i)

        
def test_mpi():
    '''
    Checks that the MPI processes have been set up correctly
    '''
    import os, re
    res = os.popen('mpirun -np 3 python %s'%(__file__.replace("test_exists.py","mpicheck.py"))).read()
    assert set(re.findall(r'\d',res)) == set('0 1 2'.split())


        
def test_model():
    '''
    Lets check that the model has compiled correctly
    That the output file exists
    
    
    '''
    import os
    print(os.system('ls'))
    

def test_all():
    '''
    Run dsmacc with a sample dataset 
    This removes a current mechanism
    Compiles a test one, 
    Runs it
    checks the results
    '''
    