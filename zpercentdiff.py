# -*- coding: utf-8 -*-


from zhdf import *
import multiprocessing as mp
import numpy as np

bg = new('lhs.h5')
lm = new('lhslump.h5')
names = list(set(bg.spec.columns) & set(lm.spec.columns))
names.sort()

ids = dict([[j,i] for i,j in enumerate(names)])
groups = len(bg.groups)


p = open('percent.csv','w')
p.write('specfract,adiff,pdiff,hour,base,group,id\n')
    


for gid in xrange(groups):

    print float(gid)/groups

    base = new('lhs.h5',groupid=gid)
    flux = base.spec.compute()
    flux['group']= [str(i).split(':')[0] for i in base.timesteps]
    flux = flux.groupby(by='group').mean()
    flux['hour'] = [int(i.split(' ')[-1]) for i in flux.index]
    base = flux[flux['hour'].apply(lambda x: x in range(24))]
    base = base.groupby(['hour']).mean()
    base = base.loc[:,names].values
    
    
    other = new('lhslump.h5',groupid=gid)
    flux = other.spec.compute()
    flux['group']= [str(i).split(':')[0] for i in other.timesteps]
    flux = flux.groupby(by='group').mean()
    flux['hour'] = [int(i.split(' ')[-1]) for i in flux.index]
    other = flux[flux['hour'].apply(lambda x: x in range(24))]
    other = other.groupby(['hour']).mean()
    other=other.loc[:,names].values
    
    
    v = abs(np.log10(base) - np.log10(other))
    m = abs(v/np.log10(base))
    
    b = np.log10(base)
    
    for row in xrange(len(v)):
        for s,d in enumerate(v[row]):
            if d<50 :
                p.write('%s,%s,%s,%s,%s,%s,%s\n'%(float(s)/len(names),d,m[row][s],row+1,b[row][s],gid,names[s]))

                
                
p.close()
