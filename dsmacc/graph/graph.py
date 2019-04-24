'''
graph generation library to use networkx
'''


import networkx as nx
import numpy as np
import pandas as pd

def normalise(x):
    x = x[:]#deepcopy error
    x -= min(x)
    x /= max(x)
    return x
    
def jgraph(posjac):
    '''
    networkx graph object from posjac at timestep
    '''

    posjac = 1 - normalise(np.log10(posjac).replace([np.inf,-np.inf],np.nan).dropna())

    split = [i.split('->') for i in posjac.index]
    #graph
    G = nx.DiGraph()

    for e in range(len(split)):

            G.add_edge(split[e][0],split[e][1],weight=posjac[e])

    G.remove_edges_from(G.selfloop_edges())


    return G



def getnx(self, ts ,save=False):
    '''
    Create a networkx graph from a DSMACC new class
    
    Usage: 
        getnx(a,a.ts[-1], 'propane')
    '''
    try: self.posjac
    except:self.create_posjac()
    
    G = nx.DiGraph()
    
    posjac = self.posjac.loc[ts,:]
    split = [i.split('->') for i in posjac.index]
    
    for e in range(len(split)):
        G.add_edge(split[e][0],split[e][1],weight=posjac[e])
    G.remove_edges_from(G.selfloop_edges())
    
    if save:
        nx.write_weighted_edgelist(G, save+'.wedgelist')
    #G=nx.read_weighted_edgelist('propane.wedgelist',create_using=nx.DiGraph)

    return G 

    
def rm_nodes (G,ignore):
    for i in ignore:
        try:G.remove_node(i)
        except:None
    return G    
    
    
    












def pagerank(a):
    return geobj2df(metric(tograph(group_hour(a.jacsp))))



def tograph(jac):
    '''
    Use hourly avg
    '''

    rt = []
    for t in jac.iterrows():
        jacsp=t[1]
        #inverse negative links
        index = np.array(jacsp.index)
        lt = list(jacsp<0)
        index[lt] = map(lambda x: '->'.join(reversed(x.split('->'))),index[lt])
        jacsp.index = index
        jacsp = jacsp.abs()

        #normalize jacsp
        jacsp  = jacsp*1.01 - jacsp.min().min()
        jacsp /= jacsp.max().max()


        split = [i.split('->') for i in jacsp.index]
        #graph
        G = nx.DiGraph()

        for e in range(len(split)):

            G.add_edge(split[e][0],split[e][1],weight=jacsp[e])


        G.remove_edges_from(G.selfloop_edges())
        rt.append({'graph':G,'time':t[0]})

    return rt


def metric(GS,met = 'nx.pagerank'):
    '''
    GS - out array from to_graph
    '''
    metfn = eval(met)

    for gt in range(len(GS)):
        res = metfn(GS[gt]['graph'])
        res = [[key, res[key]] for key, value in sorted(res.iteritems(), key=lambda k,v: (v,k))]

        GS[gt][met] = res
    return GS


def geobj2df(GS,what = 'nx.pagerank'):
    res = []
    index = []
    for s in GS:
        index.append(s['time'])
        s = pd.DataFrame(s[what])
        s.index = s[0]
        s=s[1]
        res.append(s)

    df = pd.concat(res,axis = 1).T
    df.index = index
    df = (df*1.1).subtract(df.min(axis=0
    ))
    df=df.divide(df.max(axis=1),axis=0)
    import zcreate_centrality as p

    #p.createhtml(df)

    return df
