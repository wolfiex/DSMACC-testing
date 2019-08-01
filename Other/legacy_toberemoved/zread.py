
h5file = 'dieselsup.h5'
ignore = ['EMISS','DUMMY','R']

ratebuff = 5

import numpy as np
import h5py,re,dask,os
import dask.array as da
import dask.dataframe as dd

hf = h5py.File( h5file, 'r')
groups = hf.items()
groupkeys = groups[0][1].attrs.keys()
np.warnings.filterwarnings('ignore')
print 'START'


g = groups[0][1]

shead = g.attrs['spechead'].split(',')
sindex = dict([[j,i] for i,j in enumerate(shead)])

rhead = g.attrs['ratehead'].split(',')
rindex = dict([[j,i] for i,j in enumerate(rhead)])

spec = da.from_array(g.get('spec'),chunks=100)
rate = da.from_array(g.get('rate'),chunks=100)

print spec
print rate


products = [i.split('+') for i in re.findall(r'-->([A-z0-9+]*)',g.attrs['ratehead'])]
reactants = [j.split('+') for j in re.findall(r'([A-z0-9+]{1,60})-->',g.attrs['ratehead'])]



print 'groupload'

#check regex works 
if (len(reactants) + len(products))/2 != len(rhead)-ratebuff : print 'reactants and poducts differing lengths' , len(reactants) , len(products) , len(rhead) 

###################################
### calculation arrays    #########


rn2 = re.compile(r'([\.\d]*)\s*\D[\d\D]*')
rn = re.compile(r'([\.\d\s]*)(\D[\d\D]*)')


@dask.delayed
def index(x):
    global sindex
    return [sindex[rn.sub( r'\2', j)] for j in x]



@dask.delayed
def coeff(x):
    rtn = []
    for j in x:
        try:
            rtn.append(float(rn2.sub( r'\1', j)))
        except:
            rtn.append(1.)
    return rtn
    
@dask.delayed
def conc(x):
    #''' takes in global timestep'''
    global tsp
    return [float(spec[tsp,j]) for j in x]
    

@dask.delayed
def mulprod(a,b):
    prod = 1 
    for i in xrange(len(a)):
        prod*=a[i]*b[i]
    return prod
    
        
    
    
cfarr = [];rxnid = [];prdid = []
prodloss = [[[],[]] for i in xrange(len(shead))]

for idx in xrange(len(reactants)):
    row = reactants[idx]
    cfarr.append(coeff(row))
    
    ###################################
    ### reaction prodloss arrays       #########     
        
    r = index(row)
    rxnid.append(r)
    for i in r: prodloss[i][0].append(idx)
    for i in index(products[idx]):
        prodloss[i][1].append(idx)
    
    #prodloss[sheadnumber]   =  [[rxnline],[prodline]]
    #misleading name i know!
    
        
###################################
### get flux for timestep #########

def flux_capacitor(tsp,rxns=None):
    
    #tsp = 155
    #rxns =[281] rxn number in reactants
    
    print 'tsp' , tsp
    
    if rxns==None:
        global f_rxns
        rxns = f_rxns

    elif type(rxns) == int: rxns = [rxns]
    
    fluxes = []
    for i in rxns:
        
        if '-->' not in rhead[i]: 
            fluxes.append(0)
            continue 
        
        flux = float(rate[tsp,i])

        if flux > 0 :

            flux = mulprod([float(spec[tsp,j]) for j in rxnid[i]],cfarr[i]) * flux 
        else:
            flux = 0 
            
        
        try:
            fluxes.append(flux.compute())
        except:
            fluxes.append(0)
        #a = mulprod([float(spec[tsp,j]) for j in x],cfarr[i])
        ##flux.vizualize()
        
    return np.array(fluxes)

@dask.delayed
def conc(x):
    #''' takes in global timestep'''
    global tsp
    return 
    

###############################
###### USAGE
###############################
try:
    ncores = int(os.popen('echo $NCPUS').read())
except:
    ncores=1

print 'cpus' ,ncores

import multiprocessing as mp


def adj_matrix(nin):
    global flux_mat,mytsp,pl
    nids = len(pl)
    
    setin = set(pl[nin][0])
    row = np.empty(nids,dtype=float)
    for i in xrange(nids):
        row[i] = np.sum(flux_mat[mytsp,j] for j in list(setin & set(pl[i][1])))
  
    return np.array(row)    
    
    
    
    

  
import networkx as nx
#import matplotlib.pyplot as plt
#plt.ion()   
#plt.show()    
        
 
what_specs  = list(set(shead) & set([i.split(',')[1].strip() for i in tuple(open('carbons.csv'))]))# ['O3','OH','NO','NO2']#,'OH','EMISS']
## sort by name or alphas


##global
what_ids  = [sindex[i] for i in what_specs]

pl = [prodloss[i] for i in what_ids]

f_rxns =set(re.findall(r'\d+',str(pl)))
f_rxns=np.array(list(f_rxns)).astype(np.int)

tsps = [i for i in  range(1,6*24,48)]#[0,1,2] # 1,maxz.6
flux_mat = np.matrix([flux_capacitor(ts) for ts in tsps]) 

items = [ 'pagerank','betweenness','closeness','load','eigen','degree' ]

res =  dict(zip(items,[[] for i in items]))
load = []

mtx_arr=[]

def nrmd(d):
    mx = 1# np.log10(np.max(d.values()))
    for i in d:
        try : 
            a= np.log10(d[i])/mx
            d[i] = a 
        except:None    
    return d 



def metric(what):
    
    calc={'degree':'nx.degree_centrality(G)', 'load': "nx.load_centrality(G,weight='weight')",
    'eigen':"nx.eigenvector_centrality_numpy(G,weight='weight')",
    'closeness':"nx.closeness_centrality(G,distance='weight')",
    'betweenness': "nx.betweenness_centrality(G,weight='weight')",
    'pagerank':"nx.pagerank(G)"}
    
    d = eval(calc[what])
    mx = np.max(d.values())
    #print 'max',mx
    for i in d:
        try : 
            a= d[i]/mx
            d[i] = a 
        except:None    
    return d
    






for mytsp,tspval in enumerate(tsps):
    matrix = np.matrix(mp.Pool(ncores).map(adj_matrix,range(len(pl) )))
    
    print 'mytsp', mytsp
    G = nx.from_numpy_matrix(matrix)
    
    met = mp.Pool(ncores).map(metric,items)
    
    for i,j in enumerate(items):
        res[j].append(met[i])
    
    # G.edges(data=True)
    #load.append(nx.load_centrality(G,weight='data',normalized=True))

         
    mx = np.max(matrix)
    mtx_arr.append(matrix)
    
    
    
    
    
    
    '''
    plt.imshow(matrix)
    plt.title=i 
    plt.show()
    import time
    time.sleep(1)
    '''



import pandas as pd

def group(cent):
    dta=res[cent]
    
    
    for i in xrange(len(dta)):
        if i ==0:
            df = pd.DataFrame(dta[i].values())
            
            df.index = dta[0].keys()
            df.columns=[cent+'0']
           
        else:
            df[cent+str(i)] = dta[i].values()
    
    return df
    
tsne = pd.concat(mp.Pool(ncores).map(group,res.keys()) ,axis=1)
tsne.index=what_specs

tsne.to_csv('centralitytsne.csv')
print tsne

import pickle
output = open('matrix.pkl', 'wb')
pickle.dump({'data':mtx_arr, 'specs':what_specs}, output)
output.close()


print 'dsfds'
hf.close()
#plot []sep comparison [[]] lump rates of doubles


