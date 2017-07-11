#!/usr/local/anaconda/bin/python
#/usr/bin/python
import glob,sys,os

##################
 ####read files####


myinclude = []

#include custom file here
custom = '\n#INCLUDE ./mechanisms/DUN15M4.kpp\n#INCLUDE ./mechanisms/inorganicM4.kpp\n'

### script options
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

else:

### default treatment

    # Retrieve list with kpp file in mechanisms folder
    file_list = glob.glob('./mechanisms/*.kpp')
    # Amend list by emission/deposition ini files
    file_list.extend(glob.glob('./InitCons/*.emi'))
    file_list.extend(glob.glob('./InitCons/*.dep'))

    # Remove previously compiled emission and deposition kpp files from file list
    for i in reversed(range(len(file_list))):
        if file_list[i][:18] == './mechanisms/depos':
            file_list.pop(i)
        elif file_list[i][:18] == './mechanisms/emiss':
            file_list.pop(i)

    # Sort files by modified dated
    file_list.sort(key=os.path.getmtime)#getmtime - modified getctime-created

    # List files for selection
    print '\n\n\033[92mSelect file(s) for KPP in the correct order\n' \
        +'(1. organic files, 2.inorganic files, 3. emission/deposition files): \033[0m\n\n'
    for i,f in enumerate(file_list): print '%3d'%i , ' - ', f.replace('./mechanisms/','').replace('./InitCons/','')

    selected_files = filter(lambda x: len(x)>0 ,   raw_input('Enter Number(s)\n').split(' '))


    #automatically select inorganic if organic only file selected
    if (len(selected_files)==1) & ('organic' in file_list[int(selected_files[0])]):
        myinclude.append('\n#INCLUDE ./mechanisms/inorganic.kpp\n')

    selected_files = map(int, selected_files)

    # Save file list of selected file as script input
    kpp_files = []
    # String of kpp files to hand over to makeINI scripts
    kpp_input = ""
    # Find kpp files
    for i in selected_files:
        if file_list[i].endswith('.kpp'):
            kpp_files.append(file_list[i])
            kpp_input += file_list[i].replace('./mechanisms/','').replace('.kpp','')+" "

    # Find ini files, call makeINI scripts and rename to correct kpp names
    for i in selected_files:
        if file_list[i][-4:] == '.emi':
            os.system('./src/background/makeemiss.pl "'\
                +kpp_input+'" '+file_list[i])
            file_list[i] = file_list[i].replace('./InitCons/','./mechanisms/emiss_').replace('.emi','.kpp')
        if file_list[i][-4:] == '.dep':
            os.system('./src/background/makedepos.pl "'\
                +kpp_input+'" '+file_list[i])
            file_list[i] = file_list[i].replace('./InitCons/','./mechanisms/depos_').replace('.dep','.kpp')
        myinclude.append('#INCLUDE '+file_list[int(i)]+'\n')


# save list of kpp files for model.kpp
if '--custom' in sys.argv:
    addstr=custom
else:
    addstr = "".join(myinclude)

# Write model.kpp
modelstring ='''// include file with definition of the chemical species
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
