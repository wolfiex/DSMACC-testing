from scipy.io import FortranFile

import os,sys,time,re,glob
import numpy as np

if __name__ == '__main__':
    files = glob.glob('Outputs/*')
    print files

def readfun(filename,header = True):
    '''
    reads unformatted fortran files
    '''
    f = FortranFile(filename, 'r')
    names = ''
    if header:
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
    
    


def asdf(filename):
    import pandas as pd
    data = readfun(filename)
    df = pd.DataFrame(data[1])
    df.columns = data[0].split(',')
    return df
