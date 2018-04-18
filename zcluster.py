import numpy as np
import networkx as nx
from sklearn.cluster import SpectralClustering
from sklearn import metrics
np.random.seed(1)

from zhdf import new,loaddump,pool,ncores,da,progressbar,h5py
import numpy as np
import os
 
print ''

np.warnings
a = new('BaseRun_init.h5')

n=1

G=nx.from_numpy_matrix(a.adj[:,:,n],create_using=nx.MultiDiGraph())


if True:
    #dt = a.adj[:,:,n] 

    #G=nx.from_numpy_matrix(dt,create_using=nx.MultiDiGraph())
    
    #sc = SpectralClustering(2, affinity='precomputed', n_init=100)
    #sc.fit(a.adj[:,:,n])
    #r = sc.labels_
    #print r
    
    '''
    eigen_solver : {None,arpack,lobpcg, oramg}

The eigenvalue decomposition strategy to use. AMG requires pyamg to be installed. It can be faster on very large, sparse problems, but may also lead to instabilities
'''


import community
partition = community.best_partition(G)

#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))


nx.draw_networkx_edges(G,pos, alpha=0.5)
plt.show()
            
''' 
a=[]            
for i in range(10000):
    arr=[]
    r=i
    for b in range(len(state.levels)):
        r = state.levels[0].get_blocks()[r]
        arr.append(r)
    a.append(arr)
         
            
