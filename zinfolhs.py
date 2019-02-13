from zhdf import new,loaddump,pool,ncores,da,progressbar,h5py
import numpy as np
import pandas as pd
import os,json,re,sys
import multiprocessing as mp
import networkx as nx
print ''
print ncores
from collections import Counter
import networkx as nx
from infomap import infomap
import community

np.warnings.filterwarnings('ignore')

print 'load libs'

os.system('rm centrality/lhsgroup/*')

filename = 'lhs.h5'
groups = new(filename).groups


mcm = list(pd.read_csv('src/background/smiles_mined.csv').name)
cs = [i.split(',')[-1].replace('\n','') for i in tuple(open('carbons.csv'))]
#cs.extend('RO2')



def getedge(num,allspecs,prodloss,flux,tsps):#,allspecs,a,tsps):
    edges = []
    print len(num)
    print ''
    import progressbar,re
    import numpy as np
    bar = progressbar.ProgressBar()

    for j in bar(list(num)):

        spec = allspecs[j]

        for i in allspecs:
            fluxes = set(prodloss[spec]['prod']) & set(prodloss[i]['loss'])

            if len(fluxes) > 0 :
                arr = 20 +  np.log10(np.array(flux.loc[tsps,flux.columns[list(fluxes)]].sum(axis=1)))
                edges.append([i,spec,arr])

    return edges




def mapinfomap(e):
    try:
        g= e[0]
        t= e[1]
        print 'Infomap'
        G = infomap.Infomap("-d -N 100")
        Gnx = nx.DiGraph()
        jval = np.array([float(k[2][t]) for k in edgelist if (len(k[-1])>0 and len(k[-3])>0 and k[2][t]!='')])
        #if len(jval)<1: continue
        jval = jval[jval>0]
        jmin = np.min(jval)
        jmax = np.max(jval)-jmin
        for j in edgelist:
                jedge = j[2][t]
                if str(jedge) not in ['','-inf']:
                    jedge = float(jedge)

                    jedge -= jmin
                    jedge /= jmax
                    try:
                        Gnx.add_edge(j[0],j[1],weight=abs(jedge))
                        G.addLink(toindex[j[0]],toindex[j[1]],weight=abs(jedge))
                    except Exception as e:
                        print 'fail' , e


        G.run();
        tree = G.tree

        partition = {}
        for node in tree.leafIter():
            partition[node.originalLeafIndex] = node.moduleIndex()


        groups = [[] for i in  np.empty(np.array(partition.values()).max())]

        for i,j in enumerate(speclist):
            try:
                groups[partition[i]].append(j)
            except:
                print 'no node', i,j


        groups = sorted(groups,key=lambda x : len(x),reverse=True)
        with open('centrality/lhsgroup/%04d_%04d.gps'%(g,t),'w') as f:
                for i in groups:#filter(lambda x : len(x) in range(2,11),groups)
                    f.write('-'.join(set(i))+'\n')
        return ['-'.join(set(i)) for i in groups]
    except Exception as e:
        print 'failed',e
        return ''



pool.close()
pool = mp.Pool(ncores)

for g in groups.values():
    print 'gogogo '+str(g)

    run = new(filename,groupid=g)
    allspecs = filter(lambda x: x not in ['LAT', 'LON','PRESS', 'TEMP', 'H2O', 'M','NA', 'O1D', 'R','O','O1D',
     'O3', 'O2', 'NO2', 'NO3', 'N2O5', 'H2O2', 'TEMP', 'NO', 'NA',
     'KMT05', 'KMT04', 'KMT07', 'KMT06', 'KMT01', 'HO2NO2', 'KMT03',
      'KMT02', 'HO2', 'KMT09', 'RO2', 'KMT08', 'CO', 'HNO3', 'SO3', 'SO2',
      'N2', 'OH', 'H2', 'HONO', 'HSO3', 'H2O', 'KMT12', 'KMT11', 'SA'],run.spec.columns)


    speclist = list(allspecs)
    toindex = dict(zip(speclist,range(len(speclist))))
    fromindex = dict(zip(range(len(speclist)),speclist))

    tsps = run.ts[range(24,len(run.spec),24)]

    edgelist=[]

    bar = progressbar.ProgressBar()
    results  = [pool.apply_async(getedge, args=(x,allspecs,run.prodloss,run.flux.compute(),tsps)) for x in np.array_split(range(len(allspecs)),ncores)]
    [edgelist.extend(p.get()) for p in bar(results)]

    print 'edgelist ready'

    pool.close()
    pool = mp.Pool(ncores)

    words = pool.map(mapinfomap,zip([g]*len(tsps),xrange(len(tsps))))

    l =[]
    for i in words:
        l.extend(i)

    print 'save collections'
    with open('centrality/lhsgroup/collected.txt','w') as f:
            items = Counter(l).items()
            items = sorted(items,key=lambda x:x[1],reverse=True)

            for i in items:
                f.write('%d,%s\n'%(i[1],i[0]))





os.system('/opt/pbs/bin/qdel $PBS_JOBID')
os.system('pkill screen')
