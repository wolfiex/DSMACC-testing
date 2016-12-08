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
fullstr=''.join(full).replace('\n','').replace('\t','').replace(' ','')
eqn = [i.replace(' ','').split(':') for i in re.findall(r'}([A-z0-9+-=:()*/]*);' ,fullstr)]
equations = [ i[0].split('=') for i in eqn]

 
''' Step 3 split into arrays of each reactant / product '''
eq_split = [[set(i[0].split('+')), set(i[1].split('+'))] for i in equations]
 

gen = xrange(len(equations))


#make into a class with run number
''' get all species formed ''' 
origin = {'O3','NO','NO2','NC7H16'}
species = origin | inorganic_species ^ set (['' ])
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

    species = species | set(dummy)
    
    
    for i in dummy: 
       
        if sarr[i] < 0 :
            print i
            sarr[spec2num[i]]= counter

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

#for i in origin: sarr[i] = 0 

#list(np.linspace(0,1,len(origin)))

json = '['

for i in xrange(0,int(s.max()+1)):
    print i , 'sarr'
    names = sarr[sarr==i].index
    ypos  = np.linspace(0,1,len(names))
    
    for j in xrange(len(ypos)):
        json += '{"name":"%s","x":%.2f,"y":%.2f},'%(names[j],xpos[i],ypos[j])
        

json=json[:-1]
json+= ']'
    
    
    

links = '['
for i in xrange(1,int(s.max()+1)):
    print i 
    names1 = sarr[sarr==i-1].index
    names2 = sarr[sarr==i].index
    for l in names1: 
       for m in names2: 

            for k in eq_split:
                 if (l in k[0]) and (m in k[1]): 
                    links += '{"source":"%s","target":"%s"},'%(str(l),str(m))
                    break
            continue                      
                         
              

links = links[:-1]
links+= ']'







traces = multiprocessing.Pool(4).map( trace , s.index ) 


string = '{'
for i in xrange(len(traces)):
	string += '"' +s.index[i] + '":['
	for j in traces[i][0]:
		for k in j[0].split('=')[0].split('+'):
		 	string += '"' + k +'",'
	string += '],'

string += '}'



''' pickle at filename'''



