#!/usr/local/anaconda/bin/python
#/usr/bin/python
import glob,sys,os

##################
 ####read files####


myinclude = []

#include custom file here 
custom = '\n'.join(tuple(open('mechanisms/geoschem/gckpp.kpp')))

if '--custom' in sys.argv: 
        None


elif '--copy' in sys.argv: 
    ## use the old model.kpp in the src folder. 
    os.system('cp ./src/model.kpp .')
    print "'./src/model.kpp' used"
    sys.exit()

elif '--default' in sys.argv:
    ## use only organic and inorganic .kpp
    myinclude.append('#INCLUDE ./mechanisms/organic.kpp\n')
    myinclude.append('#INCLUDE ./mechanisms/inorganic.kpp\n')
    myinclude.append('')

elif ('-l' in sys.argv) or ('--last' in sys.argv):
    file_list = glob.glob('mechanisms/*.kpp')
    file_list.sort(key=os.path.getmtime)
    myinclude.append('#INCLUDE '+file_list[-1]+'\n')
    if 'organic' in file_list[-1]: myinclude.append('\n#INCLUDE ./mechanisms/inorganic.kpp\n')
    



else:

    file_list = glob.glob('mechanisms/*.kpp')
    file_list.sort(key=os.path.getmtime)#getmtime - modified getctime-created
  

    print 'Select file(s) to open: \n\n'
    for i,f in enumerate(file_list): print '%3d'%i , ' - ', f.replace('mechanisms/','')
     
    selected_files = filter(lambda x: len(x)>0 ,   raw_input('Enter Number(s)\n').split(' '))
   
        
    #automatically select inorganic if organic only file selected
    if (len(selected_files)==1) & ('organic' in file_list[int(selected_files[0])]): myinclude.append('\n#INCLUDE ./mechanisms/inorganic.kpp\n')

    


    
    for i in selected_files: 
    
        if len(i) > 0:   myinclude.append('#INCLUDE '+file_list[int(i)]+'\n')



if '--custom' in sys.argv: 
        addstr=custom 
else:
        addstr = "".join(reversed(myinclude))


modelstring ='''
// include file with definition of the chemical species
// and chemical equations



#INCLUDE ./src/background/mechswitches.kpp //KEEP! 


'''+addstr+'''



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
