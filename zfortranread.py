from scipy.io import FortranFile

import os,sys,time,re,glob
import numpy as np

files = glob.glob('Outputs/*')
print files

def readfun(filename):
    '''
    reads unformatted fortran files
    '''
    f = FortranFile(filename, 'r')
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
