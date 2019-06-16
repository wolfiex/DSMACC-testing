'''
 run dsmacc/vis/degree/__init__.py

'''
import numpy as np
import pandas as pd
import zhdf
import networkx as nx
import dsmacc.graph as graph

damping = .95

self = zhdf.new('clfoch2.h5')
date = u'1970-12-29 12'
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


inorganics = 'O,O1D,H2O2,N2O5,HONO,HO2NO2,HSO3,H,O2,A,NA,SA,Cl,CL,SO2,SO3,H2,HNO3,O3,OH,HO2,NO,NO2,NO3'.split(',')

self.create_posjac()
self.posjac = group_hour(self.posjac)
#weights now in log10
G = graph.getnx(self,date)


def n(v):
    mx = np.max(v.values())
    mn = np.min(filter(lambda x: x>0, v.values()))
    for i in v:
        v[i] = 1e-10+((v[i])-mn)/(mx-mn)
        if v[i]<0: v[i]=0
    return v
    
def cn(v):
    mx = np.max(v.values())
    mn = np.min(v.values())

    for i in v:
        v[i] = 1e-10+((v[i])-mn)/(mx-mn)
        if v[i]<0: v[i]=0
    return v

def netdegree(G):
    inn = G.in_degree(weight='weighted')
    out = G.out_degree(weight='weighted')
    ret = {}
    for i in G.nodes():
        ret[i] = abs(inn[i]-out[i])
    return ret


#G.degree(weight='weight')))
ew = n(nx.get_edge_attributes(G,'weight'))
for (i,j),v in ew.items():
    G[i][j]['weighted']= v
    G[i][j]['distance']= 0.0002+ 1-v




#G.out_edges('CH4')

nx.set_node_attributes(G, 'indegree',  n(G.in_degree(weight='weighted')))
nx.set_node_attributes(G, 'outdegree',  n(G.out_degree(weight='weighted')))
nx.set_node_attributes(G, 'netdegree', n(netdegree(G)))




#between
nx.set_node_attributes(G, 'between', n(nx.betweenness_centrality(G,weight='weighted')))
#close
nx.set_node_attributes(G, 'closeness', n(nx.closeness_centrality(G, u=None, distance='distance', normalized=True)))

dist = {}
for nd in G.nodes():
    d = nx.shortest_path_length(G,target=nd,weight='distance')
    dist[nd] = d

nx.set_node_attributes(G, 'distanceto', dist)

pr = nx.pagerank_numpy(G, alpha=damping, personalization=None, weight='weighted', dangling=None)
nx.set_node_attributes(G, 'pr', n(pr))

ppr = {}

for nd in G.nodes():
    p = dict(zip(G.nodes(),np.repeat(0*(.1/len(G.nodes())),len(G.nodes()))))
    p[nd]=500
    
    prr = nx.pagerank_numpy(G, alpha=damping, personalization=p, weight='weighted', dangling=p)
    ppr[nd] = n(prr)
    
nx.set_node_attributes(G, 'ppr', ppr)




 
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

rpr = n(nx.pagerank_numpy(R, alpha=damping,# personalization=p,
 weight='distance', dangling=None))

rpr = dict(zip([G.nodes()[i] for i in rpr.keys()],rpr.values()))
nx.set_node_attributes(G, 'rpr', rpr)

rppr={}
for nd in R.nodes():
    p = dict(zip(R.nodes(),np.repeat(0*(.1/len(R.nodes())),len(R.nodes()))))
    p[nd]=500
    
    rprr = nx.pagerank_numpy(R, alpha=damping, personalization=p, weight='weighted', dangling=p)
    rprr = dict(zip([G.nodes()[i] for i in rprr.keys()],rprr.values()))
    rppr[G.nodes()[nd]] = n(rprr)
    
    
nx.set_node_attributes(G, 'rppr', rppr)


#remove inorganic nodes for graph visualisation
G = graph.rm_nodes(G,inorganics)



cdf = np.log10(self.spec.loc[self.timesteps[0],G.nodes()].compute())
concs = dict(zip(cdf.columns,cdf.values[0]))
nx.set_node_attributes(G, 'concs', cn(concs))



uwdeg = G.degree()
h,a=nx.hits(G,tol=1e-8,normalized=False)
h=n(h)
a=n(a)
nx.set_node_attributes(G, 'degree', uwdeg)
nx.set_node_attributes(G, 'hubs', h)
nx.set_node_attributes(G, 'authorities', a)


### write to file

from networkx.readwrite import json_graph
j = json_graph.node_link_data(G)

import json
j2 = json.dumps(j)
with open('degree.json','w') as f:
    f.write('graph = %s'%j2)

print ('Output degree.json')



########################
##COMPAREE
########################

import dsmacc.graph.STPR.dsmacc_tools as dsmacc_tools

self2 = zhdf.new('contiunue_clfoch2_0_0_280419.h5')



su = dsmacc_tools.undirect(self)
s2u = dsmacc_tools.undirect(self2)

ts = 144

difference = {}



C = nx.DiGraph()
r = []
for i in su:
    
    val = s2u[i][ts] / su[i][ts]
    val-=1
    if val != 0 :
        r.append( np.log10(abs(val) ) )
        


mnn = np.min(r)
maxx = np.max(r) - mnn        
for i in su:
    
    val = s2u[i][ts] / su[i][ts]
    val-=1
    if val != 0 :
        #difference[i] = np.log10(abs(val))
        v = i.split('->')[::-1*int(np.sign(val))] #give reversed links
        
        
        C.add_edge(v[0], v[1], weight=1e-10+(np.log10(abs(val)) - mnn)/maxx)
        
        
        
        
q = self2.spec.loc[self2.timesteps[ts],G.nodes()].compute()
w = self.spec.loc[self.timesteps[ts],G.nodes()].compute()
q.index = w.index

cdf = q.divide(w,axis=1)-1
sign = np.sign(cdf)
cdfn = np.log10(np.abs(cdf.values))
cdfn = 1e-10+(cdfn - np.min(cdfn))/(np.max(cdfn)-np.min(cdfn))

concs = dict(zip(cdf.columns,(cdfn*sign).values[0]))




nx.set_node_attributes(C, 'concs', concs)

C = graph.rm_nodes(C,inorganics)


cpr = nx.pagerank_numpy(C, alpha=damping, personalization=None, weight='weight', dangling=None)
nx.set_node_attributes(C, 'pr', n(cpr))




from networkx.readwrite import json_graph
j3 = json_graph.node_link_data(C)

import json
j24 = json.dumps(j3)
with open('difference.json','w') as f:
    f.write('graph = %s'%j24)

print ('Output difference.json')







spec = 'HCHO'
##### tree of life
import json 
hierarchical = '\n'.join(['.'.join(i) for i in nx.shortest_path(G,target=spec,weight='weighted').values()])


weight = json.dumps(nx.shortest_path_length(G,target=spec,weight='weighted'))

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

