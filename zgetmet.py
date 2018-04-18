from zhdf import new,loaddump,pool,ncores,da,progressbar,h5py,np,pd
import networkx as nx

a = new('BaseRun_init.h5')

print 'read the file'
#    g.attrs['adjspec']  = ','.join(what_specs)
#   g.attrs['adjts']  = ','.join(tsps.astype(str))



def metric(what,G):
    ''' calculate the metrics'''
    import networkx as nx
    import numpy as np
    #print what   , G 
    calc={'degree':'nx.degree_centrality(G)', 'load': "nx.load_centrality(G,weight='weight')",
    'eigen':"nx.eigenvector_centrality_numpy(G,weight='weight')",
    'closeness':"nx.closeness_centrality(G,distance='weight')",
    'betweenness': "nx.betweenness_centrality(G,weight='weight')",
    'pagerank':"nx.pagerank(G)"}
  
    d = eval(calc[what])
    mx = np.max(d.values())
    mn = np.min(d.values())
    
    print what,mx,mn
    for i in d:
        try : 
            a= (d[i]-mn)/(mx-mn)
            d[i] = 1e-8 + a 
        except:None    
    return d
    

def group(cent,res):
    ''' Create pandas csv form data'''
    import pandas as pd
    dta=res[cent]
    for i in xrange(len(dta)):
        if i ==0:
            df = pd.DataFrame(dta[i].values())
            
            df.index = dta[0].keys()
            df.columns=[cent+'00']
           
        else:
            df[cent+'%02d'%i] = dta[i].values()
    
    return df
    
        


items = [ 'betweenness','closeness','load','eigen','degree' ]#'pagerank'
res =  dict(zip(items,[[] for i in items]))
res['fluxx']=[]
res['fluxy']=[]
res['fluxnet']=[]



for n in xrange(len(a.adjts)) :
    ret = []

    dt = a.adj[:,:,n] 
    mask = dt==0

    #mn = np.log10(dt[dt>1e-50].min().min())
    #mx = np.log10(dt[dt>1e-50].max().max())
    mx = np.max(dt)
    #dt = 1e-8 + (mx-dt)/mx
    dt = mx - dt 
    
    
    #dt = np.log10(dt)-mn
    #dt = dt/(mx-mn)
    #dt = 1.001-dt
    
    dt[mask]=0  
    
    print 'go'

    G=nx.from_numpy_matrix(dt,create_using=nx.MultiDiGraph())
    #print G.edges(data=True)
    
    mydf = pd.DataFrame(dt, columns = range(len(a.adjspec)))
    #mydf.index = hf['specs']
    
    ax0 = mydf.sum(axis=0)
    ax1 = mydf.sum(axis=1)
    
    axnet = ax0-ax1
    
    
    res['fluxx'].append(dict(ax0/ax0.max()))
    res['fluxy'].append(dict(ax1/ax1.max()))
    res['fluxnet'].append(dict(axnet/abs(axnet).max()))
    
    
    
    #met = mp.Pool(ncores).map(metric,items)
    
    results = [pool.apply_async(metric, args=(x,G)) for x in items]
                    
    
    bar = progressbar.ProgressBar()            
    met = [p.get() for p in bar(results)]
    for i,j in enumerate(items):
            res[j].append(met[i])


results = [pool.apply_async(group, args=(x,res)) for x in res.keys()]
 
bar = progressbar.ProgressBar()     
tsne = pd.concat( [p.get() for p in bar(results)]  ,axis=1)
tsne.index=a.adjspec

cn = np.array(a.spec.loc[a.ts[[45,117]],a.adjspec])
for i,j in enumerate(cn):

    mask = j==0
    #j = np.log10(j)
    j[mask]=0
    
    mn = np.min(j)
    mx = np.max(j)
    
    j = 1e-8+j-mn
    j=j/(mx-mn)
    
    j[mask]=0


    tsne['conc%02d'%i] = j
    

tsne.to_csv('tsne_save.csv')
print tsne.describe()



#

H=nx.relabel_nodes(G,dict([[i,j] for i,j in enumerate(a.adjspec)]))
nx.write_gexf(H, "test.gexf")

