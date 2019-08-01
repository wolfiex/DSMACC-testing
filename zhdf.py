#reset modules loaded
import sys
if globals(  ).has_key('init_modules'):
    # second or subsequent run: remove all but initially loaded modules
    for m in sys.modules.keys(  ):
        if m not in init_modules:
            del(sys.modules[m])
else:
    # first run: find out which modules were initially loaded
    init_modules = sys.modules.keys(  )



import numpy as np
np.warnings.filterwarnings('ignore')
import h5py,re,dask,os,sys
import dask.array as da
import dask.dataframe as dd
import pandas as pd
from zgraph import *
from zmechdiagnostics import *
try: import matplotlib.pyplot as plt
except: print('unable to import matplotlib')
#from multiprocessing import Pool
#from memory_profiler import profile as mprof
'''
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

print ('multiprocessing on ' , ncores)
#pool = Pool(ncores)
'''
###############################################
'''

def timing(f):
    import time
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print ('%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0))
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
'''

def normalise(x):
    '''
    sets the smalles to 0 and the largest to 1
    '''
    x = x[:]#deepcopy error
    x -= min(x)
    x /= max(x)
    return x


inorganics = ['O', 'O1D', 'N2O5', 'HONO', 'HO2NO2', 'HSO3', 'H', 'O2', 'A', 'NA', 'SA','CO','OH','HO2','NO','NO2']
###############################################


class new():
    #reads in a selected file
    '''
    The DSMACC results group class.
    '''
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

            if type(groupid) == int:
                g = groups[groupid]
            elif type(groupid) == str:
                g = groups[self.groups[groupid]]
            else:
                g = groups[0]


            self.groupname = g[0]
            g = g[1]
            self.wall= g.attrs['wall']




            if True: # spec MUST always be included...
                #'spec' in selection:
                shead = g.attrs['spechead'].decode("utf-8").split(',')
                spec = dd.from_array(g.get('spec')[:,:],chunksize=50000, columns = shead)

                '''

                '''

                self.timesteps = spec['TIME'].compute().astype('M8[s]')

                self.s = spec
                #return None



                self.ts= np.array(self.timesteps)

                spec['TIME'] = self.timesteps
                spec = spec.set_index('TIME', sorted=True)

                self.spinup = self.ts[int( (spec.SPINUP.max()/ts).compute() ) ]
                self.M =  spec.M.mean()
                self.spec = spec/self.M

                fhead = g.attrs['fluxhead'].decode("utf-8").split(',')




            if 'rate' in selection:
                rhead = g.attrs['ratehead'].decode("utf-8").split(',')
                if len(rhead) != len(set(rhead)):
                    print ('Duplicates detected, please parse mecnahisms in future to prevent this')
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
                vhead = g.attrs['vdothead'].decode("utf-8").split(',')
                vdot = dd.from_array(g.get('vdot')[:,:],chunksize=50000, columns = vhead)
                #vdot*=-1 # convert such that -ve values suggest flux leaving the species.
                vdot['TIME'] = self.timesteps
                self.vdot = vdot.set_index('TIME', sorted=True)


            if 'jacsp' in selection:
                jhead = g.attrs['jacsphead'].decode("utf-8").split(',')
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
                for idx in range(len(self.reactants)):
                    for i in self.reactants[idx]:
                        try:self.prodloss[i]['loss'].append(idx)
                        except:None
                    for i in self.products[idx]:
                        try:self.prodloss[i]['prod'].append(idx)
                        except:None


    def inposjac(self,y):
        return self.posjac[filter(lambda x: y in x, self.posjac.columns)]


    def create_posjac(self):
        '''
        Replace our sparse jacobian with a positive variation (negative links are reversed)
        Self reactions are removed and non existant species are removed.

        Args:
            ignore - list of species to be ignored in posjac array (most commonly inorganics)
        '''
        print ('computing the posjac array')

        try:
            self.posjac
            print ('Posjac already exists, use "del <name>.posjac" to remove it')

        except:None

        #remove no existant species
        #rm = re.compile(r'\b%s\b'%'|'.join(set('->'.join(self.jacsp.columns).split('->'))-set(self.spec.columns)))
        #self.posjac = self.jacsp[filter(lambda x: not rm.search(x), self.jacsp.columns)]

        #self reactions and negatives


        contains = set(self.jacsp.columns)
        selfself = set(('%s->%s'%(i,i) for i in self.spec.columns))

        rxns = list(set(self.jacsp.columns) - selfself)

        self.posjac = dd.compute(self.jacsp[rxns])[0]

        rev = re.compile(r'(.+)->(.+)')
        #for each negative reaction
        for h in rxns:
            #our column
            dummy = self.posjac[h]
            #save static positive values - unchanged
            self.posjac[h] = dummy*(dummy>0).astype(float)

            #negative (reverse ) values only
            lt = dummy<0
            mx = np.array(dummy*(-lt.astype(float)))

            #reverse link
            hp = rev.sub(r'\2->\1',h)
            try:self.posjac[hp] = self.posjac[hp] + mx
            except:self.posjac[hp] = mx

        #remove emptys
        self.posjac = self.posjac[self.posjac.columns[(self.posjac!=0).sum().astype(bool)]]




    def rm_spinup(self):
        '''
        Remove spinup calculations from arrays
        '''
        self.timesteps = self.timesteps[self.timesteps.gt(self.spinup)][2:]
        self.ts = np.array(self.timesteps)
        for d in self.selection:
            setattr(self,d, getattr (self,d).loc[self.ts,:])
        self.timesteps = self.timesteps.reset_index()['TIME']

    def jratio(self,row,column,log = True,all = False):
        '''
        Find the ratio contribution of a species using the jacobian.
        source = column
        target = row (produced)

        log - takes the natural log
        all - returns the complete dataframe for production of target(row)
        '''
        if row == column:return False
        if not hasattr(self, 'posjac'):self.create_posjac()

        def inc(x):
             x = x.split('->')
             return x[1] == row and x[0] != row

        jh = filter(inc, self.posjac.columns )
        data = self.posjac[jh].astype(float)
        if log:data = np.log(data)
        if all:return data
        by = '%s->%s'%(column,row)

        try:return data[by].divide(data.sum(axis=1)).replace([np.inf, -np.inf], 0)
        except Exception as e:return False



    def plot (self, what, dataframe = 'spec',vbar=True ):
        '''
        Fast plotting function
        what - species / column header of interest
        dataframe - spec, rate, vdot, jacsp, flux (str)
        vbar - spinup bar
        '''
        import matplotlib.pyplot as plt
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
        import matplotlib.pyplot as plt
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
            plt.show()
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
        print ('saved')


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
    groups - a python list of important species

    todict = dict(connectivity(...))
    '''

    assert isinstance(groups,list), 'groups should be a list, eg ["O3",...]'
    if not hasattr(self, 'posjac'):self.create_posjac()

    match = re.compile(r'->(%s)\b'%('|'.join(groups)))
    denominator = set(filter(lambda x: match.search(x),self.posjac.columns))
    names = set(re.findall(r'\b([\w\d]+)->',' '.join(denominator)))
    numerator = set(['%s->%s'%(i,j) for i in names for j in groups]) & denominator

    #print (numerator, denominator,names)

    denom_sum = self.posjac[list(denominator)].sum(axis=1)

    pdiff = self.posjac[list(numerator)].divide(denom_sum,axis = 0)
    pdiff.columns = [i.split('->')[0] for i in pdiff.columns]

    return pdiff.groupby(pdiff.columns, axis=1).sum()



def jac_it(self,ts,begin = inorganics):


    self.create_posjac()
    begin = set(begin)
    addspecs = []


    for it in range(6):


        g = np.log10(connectivity(a,list(begin)).loc[ts,:]).replace([np.inf,-np.inf],np.nan).dropna().sort_values(ascending=False)
        '''
        detector = pydetect.MeanDetector()
        cpt = detector.detect(g)

        for j,i in enumerate(cpt):
            if i:break

        addspecs = cpt.index[:j]

        print addspecs
        '''


        lim = g[[i not in begin for i in g.index]].quantile(q=0.95, interpolation='nearest')
        new = set(g.index[g>lim].values)
        print (it, new-begin)
        begin = begin | new

        addspecs.append(normalise(g[list(begin)]).to_json())



    with open('connectivity.json','w') as f:
        for i,j in enumerate(addspecs):
            f.write('conn_%d = %s;\n'%(i,j))

    G = jgraph(self.posjac.loc[ts])

    with open('ch2.js','w') as f:
        vd = normalise(np.log10(a.vdot.compute().loc[ts,:]))
        print vd
        f.write('vdot = %s;\n'%(vd.to_json()))

        pr = normalise(pd.Series(nx.pagerank(G, alpha=0.85, personalization=None, max_iter=100, tol=1e-06, nstart=None, weight='weight', dangling=None)))
        f.write('pagerank = %s;\n'%(pr.to_json()))
        print pr

        cl = normalise(pd.Series(nx.closeness_centrality(G, u=None, distance='weight')))
        f.write('closeness = %s;\n'%(cl.to_json()))
        print cl

        bt = pd.Series(nx.betweenness_centrality(G, k=None, normalized=True, weight='weight', endpoints=False, seed=1))
        f.write('between = %s;\n'%(bt.to_json()))
        print bt

    return addspecs,g














def change_point(connect_df,pen = None,epsilon=None,nbkp=1):
    '''
    Change point analysis for either the connectivity method or graph metrics

least sq - l1 l2
rbf radial basis functions

    a.create_posjac()
    t = connectivity(a,inorganics,plot=2)
    r= np.log10(t[t.sum().sort_values(ascending = False).index])


 change_point(np.array(r).T[:,::50])

    '''
    import ruptures as rpt
    import matplotlib.pyplot as plt
    print('calculating change points')
    # detection
    signal = np.array(connect_df)
    algo = rpt.Binseg(model='rbf').fit(signal)#rpt.Binseg(model='l2', custom_cost=None, min_size=1, jump=1, params=None).fit(signal)
    result = algo.fit_predict(signal, n_bkps=nbkp)
    print (result)
    #algo.predict(pen=pen)

    # display
    rpt.display(signal, result, np.array(result)/2)
    plt.show()



def days_spinup(self):
    ''' print the number of days taken to spinup the model'''
    d = self.spinup - self.ts[0]
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


def error_graph (base, reduced, lumped = 'mechanisms/lumped_formatted_CRI_FULL_2.2_inorganics_True.kpp'):
    import re
    base = base.jacsp.compute()
    reduced = reduced.jacsp.compute()

    header = base.columns
    lumped = open(lumped).readlines()
    lumped = re.findall(r'(LMP\d+): ([\w,]+)',''.join(lumped))

    for n,l in lumped:

        sub = re.compile(r'\b(%s)\b'%(l.replace(',','|')))
        header = [sub.sub(n, x) for x in header]
        print l , header,l


    base.columns=header
    base = base.groupby(by=base.columns,axis=1).agg(np.sum)

    keep = set(base.columns) & set(reduced.columns)
    discard = set(base.columns) ^ set(reduced.columns)

    print( 'Ignoring:' ,discard)

    res = np.log10(reduced[keep]).divide(np.log10(base[keep]),axis=1)


    return res


def undirect(jsp):
    '''
    Remove directional links between species by finding the net weight of the jacobian
    '''

    dct={}
    specs = jsp.spec.columns
    for i in specs:
        for j in specs:
            total = []
            n = list(set([i,j]))

            try: total.append(jsp['%s->%s'%(n[0],n[1])])
            except:None
            try: total.append(-1*jsp['%s->%s'%(n[0],n[1])])
            except:None

            if len(total) >0 and i != j:
                dct['->'.join(n)] = sum(total).compute()

    return dct



''' ondefault run, not import - testing mostly'''
if __name__ == "__main__":
    #a=new('ethane.h5')
    #a.rm_spinup()
    #connectivity(a,['O3'])
    q =3
    #  python -c "from zhdf import *;a=new('ethane.h5');a.plot('O3')"
    # k && python -m dsmacc.run -s -c -r && python -c "from zhdf import *;a=new('ethane.h5');a.plot('O3')"
