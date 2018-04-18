''' A program that mines the latest smiles and inchi strings from the mcm website. 
Please do not use this unless there are species missing from the pre provided list, or a new version is released. 

'''
 
import urllib2, re 
from pandas import * 
import multiprocessing as mp 
import numpy as np 
import click


inchis = re.compile(r'<span class="inchi">(.*)<') 
smiles =  re.compile(r'<span class="smiles">(.*)<') 
synonyms =  re.compile(r'<span>\n\t\s*([\w;\-\s]*);\n')

global species
species = re.findall(r'\b(\w*)\b = IGNORE',str(tuple(open('../../src/background/mcm331complete.kpp'))))


def mine (spec): #gets text from link source. 
    try: 
        st= urllib2.urlopen('http://mcm.leeds.ac.uk/MCM/browse.htt?species=%s'%spec).read()
        print 100*species.index(spec)/len(species),'% ' + spec
        #print spec
        return [spec,smiles.findall(st)[0],inchis.findall(st)[0],';'.join(synonyms.findall(st))]    
    except Exception as e: 
        print 'Failed on: ' + spec   , e  
        return []
 

data = mp.Pool(30).map(mine, species)

df = DataFrame(data,columns= ['name','smiles','inchi','synonyms'])

df.replace('Exception: (1064, "You have an error in your SQL syntax.  Check the manual that corresponds to your MySQL server version for the right syntax to use near \'%s\' at line 1")','',inplace=True)

df.to_csv('smiles_mined.csv')


