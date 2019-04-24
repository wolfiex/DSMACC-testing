'''
 run dsmacc/vis/degree/__init__.py

'''
import numpy as np
import pandas as pd
import zhdf



self = zhdf.new('ethane.h5')
date = u'1970-12-31 12'

self.rm_spinup()

def group_hour(df,fn = np.mean,diurnal = False):
        try: df = df.compute()
        except:None


        df['group']= [str(i).split(':')[0] for i in df.index]
        df = df.groupby(by='group').agg(fn)
        if diurnal:
            day = range(24)
            hour = lambda x: x in range(24)
            df['hour'] = [int(i.split(' ')[-1]) for i in df.index]
            df = df[df['hour'].apply(hour)]
            df = df.groupby(['hour']).agg(fn)
        return df


inorganics = 'O,O1D,N2O5,HONO,HO2NO2,HSO3,H,O2,A,NA,SA,Cl,CL,SO2,SO3,H2,HNO3,O3,OH,HO2,NO,NO2,NO3'.split(',')

self.create_posjac() #ignore = inorganics)
import dsmacc.graph as graph

self.posjac = group_hour(self.posjac)


G = graph.getnx(self,date)
import networkx as nx
#rm isolates
G = graph.rm_nodes(G,list(nx.isolates(G)))


def n(v):
    mx = np.max(np.log10(v.values()))
    mn = np.min(np.log10([i+1e-50 for i in v.values()] ))
    print mx,mn
    for i in v:
        v[i] = (np.log10(v[i]+1e-50)-mn)/(mx-mn)
    return v


def n2(v):
    mx = np.max(1*(v.values()))
    mn = np.min(1*([i+1e-50 for i in v.values()] ))
    print mx,mn
    for i in v:
        v[i] = ((v[i]+1e-50)-mn)/(mx-mn)
    return v

def nnozero(v):
    x = v.values()
    x.sort()
    
    mx = x[0]
    mn = x[-1]
    print mx,mn
    for i in v:
        if v[i] >0:
            v[i] = ((v[i]+1e-50)-mn)/(mx-mn)
    return v



import networkx as nx
uwdeg = G.degree()
h,a=nx.hits(G)
h=n(h)
a=n(a)


def netdegree(G):
    inn = G.in_degree(weight='weight')
    out = G.out_degree(weight='weight')
    ret = {}
    for i in G.nodes():
        ret[i] = abs(inn[i]-out[i])
    return ret

nx.set_node_attributes(G, 'degree', uwdeg)
nx.set_node_attributes(G, 'hubs', h)
nx.set_node_attributes(G, 'authorities', a)

nx.set_node_attributes(G, 'indegree',  n(G.in_degree(weight='weight')))
nx.set_node_attributes(G, 'outdegree',  n(G.out_degree(weight='weight')))
nx.set_node_attributes(G, 'netdegree', n(netdegree(G)))
#G.degree(weight='weight')))


ew = n(nx.get_edge_attributes(G,'weight'))
for (i,j),v in ew.items():
    G[i][j]['weighted']= v
    G[i][j]['distance']= 1-v

nx.set_node_attributes(G, 'between', n2(nx.betweenness_centrality(G,weight='weighted')))
nx.set_node_attributes(G, 'closeness', n2(nx.closeness_centrality(G, u=None, distance='distance', normalized=True)))

dist = {}
for nd in G.nodes():
    d = nx.shortest_path_length(G,target=nd,weight='distance')
    dist[nd] = d

nx.set_node_attributes(G, 'distance', dist)

pr = nx.pagerank_numpy(G, alpha=0.85, personalization=None, weight='weight', dangling=None)
nx.set_node_attributes(G, 'pr', n(pr))

ppr = {}
for nd in G.nodes():
    p = dict(zip(G.nodes(),np.repeat(1./len(G.nodes()),len(G.nodes()))))
    p[nd]=500
    
    prr = nx.pagerank_numpy(G, alpha=0.85, personalization=p, weight='weight', dangling=None)
    ppr[nd] = n(prr)
    
nx.set_node_attributes(G, 'ppr', ppr)


spec = 'HCHO'
##### tree of life
import json 
hierarchical = '\n'.join(['.'.join(i) for i in nx.shortest_path(G,target=spec,weight='weight').values()])


weight = json.dumps(nx.shortest_path_length(G,target=spec,weight='weight'))

'''
tree={}
for r in nx.shortest_path(G,target=spec,weight='weight').values():
    sub = tree 
    for i,cell in enumerate(filter(lambda x: x!= spec,r[::-1])):
        if cell not in sub:
            sub[cell] = {} if i<len(r)-1 else 1
        sub=sub[cell]
            
print json.dumps(tree, indent=4)
'''


################## pr custom
import dsmacc.graph.STPR as STPR
#include all reactions for this
'''
del self.posjac
self.create_posjac()
self.posjac = group_hour(self.posjac)
'''

nsp = STPR.net2sparse(self.posjac)
nsp.init_pr()
out = nsp.pr(timestep = list(self.posjac.index).index(date))

keys = out.keys()
ch4 = dict(zip(keys,np.repeat(1./len(keys),len(keys))))
ch4['CH4']= 200
meth = nsp.pr(timestep = list(self.posjac.index).index(date),personalization = ch4)

c2h6 = dict(zip(keys,np.repeat(1./len(keys),len(keys))))
c2h6['C2H6']= 200
eth = nsp.pr(timestep = list(self.posjac.index).index(date),personalization=c2h6)


##reversed

rposjac = pd.DataFrame(self.posjac.values,columns=['->'.join(j) for j in [i.split('->')[::-1] for i in self.posjac.columns]])
nspr = STPR.net2sparse(rposjac)

nspr.init_pr()
rout = nspr.pr(timestep = list(self.posjac.index).index(date))

print out['CH4'],rout['CH4']


###################
#lets just use nx
#
#empty class make
#class Empty: pass
T = nx.to_numpy_matrix(G).T
R = nx.from_numpy_matrix(T,type(G)())


ew = n(nx.get_edge_attributes(R,'weight'))
for (i,j),v in ew.items():
    R[i][j]['weighted']= v
    R[i][j]['distance']= 1-v


rpr = n(nx.pagerank_numpy(R, alpha=0.85,# personalization=p,
 weight='distance', dangling=None))

rpr = dict(zip([G.nodes()[i] for i in rpr.keys()],rpr.values()))



#remove inorganic nodes for graph visualisation
#G = graph.rm_nodes(G,inorganics)



from networkx.readwrite import json_graph
j = json_graph.node_link_data(G)

import json
j2 = json.dumps(j)
with open('degree.json','w') as f:
    f.write('graph = %s'%j2)

print ('Output degree.json')
