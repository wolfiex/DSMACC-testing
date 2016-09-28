import os, sys, multiprocessing,re
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

species = ['CH4', 'O3']
ncores = 16

global full_mcm
full_mcm= tuple(open('full_mcm.kpp'))



#get names of all the species
all_species = []
for line in full_mcm:    
    if' IGNORE' in line: all_species.append(line.split(' =')[0])
    elif 'EQUATIONS' in line: break
    
def equations (spec):
    eq_array=[]
    for line in xrange(len(full_mcm)):
        if (' %s '%spec in full_mcm[line] and 'IGNORE' not in full_mcm[line]):eq_array.append(line)
    return eq_array        


    
def get_eqns(spec):
    
    eqns = set(equations(spec))    
    while True:
        array,output=[],[]
        
        for i in eqns:array.extend(full_mcm[i].split('=')[1].split(':')[0].replace(' ','').replace('\t','').split('+'))                   
        for i in array: output.extend(equations(i))     
        
        output = set(output)
        if output == eqns: break
        print spec
        eqns=output
        
    return eqns 
    
    
selection = multiprocessing.Pool(ncores).map(equations, species ) # for number of specs use just equations, for all , use get_eqns 




what_to_pull = []
for sct in selection: what_to_pull.extend(sct)
#uniquify 
what_to_pull = set(what_to_pull)

new_organics = [full_mcm[eqn].replace('\t','').replace('\n','').split('}')[1] for eqn in what_to_pull]




#print (add checker to check original specs not in fuirther lists ) 







lengths = [len(x) for x in selection]

ser = pd.Series(lengths)
ser.index=all_species
ser.sort()

ser.plot()

