#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import h5py,re,dask,os,sys
import dask.array as da
import dask.dataframe as dd
import pandas as pd
import time
import progressbar
#from multiprocessing import Pool
#from memory_profiler import profile as mprof

from pathos.multiprocessing import Pool

#https://github.com/deepcharles/ruptures change point analysis


try:
    import matplotlib.pyplot as plt
    plt.ion()
except:
    'no plotting allowed'
try:
    ncores = int(os.popen('qstat -f $PBS_JOBID | grep resources.used.ncpus').read().split(' ')[-1])

except:
    ncores=1

#print 'multiprocessing on ' , ncores
pool = Pool(ncores)
###############################################



bar = progressbar.ProgressBar()

def timing(f):
    import time
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        #print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap



def mp (x,fn,pool):
    global ncores
    y = np.array_split(np.array(x), ncores)
    res = pool.map(fn,y)
    rt = []
    for i in res:
        rt.extend(i)
    return rt




###############################################







class new():
    #reads in a selected file
    def __init__(self,h5file,groupid=False):

        self.origin = h5file
        #if not os.path.isfile(h5file) : #print 'no file found'; return None
        #self.hf = h5py.File( h5file, 'r')
        with h5py.File(h5file,'r') as hf:
            groups = list(filter(lambda x: type(x[1])==h5py._hl.group.Group, hf.items()))
            self.groups = dict([[i[0],j] for j,i in enumerate(groups)])
            self.groupkeys = groups[0][1].attrs.keys()
            self.flux=False
            if groupid:
                g = groups[int(groupid)][1]
            else:
                g = groups[0][1]
            self.groupname = groups[0][0]
            self.wall= g.attrs['wall']



            shead = g.attrs['spechead'].decode('utf-8').split(',')
            rhead = g.attrs['ratehead'].decode('utf-8').split(',')
            fhead = g.attrs['fluxhead'].decode('utf-8').split(',')



            #self.fhd = g.attrs['ratehead'].split(',')
            spec = dd.from_array(g.get('spec')[1:,:],chunksize=50000, columns = shead)

            if len(rhead) != len(set(rhead)):
                #print 'Duplicates detected, please parse mecnahisms in future to prevent this'
                rate = pd.DataFrame(g.get('rate')[1:,:],columns=rhead)
                rate = rate.groupby(rate.columns, axis=1).sum()

                rhead = rate.columns
                rate = dd.from_pandas(rate,chunksize=50000)
            else:
                rate = dd.from_array(g.get('rate')[1:,:],chunksize=50000,columns = rhead)

            #print g.get('flux').shape
            #print len(fhead)

            if len(fhead) != len(set(fhead)):
                ##print 'Duplicates detected, please parse mecnahisms in future to prevent this'
                flux = pd.DataFrame(g.get('flux')[1:,:],columns=fhead)
                flux = flux.groupby(flux.columns, axis=1).sum()

                fhead = flux.columns
                flux = dd.from_pandas(flux,chunksize=50000)
            else:
                flux = dd.from_array(g.get('flux')[1:,:],chunksize=50000,columns = fhead)


            self.timesteps = spec['TIME'].astype('M8[s]').compute()
            spec['TIME'] = self.timesteps
            rate['TIME'] = self.timesteps
            flux['TIME'] = self.timesteps #dd.from_array(np.array(self.timesteps[1:]))
            self.ts= np.array(self.timesteps)
            '''
            n = int(len(shead)/5)
            #print n, 'partitions'
            spec.repartition(npartitions= n)
            '''

            spec = spec.set_index('TIME', sorted=True)
            self.M =  spec.M.mean()
            self.spec = spec/self.M
            self.rate = rate.set_index('TIME', sorted=True)
            self.flux = flux.set_index('TIME', sorted=True)

            fcol = ','.join(fhead)

            self.products = [i.split('+') for i in re.findall(r'-->([A-z0-9+]*)',fcol)]
            self.reactants = np.array([j.split('+') for j in re.findall(r'([A-z0-9+]{1,60})-->',fcol)])
            '''
            try:
                self.adj = np.array(g['adj'])
                self.adjspec = np.array(g.attrs['adjspec'].split(','))
                self.adjts= np.array(g.attrs['adjts'].split(','))
            except Exception as e:
                #print e,'no adjacency matrix data'
            '''


            hf.close()

            #check regex works
            #if (len(reactants) + len(products))/2 != len(rhead)-ratebuff : #print 'reactants and poducts differing lengths' , len(reactants) , len(products) , len(rhead)


            #shead.extend(['DUMMY','CL','CLO'])
            self.prodloss = {k: {'loss':[],'prod':[]} for k in shead}
            ### reaction prodloss arrays
            for idx in range(len(self.reactants)):
                for i in self.reactants[idx]:
                    try:self.prodloss[i]['loss'].append(idx)
                    except:None
                for i in self.products[idx]:
                    try:self.prodloss[i]['prod'].append(idx)
                    except:None



    #def openhf(self):
        #self.hf =  h5py.File( h5file, 'r')
    #def closehf(self):
        #self.hf.close()
        #self.hf=False





    def splot (self,what):
        df = pd.DataFrame((self.spec[what]).compute()).plot()
        plt.show()
        return df

    def fplot (self,what):
        df = pd.DataFrame(self.flux[what].compute()).plot()
        plt.show()
        return df

    def rplot (self,what):
        df = pd.DataFrame(self.rate[what].compute()).plot()
        plt.show()
        return df


    def loss(self,spec):
        return self.flux.columns[self.prodloss[spec]['loss']]

    def prod(self,spec):
        return self.flux.columns[self.prodloss[spec]['prod']]

    '''
    def halflife(self,spec,starttime):
            rxns = self.loss(spec)
            coeff = re.compile(r'([\.\d]*)(\w+)')
            life = 0.

            def calc(r):
                calc = 1.
                for spc in r.split('-->')[0].split('+'):
                    splt = coeff.match(spc).groups()
                    if splt[1] != spec:
                        if splt[0] != '': calc *= float(splt[0])
                        calc *= self.spec.loc[starttime,spec]
                try:
                    return 1./(calc*self.rate.loc[starttime,r])

                except KeyError:
                    # removed rate col based on no-reaction
                    #print 'Skipped '+r
                    return 0

            res = pool.map(calc,rxns)
            try:
                return (1. / sum(res)).compute()
            except:
                return 0
'''


    def ropa(self, spec, save = False, top=False, time = False, plot=True,net= False):

        pr = self.prod(spec)
        ls = self.loss(spec)

        if not time: time=self.ts

        prod = abs(self.flux.loc[time,pr]).compute()
        prod = prod[prod.mean().sort_values(ascending=True).index]

        loss = abs(self.flux.loc[time,ls]).compute()
        loss = loss[loss.mean().sort_values(ascending=True).index]


        if top:
            plt.close()
            prod=prod[prod.columns[-top:]]
            loss=loss[loss.columns[-top:]]


        if net:
            plot=False
            (prod.sum(axis=1)-loss.sum(axis=1)).plot(c='orange',legend=False)
            plt.ticklabel_format(style='sci', axis='y', scilimits=(-2,2))
            if save:
                plt.savefig(save)


        if plot:
            from matplotlib import colors
            from matplotlib import cm

            x = np.linspace( .9,.3, 256)
            red = colors.LinearSegmentedColormap.from_list('',cm.Reds(x))
            blue = colors.LinearSegmentedColormap.from_list('',cm.Blues(x))

            plt.close()
            plt.style.use('seaborn-darkgrid')
            fig = plt.figure(1)
            ax0=plt.subplot(211)
            try:prod.plot.area(colormap=red,legend=False,ax=ax0, alpha=.7,stacked=True)
            except:None
            #ax.xlabel('')
            ax0.tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                labelbottom=False)
            ax0.ticklabel_format(style='sci', axis='y', scilimits=(-2,2))

            ax = plt.subplot(212,sharex=ax0)
            try:loss.plot.area(colormap=blue,legend=False,ax=ax, alpha=.7,stacked=True)
            except:None
            ax.axes.invert_yaxis()
            plt.figlegend()
            ax.ticklabel_format(style='sci', axis='y', scilimits=(-2,2))

            plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.001)

            if save:
                fig.savefig(save)
        return {'prod':prod,'loss':loss}


    def lifetime(self,spec,timestep=''):
            '''
            a + b + c > d     @ r1
            a         > f + h @ r2

            tau_A = 1/(   1/[c][d]r1   + 1/r2      )


            timestep: [NoneType=diurnalprofile, Timestring=point, default=return all, str=data]
            '''
            '''
            for prod in self.prod(spec):

                            try:
                                lifetimev-= self.flux[prod]
                            except NameError:
                                lifetimev  = -1.*self.flux[prod]

                                '''
            for loss in self.loss(spec):

                try:
                    lifetimev+= self.flux[loss]
                except NameError:
                    lifetimev  = self.flux[loss]
            if 'lifetimev' in locals() :

                tau = lifetimev/self.spec[spec]

                timetype = type(timestep).__name__

                if timetype == 'str':
                    rtn = tau.describe().compute()
                elif timetype == 'bool':
                    rtn = tau
                elif timetype == 'pandas._libs.tslib.Timestamp':
                    rtn = tau.loc[timestep].compute()[0]
                elif timetype == 'list':
                    rtn = tau.loc[timestep[0]:timestep[1]].compute()
                else:
                    rtn =tau.groupby(tau.index.map_partitions(lambda x: x.hour)).mean().compute()

                return rtn


    def dump(self,location = './', name = False):
        if not name: name = self.origin.replace('.h5','')  + self.groupname+'.dill'
        import dill


        try:self.closehf()
        except: None
        dill.dump(self,open(location+name,'wb'))
        #print 'saved'


#############################################################
## other functions
#############################################################
def loaddump(filename):
    import dill
    return dill.load(open(filename))



def mechcomp(mechs,what='spec',n_subplot = 4):
        if type(mechs) != type([]):mechs = [mechs]

        #print 'creating a comparison pdf of '+what
        from matplotlib.backends.backend_pdf import PdfPages
        from matplotlib.pyplot import tick_params,setp,tight_layout,ylabel,xlabel,savefig,close
        import progressbar

        bar = progressbar.ProgressBar()

        linestyles = ['-', ':', '--', '-.']
        data = []
        for i in mechs:
            exec('data.append(i.%s.compute())'%what)

        #data.sort_index(axis=1,inplace=True)# arrange alphabetically
        crossover = set(data[0])
        for i in data[1:]:
            crossover = crossover & set(list(i.columns))
        crossover = sorted(list(set(crossover)))
        #print crossover,data

        pp = PdfPages('compare_%s.pdf'%('_'.join([i.groupname for i in mechs])))

        for i in bar(range(0, len(crossover), n_subplot+1)):
            spselect = crossover[i:i+n_subplot]

            Axes = data[0][spselect].plot(subplots=True)
            for l,d in enumerate(data[1:]):
                d[spselect].plot(ax = Axes,linestyle = linestyles[-1*(l+1)],alpha =.8 , subplots=True)

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

            savefig(pp, format='pdf')
            close('all')

        pp.close()
        #print 'PDF out'
        close('all')



def pdiff(base,lump,what='spec',n_subplot = 4):


        #print 'creating a comparison pdf of '+what
        from matplotlib.backends.backend_pdf import PdfPages
        from matplotlib.pyplot import tick_params,setp,tight_layout,ylabel,xlabel,savefig,close
        import progressbar

        bar = progressbar.ProgressBar()

        linestyles = ['-', ':', '--', '-.']
        data = []
        for i in [base,lump]:
            exec('data.append(i.%s.compute())'%what)






        #data.sort_index(axis=1,inplace=True)# arrange alphabetically



        crossover = set(data[0])

        crossover = crossover & set(list(data[1].columns))

        crossover = sorted(list(set(crossover)))
        #print crossover,data


        pp = PdfPages('pdiff_%s.pdf'%('_'.join([i.groupname for i in [base,lump]])))

        for i in bar(range(0, len(crossover), n_subplot+1)):
            spselect = crossover[i:i+n_subplot]

            df = 100*(data[1][spselect]/data[0][spselect])
            Axes = df.plot(subplots=True)


            #data[0][spselect].plot(subplots=True)

            #for l,d in enumerate(data[1]):
                #d[spselect].plot(ax = Axes,linestyle = linestyles[-1*(l+1)],alpha =.8 , subplots=True)



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

            savefig(pp, format='pdf')
            close('all')

        pp.close()
        #print 'PDF out'
        close('all')






def alllifetimes(self):
    #print 'Calculating lifetimes for all species...'
    mcm = list(pd.read_csv('src/background/smiles_mined.csv').name)

    cs = [i.split(',')[-1].replace('\n','') for i in tuple(open('carbons.csv'))]
    cs.extend('RO2')
    allspecs = filter(lambda x: x not in ['LAT', 'PRESS', 'TEMP', 'H2O', 'M','NA', 'O1D', 'R','O'],self.spec.columns)
    allspecs = filter(lambda x: x in cs,allspecs)


    return dict([[i,self.lifetime(i)] for i in allspecs])#pool.map(self.lifetime,self.spec.columns)

    #[[f,l[f]['mean']] for f in l if type(l[f]).__name__!='NoneType'] a.timesteps[int(144*1.84)]


def lumpdiagnostics(original,lumped,filename= 'lump.mech'):

    exec(''.join(tuple(open(filename))).replace('\n',';\n'))
    ts=original.ts
    #lumplist, lumpcoeff
    #print len(lumplist)
    for i,lump in enumerate(lumplist):
         ax = original.spec.loc[ts,lump].compute().plot.area(alpha=0.2)
         lumped.spec.loc[ts,'LMP%d'%(i+1)].compute().plot(ax = ax,c= 'blue',style='^-')
         #print i+1,lumped.spec.loc[ts,'LMP%d'%(i+1)].compute().mean(), original.spec.loc[ts,lump].compute().mean().sum()

         breakme = raw_input('enter for next')
         if breakme=='break':break
         plt.clf()




#All groups

def plotall(self,spec):
    '''
    plots a species from all groups run
    '''
    data = []

    for e in self.groups.values():
         b = new(self.origin,groupid=e)
         data.append(np.array(b.spec[spec].compute()))

    return pd.DataFrame(data).T.plot()




#
if __name__ == "__main__":
    #4a=new('lhs.h5')
    q =3
    #a = new('BaseRun_init_0406.h5')
    #a.ropa('HONO')
'''
a = new()
a.calcFlux(specs=['CH4'],timesteps=[i for i in range(18)])
#print  'finished A'
iup

b = new()
b.calcFlux(specs=['CH4'],timesteps=[i for i in range(11)])
#print b



l=alllifetimes(a)
v=[[f,l[f]['mean']] for f in l if type(l[f]).__name__!='NoneType']
df  =  pd.DataFrame(np.array(v)).set_index(0).astype(float)
df[1]= [np.log10(d) for d in df[1]]
df.T.to_csv('lifetimes.csv', index = False)
df = df.sort_values(1)
df.plot()


'''
