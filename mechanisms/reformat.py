import pandas as pd
import numpy as np
import os, sys, multiprocessing, re, glob
from sympy import Symbol, expand, N
try:
    ncores = int(os.popen(r'echo $NCPUS').read())
except Exception as e:
    print(e)
    ncores=1
print(ncores)
available_cores=ncores
co2 =False

if co2:
    smilesdf = pd.read_csv('../src/background/smiles_mined.csv')
    smiles=pd.Series(smilesdf.smiles)
    smiles.index=smilesdf.name
    smiles['CO']='C'
    smiles['CO2']='C'
    smiles['DUMMY']=''
    smiles['NA']=''
    smiles =dict(list(zip(smiles.index,[str(i).upper().count('C') for i in smiles])))
    
    
print('THIS ADDS INORGANICS< DO NOT USE COMPLETE MECH')
print('todo - check duplicate matches, then also check combinations')

try: filename1=sys.argv[1]
except:filename1 = '../src/background/mcm331complete.kpp'
full = tuple(open(filename1))

try: filename=sys.argv[2]
except: filename = '../src/background/inorganic_mcm.kpp'
inorganics = tuple(open(filename))
 
fullstr='~'.join(full+inorganics).replace('\n','').replace('\t','').replace(' ','')
eqn = [re.sub(r"[\r\s\n]*",'',i).split(':') for i in re.findall(r'(\{[\. \s\w\d]*\}.*\:*);\r*~' ,fullstr)]



combined = [i.replace('\t','').replace(' ','').replace('\n','') for i in full+inorganics]

def iseqn (x):
    if (re.search(r'\{[\. \s\d]*\}', x)): 
        return True
    

combined1 = [i.split('}')[1].split(':')  for i in filter(iseqn ,  combined)]
    
nocoeff = re.compile(r'\b\d*\.*\d')


def pool_eqn(x):
    #sort the reactions
    r,p=x[0].split('=')
    p=p.split('+')
    p.sort()
    r=r.split('+')
    r.sort()
    if co2:
        cdiff=sum([smiles[nocoeff.sub('',i)] for i in p])-sum([smiles[nocoeff.sub('',i)] for i in r])
        if cdiff<0: p.extend(['CO2']*abs(cdiff))
        else:  p.extend(['CO2']*cdiff)
        
    
    p='+'.join(p)
    r='+'.join(r)
    x[0] = r+'='+p
    #replace D and exp for sympy  re.sub(r'(\d)[dD]([+-\.\d])',r'\1e\2',  x[1].split('//')[0].replace('EXP','exp')
    eqn[1] =  x[1].split('//')[0].replace(';','')
    return x

eqn = multiprocessing.Pool(available_cores).map(pool_eqn,combined1)


nocoeff = re.compile(r'\b[\d\.]*(\w+)\b')

specs = []
if co2:specs=['CO2']
for e in eqn:
    specs.extend(re.findall(r"[\w']+", e[0]))
    
specs = list(set([nocoeff.match(i).group(1) for i in specs]))
specs.sort()




string = '''// reformatted by reformat.py
// contact: daniel.ellis.research@googlemail.com
// filedata: %s
// %s species  %s reactions

''' %(filename1 + '+' + filename, len(specs),len(eqn))

print(string)


string += '''
#INLINE F90_GLOBAL
REAL(dp)::M, N2, O2, RO2, H2O
#ENDINLINE
#INLINE F90_RCONST
#ENDINLINE
#INCLUDE atoms
#DEFVAR
'''



for i in specs:
    if i == 'DUMMY': continue
    string += i+'=IGNORE;\n'




string +='''#INLINE F90_RCONST
USE constants
RO2 = 0'''


''' get RO2 from mechanism '''

dummy = False
ro2 = ''
for i in full:
    if 'RO2 = &' in i: dummy = True
    if 'CALL' in i: break
    if dummy: ro2+= i

ro2 = re.findall('C\(ind_[A-z0-9]*\)',ro2)
r2=re.compile(r'_([A-z0-9]*)\)')
ro2 = [y for y in ro2 if r2.search(y).group(1) in specs]

for i in ro2:
    string += '''&
+%s'''%i

string += '''
CALL mcm_constants(time, temp, M, N2, O2, RO2, H2O)
#ENDINLINE
#EQUATIONS
'''



for i,j in enumerate(eqn):
    if j[0][-1]=='=':j[0]+='DUMMY'
    string += '{%04d} %s : %s;\n'%(i,j[0],j[1].replace('\r',''))

string = re.sub(';\h*;',';',string)



ic_file = filename1.replace('../InitCons/','').replace('.csv','').replace('../src/background/','')
with open("formatted_"+ic_file, 'w') as f:
    f.write(string)

print("\n formatted_"+ic_file+' written')
    

