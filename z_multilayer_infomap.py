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

print ('\n', ncores)



filename = sys.argv[1]
group_id = int(sys.argv[2])-1 #jobarrays start at 1

# list of species
mcm = list(pd.read_csv('src/background/smiles_mined.csv').name)
cs = [i.split(',')[-1].replace('\n','') for i in tuple(open('carbons.csv'))]
cs.append('CO')


exclude = ['RO2','LAT', 'LON','PRESS', 'TEMP', 'H2O', 'M','NA', 'O1D', 'R','O','O1D',
 'O3', 'O2', 'NO2', 'NO3', 'N2O5', 'H2O2', 'TEMP', 'NO', 'NA',
 'KMT05', 'KMT04', 'KMT07', 'KMT06', 'KMT01', 'HO2NO2', 'KMT03',
  'KMT02', 'HO2', 'KMT09', 'KMT08', 'HNO3', 'SO3', 'SO2',
  'N2', 'OH', 'H2', 'HONO', 'HSO3', 'H2O', 'KMT12', 'KMT11', 'SA']




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
for photo in [0,1]:
    for spec in allspecs:
        for i in allspecs:
            if spec != i :
                fd = set(data.prodloss[spec]['prod']) & set(data.prodloss[i]['loss'])

                if len(fd) > 0 :
                    thresh = 50
                    #skip no reactions
                    arr = thresh +  np.log10(np.array(flux[photo].loc[:,flux[photo].columns[list(fd)]].sum(axis=1)))

                    #if smaller than threshold
                    arr[arr <0] = 0

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




        infomapWrapper = infomap.Infomap("-d -N 2 -z --inner-parallelization -2 -p 0.8 --multilayer-relax-rate 0.8 ")#infomap.Infomap("-d -N 100")
        mine = min(extent)
        maxe = max(extent)

        network = infomapWrapper.network()

        for e in edges[photo]:
            e[2] = np.array(e[2]).astype(float)



            e[2] -= mine
            e[2] /= (maxe-mine)
            for layer,r in enumerate(e[2]):
                # from (layer, node) to (layer, node) weight
                network.addMultilayerLink(layer, spec2num[e[0]], layer,spec2num[e[1]],weight=( 0.01 + 0.99*r ))
                #network.addLink( spec2num[e[0]], spec2num[e[1]],weight=( 0.01 + 0.99*r ))
                #infomapWrapper.addLink(spec2num[e[0]], spec2num[e[1]], 0.01 + 0.99*(r-mine)/(maxe-mine) )
                #infomapWrapper.addLink(int(spec2num[e[0]]), int(spec2num[e[1]]),weight=( 0.01 + 100.99*(r-mine)/(maxe-mine) ))

                #network.addLink(spec2num[e[0]], spec2num[e[1]], (0.01 + 0.99*r)*100)
                #print spec2num[e[0]], spec2num[e[1]],  e[2]
                f.write('%d %d %d %2f\n'%(layer, spec2num[e[0]], spec2num[e[1]],( 0.01 + 0.99*r )))


            '''

        #f.write('*Inter\n#layerId physicalId layerId weight\n')g
        for i in range(0,len(e[2])-1):
            #for j in range(len(e[2])):
                for k in range(len(allspecs)):
                    #if j>= i:break
                    network.addMultilayerInterLink( i, k, i+1, 1)
                    #f.write('%d %d %d %d\n'%(i,k,i,1000))


                    #infomapWrapper.addMultilayerLink( i, k, j,k, 1)
                    #network.addMultilayerLink(i, k,j, k, 1)

'''

    infomapWrapper.run()




    print("Result")
    print network.numLinks() ,  len(edges[photo]), network.numNodes(),network.sumLinkWeight()/network.numLinks(),infomapWrapper.numActiveModules()

    print("\n#node module")
    groups =  infomapWrapper.getModules()
    groups = dict((allspecs[k], v) for k, v in groups.items())
    #print(groups,np.max(groups.keys()),len(set(groups.keys())), len(data.spec.columns))

    mygroups = [[] for i in [None]*int(infomapWrapper.numActiveModules())]

    for i in groups:
        mygroups[groups[i]].append(i)


    mygroups=filter(lambda x : len(x)>0 ,mygroups)
    mygroups = sorted(mygroups,key=lambda x : len(x),reverse=True)

    for g in mygroups:
            print(g)

    with open('centrality/lhsgroup/%04d_gps.%s'%(group_id,['night','day'][photo]),'w') as f:

        for i in mygroups:#filter(lambda x : len(x) in range(2,11),groups)
            f.write('-'.join(set(i))+'\n')

    for i in edges[photo]: i[2]=list(i[2])

    with open('centrality/lhsedge/%04d_edge.%s'%(group_id,['night','day'][photo]),'w') as f:

            f.write(str(edges[photo]).replace("'",'"'))
