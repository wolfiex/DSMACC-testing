import h5py 
import numpy as np
np.warnings.filterwarnings('ignore')
import numpy as np
import networkx as nx
import multiprocessing as mp
import pandas as pd

hf = h5py.File( 'matrix.h5', 'r')

try:
    ncores = int(os.popen('echo $NCPUS').read())
except:
    ncores=1
print 'running on ',ncores

time = np.array(hf['ts']).view('<M8[ns]')


shift = 0
start= 143
end=287+1
by = 36

print range(start,end,by)
for i in range(start,end,by):
    print time[i]
items = [ 'betweenness','closeness','load','eigen','degree' ]#'pagerank'
res =  dict(zip(items,[[] for i in items]))
res['fluxx']=[]
res['fluxy']=[]
res['fluxnet']=[]

def metric(what):
    #print what   , G 
    calc={'degree':'nx.degree_centrality(G)', 'load': "nx.load_centrality(G,weight='weight')",
    'eigen':"nx.eigenvector_centrality_numpy(G,weight='weight')",
    'closeness':"nx.closeness_centrality(G,distance='weight')",
    'betweenness': "nx.betweenness_centrality(G,weight='weight')",
    'pagerank':"nx.pagerank(G)"}
  
    d = eval(calc[what])
    print what
    
    mx = np.max(d.values())
    mn = np.min(d.values())
    #
    print what,mx,mn
    for i in d:
        try : 
            a= (d[i]-mn)/(mx-mn)
            d[i] = 1e-4 + a 
        except:None    
    return d
    




for n in range(start,end,by) :
    ret = []

    dt = np.array(hf['data'][:,:,n])   
    mask = dt==0


    mn = np.log10(dt[dt>1e-50].min().min())
    mx = np.log10(dt[dt>1e-50].max().max())
    
    mx = np.max(dt)
    
     
    print mx
    dt = 1e-6 + (mx-dt)/mx
        
    
    #dt = np.log10(dt)-mn
    #dt = dt/(mx-mn)
    
    #dt = 1.001-dt
    
    dt[mask]=0
    
    print 'go'

    G=nx.from_numpy_matrix(dt,create_using=nx.MultiDiGraph())
    #print G.edges(data=True)
    
    mydf = pd.DataFrame(dt, columns = range(len(hf['specs'])))
    #mydf.index = hf['specs']
    
    ax0 = mydf.sum(axis=0)
    ax1 = mydf.sum(axis=1)
    
    axnet = ax0-ax1
    
    
    res['fluxx'].append(dict(ax0/ax0.max()))
    res['fluxy'].append(dict(ax1/ax1.max()))
    res['fluxnet'].append(dict(axnet/abs(axnet).max()))
    
    
    
    met = mp.Pool(ncores).map(metric,items)
        
    for i,j in enumerate(items):
            res[j].append(met[i])










####no idnent  
 
def group(cent):
    dta=res[cent]
    
    
    for i in xrange(len(dta)):
        if i ==0:
            df = pd.DataFrame(dta[i].values())
            
            df.index = dta[0].keys()
            df.columns=[cent+'00']
           
        else:
            df[cent+'%02d'%i] = dta[i].values()
    
    return df
    
tsne = pd.concat(mp.Pool(ncores).map(group,res.keys()) ,axis=1)
tsne.index=hf['specs']

tsne.to_csv('tsne_save.csv')
print tsne


def loaddump(filename):
    import dill
    return dill.load(open(filename))


df = pd.read_csv('tsne_save.csv')
df.index=df['/specs']
df.drop('/specs',axis=1)




b=loaddump('dieselsupclearflow.dill')

    

conc = np.array(b.spec.loc[:,df.index])[range(start,end,by)]

df2 = pd.DataFrame(conc.T,columns = ['conc%02d'%i for i in range(len(conc))])
df2.index = df.index

mask1 = df2>1e-50
mask = df2<1e-50
mn = np.log10(df2[mask1].min().min())
mx = np.log10(df2[mask1].max().max())
 
 
d = np.log10(df2)-mn
d = d/(mx-mn)
d += 0.001
d[mask]=0



df3 = pd.concat([d,df],axis=1)
df3.to_csv('finaltsne.csv')

print d.describe()


'''
import seaborn as sns; sns.set()
from matplotlib.pyplot import*

time = np.array(hf['ts'])


for n in range(start,end,by):
    print n
    dt = hf['data'][:,:,n]
    dt = np.log10(dt)
    mask = dt==-np.inf

    dt[mask] = 999 
    mn = np.min(dt)

    dt=(dt-mn+0.0001)
    dt[mask] = 0 
    dt = dt/np.max(dt)

    title(time.astype('M8[s]')[n])
    ax = sns.heatmap(dt,cmap="RdBu",mask= mask)

    #fig = ax.get_figure()
    savefig('./plots/%04d.png'%n)
    #show()    
    clf()    
    
'''    
print 'finished' 
