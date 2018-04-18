#!/usr/bin/python
'''
A program to extract relevant data regarding the MCM,
to be used for extracting subsets

use --CO2 to inclide co2 reactions where all species have smiles strings (i.e. MCM)
use --onefile to ignore inorganics
use --RO2 to add R as a reaction species for all RO2 reactions.
use --primary only use species from orgin (set below) in addition to inorganics. If --onefile is used, only reactions containing reactants entirely from origin are used. Not using this flag prompts for a IC file selection, or all option during the program run. {'O3','NO','NO2','CH4'} are added automatically
use --additional:<filename.add> for additional functions to model.kpp (e.g. --additional:geosfns.add)

D.Ellis 2017
'''

import pandas as pd
import numpy as np
import os, sys, multiprocessing, re, glob
from sympy import Symbol, expand, N

available_cores = 4
origin='NO,CH4'

print sys.argv



simplify = '--simplify' in sys.argv
include_CO2 = '--CO2' in sys.argv
single_file= '--onefile' in sys.argv
include_RO2 = '--RO2' in sys.argv
if '--primary' in sys.argv: origin = set(origin.split(','))
else: origin = set()

additional = False
for i in sys.argv:
    if '--additional:' in i:
        additional = i.replace('--additional:','')
        break

sys.argv = list(filter(lambda x: '--' not in x, sys.argv))#remove any flags, leaving only filenames

try: filename1=sys.argv[1]
except:filename1 = '../src/background/mcm331complete.kpp'
full = tuple(open(filename1))

TUVvers=''
for i in full:
    if 'TUVvers' in i:
        print i
        TUVvers = '''
#INLINE F90_INIT
  TUVvers = %d
#ENDINLINE'''%int(re.findall(r'=\s*(\d+)\s*', i)[0])
        break

if(single_file):
    print 'only using one file'
    inorganics=()
else:
    try: filename=sys.argv[2]
    except: filename = '../src/background/inorganic_mcm.kpp'
    inorganics = tuple(open(filename))
##############

gen = xrange(len(full))
nocoeff = re.compile(r'\b[\d\.]*(\w+)\b')
ic_file = 'primary'

####################################################################################


####################################################################################
''' Step 1 split array into reactants and products '''
fullstr='~'.join(full+inorganics).replace('\n','').replace('\t','').replace(' ','')
eqn = [i.replace(' ','').split(':') for i in re.findall(r'[^/]{0,2}\{[\. \s\w\d]*\}([A-z0-9+-=:()*/]*);~' ,fullstr)]

#sort
eqn = sorted(eqn,key = lambda x: x[1])



allspecstest = '='.join([i[0] for i in eqn])
all_species = set(nocoeff.findall(allspecstest))

inorganic_species = set(['DUMMY', 'N2O5', 'H2O2', 'NO', 'H2', 'NA', 'HONO', 'OH', 'SO2', 'O', 'HNO3', 'SO3', 'O1D', 'HO2', 'HO2NO2', 'CO', 'SA', 'O3', 'HSO3', 'NO2', 'NO3'])
 #inorganic_species =   set(re.findall(r'[^/]{0,2}\{[\. \s\w\d]*\}([A-z0-9+-=:()*/]*);~' ,'~'.join(inorganics).replace('\n','').replace('\t','').replace(' ','')))


''' Step 1 extract all species '''
#inorganic_species = set(re.findall(r'([A-z0-9]*)[\s=]*IGNORE' ,str(inorganics)))
#'all_species = re.findall(r'\b[\d\.]*(\w+)\b[\s=]*IGNORE' ,str(full))

if all_species==[]: sys.exit('Failed to load file-'+filename1)

#species dataframe
sarr = pd.Series(index=all_species); sarr[:]=-1

#dictionarys for reference
num2spec = dict(enumerate(all_species))
spec2num = {v: k for k, v in num2spec.iteritems()}



####################################################################################
''' Step 3 remove duplicate reactions and merge rates'''
#merge duplicated reactions

def pool_eqn(x):
    #sort the reactions
    r,p=x[0].split('=')
    p=p.split('+')
    p.sort()
    p='+'.join(p)
    r=r.split('+')
    r.sort()
    r='+'.join(r)
    x[0] = r+'='+p
    #replace D and exp for sympy
    x[1] = re.sub(r'(\d)[dD]([+-\.\d])',r'\1e\2',  x[1].split('//')[0].replace('EXP','exp').replace(';',''))
    return x

eqn = multiprocessing.Pool(available_cores).map(pool_eqn,eqn)
eqdf = pd.DataFrame(eqn)
eqdf.drop_duplicates(inplace=True) #remove exact duplicates

#get constants as not to confuse sympy
constants = re.findall(r'\b([A-z]\w+)\b',','.join(eqdf[1]))
for i in set(constants+['M','J']):  exec(i + '= Symbol("%s")'%i)

#duplicate reactions
dup_rxn = np.array(eqdf[eqdf[0].duplicated()][0])
dup = eqdf[0].duplicated(keep=False)

print 'waiting for simplification'

eqn = np.array(eqdf[[not i for i in dup]])

for q in dup_rxn:
    eqn = np.append(eqn,[q,'+'.join(eqdf[eqdf[0] == q][1])])

try: eqn.shape[1]
except: eqn = eqn.reshape((len(eqn)/2,2))


if simplify:
    def simplifyn(x):
        exec('x[1] = str(N(expand(%s),3))'%x[1])
        return x
else:
    def simplifyn(x):
        return x


eqn = multiprocessing.Pool(available_cores).map(simplifyn,eqn)



####################################################################################

''' Step 4 split into arrays of each reactant / product '''
def prodrct(x):
    i = x[0].split('=')
    return [set(nocoeff.findall(i[0])), set(nocoeff.findall(i[1]))]

eq_split = multiprocessing.Pool(available_cores).map(prodrct,eqn)
gen = xrange(len(eqn))


####################################################################################

''' Step 5 select primary species'''

if not len(origin):

    file_list = glob.glob('../InitCons/*.csv')

    print 'Select file to open: \n\n'
    print 'a  -  all'
    for i,f in enumerate(file_list): print i , ' - ', f.replace('../InitCons/','')

    inpt = raw_input('Enter Number \n')

    if inpt=='a':
        print 'all species selected'
        origin = set(all_species)
        ic_file = 'full mcm organics'
    else:
        ic_file = file_list[int(inpt)]
        print ic_file
        ics = pd.read_csv(ic_file,header=2)
        origin = set(ics['Species'].iloc[9:])


species = origin | {'O3','NO','NO2','CH4'}
if not single_file : species |= inorganic_species



####################################################################################

''' Step 6 Formation loop '''
# sarr contains cycle in which species first appears.

counter = 0
previous = ''
for i in species:
    try:
        if sarr[i] < 0 : sarr[spec2num[i]]= 0
    except: None


#main loop
while True:
    newlyfound = ''
    skipped = ''
    counter += 1 ;print str(counter) + ["th", "st", "nd", "rd"][counter%10 if counter%10<4 and not (10<counter%100<14) else 0] + '\033[37m iteration'

    dummy = []
    for i in gen:
        if eq_split[i][0].issubset(species):
            dummy.extend(eq_split[i][1])

    species = set([nocoeff.match(i).group(1) if i!= '' else ''  for i in  species | set(dummy)])

    for i in dummy:
        try:
            if sarr[i] < 0 :
                newlyfound += ' '+i
                sarr[spec2num[i]] = counter
        except:
            if i!='DUMMY':skipped += ' '+i

    print '\033[90m NewlyFormed: '+newlyfound
    print ' Skipped: '+skipped+'\33[00m'

    dummy = []

    if previous == species: break
    previous = species


#get reaction names
def isrxn (i):
    if eq_split[i][0].issubset(species) + eq_split[i][1].issubset(species) == 2:    return int(i)

reactions  = [x for x in multiprocessing.Pool(available_cores).map(isrxn,gen) if x!=None]

eq_split = np.array(eq_split)[reactions]
eqn = np.array(eqn)[reactions]
species = species-set(['EMISS','DUMMY'])



####################################################################################

''' CO2 addition '''
#cstr is a diagnostic for addition / loss
# additional cs are added to C_mismatch.txt
if include_CO2 and ('CO2' not in all_species):
    print 'Including CO2'
    c=[]
    species = species|set(['CO2'])

    '''
    def is_excited (x):
        try: return len(cs.findall(smiles[r[:-1]]))
        except Exception as e: print str(e)+x; return 0
    '''

    cs= re.compile(r'c',re.IGNORECASE)

    cstr =''
    smilesdf = pd.read_csv('../src/background/smiles_mined.csv')
    smiles=pd.Series(smilesdf.smiles)
    smiles.index=smilesdf.name
    smiles['CO']='C'
    smiles['CO2']='C'

    for n,i in enumerate(eq_split):
        rc,pc=0,0
        for r in i[0]:
            try:rc+= len(cs.findall(smiles[r]))
            except : None #rc += is_excited(r)
        for p in i[1]:
            try:pc+= len(cs.findall(smiles[p]))
            except : None #pc += is_excited(r)

        if rc-pc != 0:
            print n
            c.append(n)
            cstr += '+'.join([j for j in i[0]]) + ' --> ' + '+'.join([j for j in i[1]]) + '  ' + str(rc-pc) + ' r:%s p:%s '%(rc,pc)+ '\n'
            eqn[n][0]+='+CO2'

    with open('C_mismatch.txt', 'w') as f: f.write(cstr)


''' RO2 addition '''
#since RO2 species do not appear in the RO2 reactions,
#an R species is added to the mechanism in order to keep track of this.
# R is defined as a fix variable == 1

if include_RO2 and ('RO2' not in all_species):
    print 'Including RO2'

    r=[]
    rs= re.compile(r'\*RO2',re.IGNORECASE)
    for n,i in enumerate(eqn):
        if rs.search(i[1]):
            r.append(n)
            eqn[n][0]= 'R+'+eqn[n][0]


####################################################################################

''' FILESTUFFS '''


####################################################################################

''' get RO2 from mechanism '''

dummy = False
ro2 = ''
for i in full:
    if 'RO2 = &' in i: dummy = True
    if 'CALL' in i: break
    if dummy: ro2+= i

ro2 = re.findall('C\(ind_[A-z0-9]*\)',ro2)
r2=re.compile(r'_([A-z0-9]*)\)')
ro2 = [y for y in ro2 if r2.search(y).group(1) in species]


'''
correct species only
'''

species = list(set(species))
species.sort()

if inpt=='a': origin=['all']

string = '''// parsed by MCMsubset.py
// contact: daniel.ellis.research@googlemail.com
// filedata: %s
// primary organics: %s
// %s species  %s reactions

''' %(ic_file,list(origin),len(species),len(reactions))

print string

string+= TUVvers

string += '''
#INLINE F90_GLOBAL
REAL(dp)::M, N2, O2, RO2, H2O
#ENDINLINE
#INLINE F90_RCONST
#ENDINLINE
#INCLUDE atoms
#DEFVAR
'''

rint = re.compile(r'\d')

for i in species:
    if i == '' or i[0].isdigit(): continue#i = 'DUMMY'
    string += i+'=IGNORE;\n'

string +='''#INLINE F90_RCONST
USE constants
RO2 = 0'''

for i in ro2:
    string += '''&
+%s'''%i

string += '''
CALL mcm_constants(time, temp, M, N2, O2, RO2, H2O)
#ENDINLINE
#EQUATIONS
'''

for i,j in enumerate(eqn):
    string += '{%04d} %s : %s;\n'%(i,j[0],j[1])

string = re.sub(r';\h*;',';',string)

if additional:
    string+= '''
#INCLUDE ./mechanisms/''' + additional


ic_file = filename1.replace('../InitCons/','').replace('.csv','').replace('../src/background/','')
with open("subset_"+ic_file, 'w') as f:
    f.write(string)
    print "\n subset_"+ic_file+' written'
