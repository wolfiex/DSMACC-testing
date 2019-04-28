name = "reformat"
#from ..helperscripts import picker
import glob,sys,os,re,pathos
import pandas as pd
import numpy as np
from sympy import Symbol, expand, N

def iseqn (x):
    #find equations
    if (re.search(r'\{[\. \s\d]*\}', x)):
        return True

def pool_eqn(x):
    #sort the reactions
    r,p=x[0].split('=')
    p=p.split('+')
    p.sort()
    r=r.split('+')
    r.sort()
    #p='+'.join(p)
    #r='+'.join(r)
    x[0] = [r,p]
    #replace D and exp for sympy  re.sub(r'(\d)[dD]([+-\.\d])',r'\1e\2',  x[1].split('//')[0].replace('EXP','exp')
    x[1] =  x[1].split('//')[0].replace(';','')
    return x

def categorise(x):
    cat2 = 'Radicals/Other'
    if 'RO2' in x[1]:
        cat = re.search(r'RO2[\w]*\b',x[1]).group()
        cat2 = 'RO2'

    elif 'J(' in x[1]:
        cat = 'hv'
        cat2 = 'Photolysis'
    elif '*O2' in x[1] :
        cat = 'O2'
        cat2 = 'Decomposition'
    elif 'H2O' in x[1] :
        cat = 'H2O'
    else:
        radical = set(x[0][0]) & set('OH,HO2,NO,NO2,NO3,Cl,CL,O3'.split(','))
        if len(radical):
            cat = list(radical)[0]
        else:
            try: cat = re.search(r'K[\w]*\b',x[1]).group()
            except: cat = 'Uni-molecular'
            cat2 = 'Decomposition'


    return ['->'.join(['+'.join(i) for i in x[0] ]) , x[1] , cat,cat2]



def reformat_kpp(file_list = False ,inorganics=False,available_cores = 1):

    if not file_list:
        #read files from picker
        file_list = picker.Picker('mechanisms/[!(formatted)]*.kpp',remove=['mechanisms/','.kpp'],title = 'Select Mechanisms').getSelected()
        file_text = [open('mechanisms/%s.kpp'%i,'r').read() for i in file_list]
        if inorganics:
            file_list.append('inorganics')
            file_text.append(open('src/background/inorganic_mcm.kpp','r').read())
        if file_list == ['inorganics']: sys.exit('You forgot to enter a file to reformat')
        fullstr='~'.join(file_text)
    else:
        #read given files
        file_text = [open('mechanisms/%s.kpp'%i,'r').read() for i in file_list]
        fullstr='~'.join(file_text)

    minfull = re.sub(r' |\n|\t|\s|\r','', fullstr).upper()



    eqn = [i.split(':') for i in re.findall(r'[^/]{1,2}\s*\{[\.\W\s\d]*?\}([^;]+)' ,'   '+minfull,re.S|re.M)]

    nocoeff = re.compile(r'\b\d*\.*\d*([\W\d\w]+)\b')
    specs = []
    for e in eqn: specs.extend(re.findall(r"[\w']+", e[0]))

    specs = list(set((nocoeff.sub(r'\1',i) for i in specs)))
    specs.sort()

    eqn = map(pool_eqn,eqn)

    eqn = map(categorise,eqn)


    #print eqn

    return  pd.DataFrame(eqn,columns='eqn,rate,category,group'.split(','))


if __name__ == '__main__':
    print 'lets go - quickstart test of propane.kpp'
    ret = reformat_kpp(['formatted_butane_inorganics_True.kpp'])
    tally = ret.groupby(['category','group']).count()
    #filter lone reactions
    tally = tally[tally.eqn>1]
    tally.index = ['_'.join([j,i]).strip() for i,j in tally.index.values]
    tally.sort_index(inplace=True)
    print tally['eqn'].to_json()
    print set(ret.group)
    #tally /= tally.sum()
