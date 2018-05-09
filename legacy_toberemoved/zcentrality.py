from zhdf import new,loaddump,pool,ncores,da
import numpy as np
import os
 
print ''

np.warnings.filterwarnings('ignore')



a = new('BaseRun_init.h5')

what_specs  = list(set(a.spec.columns) & set([i.split(',')[1].strip() for i in tuple(open('carbons.csv'))]))


a.calcFlux(specs=what_specs,timesteps=[i for i in range(len(a.ts))])

a.dump()

b = a 
#b=loaddump('dieselsupclearflow.dill')

#############b.flux=False

what_specs  = list(set(b.spec.columns) & set([i.split(',')[1].strip() for i in tuple(open('carbons.csv'))]))





def adj_matrix(spcz,prodloss,allspecs,flux,lents):
    ''' create adj matrix for animation '''
    import numpy as np
    rows=[]
    for spc in spcz :
        #try:
            inspec = set(prodloss[spc]['loss'])
            
            row = []
            for i in xrange(len(allspecs)):
                match = np.array(list( inspec & set(prodloss[allspecs[i]]['prod'])))
                
                if len(match)==0:
                    row.append(np.zeros(lents))
                else:
                    row.append(np.array(flux.loc[match,:].sum()))
                    
            rows.append(row)
        #except Exception as err:
         #   print inspec, spc , err, 'err'
    #print rows        
    return rows    
       

print 'start'

#print b.flux.loc[[5204,5205],:].sum().compute()
try: 
    i[0]=type(b.mat)
except:


                results = [pool.apply_async(adj_matrix, args=(x,b.prodloss,what_specs,b.flux,len(b.ts),)) for x in np.array_split(what_specs,ncores)]
                

                print 'calc'
                
                #results = [p.get() for p in results] 
                
                #print results[1]
                
                #results = [i for j in results for j in i]
                print 'dne'
                res = []
                
                [res.extend(p.get()) for p in results]
                
                
                print np.array(res).shape
                
                
                #b.mat = da.from_array(np.array(res),chunks = (5000,5000,1000))
              
                #b.map = msgpack.packb(np.array(res), default=m.encode)
                #x_rec = msgpack.unpackb(x_enc, object_hook=m.decode)
                
                import h5py
                hf = h5py.File( 'matrix.h5', 'w')

                

                hf.create_dataset(  name = 'specs',data = what_specs,dtype='S15', compression="gzip", compression_opts=9)
                
                hf.create_dataset(  name = 'ts',data =b.ts.astype('<i8'), compression="gzip", compression_opts=9,dtype='<i8')
                #to undo nparr.view('<M8[ns]')

                hf.create_dataset(  name = 'data',data = np.array(res).astype(np.float) ,dtype=np.float, compression="gzip", compression_opts=9)
                
                hf.close()


                
                
    
                print 'fin'
    
    
    
    
'''
                ax = sns.heatmap(np.array(results))

                fig = ax.get_figure()
                fig.savefig('./plots/%04d.png'%n)
    
    '''


'''
In [1]: import numpy as np

In [2]: import networkx as nx

In [3]: A=np.matrix([[1,2],[3,0]])

In [4]: G=nx.from_numpy_matrix(A,create_using=nx.MultiDiGraph())

In [5]: G.edges(data=True)
Out[5]: [(0, 0, {'weight': 1}), (0, 1, {'weight': 2}), (1, 0, {'weight': 3})]



'''
