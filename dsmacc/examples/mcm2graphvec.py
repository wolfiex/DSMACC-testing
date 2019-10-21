# Lets get the node embeddings for the mcm
import networkx as nx
import numpy as np
import multiprocessing as mp
#https://github.com/aditya-grover/node2vec.git
# run as module to create full


np.random.seed(42)
import node2vec as n2v
from gensim.models import Word2Vec

exists = True


if not exists:
    
    from ..graph.mcm_tograph import *
    G = getG(['full_mcm_2019'],ignore = [''])
    nodes = [{'name': n} for n in G]
    nx.write_gpickle(G,"fullmcm.gpickle")
    print(nodes)

    Gf = nx.read_gpickle('./fullmcm.gpickle')
    G = nx.MultiDiGraph()
    G.add_weighted_edges_from([(i[0],i[1],1.) for i in Gf.edges()])

    # Generate walks
    graph = n2v.Graph(G,True,p=0.15, q=.85)
    graph.preprocess_transition_probs()
    walks = graph.simulate_walks(50000,5) #args.num_walks, args.walk_length)

    walks = [map(str, walk) for walk in walks]
    np.save('walks.npy',walks)
else:
    walks = np.load('walks.npy',allow_pickle= True)







def w2v (s):
    print ('running ',s ,'walks')

    model = Word2Vec(walks, size=s, window=1, min_count=0, sg=1, workers=50, iter=100)

    model.wv.save_word2vec_format('mcm_emb%s.txt'%s)
    #pandas.read_csv('mcm_emb.txt',skiprows=1,header=None,delimiter = ' ').c
    print ('done ',s ,'walks')
    return 1




#mp.Pool(2).map(w2v,[2,100])

from word2veckeras.word2veckeras import Word2VecKeras

print ('go')
model = Word2VecKeras(Word2Vec(walks[:100]), size=s, iter=100)