from zhdf import new,loaddump,pool,ncores,da,progressbar,h5py
import numpy as np
import pandas as pd
import os,json,re,sys
import multiprocessing as mp
import networkx as nx
print ''
print ncores
np.warnings.filterwarnings('ignore')

noro2= True

filename = sys.argv[1]
prefix = 'centrality/'+filename.split('.')[0]
a = new(filename)

#ro2 considerations qsub -I  -q x-large -X -lselect=7:ncpus=1:mem=50G -l place=vscatter:shared
try:
    if noro2: print dsafdsa
    a.spec.RO2
    ro2go=True
except:
    ro2go=False
    ro2list=set([])

if ro2go:
    ro2file= re.sub(r'\s|\\t|\\n|\'|,','',str(tuple(open('src/background/mcm331complete.kpp'))))
    ro2 = list(set(re.findall(r'ind_([\w\d]+)\b',ro2file)) & set(a.spec.columns))
    ro2eq = re.findall(r'}([\w\+=\.\d]+):[\+-\/\(\)\.\w\d\*]*\bRO2\b[\+-\/\(\)\.\w\d\*]*;',ro2file)
    ro2list = []
    for n,i in enumerate(a.flux.columns):
        if i.replace('-->','=') in ro2eq:
            ro2list.append(n)
    ro2list=set(ro2list)



mcm = list(pd.read_csv('src/background/smiles_mined.csv').name)
if ro2go:  mcm.extend(['CO2','RO2'])
cs = [i.split(',')[-1].replace('\n','') for i in tuple(open('carbons.csv'))]
cs.extend('RO2')
allspecs = filter(lambda x: x not in ['LAT', 'LON','PRESS', 'TEMP', 'H2O', 'M','NA', 'O1D', 'R','O','O1D', 
 'O3', 'O2', 'NO2', 'NO3', 'N2O5', 'H2O2', 'TEMP', 'NO', 'NA',
 'KMT05', 'KMT04', 'KMT07', 'KMT06', 'KMT01', 'HO2NO2', 'KMT03',
  'KMT02', 'HO2', 'KMT09', 'KMT08', 'CO', 'HNO3', 'SO3', 'SO2', 
  'N2', 'OH', 'H2', 'HONO', 'HSO3', 'H2O', 'KMT12', 'KMT11', 'SA'],a.spec.columns)


#allspecs = filter(lambda x: x in cs,allspecs)
print allspecs

speclist = list(allspecs)
toindex = dict(zip(speclist,range(len(speclist))))
fromindex = dict(zip(range(len(speclist)),speclist))


def getedge(num,allspecs,prodloss,flux,ro2list,tsps):#,allspecs,a,tsps):
    edges = []
    print len(num)
    print ''
    import progressbar,re
    import numpy as np
    bar = progressbar.ProgressBar()

    for j in bar(list(num)):

        spec = allspecs[j]

        for i in allspecs:
            fluxes = set(prodloss[spec]['prod']) & set(prodloss[i]['loss'])


            if len(fluxes & ro2list)>0:
                fluxes = fluxes & ro2list
                arr = 20 +  np.log10(np.array(flux.loc[tsps,flux.columns[list(fluxes)]].sum(axis=1)))
                edges.append(['RO2',spec,arr ])

            if len(fluxes) > 0 :
                arr = 20 +  np.log10(np.array(flux.loc[tsps,flux.columns[list(fluxes)]].sum(axis=1)))
                edges.append([i,spec,arr])


    return edges
    
    ################################

tsps = a.ts#[[143,144,33]]#,143+144/2 6 hoursr a.ts[range(0,len(a.ts),4)]
print tsps

##########################

if ro2go:
    ro2fract = a.spec.loc[tsps,ro2].compute()
    ro2val = a.spec.loc[tsps,'RO2'].compute()





edgelist=[]

bar = progressbar.ProgressBar()
results  = [pool.apply_async(getedge, args=(x,allspecs,a.prodloss,a.flux.compute(),ro2list,tsps)) for x in np.array_split(range(len(allspecs)),ncores)]
[edgelist.extend(p.get()) for p in bar(results)]

print 'edgelist ready'


import numpy as np
from collections import Counter
import networkx as nx
from infomap import infomap
import community

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
from matplotlib import rcParams

rcParams['figure.figsize'] = (8, 6)
rcParams['axes.titlepad'] = 12
rcParams['axes.titlesize'] = 18
rcParams['axes.labelsize'] = 12

#for t in xrange(len(tsps)):
def mapinfomap(t):    
    
    print 'Infomap'
    #i=0 # location in time array


    G = infomap.Infomap("-d -N 100")
    Gnx = nx.DiGraph()

    jval = np.array([float(k[2][t]) for k in edgelist if (len(k[-1])>0 and len(k[-3])>0 and k[2][t]!='')])
    #if len(jval)<1: continue
    jval = jval[jval>0]
    jmin = np.min(jval)
    jmax = np.max(jval)-jmin
    for j in edgelist:
            jedge = j[2][t]
            if str(jedge) not in ['','-inf']:
                jedge = float(jedge)

                jedge -= jmin
                jedge /= jmax
                try:
                    Gnx.add_edge(j[0],j[1],weight=abs(jedge))
                    G.addLink(toindex[j[0]],toindex[j[1]],weight=abs(jedge))
                except Exception as e:
                    print 'fail' , e


    G.run();
    tree = G.tree

    partition = {}
    for node in tree.leafIter():
        partition[node.originalLeafIndex] = node.moduleIndex()


    groups = [[] for i in  np.empty(np.array(partition.values()).max())]

    for i,j in enumerate(speclist):
        try:
            groups[partition[i]].append(j)
        except:
            print 'no node', i,j


    groups = sorted(groups,key=lambda x : len(x),reverse=True)
    '''
    with open('centrality/%04d.groups'%t,'w') as f:
        f.write('lumplist=\n')
        f.write(str(groups).replace("'",'"'))

    with open('centrality/%04d.groupslimited'%t,'w') as f:
        f.write('lumplist=\n')
        lumpedlim = str(filter(lambda x : len(x) in range(2,11),groups)).replace("'",'"')
        f.write(lumpedlim)
        '''
    with open('centrality/%04d.gps'%t,'w') as f:
    
            for i in groups:#filter(lambda x : len(x) in range(2,11),groups)
                f.write('-'.join(set(i))+'\n')
    return ['-'.join(set(i)) for i in groups]

pool.close()

words = mp.Pool(ncores).map(mapinfomap,xrange(len(tsps)))

l =[]
for i in words:
    l.extend(i)

from collections import Counter

with open('centrality/collected.txt','w') as f:
        items = Counter(l).items()
        items = sorted(items,key=lambda x:x[1],reverse=True)
        
        for i in items:
            f.write('%d,%s\n'%(i[1],i[0]))





'''




def merge_nodes(G,nodes, new_node, attr_dict=None, **attr):
    """
    Merges the selected `nodes` of the graph G into one `new_node`,
    meaning that all the edges that pointed to or from one of these
    `nodes` will point to or from the `new_node`.
    attr_dict and **attr are defined as in `G.add_node`.
    """
    if len(nodes)>1:
        G.add_node(new_node,attr_dict=attr_dict) # Add the 'merged' node
        ln = len(nodes)
        add=[]
        sn = set(nodes)
        for n1,n2,data in G.edges(data=True):
            # For all edges related to one of the nodes to merge,
            # make an edge going to or coming from the `new gene`.
            if len(sn & set([n1,n2]))==1:
                if n1 in nodes:
                    add.append([new_node,n2,data['weight']])
                elif n2 in nodes:
                    add.append([n1,new_node,data['weight']])

        for n in nodes: # remove the merged nodes
            try:
                G.remove_node(n)
            except:
                print 'cant remove' + n , nodes,add
    
        for i in pd.DataFrame(add).groupby([0,1],as_index=False).sum().values:
            G.add_edge(i[0],i[1],weight = float(i[2])/ln)
            print i



    return G

print 'merge nx'
sizedict ={}
maxg = len(groups[0])
for n,g in enumerate(groups):
    Gnx = merge_nodes(Gnx,g,'%d_group'%n ,{'size':len(g)})
    sizedict['%d_group'%n]= len(g)

#sizes = [10*float(sizedict[x])/maxg for x in Gnx.nodes()]


#nx.draw(Gnx, with_labels=False)#,node_size=sizes,node_color = [i/10. for i in sizes])
data = nx.readwrite.json_graph.node_link_data(Gnx, attrs={'source': 'source', 'target': 'target', 'weight': 'weight', 'id': 'id'})

import json
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)


print lumpedlim.replace(']',']\n')

'''