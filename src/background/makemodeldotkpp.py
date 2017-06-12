#!/usr/local/anaconda/bin/python 
#/usr/bin/python
import glob,sys,os

##################
 ####read files####
 
'''
#INCLUDE ./mechanisms/organic.kpp
#INCLUDE ./mechanisms/inorganic.kpp
'''
#include custom file here 
custom = '\n'.join(tuple(open('mechanisms/geoschem/gckpp.kpp')))

if '--custom' in sys.argv: 
    myinclude=custom

else:

    file_list = glob.glob('mechanisms/*.kpp')
    file_list.sort(key=os.path.getmtime)#getmtime - modified getctime-created

    print 'Select file to open: \n\n'
    for i,f in enumerate(file_list): print i , ' - ', f.replace('./mechanisms/','')
    inc_file = file_list[int(input('Enter Number \n'))]
    
    myinclude = '#INCLUDE '+inc_file
    
    if 'organic' in inc_file: myinclude+='\n#INCLUDE ./mechanisms/inorganic.kpp'


    print myinclude





modelstring ='''
// include file with definition of the chemical species
// and chemical equations

#INCLUDE ./src/background/mechswitches.kpp

'''+myinclude+'''

#INCLUDE ./src/util.inc
#INCLUDE ./src/global.inc


#DOUBLE ON
// computer language for code produced by kpp
#LANGUAGE FORTRAN90
//#LANGUAGE FORTRAN77
// #LANGUAGE C

// initial concentrations
#INITVALUES
// conversion from mixing ratio to concentration
CFACTOR = 2.5E19;
// initial mixing ratios
ALL_SPEC = 0.;

// integrator should usually be rosenbrock

#INTEGRATOR rosenbrock
//#INTEGRATOR kpp_lsode
//#INTEGRATOR ros2_manual
//#INTEGRATOR radau5

// driver file that calls kpp subroutines
#DRIVER ./src/driver

// set indices of unused species to ind_*=0
#DUMMYINDEX ON

// do not create Stoichiom files
#STOICMAT OFF

// do not create Hessian files
#HESSIAN OFF

// do not create Mex files
#MEX OFF

// equation IDs
#EQNTAGS ON

'''

with open("model.kpp", 'w') as f:
    f.write(modelstring)
