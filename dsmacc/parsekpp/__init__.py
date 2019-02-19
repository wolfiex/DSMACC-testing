name = "parsekpp"
from ..helperscripts import picker
import glob,sys,os,re

def make_model_dot(last = False):
    '''
    if last takes latest changed files
    '''

    vers = 'Unknown'
    tuv='1'

    verre = re.compile(r'\/\/\s*(?i)ver[s]*\s*[:=]\s*\'(.*)\'')
    tuvre = re.compile(r'\/\/\s*(?i)tuv\s*[:=]\s*\'(.*)\'')

    if last:
        file_list = glob.glob('mechanisms/*.kpp')
        file_list.sort(key=os.path.getmtime)
        file_list = [file_list[-1].replace('mechanisms/','').replace('.kpp','')]

    else:
        file_list = picker.Picker('mechanisms/*.kpp',remove=['mechanisms/','.kpp'],title = 'Select Mechanisms').getSelected()

    print file_list

    myinclude = []

    for thisfile in file_list:
                myinclude.append('#INCLUDE mechanisms/'+thisfile+'.kpp\n')

                for line in tuple(open('mechanisms/'+thisfile+'.kpp')):
                    if verre.match(line):
                        vers = verre.match(line).group(1)
                    if tuvre.match(line):
                        tuv = tuvre.match(line).group(1)


    print 'tuv',tuv,'. ver',vers

    addstr = "".join(reversed(myinclude))

    modelstring ='''
    // include file with definition of the chemical species
    // and chemical equations
    #INCLUDE ./src/background/mechswitches.kpp //KEEP!
    '''+addstr+'''
    #INCLUDE ./src/util.inc
    #INCLUDE ./src/global.inc
    #INLINE F90_GLOBAL
    !model  variable parameters
    character(len=30) :: version="'''+vers+'''"
    INTEGER :: TUVvers='''+str(int(tuv))+'''
    #ENDINLINE
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

    with open("./model.kpp", 'w') as f:
        f.write(modelstring)
    print 'written file'
