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

else:

# Retrieve list with kpp file in mechanisms folder
    file_list = glob.glob('mechanisms/*.kpp')

# Remove emission and deposition files from file list
    try:
        file_list.remove('mechanisms/emiss.kpp')
    except:
        pass
    try:
        file_list.remove('mechanisms/depos.kpp')
    except:
        pass
# Sort files by modified dated
    file_list.sort(key=os.path.getmtime)#getmtime - modified getctime-created
# Add options for emissions and deposisitions
    file_list.append('emiss.dat (from InitCons)')
    file_list.append('depos.dat (from InitCons using standard vd)')
    file_list.append('depos.dat (from InitCons without standard vd)')


    print '\n\n\033[92mSelect file(s) for KPP in the correct order\n' \
        +'(1. organic files, 2.inorganic files, 3. emission/deposition files): \033[0m\n\n'
    for i,f in enumerate(file_list): print '%3d'%i , ' - ', f.replace('mechanisms/','')

    selected_files = filter(lambda x: len(x)>0 ,   raw_input('Enter Number(s)\n').split(' '))
    file_list[-3:] = ['mechanisms/emiss.kpp', 'mechanisms/depos.kpp', 'mechanisms/depos.kpp'] # define file names



    #automatically select inorganic if organic only file selected
    if (len(selected_files)==1) & ('organic' in file_list[int(selected_files[0])]): myinclude.append('\n#INCLUDE ./mechanisms/inorganic.kpp\n')


    for i in selected_files:
        if len(i) > 0:
            myinclude.append('#INCLUDE '+file_list[int(i)]+'\n')
            #if(int(i)==len(file_list)-3: os.system('cd mechanisms && perl makedepos.pl "')


if '--custom' in sys.argv:
        addstr=custom
else:
        addstr = "".join(myinclude)


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

selected_files = map(int, selected_files)

# Save file list of selected file as script input
kpp_files = []
for i in selected_files:
    if i < len(file_list)-3:
        file_list[i]
        kpp_files.append((file_list[i].replace('mechanisms/','').replace('.kpp','')))
kpp_files = '"'+" ".join(kpp_files)+'"'
# for i in selected_files:
#     print " ".join(file_list[int(i)])

# Generate correct ini kpp files
for i in selected_files:
    if i == len(file_list)-3: os.system('cd mechanisms && ./makeemiss.pl '+kpp_files+' && cd ..')
    if i == len(file_list)-2: os.system('cd mechanisms && ./makedepos.pl '+kpp_files+' && cd ..')
    if i == len(file_list)-1: os.system('cd mechanisms && ./makedepos.pl '+kpp_files+' ../InitCons/depos.dat 0 && cd ..')

