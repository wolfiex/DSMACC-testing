
from pathos.multiprocessing import Pool
import os

tsne = True

try:
    ncores = int(os.popen('qstat -f $PBS_JOBID | grep resources.used.ncpus').read().split(' ')[-1])

except:
    ncores=1
print 'multiprocessing on ' , ncores
pool = Pool(ncores)

from collections import Counter
import glob


type = ['night','day','*']

for t in type:

    f = glob.glob('lhsgroup/*_gps.'+t)
    lf = len(f)
    print 'nfiles',lf

    def readme(x):
        return ['-'.join(set(i.strip().split('-')))  for i in tuple(open(x))]

    batch = pool.map(readme,f)

    l = []

    for i in batch:
        l.extend(i)

    print len(l)




    print 'save collections'
    with open('lhs_'+t+'.txt','w') as f:
                items = Counter(l).items()
                items = sorted(items,key=lambda x:x[1],reverse=True)

                for i in items:
                    f.write('%d,%d,%s\n'%(i[1],100.*(float(i[1])/lf),i[0]))


if tsne:

    import pandas as pd
    import numpy as np
    import sklearn
    from sklearn.manifold import TSNE

    it = [[i[0].split('-'),i[1]] for i in items]


    specs = list(set([i for j in it for i in j[0]]))
    specs.sort()

    df = pd.DataFrame(np.zeros(shape = (len(specs),len(specs))).astype(int))
    df.index = df.columns = specs

    for z in it:
        if z[1] > 300:
            z1 = z[0]
            for i in z1:
                for j in z1:
                    mean = df.loc[i,j] != 0
                    df.loc[i,j]+=z[1]
                    if mean: df.loc[i,j]/=2


    rm = df.columns[(df.sum()==0)]
    keep = df.columns[(df.sum()!=0)]

    df= df.loc[keep,keep]

    print df.head()
    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
    res = tsne.fit_transform(sklearn.preprocessing.normalize(df))

    print res
    res = pd.DataFrame(res)
    res.index = keep
    res.columns=['x','y']
    res['size'] = df.sum()


    res = res - res.min()
    res = res / res.max()



    from sklearn.cluster import DBSCAN
    db = DBSCAN(eps=0.07, min_samples=3).fit(res.values)
    g = db.labels_



    res['labels']=g

    res.to_csv('tsnegroups')

    with(open('res.json','w')) as f:
        f.write(res.to_json(orient='index'))


    res['size']*=40

    import matplotlib
    import matplotlib.pyplot as plt
    cmap = matplotlib.cm.get_cmap('Spectral')
    res.plot(kind='scatter',x='x',y='y',c='labels',alpha=0.4,s=res['size'], cmap=cmap)
    plt.show()
