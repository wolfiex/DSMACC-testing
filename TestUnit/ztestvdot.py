'''
ignore 

import sys
file = sys.argv[1]
from zhdf import *
import numpy as np
a = new(file)

print '---------'




for row in np.random.randint(len(a.rate.columns), size=4):
    specscol = a.rate.columns[row]
    specs = specscol.split('-->')[0]
    specs = specs.split('+')
    dt = a.rate.index.compute()[11]
    conc = a.rate.loc[dt,specscol]
    print float(conc.compute()), 'rate'
    for i in specs:
        try:
            int(specscol[0])
            conc = 0
        except:
            conc *= (a.spec[dt,i]*a.M)
            print float((a.spec[dt,i]*a.M).compute()),i

    print specscol,row
    print 'flux',float(a.flux[a.rate.index.compute()[11],specscol].compute()),'ropa',float(conc.compute())

    print 'diff' , float((a.flux[dt,specscol] - conc).compute())
    print '-------------------------'

    #print a.flux[specscol].compute()

if 1==1:
    spc = a.vdot.columns[row]
    
    cols = []
    for c in a.jacsp.columns:
         try:
             v = c.split('->')
             if spc in v:
                 cols.append(c)
             
         except:None
        
    
    
    
    specs = specscol.split('-->')[0]
    specs = specs.split('+')
    dt = a.rate.index.compute()[11]
    conc = a.rate.loc[dt,specscol]
    print float(conc.compute()), 'rate'
    for i in specs:
        try:
            int(specscol[0])
            conc = 0
        except:
            conc *= (a.spec[dt,i]*a.M)
            print float((a.spec[dt,i]*a.M).compute()),i

    print specscol,row
    print 'flux',float(a.flux[a.rate.index.compute()[11],specscol].compute()),'ropa',float(conc.compute())

    print 'diff' , float((a.flux[dt,specscol] - conc).compute())
    print '-------------------------'
    
    '''

    #print a.flux[specscol].compute()