import numpy as np
import pandas as pd
from numpy import array, float32
import re

lines = re.findall(r"'(.*-->.*)'",''.join(open('model_Monitor.f90','r').readlines()).replace(' ',''))
names = dict(re.findall(r"RCONST\((\d+).*= (.*)\n",''.join(open('model_Rates.f90','r').readlines())))

match = {}
for i,j in enumerate(lines):
    match[j] = names[str(i+1)]


data = np.load('autorate.npy')

exec('data='+str(data))
keys = data.keys()



k = []
vals =[]
for i in keys:
    try:
            dummy = list(data[i])
            dummy.append(match[i])

            vals.append(dummy)
            k.append(i)
    except: print('ignoring',i)

df = pd.DataFrame(vals, index = k, columns = 'x y rate'.split())

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans,DBSCAN
from sklearn.preprocessing import normalize

kmeans = KMeans(n_clusters=3,max_iter= 100000,tol= 1e-19)
kmeans.fit(df['x y'.split()])

df['kmeans'] = kmeans.predict(df['x y'.split()])+1

df['kmeans'] = DBSCAN(eps=20, min_samples=2).fit(df['x y'.split()]).labels_+1
dbs = 1


if dbs:
    df['labels']= 1
    ndf = []

    for i in set(df['kmeans']):

        cl = df['kmeans'] == i
        sdf = df[cl]
        eps = ( .0001)

        db = DBSCAN(eps=eps, min_samples=2).fit(normalize(sdf['x y'.split()])).labels_ + 1
        sdf['labels'] = db
        ndf.append(sdf)
        print len(set(sdf['labels']))

    df = pd.concat(ndf)
else:
    df['labels'] = df['kmeans']

df.to_csv('RateAE.csv')

df.plot(kind='scatter',x='x',y='y',c='kmeans', cmap='viridis',alpha=.95)
plt.show()
