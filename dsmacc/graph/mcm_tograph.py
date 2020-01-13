from ..parsekpp.reactiontypes import reformat_kpp
from .. import datatables
__tableloc__ = datatables.__file__
import csv

def getG(mechlist=['inorganics'], ignore = ['inorganics']):
    print ('note this does not handle coefficients - it is just a sample plotting script')
    reactions  = reformat_kpp(mechlist).values
    print (reactions)
    import pandas as pd

    s = pd.read_csv(''+__tableloc__.replace('__init__.py','smiles_mined.csv'))
    s = set(s.loc[map(lambda x: 'c' in str(x).lower(),s.smiles.values),:].name.values)&set(['CH4'])

    conly = True


    save = []
    nodes = []
    rtype=[]
    if ignore == ['inorganics']:
        ignore = 'OH,HO2,NO,NO2,NO3,Cl,CL,O,O3'.split(',')
        ignore .extend(["O", "CL", "H2", "NO", "O3", "OH", "ACR", "HO2", 'HSO3','HNO3', 'SA','NA','N2O5',"NO2", "NO3", "NOA", "O1D", "SO2", "SO3",'HNO3'])
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
    import sys
    nm = sys.argv[1]


    G = getG([nm])
    nodes = [{'name': n} for n in G]
    l = G.edges()

    for s,t in l:
        print (G[s][t])

    print (l)
    edges = [{'source': s, 'target': t, 'value': 1,'group':G[s][t][0]['group']} for s,t in l]#G[s][t]['weight'] 'group':G[s][t]['group']
    import json
    import networkx as nx
    json.dump({'nodes': nodes, 'links': edges}, open('./%s.json'%nm, 'w'))
    nx.write_gexf(G, "%s.gexf"%nm)




    #adj = np.adjacency_matrix(G)
