import sklearn


import numpy as np
float_formatter = lambda x: "%.3f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})
from sklearn.datasets.samples_generator import make_circles
from sklearn.cluster import SpectralClustering, KMeans
from sklearn.metrics import pairwise_distances
from matplotlib import pyplot as plt
#import networkx as nx
import seaborn as sns
sns.set()

#from _spectral import SpectralClustering
from sklearn.cluster import SpectralClustering
X = np.array([
    [1, 3], [2, 1], [1, 1],
    [3, 2], [7, 8], [9, 8],
    [9, 9], [8, 7], [13, 14],
    [14, 14], [15, 16], [14, 15]
])


X, clusters = make_circles(n_samples=1000, noise=.05, factor=.5, random_state=0)
Y, clusters = make_circles(n_samples=2000, noise=.06, factor=0.5, random_state=0)

X = np.concatenate([X,Y*2.3],axis=0)
#print(help(make_circles))
 
 #plt.scatter(X[:,0], X[:,1])
# Cluster
m= len(X)-1

sc = SpectralClustering(n_clusters=20, affinity='nearest_neighbors', random_state=0,n_auto=1e-4, assign_labels='discretize')
sc_clustering = sc.fit(X)

print (np.max(sc_clustering.labels_))

plt.scatter(X[:,0], X[:,1], c=sc_clustering.labels_, cmap='rainbow', alpha=0.7, edgecolors='b')

plt.show()

'''
# nearest neigbour plot
import networkx as nx
plt.scatter(X[:,0], X[:,1], c='white', cmap='rainbow', alpha=0.7, edgecolors='b')
G = nx.from_numpy_matrix(sc_clustering.affinity_matrix_.toarray() )
nx.draw_networkx_edges(G, X, width=1,alpha=.5 , edge_color='purple')
plt.show()
'''