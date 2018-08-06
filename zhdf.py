import numpy as np
np.warnings.filterwarnings('ignore')
import h5py,re,dask,os,sys
import dask.array as da
import dask.dataframe as dd
import pandas as pd
#from multiprocessing import Pool
#from memory_profiler import profile as mprof

from pathos.multiprocessing import Pool


print ''

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
pool = Pool(ncores)
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
    return rt




###############################################







class new():
    #reads in a selected file
    def __init__(self,h5file,groupid=None):

        self.origin = h5file
        #self.hf = h5py.File( h5file, 'r')
        with h5py.File(h5file) as hf:
            groups = list(filter(lambda x: type(x[1])==h5py._hl.group.Group, hf.items()))
            self.groupkeys = groups[0][1].attrs.keys()
            self.flux=False

            g = groups[0][1]
            self.groupname = groups[0][0]

            shead = g.attrs['spechead'].split(',')
            rhead = g.attrs['ratehead'].split(',')
            fhead = g.attrs['fluxhead'].split(',')
            self.fhd = g.attrs['ratehead'].split(',')
            spec = dd.from_array(g.get('spec')[1:,:],chunksize=50000, columns = shead)

            if len(rhead) != len(set(rhead)):
                print 'Duplicates detected, please parse mecnahisms in future to prevent this'
                rate = pd.DataFrame(g.get('rate')[1:,:],columns=rhead)
                rate = rate.groupby(rate.columns, axis=1).sum()

                rhead = rate.columns
                rate = dd.from_pandas(rate,chunksize=50000)
            else:
                rate = dd.from_array(g.get('rate')[1:,:],chunksize=50000,columns = rhead)

            print g.get('flux').shape
            print len(fhead)

            if len(fhead) != len(set(fhead)):
                #print 'Duplicates detected, please parse mecnahisms in future to prevent this'
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
            print n, 'partitions'
            spec.repartition(npartitions= n)
            '''

            spec = spec.set_index('TIME', sorted=True)
            self.M =  spec.M.mean()
            self.spec = spec/self.M
            self.rate = rate.set_index('TIME', sorted=True)
            self.flux = flux.set_index('TIME', sorted=True)

            fcol = ','.join(rhead)

            self.products = [i.split('+') for i in re.findall(r'-->([A-z0-9+]*)',fcol)]
            self.reactants = np.array([j.split('+') for j in re.findall(r'([A-z0-9+]{1,60})-->',fcol)])

            try:
                self.adj = np.array(g['adj'])
                self.adjspec = np.array(g.attrs['adjspec'].split(','))
                self.adjts= np.array(g.attrs['adjts'].split(','))
            except Exception as e:
                print e,'no adjacency matrix data'



            hf.close()

            #check regex works
            #if (len(reactants) + len(products))/2 != len(rhead)-ratebuff : print 'reactants and poducts differing lengths' , len(reactants) , len(products) , len(rhead)


            #shead.extend(['DUMMY','CL','CLO'])
            self.prodloss = {k: {'loss':[],'prod':[]} for k in shead}
            ### reaction prodloss arrays
            for idx in xrange(len(self.reactants)):
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
        return self.rate.columns[self.prodloss[spec]['loss']]

    def prod(self,spec):
        return self.rate.columns[self.prodloss[spec]['prod']]


    def dump(self,location = './', name = False):
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
    import dill
    return dill.load(open(filename))



def joyplot(self):
     df = pd.DataFrame((self.spec[what]/self.M).compute())
     import seaborn as sns









#
'''
a = new()
a.calcFlux(specs=['CH4'],timesteps=[i for i in range(18)])
print  'finished A'
iup

b = new()
b.calcFlux(specs=['CH4'],timesteps=[i for i in range(11)])
print b'''
