import networkx as nx
import __init__ as STPR
import pandas as pd
import numpy as np

G = nx.DiGraph()
    
keys = [(2, 3), (3, 2), (4, 1), (4, 2), (5, 2), (5, 4),
                    (5, 6), (6, 2), (6, 5), (7, 2), (7, 5), (8, 2),
                    (8, 5), (9, 2), (9, 5), (10, 5), (11, 5)]
    
    
net_edges=pd.DataFrame(np.ones((2,len(keys))),columns = ['%s->%s'%(i[0],i[1]) for i in keys])
#create
G.add_edges_from(keys)


print ('`````````````````````````')

nsp = STPR.net2sparse(net_edges)
nsp.init_pr()
out = nsp.pr()

print ('`````````````````````````')

prn = nx.pagerank_numpy(G)
prx= nx.pagerank(G)
prs= nx.pagerank_scipy(G)

from algorithms import nx_np_pr,google_matrix
test = nx_np_pr(G)


diff = []
print ('[out[str(i)],prn[int(i)],prx[int(i)],test[int(i)],mydiff,name]')
for i in nsp.names:
    
    mydiff = np.abs([out[str(i)]-test[int(i)]])
    print (['%.3e'%float(i) for i in [out[str(i)],prn[int(i)],prx[int(i)],test[int(i)],mydiff,i]])
    diff.append(mydiff)

if np.max(diff) >1e-5:
    assert 'Test Failed'
else: 
    print ('We are doing well... Testing successful. ') 
    

