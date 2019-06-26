<<<<<<< HEAD
from ..parsekpp.reactiontypes import reformat_kpp
from .. import datatables
__tableloc__ = datatables.__file__

def getG(mechlist=['inorganics']):
    print 'note this does not handle coefficients - it is just a sample plotting script'
    reactions  = reformat_kpp(mechlist).values
    print reactions
    import pandas as pd

    s = pd.read_csv('./'+__tableloc__.replace('__init__.pyc','smiles_mined.csv'))
    s = set(s.loc[map(lambda x: 'c' in str(x).lower(),s.smiles.values),:].name.values)&set(['CH4'])

    conly = True


    save = []
    nodes = []
    rtype=[]
    ignore = 'OH,HO2,NO,NO2,NO3,Cl,CL,O,O3'.split(',')
    for rxn in reactions:
        e = rxn[0].split('->')

        for r in e[0].split('+'):
            if r not in ignore:
                for p in e[1].split('+'):
                    if p not in ignore and r != p:

                        combined = [r,p]
                        if len(set(combined)^s) > conly:
                            save.append((r,p,{'group':rxn[-1],'subgroup':rxn[-2]}))
                            nodes.extend(combined)
                            rtype.append(rxn[-1])

    nodes = list(set(nodes))


    import json
    import networkx as nx

    G = nx.MultiDiGraph()
    G.add_edges_from( save )

    return G
    #nx.set_edge_attributes(G, 'group', rtype)

    #'size': G.node[n]['count']

if __name__ == '__main__':

    G = getG(['ISOP_CH4'])
    nodes = [{'name': n} for n in G]
    l = G.edges()

    for s,t in l:
        print G[s][t]

    print l
    edges = [{'source': s, 'target': t, 'value': 1,'group':G[s][t][0]['group']} for s,t in l]#G[s][t]['weight'] 'group':G[s][t]['group']

    json.dump({'nodes': nodes, 'links': edges}, open('./mcm_tograph.json', 'w'))
=======
from ..parsekpp.reactiontypes import *

print 'note this does not handle coefficients - it is just a sample plotting script'
reactions  = reformat_kpp(['ISOP_CH4']).values

print reactions 
import pandas as pd
s = pd.read_csv('src/background/smiles_mined.csv') 
s = set(s.loc[map(lambda x: 'c' in str(x).lower(),s.smiles.values),:].name.values)&set(['CH4'])

conly = True


save = []
nodes = []
rtype=[]
ignore = 'OH,HO2,NO,NO2,NO3,Cl,CL,O,O3'.split(',')
for rxn in reactions:
    e = rxn[0].split('->')
    
    for r in e[0].split('+'):
        if r not in ignore:
            for p in e[1].split('+'):
                if p not in ignore and r != p:
                    
                    combined = [r,p]
                    if len(set(combined)^s) > conly: 
                        save.append((r,p,{'group':rxn[-1]}))
                        nodes.extend(combined)
                        rtype.append(rxn[-1])
                    
nodes = list(set(nodes))                 
print save,nodes





import json
import networkx as nx

G = nx.MultiDiGraph()
G.add_edges_from( save )

#nx.set_edge_attributes(G, 'group', rtype)

nodes = [{'name': n} for n in G]#'size': G.node[n]['count']


l = G.edges()

for s,t in l:
    print G[s][t]

print l
edges = [{'source': s, 'target': t, 'value': 1,'group':G[s][t][0]['group']} for s,t in l]#G[s][t]['weight'] 'group':G[s][t]['group']

json.dump({'nodes': nodes, 'links': edges}, open('./mcm_tograph.json', 'w'))


>>>>>>> 627465599f3470471195f52354ed1306354027f3
