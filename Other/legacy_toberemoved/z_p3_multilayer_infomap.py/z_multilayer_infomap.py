'''
READ....

Daniel Ellis 2018
'''
'''
For each group - read as argument and use jobArray -

    for day / night hours
        calculate edgelist
            create a multilayer network
                save both groupings at prefix with .day .night extentions
'''


#

from zhdf import new,loaddump,pool,ncores,da,progressbar,h5py
import numpy as np
import pandas as pd
import os,json,re,sys
import multiprocessing as mp
import networkx as nx
#from infomap
import infomap

print('\n', ncores)



myInfomap = infomap.Infomap("--two-level --directed")

# Access the default network to add links programmatically
network = myInfomap#.network()

# Add weight as optional third argument
network.addLink(0, 1)
network.addLink(0, 2)
network.addLink(0, 3)
network.addLink(1, 0)
network.addLink(1, 2)
network.addLink(2, 1)
network.addLink(2, 0)
network.addLink(3, 0)
network.addLink(3, 4)
network.addLink(3, 5)
network.addLink(4, 3)
network.addLink(4, 5)
network.addLink(5, 4)
network.addLink(5, 3)

# Run the Infomap search algorithm to find optimal modules
myInfomap.run()

print(("Found {} modules with codelength: {}".format(myInfomap.numTopModules(), myInfomap.codelength())))

print("Result")
print("\n#node module")
for node in myInfomap.iterTree():
  if node.isLeaf():
    print(("{} {}".format(node.physicalId, node.moduleIndex())))





dfasd =gf
filename = sys.argv[1]
group_id = int(sys.argv[2])-1 #jobarrays start at 1



# list of species
mcm = list(pd.read_csv('src/background/smiles_mined.csv').name)
cs = [i.split(',')[-1].replace('\n','') for i in tuple(open('carbons.csv'))]

exclude = ['RO2','LAT', 'LON','PRESS', 'TEMP', 'H2O', 'M','NA', 'O1D', 'R','O','O1D',
 'O3', 'O2', 'NO2', 'NO3', 'N2O5', 'H2O2', 'TEMP', 'NO', 'NA',
 'KMT05', 'KMT04', 'KMT07', 'KMT06', 'KMT01', 'HO2NO2', 'KMT03',
  'KMT02', 'HO2', 'KMT09', 'KMT08', 'CO', 'HNO3', 'SO3', 'SO2',
  'N2', 'OH', 'H2', 'HONO', 'HSO3', 'H2O', 'KMT12', 'KMT11', 'SA']




#read data
data = new(filename,group_id)
allspecs = [x for x in data.spec.columns if x not in exclude]
spec2num = dict(list(zip(allspecs,list(range(len(allspecs))))))

#split into day and night
flux = data.flux.compute()
flux['group']= [str(i).split(':')[0] for i in data.timesteps]

flux = flux.groupby(by='group').mean()
flux['hour'] = [i.split(' ')[-1] for i in flux.index]

day = '10,11,12,13,14'.split(',')
day = flux[flux.hour.apply(lambda x: x in day)]

night = '22,23,00,01,02'.split(',')
night = flux[flux.hour.apply(lambda x: x in night)]


#edges
extent = []
flux = [night,day]#0,1
edges= [[],[]]
for photo in [0]:
    for spec in allspecs:
        for i in allspecs:
            if spec != i :
                f = set(data.prodloss[spec]['prod']) | set(data.prodloss[i]['loss'])

                if len(f) > 0 :
                    #skip no reactions
                    arr = 20 +  np.log10(np.array(flux[photo].loc[:,flux[photo].columns[list(f)]].sum(axis=1)))
                    if arr.sum()>0:
                        #skip non fluxes
                        edges[photo].append([i,spec,arr])

                        extent.extend([min(arr),max(arr)])


    '''
    --markov-time 3
    --weight-threshold <n>
    Limit the number of links to read from the network. Ignore links with less weight than the threshold. (Default: 0)
    --pre-cluster-multiplex
    Pre-cluster multiplex networks layer by layer.'''

    infomapWrapper = infomap.Infomap("-d -N 100 ")#infomap.Infomap("-d -N 100")
    mine = min(extent)
    maxe = max(extent)

    network = infomapWrapper.network

    for e in edges[photo]:
        e[2] = np.array(e[2]).astype(float)

        e[2] -= mine
        e[2] /= (maxe-mine)
        #for layer,r in enumerate(e[2]):
            # from (layer, node) to (layer, node) weight
            #network.addMultiplexLink(layer, spec2num[e[0]], layer, spec2num[e[1]], 0.1 + 0.9*(r-mine)/(maxe-mine) )
            #infomapWrapper.addLink(spec2num[e[0]], spec2num[e[1]], 0.01 + 0.09*(r-mine)/(maxe-mine) )
        network.addLink(spec2num[e[0]], spec2num[e[1]], weight = 0.01 + 0.09*e[2][0])
        #print spec2num[e[0]], spec2num[e[1]],  e[2]


    '''
    for i in range(len(e[2])):
        for j in range(len(e[2])):
            for k in range(len(allspecs)):
                network.addMultiplexLink(i, k, j, k, 10 )
    '''

    infomapWrapper.run()

    tree = infomapWrapper.tree

    print(("Found %d modules with codelength: %f" % (tree.numTopModules(), tree.codelength())))


    partition = {}
    for node in tree.leafIter():
        partition[node.originalLeafIndex] = node.moduleIndex()


    groups = [[] for i in  np.empty(np.array(list(partition.values())).max())]

    for i,j in enumerate(allspecs):
        try:
            groups[partition[i]].append(j)
        except:
            print('no node', i,j)


    groups = sorted(groups,key=lambda x : len(x),reverse=True)

    for g in groups:
            print(g)
    with open('centrality/lhsgroup/%04d_gps.%s'%(group_id,['night','day'][photo]),'w') as f:

        for i in groups:#filter(lambda x : len(x) in range(2,11),groups)
            f.write('-'.join(set(i))+'\n')
