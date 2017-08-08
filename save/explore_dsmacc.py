print 'loading libraries'
import pandas as pd
import numpy as np
import netCDF4
from netCDF4 import Dataset
import glob,sys,os,re,multiprocessing
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
        self.icsstr = nc.initial_conditions_str



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



        specs = specs.iloc[1:]
        rates = rates.iloc[1:]

        specs.index = pd.to_datetime(specs.TIME, unit='s')
        rates.index = pd.to_datetime(specs.TIME, unit='s')



        self.params = specs[specs.columns[:7]].describe().loc[['mean','std']]
        specs = specs[specs.columns[7:]]
        rates = rates[rates.columns[6:]]



        hasconc = specs.sum()>0
        self.noconc = specs.columns[hasconc==False]
        specs=specs[specs.columns[hasconc]]


        hasrate = rates.sum()>0
        self.norate = rates.columns[hasrate==False]
        rates=rates[rates.columns[hasrate]]

        specs = specs/(self.M)

        if (len(specs.columns) != len(set(specs.columns))) :
            print 'duplicate columns detected in specs, collapsing these through summation'
            specs= specs.groupby(specs.columns,axis=1).sum()

        if (len(rates.columns) != len(set(specs.columns))) :
            print 'duplicate columns detected in rates , collapsing these through summation'
            rates=rates.groupby(rates.columns,axis=1).sum()


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

    def ics(self,latex=False,remake=''):
           if sys.version_info[0] <3: from StringIO import StringIO
           else: from io import StringIO
           df = pd.read_csv(StringIO(self.icsstr),sep=',',header=1)
           df.index= df.Species
           df.drop(['Index','Species'], axis = 1 , inplace=True)
           df = df[[i[0] not in ['x','X'] for i in df.index]]

           print df

           if latex:
               data = r'''
                \documentclass{article}
                \usepackage{booktabs}
                \begin{document}

                '''+ df.to_latex() + r'''

                \end{document}'''

               with open('latex_ics.tex','w') as f: f.write(data)
               os.system('pdflatex latex_ics.tex && rm *.aux *.log')
           if remake != '':
               with open(remake+'.csv' ,'w') as f : f.write(self.icsstr)

           return df

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
        rn = re.compile(r'([\.\d\s]*)(\D[\d\D]*)')
        ren2 = re.compile(r'([\.\d]*)\s*\D[\d\D]*')
        for i in self.xlen(self.reactants):
            rcol = []
            for j in self.reactants[i]:
                selection = rn.sub( r'\2', j)
                if selection in self.noconc: dummy = 0
                else: dummy = specs[selection]

                try: rcol.append( float(rn2.sub( r'\1', j) * dummy ))
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


    def reactswith(self,spec,d='all'):
        dirdict = {'all':re.compile(r'.*\b[\d\.]*'+spec+r'\b.*'),
            'reactants':re.compile(r'.*\b[\d\.]*'+spec+r'\b.*-->.*'),
            'products':re.compile(r'.*-->.*\b[\d\.]*'+spec+r'\b.*')}
        return filter(lambda x: dirdict[d].match(x),self.rnames)


    def symdiff(self, other ,what='specs'):
        '''
        Return elements which exist in only one sett
        '''
        exec('data = self.%s'%what)
        exec('data1 = other.%s'%what)

        return set(data.columns) ^ set(data1.columns)

    def printdiff(self, other ,what='specs'):
        '''
        Return elements which exist in only one sett
        '''
        exec('data = set(self.%s.columns)'%what)
        exec('data1 = set(other.%s.columns)'%what)

        print '\033[1;31,m',sorted(list(data -data1))
        print  '\033[0;0,m' ,sorted(list(data1-data))



    def intersect(self, other ,what='specs'):
            '''
            Return elements which exists in both sets
            '''
            exec('data = self.%s'%what)
            exec('data1 = other.%s'%what)

            return set(data.columns) & set(data.columns)


    def ropaplot(self,spec='OH',log=False, percent = 95, alpha = 0.8, stacked = True , plot = 'all'):
        if type(self.flux==bool): self.ropa()


        style.use('ggplot')

        rct = self.reactswith(spec,d='reactants')
        prd = self.reactswith(spec,d='products')

        rxn_list = list(self.rates.columns)

        '''rct or prd'''
        def getgroup(tpe):
            i_rxn = [rxn_list.index(i) for i in tpe]

            df = pd.DataFrame([self.flux[:,i] for i in i_rxn]).T
            df.index = self.specs.index
            df.columns = tpe

            #lets get a quantile based cut
            c=df.mean()
            c.sort_values()
            cut = pd.qcut(c, q=100,labels=False)

            main= c[cut>=percent].index
            other = c[cut<percent].index

            newdf = df[main].loc[:,:]
            newdf.loc[:,'total_others']=  df.loc[:,other].sum(axis = 1)
            return newdf



        rcdf = getgroup(rct)*-1
        prdf = getgroup(prd)

        if plot in ['stacked','all']:
            ax= rcdf.plot.area(cmap= get_cmap('YlOrRd'),alpha=alpha,stacked=stacked)
            prdf.plot.area(ax =ax, cmap= get_cmap('YlGnBu'), alpha=alpha,stacked=stacked)

            totalmax = max([abs(prdf.max().max()),rcdf.max().max()])
            ylim([-totalmax*1.1,totalmax*1])

            title('Flux comparison at %s percetile. Stacked:%s'%(percent,stacked))
            legend(loc='lower right',bbox_to_anchor = (0,0,1.4,0),bbox_transform = gcf().transFigure,fontsize = 5,fancybox=True )
            tight_layout()

        # line plit of stacked
        if plot in ['line','all']:
            ax= rcdf.plot(cmap= get_cmap('YlOrRd'),)
            prdf.plot(ax =ax, cmap= get_cmap('YlGnBu'), )

            title('Flux comparison at %s percetile. [Lineplot] '%(percent))
            legend(loc='lower right',bbox_to_anchor = (0,0,1.4,0),bbox_transform = gcf().transFigure,fontsize = 5,fancybox=True )
            tight_layout()

        if plot  in ['steadyflux','all']:


            p=prdf.resample('H').mean()
            r=rcdf.resample('H').mean()



            globmax = pd.DataFrame([p.max(axis=1),abs(r.min(axis=1))]).max()
            #globmin = pd.DataFrame(p.min(axis=1,(r*-1).min(axis=1)).min()

            def steadyflux(z,ax=False):
                z=z.apply(lambda x:x/globmax,raw=True)
                cols = z.columns
                z['hours'] = [i.strftime('%H') for i in z.index]
                z['day']= [i.strftime('%d') for i in z.index]
                z1= z.groupby(['day','hours'],as_index=True).sum()

                for i in set(z.day):
                    d =  z1.loc[i]
                    if ax!=False: d.plot(ax=ax,cmap= get_cmap('viridis_r'),legend=False)
                else:  d.plot(cmap= get_cmap('viridis_r'),legend=True)
                legend(loc='lower right',bbox_to_anchor = (0,0,1.4,0),bbox_transform = gcf().transFigure,fontsize = 5,fancybox=True )
                tight_layout()
                return ax

            from matplotlib import gridspec
            f=figure()
            gs = gridspec.GridSpec(2, 1, height_ratios=[2, 2])
            ax0 = subplot(gs[0])
            ax1 = subplot(gs[1], sharex = ax0)
            ax0 = steadyflux(p,ax0)
            ax1 = steadyflux(r,ax1)



            yticks = ax1.yaxis.get_major_ticks()
            yticks[-1].label1.set_visible(False)
            subplots_adjust(hspace=.01)
            legend(loc='lower right',bbox_to_anchor = (0,0,1.4,0),bbox_transform = gcf().transFigure,fontsize = 5,fancybox=True )

            tight_layout()

            show()
            ########

            clf()


        return [rcdf,prdf]

''' to i'''
def togephi(self,tmin = 1, tmax =144, edgelist = True):
        #pip install netwrokx --user`
        #use R and Igraph if possible!
        if type(self.flux)==bool: self.ropa()
        import networkx as nx
        #snames
        rn = re.compile(r'([\.\d\s]*)(\D[\d\D]*)')


        def getedges(iloc):
            print self,tmin,tmax,iloc
            weight = self.flux[tmin:tmax,iloc].mean()


            rxn = self.rnames[iloc].split('-->')
            res = []
            if weight>0:
                for i in rxn[0].split('+'):
                    for j in rxn[1].split('+'):

                        res.append([rn.sub(r'\2',i),rn.sub(r'\2',j),weight])

            return res

        matrix = [getedges(i) for i in xrange(len(self.rnames))]# multiprocessing.Pool(4).map(getedges,[1,2,3,4,5,6,7,8,9])
        matrix = [item for sublist in matrix for item in sublist]

        df = pd.DataFrame(matrix)

        df.groupby([0,1],as_index=False ).sum()

        G = nx.DiGraph()

        for i in df.iterrows():
            i=i[1]
            G.add_edge(i[0],i[1],weight=i[2])

        print df
#
        #degree = G.degree()
        #nolinks = [n for n in degree if degree[n] == 0]

        #only carbons
        for i in set(G.nodes())-set(pd.read_csv('carbons.csv').species):#|set(nolinks):
            G.remove_node(i)

        nodenames = G.nodes()

        mu = self.specs.iloc[tmin:tmax].mean()
        mu = np.log10(mu)
        mu += mu.min()
        mu /= mu.max()
        mu = mu[nodenames]

        nx.set_node_attributes(G, 'conc', dict(zip(mu.index,[float(i) for i in mu])))

        primaryHC = self.ics().index
        nx.set_node_attributes(G, 'primary', dict(zip(nodenames,[int(i in primaryHC ) for i in nodenames])))




        nx.write_gexf(G, "test.gexf")

        if edgelist: nx.write_edgelist(G,'test.edgelist',comments = '# ', data = ['weight'] )



        return G







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
            if cols == []:
                print 'no columns left, omitting'
                continue

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


if __name__ == '__main__':
    a = new()

print 'ready'
