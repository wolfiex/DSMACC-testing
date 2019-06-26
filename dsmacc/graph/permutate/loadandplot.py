

import re
import pandas as pd
import numpy as np
from subset_extract import *
import networkx as nx

results =np.load('global_graph.npy')

from scipy.stats.stats import pearsonr




#nodees
data = []
for i in results:

    data.append([i['nodes'],i['edges'],len(i['VOC'])])
data = np.array(data)
df = pd.DataFrame(data,columns = ['nodes','edges','vocs'])
df = df.astype(float)
df.sort_values('nodes', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
df.to_csv('nodeedge_%s_%s.csv'%(','.join(df.min().values.astype(str)),','.join(df.max().values.astype(str))))


#nodees
data = []
for i in results:

    data.append([i['indegree'],i['outdegree'],i['edges']])
data = np.array(data)
df = pd.DataFrame(data,columns = ['indegree','outdegree','edges'])
df = df.astype(float)
df.sort_values('indegree', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
df.sort_values('outdegree', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
df.to_csv('degreecorr_%s_%s.csv'%(','.join(df.min().values.astype(str)),','.join(df.max().values.astype(str))))
print 'degree', pearsonr(df.indegree.values,df.outdegree.values)

#nodees
data = []
for i in results:

    data.append([i['transivity'],i['density'],i['nodes']])
data = np.array(data)
df = pd.DataFrame(data,columns = ['transivity','density','nodes'])
df = df.astype(float)
df.sort_values('transivity', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
df.sort_values('density', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
df.to_csv('transdense_%s_%s.csv'%(','.join(df.min().values.astype(str)),','.join(df.max().values.astype(str))))
print 'transdense'

#nodees
data = []
for i in results:

    data.append([i[j] for j in fn.columns])
data = np.array(data)
df = pd.DataFrame(data,columns = fn.columns)
df = df.astype(float)
df.to_csv('assortivity.csv')
print 'assort'



G = makeG(subset(eqns,vocs)[1])
din = {}
dout ={}
for n in G.nodes():
    din[n]=[]
    dout[n]=[]


for i in results:

    for j in i['ndin']:
        j=j[0]
        din[j].append(i['ndin'][j])
    for j in i['ndout']:
        j=j[0]
        dout[j].append(i['ndout'][j])

degprof = [din,dout]



print 'savedprof'
np.save('degprof.npy',degprof)
print 'saved'




print 'use this for tsne'
