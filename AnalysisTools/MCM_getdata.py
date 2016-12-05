#!/usr/bin/python
''' 
A program to extract relevant data regarding the MCM, 
to be used for extracting subsets

D.Ellis 2016
'''

import pandas as pd
import numpy as np
import os, sys, multiprocessing,re 

available_cores = 16

try: filename=sys.argv[1]
except:filename = 'full_mcm_331.kpp'
full = tuple(open(filename))
try: filename=sys.argv[2]
except:filename = 'inorganics_mcm_331.kpp'
inorganics = tuple(open(filename))


gen = xrange(len(full))



''' Step 1 extract all species '''
inorganic_species =  set(re.findall(r'([A-z0-9]*)[\s=]*IGNORE' ,str(inorganics)))
all_species =  re.findall(r'([A-z0-9]*)[\s=]*IGNORE' ,str(full))
sarr = pd.Series(index=all_species)
sarr[:]=-1

#dictionarys for reference
num2spec = dict(enumerate(all_species))
spec2num = {v: k for k, v in num2spec.iteritems()}



''' Step 2 split array into reactants and products '''
equations = [i.replace(' ','').split('=') for i in re.findall(r'\}\s*\\t*([A-z0-9/+=\s]*)\:' ,str(full))]
        

''' Step 3 split into arrays of each reactant / product '''
eq_split = [[set(i[0].split('+')), set(i[1].split('+'))] for i in equations]


#''' Step 4 convert to numerical '''
# 

gen = xrange(len(equations))


#make into a class with run number
''' get all species formed ''' 

species = {'O3','CH4','C4H6'} | inorganic_species
counter = 0 
previous = '' 

while True: 
    counter += 1 
    print counter 

    dummy = []
    for i in gen:
        if eq_split[i][0].issubset(species): dummy.extend(eq_split[i][1])

    species = species | set(dummy)
    
    
    for i in dummy: 
       
        if sarr[i] < 0 :
            print i
            sarr[spec2num[i]]= counter

    dummy = []

    if previous == species: break
    previous = species








#multiprocessing.Pool(ncores).map( simulate , numbered ) 






''' pickle at filename'''




