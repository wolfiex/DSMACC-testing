#!/usr/local/anaconda/bin/python
#/usr/bin/python
import glob,sys,os

##################
 ####read files####


myinclude = []

if '--custom' in sys.argv:
    os.system('cp ./src/model.kpp .')
    print "'./src/model.kpp' used"
    sys.exit()

elif '--default' in sys.argv:
    myinclude.append('#INCLUDE ./mechanisms/organic.kpp\n')
    myinclude.append('#INCLUDE ./mechanisms/inorganic.kp\n')
    myinclude.append('')

else:

    inc_id = []
    file_list = glob.glob('mechanisms/*.kpp')
    file_list.sort(key=os.path.getmtime)#getmtime - modified getctime-created
    file_list.append('exit')

    print 'Select file to open: \n\n'
    for i,f in enumerate(file_list): print i , ' - ', f
    while inc_id != len(file_list)-1:
        inc_id = input('Enter Number(s)\n')
        myinclude.append('#INCLUDE '+file_list[inc_id]+'\n')

    #if 'organic' in inc_file: myinclude+='\n#INCLUDE ./mechanisms/inorganic.kpp'


print "".join(myinclude[:-1])





modelstring ='''
// include file with definition of the chemical species
// and chemical equations

'''+"".join(myinclude[:-1])+'''

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
