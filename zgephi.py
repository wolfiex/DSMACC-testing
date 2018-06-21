from zhdf import new,loaddump,pool,ncores,da,progressbar,h5py
import numpy as np
import pandas as pd
import os,json,re,sys
import multiprocessing as mp
import networkx as nx
print ''
print ncores
np.warnings.filterwarnings('ignore')

a = new(sys.argv[1])

mcm = list(pd.read_csv('src/background/smiles_mined.csv').name)
mcm.extend(['CO2'])
cs = [i.split(',')[-1].replace('\n','') for i in tuple(open('carbons.csv'))]
allspecs = filter(lambda x: x not in ['LAT', 'PRESS', 'TEMP', 'H2O', 'M', 'RO2','NA', 'O1D', 'R'],a.spec.columns)
allspecs = filter(lambda x: x in cs,allspecs)
print allspecs
for i in enumerate(a.flux.index.compute()):print i
tm = int(raw_input('enter time index: '))

tsps = [a.flux.index.compute()[tm]]# 6 hoursr a.ts[range(0,len(a.ts),4)]



def getedge(spec):#,allspecs,a,tsps):
   # spec = allspecs[spec]
    edges = []
    for i in allspecs:
        fluxes = set(a.prodloss[spec]['prod']) & set(a.prodloss[i]['loss'])

        #print len(fluxes)
        if len(fluxes) >0 :
            arr = 20 +  np.log10(np.array(a.flux.loc[tsps,a.flux.columns[list(fluxes)]]))
            edges.append([i,spec,re.sub(r'\s+',' ',str(arr)) ])
    return edges


edgelist=[]
for j in allspecs:
    edgelist.extend(getedge(j))



df = pd.DataFrame(edgelist)
df.columns = ['source','target','flux']
df.flux =[str(i).replace('        -inf',' 0') for i in df.flux]

edgelist = np.array(df)
edgelist[:,2] = [re.sub(r'[\[\]]','',i).split(' ') for i in edgelist[:,2]]
nodes = pd.DataFrame(20 +np.log10(np.array(a.spec.loc[tsps,allspecs].compute()).T),index = allspecs, columns = range(len(tsps)))
nodes[nodes<0]=0
nodes/=nodes.max()



for i in [0]:

    G = nx.DiGraph()
    jval = np.array([float(k[2][i]) for k in edgelist if (len(k[-1])>1 and len(k[-3])>1 and k[2][i]!='')])
    if len(jval)<1: continue
    jval = jval[jval>0]

    jmin = np.min(jval)
    jmax = np.max(jval)-jmin

    for j in edgelist:

        jedge = j[2][i]
        if jedge not in ['','-inf']:
            jedge = float(jedge)

            jedge -= jmin
            jedge /= jmax
            G.add_edge(j[0],j[1],weight=abs(jedge))


    nx.write_gexf(G, "test.gexf")


print 'finif'
