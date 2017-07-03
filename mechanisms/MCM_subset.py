#!/usr/bin/python
''' 
A program to extract relevant data regarding the MCM, 
to be used for extracting subsets

D.Ellis 2016
'''

import pandas as pd
import numpy as np
import os, sys, multiprocessing,re , glob
from sympy import *
available_cores = 16
include_CO2 = True
import re as rx

try: filename1=sys.argv[1]
except:filename1 = 'mcm331complete.kpp'
full = tuple(open(filename1))
try: filename=sys.argv[2]
except:filename = 'inorganic_mcm.kpp'
inorganics = tuple(open(filename))
##############





gen = xrange(len(full))
nocoeff = rx.compile(r'\b[\d\.]*(\w+)\b')

''' Step 1 extract all species '''
inorganic_species =  set(rx.findall(r'([A-z0-9]*)[\s=]*IGNORE' ,str(inorganics)))
all_species =  rx.findall(r'\b[\d\.]*(\w+)\b[\s=]*IGNORE' ,str(full))
if all_species==[]: sys.exit('Failed to load file-'+filename1)
sarr = pd.Series(index=all_species)
sarr[:]=-1

#dictionarys for reference
num2spec = dict(enumerate(all_species))
spec2num = {v: k for k, v in num2spec.iteritems()}


''' Step 2 split array into reactants and products '''
fullstr=''.join(full+inorganics).replace('\n','').replace('\t','').replace(' ','')
eqn = [i.replace(' ','').split(':') for i in rx.findall(r'[^/]{0,2}\{[\. \s\w\d]*\}([A-z0-9+-=:()*/]*);' ,fullstr)] 

''' Step3 remove duplicate reactions and merge rates'''
#merge duplicated reactions

def reorder(x):
    r,p=x.split('=')
    p=p.split('+')
    p.sort()
    p='+'.join(p)
    r=r.split('+')
    r.sort()
    r='+'.join(r)
    return r+'='+p


eqdf = pd.DataFrame(eqn) 
eqdf[0] = [reorder(i) for i in eqdf[0]]
eqdf[1] =[rx.sub(r'(\d)[dD]([+-\.\d])',r'\1e\2',  str(i).split('//')[0].replace('EXP','exp')) for i in eqdf[1]]
 
 
grp = ','.join(eqdf[1])
constants = rx.findall(r'\b([A-z]\w+)\b',grp)
for i in set(constants+['M','J']):  exec(i + '= symbols("%s")'%i)
 
#eqdf[1] =[exec('str(N(expand(%s),3))'%(i)) for i in eqdf[1]]

print 'compile all res' 
print 'waiting for simplification'

new1=[]
for i in eqdf[1]:
    exec('dummyvar = str(N(simplify(%s),3))'%(i.replace(';','')))#symbolic engineness
    new1.append(dummyvar)


eqdf[1]=new1

eqdf = eqdf.drop_duplicates() #remove exact duplicates
# combine reaction rates for other duplicates
dupreactions = np.array(eqdf[eqdf[0].duplicated()][0])
dup = eqdf[0].duplicated(keep=False)
eqn = np.array(eqdf[[not i for i in dup]])
for q in dupreactions: 
    exec('joined = str(N(simplify(%s),3))'%('+'.join(eqdf[eqdf[0] == q][1])))
    eqn = np.append(eqn,[q,joined])
try: eqn.shape[1]
except: eqn = eqn.reshape((len(eqn)/2,2))






equations = [ i[0].split('=') for i in eqn]

 
''' Step 3 split into arrays of each reactant / product '''
eq_split = [[set(i[0].split('+')), set(i[1].split('+'))] for i in equations]
gen = xrange(len(equations))


''' Step 4 get primary species'''

###selcted species - if use_origin=True
# all -a else select init cons file

file_list = glob.glob('../InitCons/*.csv')

print 'Select file to open: \n\n'
print 'a  -  all'
for i,f in enumerate(file_list): print i , ' - ', f

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


origin |= {'O3','NO','NO2','CH4'}
species = origin | inorganic_species ^ set ([''])#set(['H2','CO']) ^ set ([''])#inorganic_species ^ set ([''])



#make into a class with run number
''' Step 5 get all species formed ''' 

print 'use sympy on eqn'

counter = 0 
previous = '' 


for i in species: 
    try:        
        if sarr[i] < 0 :
            print i
            sarr[spec2num[i]]= 0
    except: print i      

while True: 
    counter += 1 
    print counter

    dummy = []
    for i in gen:
        if eq_split[i][0].issubset(species): 
            dummy.extend(eq_split[i][1])

    species = set([nocoeff.match(i).group(1) if i!= '' else ''  for i in  species | set(dummy)])
    print species
    
    for i in dummy:
        try:
            if sarr[i] < 0 :
                print i
                sarr[spec2num[i]] = counter
        except: print 'skipping-'+i
    dummy = []

    if previous == species: break
    previous = species



reactions = []

for i in gen:
    if (eq_split[i][0].issubset(species)) and (eq_split[i][1].issubset(species)): reactions.append(i)
    

### using all reactions generated from specie list 
##  if a species is in the products, and all reactants present...
#   this is a generation reaction


def trace( spec ):
    created = []
    loss = []
    for i in reactions: 
        if  spec in eq_split[i][1]: created.append(eqn[i] )
        elif spec in eq_split[i][0]:   loss.append(eqn[i] )
    return [created,loss]

 
s = sarr[sarr>-1]
xpos = np.linspace(0,1,s.max()+1)




c =[]

if include_CO2: 

    species = species^set(['CO2'])

    def is_excited (x):
        try: return len(cs.findall(smiles[r[:-1]])) 
        except Exception as e: print str(e)+x; return 0

    cs= rx.compile(r'c',rx.IGNORECASE)

    cstr =''
    smilesdf = pd.read_csv('../src/background/smiles_mined.csv')
    smiles=pd.Series(smilesdf.smiles)
    smiles.index=smilesdf.name
    smiles['CO']='C'
      
    for i in eq_split:
        rc,pc=0,0
        for r in i[0]: 
            try:rc+= len(cs.findall(smiles[r]))  
            except : print r #rc += is_excited(r)     
        for p in i[1]: 
            try:pc+= len(cs.findall(smiles[p]))  
            except : print p #pc += is_excited(r)           
        
        
        if rc-pc != 0: 
        
            c.append('+'.join([j for j in i[0]]) + '=' + '+'.join([j for j in i[1]]))
            cstr += '+'.join([j for j in i[0]]) + ' --> ' + '+'.join([j for j in i[1]]) + '  ' + str(rc-pc) + ' r:%s p:%s '%(rc,pc)+ '\n'

    with open('C_mismatch.txt', 'w') as f: f.write(cstr)
    
    

traces = multiprocessing.Pool(4).map( trace , s.index ) 

species = species-set(['EMISS','DUMMY'])


dummy = False
ro2 = ''
for i in full: 
    if 'RO2 = &' in i: dummy = True
    if 'CALL' in i: break
    if dummy: ro2+= i 
    
ro2 = rx.findall('C\(ind_[A-z0-9]*\)',ro2)
ro2 = [y for y in ro2 if rx.search('_([A-z0-9]*)\)',y).group(1) in species]




string = '''// parsed by MCMsubset.py 
// contact: daniel.ellis.research@googlemail.com
// filedata: %s
// primary organics: %s
// %s species  %s reactions

''' %(ic_file,list(origin),len(species),len(reactions))

print string

string += '''
#INLINE F90_GLOBAL
REAL(dp)::M, N2, O2, RO2, H2O
#ENDINLINE
#INLINE F90_RCONST
#ENDINLINE 
#INCLUDE atoms
#DEFVAR
'''

#HNO3=IGNORE;
#SO2=IGNORE;
#SO3=IGNORE;
#NO3=IGNORE;

for i in species:
    if i == '': continue#i = 'DUMMY'
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

'''
dummy = False
for i in inorganics:
    if '#EQUATIONS' in i: dummy = True
    if dummy:
        string += i 
'''

for i in reactions:
    j = eqn[i]
    if j[0] in c: j[0]=j[0]+'+CO2'
    string += '{%04d} %s : %s;\n'%(i,j[0],j[1]) 






string = rx.sub(r';\h*;',';',string)

with open("subset_"+filename1, 'w') as f:
    f.write(string)
    print "\n subset_"+filename1+' written'
    






