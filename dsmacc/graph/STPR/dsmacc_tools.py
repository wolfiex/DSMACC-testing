import time
from pathos.multiprocessing import ProcessPool
import numpy as np
import pandas as pd   

def undirect(self,ncores=4):
    '''
    Remove directional links between species by finding the net weight of the jacobian
    
    '''

    dct={}
    specs = self.spec.columns
    iterate = []
    for i in specs:
        for j in specs:
            if i==j: break
            iterate.append(list(set([i,j])))
            
    self = self.jacsp.compute()


    def net(d):
        ret = []
        for n in d:
            total =[]
            try: total.append(self['%s->%s'%(n[0],n[1])])
            except:None
            try: total.append(-self['%s->%s'%(n[1],n[0])])
            except:None

            if len(total) > 0 :
                ret.append(['->'.join(n), sum(total)])
        return ret

    dct = ProcessPool(nodes=ncores).amap(net,np.array_split(iterate,ncores))

    while not dct.ready():
         time.sleep(5); print(".")

    dct = dct.get()

    return dict([i for j in dct for i in j])


def net_combine(base,change):
    '''
    combines two net systems of equal node names
    Inputs:
        undirected(base)
        undirected(change)
    Returns:
        net concatenated graph
    '''

    a = pd.concat(  base.values(),axis=1, keys =   base.keys()).dropna()
    b = pd.concat(change.values(),axis=1, keys = change.keys()).dropna()

    keep = list(set(a.keys()) & set(b.keys()))
    dismiss = set(a.keys()) ^ set(b.keys())

    print('Ignored species',dismiss)
    net_edges = b[keep].divide(a[keep],axis=1)
    
    return net_edges.dropna(axis=1) #rm 0/0 columns