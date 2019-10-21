from zhdf import new,loaddump,da,h5py
import numpy as np
import pandas as pd
import os,json,re,sys
import networkx as nx
#from infomap
import infomap
import tensorflow as tf #v2.0


filename = 'lhs_general.h5'#sys.argv[1]
group_id = 0 #int(sys.argv[2])-1 #jobarrays start at 1


exclude = ['RO2','LAT', 'LON','PRESS', 'TEMP', 'H2O', 'M','NA', 'O1D', 'R','O','O1D',
 'O3', 'O2', 'NO2', 'NO3', 'N2O5', 'H2O2', 'TEMP', 'NO', 'NA',
 'KMT05', 'KMT04', 'KMT07', 'KMT06', 'KMT01', 'HO2NO2', 'KMT03',
  'KMT02', 'HO2', 'KMT09', 'KMT08', 'HNO3', 'SO3', 'SO2',
  'N2', 'OH', 'H2', 'HONO', 'HSO3', 'H2O', 'KMT12', 'KMT11', 'SA']



#read data
data = new(filename,group_id)
allspecs = filter(lambda x: x not in exclude ,data.spec.columns)

try:
    spec2num = np.load('spec2num.txt')

except:
    spec2num = dict(zip(data.spec.columns,range(len(data.spec.columns))))
    np.save('spec2num.txt',spec2num)


data.create_posjac()
data.posjac = (np.log10(data.posjac)+20).apply(lambda x : np.nan_to_num(x * np.isfinite(x)))


layers = 24 #4h


keep = []
keepid = []
keepname = []
for rr in data.posjac.columns:
    d = rr.split('->')
    if d[1]!= d[0]:
        try:
            id = [spec2num[i] for i in d]
            keepid.append(id)
            if d[0] in allspecs and d[1] in allspecs:
                keep.append(id)
                keepname.append(rr)
        except:
            print 'pass', d

#tf.SparseTensor(indices= np.array(keepid).astype(int), values = range(l
#    ...: en(keepid)),dense_shape = max(keepid))


start = 0

# adjacency for tf
np.save('REDUCE/adj_%04d_%03d.npy', [keepid,data.posjac.iloc[start:start+layers].mean().values])



for start in range(0,1):#len(data.posjac),layers):
    infomapWrapper = infomap.Infomap("-d -N 2 -z --inner-parallelization -2 -p 0.8 --multilayer-relax-rate 0.8 ")
    for col in range(len(keepname)):
        pslice = data.posjac[keepname[col]].iloc[start:start+layers].values
        for l in range(layers):

            infomapWrapper.network.addMultiplexLink(l, keep[col][0], l,keep[col][1], pslice[l])



    infomapWrapper.run()

    print("Result")
    network = infomapWrapper.network
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




print 'fi'
