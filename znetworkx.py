from zhdf import new,loaddump,pool,ncores,da,progressbar,h5py
import numpy as np
import pandas as pd
import os,json,re,sys
#import multiprocessing as mp
import networkx as nx
print ''
print ncores
np.warnings.filterwarnings('ignore')

noro2= True

filename = sys.argv[1]
prefix = 'centrality/'+filename.split('.')[0]
a = new(filename)

#ro2 considerations qsub -I  -q x-large -X -lselect=7:ncpus=1:mem=50G -l place=vscatter:shared
try:
    if noro2: print dsafdsa #intentional fallover
    a.spec.RO2
    ro2go=True
except:
    ro2go=False
    ro2list=set([])

if ro2go:
    ro2file= re.sub(r'\s|\\t|\\n|\'|,','',str(tuple(open('src/background/mcm331complete.kpp'))))
    ro2 = list(set(re.findall(r'ind_([\w\d]+)\b',ro2file)) & set(a.spec.columns))
    ro2eq = re.findall(r'}([\w\+=\.\d]+):[\+-\/\(\)\.\w\d\*]*\bRO2\b[\+-\/\(\)\.\w\d\*]*;',ro2file)
    ro2list = []
    for n,i in enumerate(a.flux.columns):
        if i.replace('-->','=') in ro2eq:
            ro2list.append(n)
    ro2list=set(ro2list)



mcm = list(pd.read_csv('src/background/smiles_mined.csv').name)
if ro2go:  mcm.extend(['CO2','RO2'])
cs = [i.split(',')[-1].replace('\n','') for i in tuple(open('carbons.csv'))]
cs.extend('RO2')
allspecs = filter(lambda x: x not in ['LAT', 'PRESS', 'TEMP', 'H2O', 'M','NA', 'O1D', 'R','O'],a.spec.columns)
allspecs = filter(lambda x: x in cs,allspecs)
print allspecs
if len(allspecs)<1: sys.exit('no species in allspecs, exiting')


tsps = a.ts[[45,45+144/2]]# 6 hoursr a.ts[range(0,len(a.ts),4)]
print tsps
if ro2go:
    ro2fract = a.spec.loc[tsps,ro2].compute()
    ro2val = a.spec.loc[tsps,'RO2'].compute()


def getedge(num,allspecs,prodloss,flux,ro2list,tsps):#,allspecs,a,tsps):
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


            if len(fluxes & ro2list)>0:
                fluxes = fluxes & ro2list
                arr = 20 +  np.log10(np.array(flux.loc[tsps,flux.columns[list(fluxes)]].sum(axis=1)))
                edges.append(['RO2',spec,re.sub(r'\s+',' ',str(arr)) ])

            if len(fluxes) > 0 :
                arr = 20 +  np.log10(np.array(flux.loc[tsps,flux.columns[list(fluxes)]].sum(axis=1)))
                edges.append([i,spec,re.sub(r'\s+',' ',str(arr)) ])


    return edges

def centrality (G,i,num,allspecs):
        import networkx as nx
        def catch(item,what):
            try:
                return item[what]
            except Exception as e:

                return 0

        print 'current', num

        try:
            if num ==0:
                pagerank =nx.pagerank(G)
                return ['pr%3d'%i,[catch(pagerank,k) for k in allspecs ]]
            elif num ==1:
                deg =nx.degree_centrality(G)
                return ['dg%3d'%i,[catch(deg,k) for k in allspecs]]
            elif num ==2:
                close =nx.closeness_centrality(G,distance='weight')
                return ['cl%3d'%i,[catch(close,k) for k in allspecs]]
            elif num ==3:
                bet =nx.betweenness_centrality(G,weight='weight')
                return ['bt%3d'%i, [catch(bet,k) for k in allspecs]]
            elif num ==4:
                cent =nx.eigenvector_centrality(G,weight='weight')
                return ['ev%3d'%i,[catch(cent,k) for k in allspecs]]
        except: return None
        return None

def minigraph(edgelist,i,ro2ts):
    import numpy as np
    import networkx as nx
    print len(edgelist)

    G = nx.DiGraph()
    jval = np.array([float(k[2][i]) for k in edgelist if (len(k[-1])>1 and len(k[-3])>1 and k[2][i]!='')])
    #if len(jval)<1: continue
    jval = jval[jval>0]
    jmin = np.min(jval)
    jmax = np.max(jval)-jmin


    for j in edgelist:
        if j[0] != 'RO2':
            jedge = j[2][i]
            if jedge not in ['','-inf']:
                jedge = float(jedge)

                jedge -= jmin
                jedge /= jmax

                G.add_edge(j[0],j[1],weight=abs(jedge))
        else:

            jedge = j[2][i]
            if jedge not in ['','-inf']:
                jedge = float(jedge)

                jedge -= jmin
                jedge /= jmax

                for s in ro2ts.index:

                    #if ro2ts[s]>1.8e-5:
                        G.add_edge(s,j[1],weight=abs(jedge)*ro2ts[s])
    return G


edgelist=[]

bar = progressbar.ProgressBar()
results  = [pool.apply_async(getedge, args=(x,allspecs,a.prodloss,a.flux.compute(),ro2list,tsps)) for x in np.array_split(range(len(allspecs)),ncores)]
[edgelist.extend(p.get()) for p in bar(results)]

print 'edgelist ready'


df = pd.DataFrame(edgelist)
df.columns = ['source','target','flux']
df.flux =[str(i).replace('        -inf',' 0') for i in df.flux]
df.to_csv(prefix+'_link.csv')


print df.head()

df=pd.read_csv(prefix+'_link.csv',index_col=0)
edgelist = np.array(df)
edgelist[:,2] = [re.sub(r'[\[\]]','',i).split(' ') for i in edgelist[:,2]]
nodes = pd.DataFrame(20 +np.log10(np.array(a.spec.loc[tsps,allspecs].compute()).T),index = allspecs, columns = range(len(tsps)))
nodes[nodes<0]=0
nodes/=nodes.max()


for i in xrange(len(tsps)):
    if ro2go:
        ro2ts = ro2fract.iloc[i]/ro2val.iloc[i]
    else:
        ro2ts=False


    results  = [pool.apply_async(minigraph, args=(x,i,ro2ts)) for x in np.array_split(edgelist,ncores)]
    counter = 1
    G = results[0].get()
    for p in results[1:]:
        counter +=1

        G = nx.compose(G, p.get())
        print 'joined', counter



    graphspecs=list(G.nodes())
    print 'write gexf', i , tsps[i]
    nx.write_gexf(G, prefix+"_test%03d.gexf"%i)

    results  = [pool.apply_async(centrality, args=(G,i,x,allspecs)) for x in list(xrange(5))]

    for p in results:
        d = p.get()

        try:
            if len(d)>1:
                print d[0]
                nodes[d[0]]=d[1]
        except:None


print nodes
nodes.to_csv(prefix+'_nodes.csv')

df = pd.DataFrame([['%3d'%i[0],i[1]] for i in enumerate(tsps)])
df.to_csv(prefix+'_datelist.csv')
print 'finif'


pnt=[]
title = []
specs=[]
for i,j in enumerate(nodes.columns):
    col=2*i
    try:
        dt=str(df.iloc[int(j.split(' ')[-1])][1]).split(' ')[1]
    except:
        dt=str(df.iloc[int(j)][1]).split(' ')[1]
    title.append(str(j)+dt)
    title.append(str(j)+dt)

    a1 = nodes[j].sort_values(ascending=False).head(20)
    pnt.append(a1.index )
    pnt.append(['%.2f'%k for k in a1.values])
    specs.extend(a1.index)

t20 = pd.DataFrame(pnt).T
t20.columns=title
title.sort()
t20=t20[title]

t20.to_csv('t20.csv')



specs=set(specs)
