print 'loading libraries'
import pandas as pd
import numpy as np
import netCDF4
from netCDF4 import Dataset
import glob,sys,os,re
from matplotlib.pyplot import *
from copy import copy

class new():
    #reads in a selected file
    def __init__(self,filename='',groupid=None):
        self.flux=False
        if filename=='': 
            file_list = glob.glob('*.nc')
            file_list.sort(key=os.path.getctime) #getmtime - modified getctime-created
            print 'Select file to open: \n'
            for i,f in enumerate(file_list): print i , ' - ', f
            filename = file_list[int(input('Enter Number \n'))]
        nc = Dataset(filename,'r')
        self.filename = filename
        self.date = nc.date
        self.description = nc.description

  
        if len(nc.groups) > 1: 
            if groupid==None:
                print 'Select Simulation: \n\n'
                for i,g in enumerate(nc.groups): print i , ' - ', g
                groupid=int(input('Enter Number \n'))
        else:
            groupid=0
        
                    
        self.group = tuple(nc.groups)[groupid]
        self.wall = nc.groups[self.group].WALL_time
        print self.group, 'took', self.wall, 'seconds to compute.'


        rates = pd.DataFrame(nc.groups[self.group].variables['Rate'][:])
        rates.columns = nc.groups[self.group].variables['Rate'].head.split(',')[:]
             
        specs = pd.DataFrame(nc.groups[self.group].variables['Spec'][:])
        specs.columns = nc.groups[self.group].variables['Spec'].head.split(',')
        
        self.M = specs.M.mean()
        
        specs.index = pd.to_datetime(specs.TIME, unit='s') 
        rates.index = pd.to_datetime(specs.TIME, unit='s') 

        specs = specs.ix[1:]
        rates = rates.ix[1:]
        
        self.params = specs[specs.columns[:7]].describe().ix[['mean','std']]
        specs = specs[specs.columns[7:]]
        rates = rates[rates.columns[6:]]

        
       
        hasconc = specs.sum()>0   
        self.noconc = specs.columns[hasconc==False]  
        specs=specs[specs.columns[hasconc]]
        
        
        hasrate = rates.sum()>0        
        self.norate = rates.columns[hasrate==False]       
        rates=rates[rates.columns[hasrate]] 
   
        specs = specs/(self.M)
                   
        self.specs = specs
        self.rates = rates
        
        self.snames = specs.columns
        self.rnames = rates.columns
        
        
    def plot(self,cols,what='specs', **kwargs):
        exec('data = self.%s'%what)
        data[cols].plot()
        ylabel('mixing ratio')
        legend()
        show()
        
        
        
         
    def pdfdiagnostics(self,what='specs',n_subplot = 5):
        print 'creating a diagnostic pdf of '+what
        from matplotlib.backends.backend_pdf import PdfPages
        exec('data = self.%s'%what)

        data.sort_index(axis=1,inplace=True)# arrange alphabetically
        pp = PdfPages('%s.pdf'%self.group)
        
        for i in xrange(0, len(data.columns), n_subplot+1):
            Axes = data[data.columns[i:i+n_subplot]].plot(subplots=True)  
            tick_params(labelsize=6)

            #y ticklabels
            [setp(item.yaxis.get_majorticklabels(), 'size', 7) for item in Axes.ravel()]
            #x ticklabels
            [setp(item.xaxis.get_majorticklabels(), 'size', 5) for item in Axes.ravel()]
            #y labels
            [setp(item.yaxis.get_label(), 'size', 10) for item in Axes.ravel()]
            #x labels
            [setp(item.xaxis.get_label(), 'size', 10) for item in Axes.ravel()]

            tight_layout() 
            ylabel('mix ratio')

            #plt.locator_params(axis='y',nbins=2)
            print '%.03f'%(float(i) / float(len(data.columns)) ) , '% done'  
            savefig(pp, format='pdf')
            close('all') 
                            
        pp.close()
        print 'PDF out'
        close('all')     
        
    
    xlen = lambda self,x: xrange(len(x))
        
    def ropa(self):  
        print 'running the ropacode'
        
        '''reactants and products list'''
        rate_head = '\n'+'\n'.join(self.rates.columns)+'\n'
        self.products = [i.split('+') for i in re.findall(r'-->([A-z0-9+]*)',rate_head)]
        self.reactants = [j.split('+') for j in re.findall(r'\n([A-z0-9+]{1,60})[-->]{0,1}',rate_head)]


        #print rate_head
        if len(self.reactants) != len(self.products) : print 'reactants and poducts differing lengths'
                
                
        specs = self.specs*self.M         

        flux = []

        for i in self.xlen(self.reactants):
            rcol = []
            for j in self.reactants[i]:
                selection = re.sub(r'([\.\d\s]*)(\D[\d\D]*)', r'\2', j)
                if selection in self.noconc: dummy = 0 
                else: dummy = specs[selection]

                try: rcol.append( float(re.sub(r'([\.\d]*)\s*\D[\d\D]*', r'\1', j) * dummy ))
                except: rcol.append(dummy) # coeff = 1 if not yet specified

            prod = 1
            for k in rcol: prod *= k
            flux.append(prod * self.rates[self.rates.columns[i]])
                
        flux = np.array(np.array(flux).tolist()).T
        self.flux = flux
        
        
        
    def d3ropatool(self):
        print 'making an NCFILE for the online tool: \nwww-users.york.ac.uk/~dp626/MCMtools/dsmaccropa\n'
        if type(self.flux==bool): self.ropa()

        rate_head = '\n'+'\n'.join(self.rates.columns)+'\n'

        ''' Define spec locations '''
        locs2 = dict(enumerate(self.specs.columns[7:]))
        locs = {v: k for k, v in locs2.iteritems()}
        
        ''' get all species interaction '''
        def combine(ln): return  [[[re.sub(r'([\.\d\s]*)(\D[\d\D]*)', r'\2',r),re.sub(r'([\.\d\s]*)(\D[\d\D]*)', r'\2',p)],ln] for p in 
                self.products[ln] for r in self.reactants[ln]]

        dummy = np.vectorize(combine)(self.xlen(self.reactants))
        edges = [] ; [edges.extend(i) for i in dummy] ; edges.sort() #because why not 

        ''' 2 extract non duplicated list of reactions '''
        individual = list(set(frozenset(i[0]) for i in edges))



        ''' 4 Make a combination of these '''

        flux_data = []


        for i in individual:
            fp , fm =[],[]
            st = list(i)
            try:
                #if True:   
                d0, d1 = locs[st[0]],locs[st[1]]

                dummy  = [j for j in self.xlen(edges) if i == set(edges[j][0])]   
                for k in dummy:
                    edge = edges[k]

                    if st[0] == edge[0][0]: fp.append(edge[1])
                    else:                   fm.append(edge[1])

                flux_data.append([[fp,fm] ,d0,d1])
            except IndexError as e: print e, st # if self reaction
            except KeyError as e : print 'no concentration for', e  #no specie concentration 


        flux_data = np.array(flux_data)

        #ncdf info 
        combinations = str(list(flux_data[:,0]))
        src = np.array(flux_data[:,1])
        tar = np.array(flux_data[:,2])

        times =  np.array(self.specs.index).astype(int)

        #rateheaders = [x.strip() for x in rate_head.split('\n') if x.strip()]
        #rates = np.array([i.split('-->') for i in rateheaders])

        rate_head = '[' + rate_head.replace('\n','","').replace('-->','>')[2:-2] +']'
        locs_json = str(locs).replace("u'",'"').replace("\'",'"') 
        conc = np.array(self.specs[self.specs.columns])

        nrows = conc.shape[0]
        info_file = Dataset('ropa_'+self.filename, 'w', format='NETCDF3_CLASSIC')

        info_file.createDimension('time', nrows)
        info_file.createDimension('specs', conc.shape[1])
        info_file.createDimension('fluxes', self.flux.shape[1])
        info_file.createDimension('sourcetarget', len(src))
        info_file.createDimension('dict', len(locs_json))
        info_file.createDimension('comb', len(combinations))
        info_file.createDimension('timestr', len(times))
        info_file.createDimension('rateheader', len(rate_head))

        cnc  = info_file.createVariable('concentration', 'f8', ('time', 'specs'))
        cnc[:,:] = conc
        flx  = info_file.createVariable('edge-length', 'f8', ('time', 'fluxes'))
        flx[:,:] = self.flux
        rt  = info_file.createVariable('rate', 'c', 'rateheader')
        rt[:] = rate_head
        sources  = info_file.createVariable('source', 'i4', 'sourcetarget')
        sources[:] = src
        targets  = info_file.createVariable('target', 'i4', 'sourcetarget')
        targets[:] = tar
        dictn  = info_file.createVariable('nodes', 'c', 'dict')
        dictn[:] = locs_json
        comb  = info_file.createVariable('combinations', 'c', 'comb')
        comb[:] = combinations
        stime  = info_file.createVariable('timeseconds', 'f8', 'time')
        stime[:] = times
        info_file.close()
        print 'nc write'        
        
        

    def symdiff(self, other ,what='specs'):
        '''
        Return elements which exist in only one sett
        '''    
        exec('data = self.%s'%what)
        exec('data1 = other.%s'%what)
        
        return set(data.columns) ^ set(data.columns)
        
    def intersect(self, other ,what='specs'):
            '''
            Return elements which exists in both sets
            '''    
            exec('data = self.%s'%what)
            exec('data1 = other.%s'%what)
            
            return set(data.columns) & set(data.columns)
            
        
        
""" multiclass"""

def geos2mcm(x):

    dictionary = {
    'HNO2':'HONO',
    'ISOP':'C5H8',
    'HAC':'ACETOL',
    'INPN':'NISPOOH',
    'ISN1':'NC4CHO',
    'ISNOOA':'NC4CO3'
    }
    
    try: y = dictionary[x]
    except: y=x
    return y
    
    

def mechcomp (mechanisms,species = None,n_subplot = 5, parsenames = False,log=False, ppb = True):
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib import patches
    df = pd.DataFrame()
    style.use('ggplot')
    
    leg = []
        
    linetypes = ['solid','dashed','dotted','dashdot']
    
    if len(mechanisms) > len(linetypes): 
        print 'Number of mechanisms must be less than' + len(linetypes)
        return None


    
    for n,cls in enumerate(mechanisms):
        i = copy(cls); mechanisms[n] = i #make a copy so that we dont overwrite the original 
        
        if ppb: i.specs = i.specs*1e9
        
        i.specs['id'] = i.filename
        
        if parsenames: i.specs.columns = [geos2mcm(k) for k in i.specs.columns]
        
        if (len(i.specs.columns) != len(set(i.specs.columns))) : 
            print 'duplicate columns detected in '+ i.filename+i.group +'+ , collapsing these through summation'
            i.specs= i.specs.groupby(i.specs.columns,axis=1).sum()
            
        df = pd.concat([df,i.specs])
        leg.append(patches.Patch(label = i.filename,ls = linetypes[n],capstyle = 'round',lw=0.01,color = 'grey',fill=False,clip_on = True,aa=True))
        
    df.dropna(axis = 1 , inplace=True)     
    df.sort_index(axis=1,inplace=True)# arrange alphabetically
    pp = PdfPages('compare.pdf')
        

        
    for sbplt in xrange(0, len(df.columns), n_subplot+1):
            
            cols = list(set(df.columns)^set(['id']))[sbplt:sbplt+n_subplot]
            for n,c in enumerate(mechanisms):  
                if n > 0 :
                    ax = df.loc[df.id == c.filename][cols].plot(ax=ax , linestyle = linetypes[n],legend = False,logy=log, subplots = True)
                else: 
                    ax = df.loc[df.id == c.filename][cols].plot(subplots = True, legend = False, logy=log,title = [ i for i  in cols],fontsize=10)
            
            Axes = ax
            tick_params(labelsize=6)

            #y ticklabels
            [setp(item.yaxis.get_majorticklabels(), 'size', 5) for item in Axes.ravel()]
            #x ticklabels
            [setp(item.xaxis.get_majorticklabels(), 'size', 5) for item in Axes.ravel()]
            #y labels
            [setp(item.yaxis.get_label(), 'size', 10) for item in Axes.ravel()]
            #x labels
            [setp(item.xaxis.get_label(), 'size', 10) for item in Axes.ravel()]

            

            #titles 

           
            if ppb:ylabel('ppbV')
            else:ylabel('mix ratio')
            
            
            legend(handles = leg, loc='lower right',bbox_to_anchor = (0,0,1,1),bbox_transform = gcf().transFigure,fontsize = 5,fancybox=True,handlelength = 3 )
            tight_layout()
            
            #aha.dsju(3)
            print '%.03f'%(float(sbplt) / float(len(df.columns)) ) , '% done'  
            savefig(pp, format='pdf')
            close('all') 
                            
    pp.close()
    print 'PDF out'
    close('all')     
        
        

    


    show()
    
    ##return df 
        
    
    
        
print 'ready'            


