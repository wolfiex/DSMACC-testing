from scipy.io import FortranFile
import numpy as np

def readfun(filename):
            '''
            reads unformatted fortran files
            '''
            f = FortranFile(filename, 'r')
            names = b''.join(f.read_reals('c')).decode('utf-8')
            data = []
            while True:
                    try:
                        data.append(f.read_reals(dtype=np.float_))
                    except TypeError:
                        break
                #array = np.reshape(array, (nspecs,-1))

            f.close()
            return [names.replace(' ',''),np.array(data)]

        