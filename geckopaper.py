import pandas as pd
import numpy as np
import netCDF4
from netCDF4 import Dataset
import glob,sys,os
from matplotlib.pyplot import *
import matplotlib.image as image

myfile = sys.argv[1]

nc = Dataset(myfile,'r')
print nc.date, '\n', nc.description,'\n'

class spec(object):
    '''A descriptor for the plot sizes'''
    def __init__(self,name,ymin,ymax):
        self.name = name
        self.ymin = ymin
        self.ymax = ymax


plots = [ spec('O3',30,100),spec('OH',0,0.0002),spec('HO2',0,0.0020),spec('HNO3',0,7),spec('NC7H16',0,25),spec('HCHO',0,3),spec('MGLYOX',0,0.8)]
groups = tuple(nc.groups)




for i in plots:
    
    im = image.imread('./geckoplots/%s.png'%i.name)
    imshow(im, aspect='auto', extent=(0, 430, i.ymin, i.ymax), zorder=-1, cmap=cm.gray)
    title(i.name)
    for g in groups:
    
            specs = pd.DataFrame(nc.groups[g].variables['Spec'][:])
            specs.columns = nc.groups[g].variables['Spec'].head.split(',')

            #rates = pd.DataFrame(nc.groups[g].variables['Rate'][:])
            #rates.columns = nc.groups[g].variables['Rate'].head.split(',')[:-2]

            
            a = specs[i.name]/specs.M
            a = a.map(lambda x : float(x)/1e-9 ) 
            
            
            a.plot(linewidth=2,label = g)




    legend(loc='UL')
    savefig('geckoplots/mixed_%s.png'%i.name)
    print 'Saved:', i.name
    close()
    
    
# for the nox    
im = image.imread('./geckoplots/nox.png')
imshow(im, aspect='auto', extent=(0, 430, 1e-1, 1e1), zorder=-1, cmap=cm.gray)
title('NOx')
for g in groups:
    
            specs = pd.DataFrame(nc.groups[g].variables['Spec'][:])
            specs.columns = nc.groups[g].variables['Spec'].head.split(',')

            #rates = pd.DataFrame(nc.groups[g].variables['Rate'][:])
            #rates.columns = nc.groups[g].variables['Rate'].head.split(',')[:-2]

            
            a = specs.NO
            b = specs.NO2
            c=a+b
            c= c/specs.M
            c = c.map(lambda x : float(x)/1e-9 ) 
            
            
            c.plot(linewidth=2,label = g)




legend(loc='UL')
savefig('geckoplots/mixed_nox.png')
print 'Saved:', 'nox'

    
nc.close()
