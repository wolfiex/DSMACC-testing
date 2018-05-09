from zhdf import new,loaddump,pool,ncores,da,progressbar,h5py
import numpy as np
import pandas as pd
import os,json,re
import multiprocessing as mp
import networkx as nx 
print ''
print ncores
np.warnings.filterwarnings('ignore')

a = new('methane.h5')

mcm = list(pd.read_csv('src/background/smiles_mined.csv').name)
mcm.extend(['CO2'])
cs = [i.split(',')[-1].replace('\n','') for i in tuple(open('carbons.csv'))]
allspecs = filter(lambda x: x not in ['LAT', 'PRESS', 'TEMP', 'H2O', 'M', 'RO2','NA', 'O1D', 'R'],a.spec.columns)
allspecs = filter(lambda x: x in cs,allspecs)
print allspecs

tsps = a.ts[range(0,len(a.ts),4)]# 6 hoursr
print tsps


def getedge(spec):
   # spec = allspecs[spec]                  
    edges = []
    for i in allspecs:
        fluxes = set(a.prodloss[spec]['prod']) & set(a.prodloss[i]['loss']) 
        if len(fluxes) >0 :
            arr = 20 +  np.log10(np.array(a.flux.loc[tsps,a.flux.columns[list(fluxes)]].sum(axis=1)))
            edges.append([i,spec,re.sub(r'\s+',' ',str(arr)) ])
    return edges        
    
edgelist=[]
for j in allspecs: 

    edgelist.extend(getedge(j))
    
df = pd.DataFrame(edgelist)
df.columns = ['source','target','flux']
df.flux =[str(i).replace('        -inf',' 0') for i in df.flux]
df.to_csv('link.csv')
print df


edgelist = np.array(df)
edgelist[:,2] = [re.sub(r'[\[\]]','',i).split(' ') for i in edgelist[:,2]]


nodes = pd.DataFrame(20 +np.log10(np.array(a.spec.loc[tsps,allspecs].compute()).T),index = allspecs, columns = range(len(tsps)))

for i in xrange(len(tsps)):

    G = nx.DiGraph()
    for j in edgelist:
        G.add_edge(j[0],j[1],weight=abs(float(j[2][i])))
    
    
    try:    
        pagerank =nx.pagerank(G)    
    
        nodes['pr%3d'%i]= [pagerank[k] for k in allspecs]
    except:None


    deg =nx.degree_centrality(G)    
    
    nodes['dg%3d'%i]= [deg[k] for k in allspecs]


    close =nx.closeness_centrality(G,distance='weight')    
    
    nodes['cl%3d'%i]= [close[k] for k in allspecs]


    bet =nx.betweenness_centrality(G,weight='weight')    
    
    nodes['bt%3d'%i]= [bet[k] for k in allspecs]



    cent =nx.load_centrality(G,weight='weight')    
    
    nodes['ld%3d'%i]= [cent[k] for k in allspecs]



    #cent =nx.eigenvector_centrality(G,weight='weight')    
    
    #nodes['ev%3d'%i]= [cent[k] for k in allspecs]


    #communicability = nx.communicability_centrality(G)
    
    #nodes['cm%3d'%i]= [communicability[k] for k in allspecs]


import seaborn
import matplotlib.pyplot as plt

print nodes
nodes.to_csv('nodes.csv')

df = pd.DataFrame([['%3d'%i[0],i[1]] for i in enumerate(tsps)])
df.to_csv('datelist.csv')
print 'finif'

d = pd.DataFrame(a.spec.compute())
import seaborn as sns
d.plot(subplots=True,legend=False)

seaborn.despine(left=True,bottom=True,right=True,trim=True)









