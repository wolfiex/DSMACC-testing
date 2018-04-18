import os
os.environ["CC"] = "gcc"
os.environ["CXX"] = "g++"

# Using post-0.2.2 scipy_distutils to display fortran compilers
from numpy.distutils.fcompiler import new_fcompiler
compiler = new_fcompiler(compiler='intel') # or new_fcompiler(compiler='intel')
compiler.dump_properties()

#Generate add.f wrapper
from numpy import f2py
with open("splinecf.f90") as sourcefile:
    sourcecode = sourcefile.read()

    '''
    print 'Fortran code'
    print sourcecode
    '''

# f2py.compile(sourcecode, modulename='add', extra_args = '--compiler=gnu --fcompiler=g$
f2py.compile(sourcecode, modulename='splinecf', extra_args = '--compiler=gnu')
# f2py.compile(sourcecode, modulename='add')

import splinecf
