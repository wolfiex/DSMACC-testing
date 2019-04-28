from zhdf import new,loaddump,pool,ncores,da,progressbar,h5py
import numpy as np
import os
 
print ''

np.warnings.filterwarnings('ignore')





a = new('methane.h5')

print 'read the file'


#sepcies we want
what_specs  = np.array(list(set(a.spec.columns) & set([i.split(',')[1].strip() for i in tuple(open('carbons.csv'))])))

#timestep index
tsid = range(1,145,6)#[45,117]

tsps = a.ts[tsid]





def adj_matrix(spcz,prodloss,allspecs,flux,lents):
    ''' create adj matrix for graphing '''
    import numpy as np
    rows=[]
    for spc in spcz :
        
            inspec = set(prodloss[spc]['loss'])
            
            row = []
            for i in xrange(len(allspecs)):
                match = np.array(list( inspec & set(prodloss[allspecs[i]]['prod'])))
                
                if len(match)==0:
                    res= [0]*lents
                    row.append(res)
                else:
                    match = flux.columns[match]
                    res = np.array(flux.loc[:,match].sum(axis=1))
                    row.append(res)
                    
            rows.append(row)    
            #print np.array(row).shape
            
    return rows    
    
    
print 'Creating call'
flx =a.flux.loc[tsps,:].compute()


results = [pool.apply_async(adj_matrix, args=(x,a.prodloss,what_specs,flx,len(tsps),)) for x in np.array_split(what_specs,ncores)]
                
res = [] 
bar = progressbar.ProgressBar()  
print 'Calculating results'           
[res.extend(p.get()) for p in bar(results)]

res=np.array(res)

                
print res.shape    

with h5py.File( a.origin, 'a') as hf:
    g = hf[a.groupname]
    try:
        g.create_dataset('adj', data=res , chunks=True,maxshape=(None,None,None),dtype= np.float16)
    except Exception as e: 
        print 'IGNORE:',e 
        del  hf[a.groupname]['adj']
        g.create_dataset('adj', data=res , chunks=True,maxshape=res.shape)
    g.attrs['adjspec']  = ','.join(what_specs)
    g.attrs['adjts']  = ','.join(tsps.astype(str))




print 'killing session'
#os.system('/opt/pbs/bin/qdel $PBS_JOBID')  
    
