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

print 'depreciated'
sys.exit()

from infomapfolder import infomap

print ('\n', ncores)

# list of species
mcm = list(pd.read_csv('src/background/smiles_mined.csv').name)
cs = [i.split(',')[-1].replace('\n','') for i in tuple(open('carbons.csv'))]
cs.append('CO')
exclude = ['RO2','LAT', 'LON','PRESS', 'TEMP', 'H2O', 'M','NA', 'O1D', 'R','O','O1D',
 'O3', 'O2', 'NO2', 'NO3', 'N2O5', 'H2O2', 'TEMP', 'NO', 'NA',
 'KMT05', 'KMT04', 'KMT07', 'KMT06', 'KMT01', 'HO2NO2', 'KMT03',
  'KMT02', 'HO2', 'KMT09', 'KMT08', 'HNO3', 'SO3', 'SO2',
  'N2', 'OH', 'H2', 'HONO', 'HSO3', 'H2O', 'KMT12', 'KMT11', 'SA']


filename = sys.argv[1]
group_id = int(sys.argv[2])-1 #jobarrays start at 1



#read data
data = new(filename,group_id)
allspecs = filter(lambda x: x not in exclude ,data.spec.columns)
spec2num = dict(zip(allspecs,range(len(allspecs))))

#split into day and night
flux = data.flux.compute()
flux['group']= [str(i).split(':')[0] for i in data.timesteps]

flux = flux.groupby(by='group').mean()
flux['hour'] = [i.split(' ')[-1] for i in flux.index]

day = '10,11,12,13,14'.split(',')[0]
print   'dsafdas'
#########
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
                f = set(data.prodloss[spec]['prod']) & set(data.prodloss[i]['loss'])

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
--pre-cluster-multilayer
    --weight-threshold
    --two-level --map
    -p<f> --teleportation-probability .15
    --multilayer-relax-rate <f>
[Deprecated, use multilayer-relax-rate] The probability to relax the constraint to move only in the current layer and instead move to a random layer where the same physical node is present. If negative, the inter-links have to be provided. (Default: -1)
    Pre-cluster multiplex networks layer by layer.'''


    with open('test.net','w') as f:

        f.write('# %s.net - Multilayer network \n*Vertices %d\n#physicalId name\n'%(group_id,len(allspecs)) )

        for i,s in enumerate(allspecs):
            f.write('%d "%s"\n'%(i,s))

        f.write('*Intra\n#layerId physicalId physicalId weight\n')




        G = infomap.Infomap("-d -N 2 -z")#infomap.Infomap("-d -N 100")
        Gnx = nx.DiGraph()

        mine = min(extent)
        maxe = max(extent)

        #network = infomapWrapper.network()

        for e in edges[photo]:
            e[2] = np.array(e[2]).astype(float)



            e[2] -= mine
            e[2] /= (maxe-mine)
            for layer,r in enumerate(e[2]):
                # from (layer, node) to (layer, node) weight
                Gnx.add_edge(spec2num[e[0]],spec2num[e[1]],weight = ( 0.01 + 0.99*r ))
                G.addLink( spec2num[e[0]],spec2num[e[1]],weight = ( 0.01 + 0.99*r ))
                #infomapWrapper.addLink(spec2num[e[0]], spec2num[e[1]], 0.01 + 0.99*(r-mine)/(maxe-mine) )
                #infomapWrapper.addLink(int(spec2num[e[0]]), int(spec2num[e[1]]),weight=( 0.01 + 100.99*(r-mine)/(maxe-mine) ))

                #network.addLink(spec2num[e[0]], spec2num[e[1]], (0.01 + 0.99*r)*100)
                #print spec2num[e[0]], spec2num[e[1]],  e[2]
                f.write('%d %d %d %2f\n'%(layer, spec2num[e[0]], spec2num[e[1]],( 0.01 + 0.99*r )))
                break




    G.run();
    tree = G.tree


    partition = {}
    for node in tree.leafIter():
        partition[node.originalLeafIndex] = node.moduleIndex()


    groups = [[] for i in  np.empty(np.array(partition.values()).max())]

    for i,j in enumerate(allspecs):
        try:
            groups[partition[i]].append(j)
        except:
            print 'no node', i,j


    groups = sorted(groups,key=lambda x : len(x),reverse=True)

    '''
        #f.write('*Inter\n#layerId physicalId layerId weight\n')
        for i in range(0,len(e[2])-1):
            #for j in range(len(e[2])):
                for k in range(len(allspecs)):
                    #if j>= i:break
                    network.addMultilayerInterLink( i, k, i+1, 1)
                    #f.write('%d %d %d %d\n'%(i,k,i,1000))


                    #infomapWrapper.addMultilayerLink( i, k, j,k, 1)
                    #network.addMultilayerLink(i, k,j, k, 1)



    infomapWrapper.run()




    print("Result")
    print network.numLinks() ,  len(edges[photo]), network.numNodes(),network.sumLinkWeight()/network.numLinks()

    print("\n#node module")
    groups =  infomapWrapper.getModules()
    groups = dict((allspecs[k], v) for k, v in groups.items())
    print(groups,np.max(groups.keys()),len(set(groups.keys())), len(data.spec.columns))

    mygroups = []*infomapWrapper.numActiveModules()

    for i in groups:
        mygroups[groups[i]].append(i)





    infomapWrapper.writeTree('hi.tree')
    '''


    sdfads=fdsfd

    '''jwww.mdpi.com/1999-4893/10/4/112/htm

    Appendix A.2. Clustering a Multilayer Network
The multilayer network in Figure 4a can be described with the multilayer network format in fig3a.net below and clustered for relax rate r=0.4 with the command
./Infomap --input-format multilayer --multilayer-relax-rate 0.4 fig3a.net .
See Appendix A.5 for the overlapping clustering output, and Appendix A.4 for an alternative representation with a sparse memory network. In fact, Infomap internally represents the multilayer network in fig3a.net for r=0.4 with the sparse memory network in Appendix A.4 with transition rates r/2 between state nodes in different layers, since r/2 stays among state nodes in the same layer in this symmetric two-layer network.
# fig3a.net - Multilayer network
# Lines starting with # are ignored
*Vertices 5
#physicalId name
1 "i"
2 "j"
3 "k"
4 "l"
5 "m"
*Intra
#layerId physicalId physicalId weight
1 1 4 1
1 4 1 1
1 1 5 1
1 5 1 1
1 4 5 1
1 5 4 1
2 1 2 1
2 2 1 1
2 1 3 1
2 3 1 1
2 2 3 1
2 3 2 1

'''






    tree = infomapWrapper.tree

    print("Found %d modules with codelength: %f" % (tree.numTopModules(), tree.codelength()))



    partition = {}
    for node in tree.leafIter():
        partition[node.originalLeafIndex] = node.moduleIndex()


    groups = [[] for i in  np.empty(np.array(partition.values()).max())]

    for i,j in enumerate(allspecs):
        try:
            groups[partition[i]].append(j)
        except:
            print 'no node', i,j


    groups = sorted(groups,key=lambda x : len(x),reverse=True)

    for g in groups:
            print(g)
    with open('centrality/lhsgroup/%04d_gps.%s'%(group_id,['night','day'][photo]),'w') as f:

        for i in groups:#filter(lambda x : len(x) in range(2,11),groups)
            f.write('-'.join(set(i))+'\n')
