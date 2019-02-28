import numpy as np
np.warnings.filterwarnings('ignore')
import h5py,re,dask,os,sys
import dask.array as da
import dask.dataframe as dd
import pandas as pd
from zgraph import *
#from multiprocessing import Pool
#from memory_profiler import profile as mprof

from pathos.multiprocessing import Pool
try:
    import matplotlib.pyplot as plt
    plt.ion()
except:
    'no plotting allowed'
try:
    ncores = int(os.popen('qstat -f $PBS_JOBID | grep resources.used.ncpus').read().split(' ')[-1])
except:
    ncores=1

print 'multiprocessing on ' , ncores
#pool = Pool(ncores)
###############################################

import time
import progressbar

bar = progressbar.ProgressBar()

def timing(f):
    import time
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap



def mp (x,fn,pool):
    global ncores
    y = np.array_split(np.array(x), ncores)
    res = pool.map(fn,y)
    rt = []
    for i in res:
        rt.extend(i)
    return

inorganics = ['O', 'O1D', 'N2O5', 'HONO', 'HO2NO2', 'HSO3', 'H', 'O2', 'A', 'NA', 'SA','CO','OH','HO2','NO','NO2']
###############################################


class new():
    #reads in a selected file
    def __init__(self, h5file, groupid=False,selection = 'spec,rate,flux,vdot,jacsp'.split(','),
        prodloss = True,ts = 600):

        '''
        h5file     - filename
        groupid    - select a specific group entry
        selections - which data sections to provide in the class
        prodloss   - create rxn/ropa dictionaries

        '''

        self.origin = h5file
        self.selection = selection
        #if not os.path.isfile(h5file) : print 'no file found'; return None
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
            


            if True: # spec MUST always be included...
                #'spec' in selection:
                shead = g.attrs['spechead'].split(',')
                spec = dd.from_array(g.get('spec')[:,:],chunksize=50000, columns = shead)
                self.timesteps = spec['TIME'].compute().astype('M8[s]')



                self.ts= np.array(self.timesteps)
                spec['TIME'] = self.timesteps
                spec = spec.set_index('TIME', sorted=True)
                self.spinup= self.ts[int( (spec.SPINUP.max()/ts).compute() ) ]
                self.M =  spec.M.mean()
                self.spec = spec/self.M

                fhead = g.attrs['fluxhead'].split(',')




            if 'rate' in selection:
                rhead = g.attrs['ratehead'].split(',')
                if len(rhead) != len(set(rhead)):
                    print 'Duplicates detected, please parse mecnahisms in future to prevent this'
                    rate = pd.DataFrame(g.get('rate')[:,:],columns=rhead)
                    rate = rate.groupby(rate.columns, axis=1).sum()

                    rhead = rate.columns
                    rate = dd.from_pandas(rate,chunksize=50000)
                else:
                    rate = dd.from_array(g.get('rate')[:,:],chunksize=50000,columns = rhead)

                rate['TIME'] = self.timesteps
                self.rate = rate.set_index('TIME', sorted=True)




            if 'flux' in selection:

                if len(fhead) != len(set(fhead)):
                    #print 'Duplicates detected, please parse mecnahisms in future to prevent this'
                    flux = pd.DataFrame(g.get('flux')[:,:],columns=fhead)
                    flux = flux.groupby(flux.columns, axis=1).sum()

                    fhead = flux.columns
                    flux = dd.from_pandas(flux,chunksize=50000)
                else:
                    flux = dd.from_array(g.get('flux')[:,:],chunksize=50000,columns = fhead)
                flux['TIME'] = self.timesteps
                self.flux = flux.set_index('TIME', sorted=True)


            if 'vdot' in selection:
                vhead = g.attrs['vdothead'].split(',')
                vdot = dd.from_array(g.get('vdot')[:,:],chunksize=50000, columns = vhead)
                #vdot*=-1 # convert such that -ve values suggest flux leaving the species.
                vdot['TIME'] = self.timesteps
                self.vdot = vdot.set_index('TIME', sorted=True)


            if 'jacsp' in selection:
                jhead = g.attrs['jacsphead'].split(',')
                jacsp = dd.from_array(g.get('jacsp')[:,:],chunksize=50000, columns = jhead)
                jacsp['TIME'] = self.timesteps
                self.jacsp=jacsp.set_index('TIME', sorted=True)


            hf.close()


            if prodloss:
                fcol = ','.join(fhead)
                self.products = [i.split('+') for i in re.findall(r'-->([A-z0-9+]*)',fcol)]
                self.reactants = np.array([j.split('+') for j in re.findall(r'([A-z0-9+]{1,60})-->',fcol)])

                self.prodloss = {k: {'loss':[],'prod':[]} for k in shead}
                ### reaction prodloss arrays
                for idx in xrange(len(self.reactants)):
                    for i in self.reactants[idx]:
                        try:self.prodloss[i]['loss'].append(idx)
                        except:None
                    for i in self.products[idx]:
                        try:self.prodloss[i]['prod'].append(idx)
                        except:None


    def rm_spinup(self):
        '''
        Remove spinup calculations from arrays
        '''
        self.timesteps = self.timesteps[self.timesteps.gt(self.spinup)][2:]
        self.ts = np.array(self.timesteps)
        for d in self.selection:
            setattr(self,d, getattr (self,d).loc[self.ts,:])


    def jratio(self,row,column,log = True,signs = True):
        '''
        Find the ratio contribution of a species using the jacobian.
        source = column
        target = row (produced)
        '''
        if row == column:
            print 'same spec, skipping'
            return False

        def inc(x):
             x = x.split('->')
             return x[1] == row and x[0] != row

        jh = filter(inc, self.jacsp.columns )
        data = self.jacsp[jh].astype(float)
        data = np.abs(data[:])
        if log:
            data += 1
            data = np.log(data)


        by = '%s->%s'%(column,row)
        try:
            dummy = self.jacsp[by]
            if signs: signs = np.sign(dummy)
            else: signs = 1
        except: return False

        return data[by].divide(data.sum(axis=1)).replace([np.inf, -np.inf], 0)


    def plot (self, what, dataframe = 'spec',vbar=True ):
        '''
        Fast plotting function
        what - species / column header of interest
        dataframe - spec, rate, vdot, jacsp, flux (str)
        vbar - spinup bar
        '''
        df = pd.DataFrame((getattr (self,dataframe)[what]).compute()).plot()
        if vbar:
            plt.axvline(x=self.spinup,color='grey', ls='--')
        plt.show()
        return df


    def loss(self,spec):
        '''Returns loss reactions'''
        return self.flux.columns[self.prodloss[spec]['loss']]

    def prod(self,spec):
        '''Returns production reactions'''
        return self.flux.columns[self.prodloss[spec]['prod']]



    def ropa(self, spec, save = False, top=False, time = False, plot=True,net= False):
        '''
        Create a ropa timeseries
        '''

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



    def lifetime(self,spec,timestep='',loss=False):
            '''
            a + b + c > d     @ r1
            a         > f + h @ r2

            tau_A = 1/(   1/[c][d]r1   + 1/r2      )
            tau_A = 1/ (sum of fluxes out)


            returns log10 of flux


            timestep: [NoneType=diurnalprofile, Timestring=point, default=return all, str=data]
            '''
            '''
            for prod in self.prod(spec):

                            try:
                                lifetimev-= self.flux[prod]
                            except NameError:
                                lifetimev  = -1.*self.flux[prod]

                                '''

            tau = 1/self.vdot[spec]

            if loss:
                tau = tau[tau>0]

            return np.log10(tau)


    def dump(self,location = './', name = False):
        '''
        Save this new DSMACC class as a dill file.
        Useful if we need a fast loading dataset for a single run out of many.
        '''
        if not name: name = self.origin.replace('.h5','')  + self.groupname+'.dill'
        import dill

        try:self.closehf()
        except: None
        dill.dump(self,open(location+name,'wb'))
        print 'saved'


#############################################################
## other functions
#############################################################
def loaddump(filename):
    '''unpickle the dill file of a previous simulation'''
    import dill
    return dill.load(open(filename))


def group_hour(df,fn = np.mean,diurnal = False):
        try: df = df.compute()
        except:None


        df['group']= [str(i).split(':')[0] for i in df.index]
        df = df.groupby(by='group').agg(fn)
        if diurnal:
            day = range(24)
            hour = lambda x: x in range(24)
            df['hour'] = [int(i.split(' ')[-1]) for i in df.index]
            df = df[df['hour'].apply(hour)]
            df = df.groupby(['hour']).agg(fn)
        return df

def connectivity(self,groups,ignore = [''],plot = False):
    '''
    custom implementation of the connectivity method
    self = dsmacc.new class object
    groups - list of important species

    todict = dict(connectivity(...))
    '''

    assert isinstance(groups,list), 'groups should be a list, eg ["O3",...]'

    def contribution(i,self,groups):
        counter = 1
        for j in groups:
                try:
                    total += self.jratio(j,i,signs=False)
                    counter +=1

                except: total = self.jratio(j,i,signs=False)

        try: return [i,total.divide(counter)]
        except:return [i,False]


    rt = [contribution(k,self,groups) for k in set(self.vdot.columns)^set(ignore)]

    print rt
    rt = filter(lambda x: type(x[1])!=bool, rt)




    df = pd.concat((i[1] for i in rt), axis=1)
    df.columns =  (i[0] for i in rt)

    if plot:
        np.abs(df).plot(kind='area')


    return df





def mechcomp(mechs,what='spec',n_subplot = 4):
        '''Compare PDF diagnostic for two differnt runs/mechanisms'''
        if type(mechs) != type([]):mechs = [mechs]

        print 'creating a comparison pdf of '+what
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
        print crossover,data

        pp = PdfPages('compare_%s.pdf'%('_'.join([i.groupname for i in mechs])))

        for i in bar(xrange(0, len(crossover), n_subplot+1)):
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
        print 'PDF out'
        close('all')



def pdiff(base,lump,what='spec',n_subplot = 4):
        '''
        Calculate the percentage difference between two returns
        '''
        print 'creating a comparison pdf of '+what
        from matplotlib.backends.backend_pdf import PdfPages
        from matplotlib.pyplot import tick_params,setp,tight_layout,ylabel,xlabel,savefig,close
        import progressbar

        bar = progressbar.ProgressBar()

        linestyles = ['-', ':', '--', '-.']
        data = []
        for i in [base,lump]:
            exec('data.append(i.%s.compute())'%what)

        crossover = set(data[0])
        crossover = crossover & set(list(data[1].columns))
        crossover = sorted(list(set(crossover)))
        print crossover,data

        pp = PdfPages('pdiff_%s.pdf'%('_'.join([i.groupname for i in [base,lump]])))

        for i in bar(xrange(0, len(crossover), n_subplot+1)):
            spselect = crossover[i:i+n_subplot]

            df = 100*(data[1][spselect]/data[0][spselect])
            Axes = df.plot(subplots=True)

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
        print 'PDF out'
        close('all')





def lumpdiagnostics(original,lumped,filename= 'lump.mech'):
    exec(''.join(tuple(open(filename))).replace('\n',';\n'))
    ts=original.ts
    #lumplist, lumpcoeff
    print len(lumplist)
    for i,lump in enumerate(lumplist):
         ax = original.spec.loc[ts,lump].compute().plot.area(alpha=0.2)
         lumped.spec.loc[ts,'LMP%d'%(i+1)].compute().plot(ax = ax,c= 'blue',style='^-')
         print i+1,lumped.spec.loc[ts,'LMP%d'%(i+1)].compute().mean(), original.spec.loc[ts,lump].compute().mean().sum()

         breakme = raw_input('enter for next')
         if breakme=='break':break
         plt.clf()

def days_spinup(self):
    ''' print the number of days taken to spinup the model'''
    d = self.spinup - self.ts[0]
    print d
    return d

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



''' ondefault run, not import - testing mostly'''
if __name__ == "__main__":
    a=new('ethane.h5')
    a.rm_spinup()
    #connectivity(a,['O3'])
    q =3
    #  python -c "from zhdf import *;a=new('ethane.h5');a.plot('O3')"
    # k && python -m dsmacc.run -s -c -r && python -c "from zhdf import *;a=new('ethane.h5');a.plot('O3')"
