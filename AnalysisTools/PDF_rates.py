import numpy as np
import pandas as pd
import sys,os,re,multiprocessing,netCDF4
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#netcdf file path
ncfile = sys.argv[1]
steadystate=False 
n_subplot = 5
netCDF_data = Dataset(ncfile, mode='r')
walltime=[]
global spc,group


#fractional difference, diurnal steady state
def ss (limit=1e-3):

    resample = (spc.resample('d',how='sum',axis=0,label='left'))
    fracdiff = (resample.diff().abs()/resample).sum(axis=1)    

    fracdiff=fracdiff/len(fracdiff) 
    fracdiff[1:-2].plot(ylim=[0,7e-3])
    plt.plot([limit]*2*len(fracdiff))
    plt.title(group)

    plt.savefig('%s_fracdiff.png'%group)
    
    print 'steady state'
    
    for i,j in enumerate(fracdiff):
        if j<limit: return [i, fracdiff.index[i]]
    return [0,0] # if none 




for group in netCDF_data.groups:
    plt.close('all') 
    walltime.append(pd.DataFrame([netCDF_data.groups[group].WALL_time], index = [group]))#for analysis of run times 
    
    print '\n\nReading', group
    #data
    spc = pd.DataFrame(netCDF_data.groups[group].variables['Rate'][:])
    spc.columns = str(netCDF_data.groups[group].variables['Rate'].head).split(',')
    spc.index = pd.to_datetime(spc.TIME, unit='s') 
    #rte = pd.DataFrame(netCDF_data.groups[group].variables['Rate'][:])
    #rte.columns = str(netCDF_data.groups[group].variables['Rate'].head).split(',')

    
    spc = spc.iloc[1:-1]#remove nan row
   
    M= spc['M'].mean()

   
    
    columns = spc.columns
    index = spc.index
    spc = pd.DataFrame( np.array(spc)/M )
    spc.index = index
    spc.columns = columns
    
    spc['M'] = M
 
    
    columns = []
    for i in spc.columns:
        if sum(spc[i])>0: columns.append(i) #only take those which have a concentration. 
    
    
    
    
    #columns = ['OH','NO','NO2','CO','CH4','CH3O2','CH3OOH','HCHO','CH3O']
    
    
    
    
    
    columns = sorted(list(set(columns)-set(['TIME','DUMMY'])))

    spc = spc[columns] 
    
    #spc.sort_index(axis=1,inplace=True)# arrange alphabetically

    if steadystate: vert = ss(1e-3)  

    pp = PdfPages('%s.pdf'%group)
    
    
    for i in xrange(0, len(columns), n_subplot+1):
        Axes = spc[columns[i:i+n_subplot]].plot(subplots=True)
        
        if steadystate: plt.axvline(vert[1], color='r', linestyle='-', linewidth=4 )

        plt.tick_params(labelsize=6)
        
        
        #y ticklabels
        [plt.setp(item.yaxis.get_majorticklabels(), 'size', 7) for item in Axes.ravel()]
        #x ticklabels
        [plt.setp(item.xaxis.get_majorticklabels(), 'size', 5) for item in Axes.ravel()]
        #y labels
        [plt.setp(item.yaxis.get_label(), 'size', 10) for item in Axes.ravel()]
        #x labels
        [plt.setp(item.xaxis.get_label(), 'size', 10) for item in Axes.ravel()]


        plt.tight_layout() 
        plt.ylabel('mix ratio')
        
        
        
        
        #plt.locator_params(axis='y',nbins=2)
        print '%.03f'%(float(i) / float(len(columns)) ) , '% done'  
  
        plt.savefig(pp, format='pdf')
        plt.close('all') 
               
    pp.close()
    print 'PDF out'
    plt.close('all') 


    
wall = pd.concat(walltime)[0]
wall.map(lambda x: x-min(wall)).plot().set_ylabel('seconds difference from the slowest (%s)'%min(wall))
plt.savefig('walltime.png')




