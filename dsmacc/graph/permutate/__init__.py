'''
Dep.:
    networkx > 2

Change in assign attribute argument order.
this causes a hash error (unsurprisingly)

'''


import re
import pandas as pd
import numpy as np
from subset_extract import *
import networkx as nx

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)


fn = pd.read_csv('../../datatables/functionalgroups_regexmatched.csv')
fn.index = fn.name
fn = fn[[u'PAN', u'Carb. Acid', u'Ester', u'Ether',
       u'Per. Acid', u'Hydro peroxide', u'Nitrate', u'Aldehyde', u'Ketone',
       u'Alcohol', u'Criegee', u'Alkoxy rad', u'Peroxalkyl rad',
       u'Peroxyacyl rad', u'nogroups']].astype(int)


t = open('fullmcm.kpp').read().replace(' ','')
eqns = split_eqn(re.findall(r'\}([\w\d\+]+)=([\w\d\+]+):([^;]+)',t))

# primary vocs
vocs ='CH4,C2H6,CH3OH,C2H5OH,NPROPOL,IPROPOL,NBUTOL,BUT2OL,IBUTOL,TBUTOL,PECOH,IPEAOH,ME3BUOL,IPECOH,IPEBOH,CYHEXOL,MIBKAOH,ETHGLY,PROPGLY,MBO,HCHO,CH3CHO  C2H5CHO,C3H7CHO,IPRCHO,C4H9CHO,ACR,MACR,C4ALDB,C3H8,NC4H10,IC4H10,NC5H12,IC5H12,NEOP,NC6H14,M2PE,M3PE,M22C4,M23C4,NC7H16,M2HEX,M3HEX,NC8H18,NC9H20,NC10H22,NC11H24,NC12H26,CHEX,C2H4,C3H6,BUT1ENE,CBUT2ENE,TBUT2ENE,MEPROPENE,PENT1ENE,CPENT2ENE,TPENT2ENE,ME2BUT1ENE,ME3BUT1ENE,ME2BUT2ENE,HEX1ENE,CHEX2ENE,THEX2ENE,DM23BU2ENE,C2H2,BENZENE,TOLUENE,OXYL,MXYL,PXYL,EBENZ,PBENZ,IPBENZ,TM123B,TM124B,TM135B,OETHTOL,METHTOL,PETHTOL,DIME35EB,DIET35TOL,STYRENE,BENZAL,CH3CL,CH2CL2,CHCL3,CH3CCL3,TCE,TRICLETH,CDICLETH,TDICLETH,CH2CLCH2CL,CCL2CH2,CL12PROP,CHCL2CH3,CH3CH2CL,CHCL2CHCL2,CH2CLCHCL2,VINCL,C4H6,C5H8,CH3OCHO,METHACET,ETHACET,NPROACET,IPROACET,NBUTACET,SBUTACET,TBUACET,CH3OCH3,DIETETHER,MTBE,DIIPRETHER,ETBE,MO2EOL,EOX2EOL,PR2OHMOX,BUOX2ETOH,BOX2PROL,CH3BR,DIBRET,CH3COCH3,MEK,MPRK,DIEK,MIPK,HEX2ONE,HEX3ONE,MIBK,MTBK,CYHEXONE,APINENE,BPINENE,LIMONENE,BCARY,HCOOH,CH3CO2H,PROPACID,DMM,DMC,DMS,ETHOX'.split(',')


# get reaction category
def categorise(x):
    '''
    x = [[reactants],rate]
    '''

    cat2 = 'Radicals/Other'
    if 'RO2' in x[1]:
        cat = re.search(r'RO2[\w]*\b',x[1]).group()
        cat2 = 'RO2'

    elif 'J(' in x[1]:
        cat = 'hv'
        cat2 = 'Photolysis'
    elif '*O2' in x[1] :
        cat = 'O2'
        cat2 = 'Decomposition'
    elif 'H2O' in x[1] :
        cat = 'H2O'
    else:
        radical = set(x[0]) & set('OH,HO2,NO,NO2,NO3,Cl,CL,O3'.split(','))
        if len(radical):
            cat = list(radical)[0]
        else:
            try: cat = re.search(r'K[\w]*\b',x[1]).group()
            except: cat = 'Uni-molecular'
            cat2 = 'Decomposition'
    return [cat,cat2]







def makeG(eqns):
    #create full mcm graph
    save = []
    nodes = []

    for c,e in enumerate(eqns):
        react = e[0]#.split('+')
        cat = categorise([react,e[2]])

        for r in react:
            repeat=1
            test = coeff.match(r)
            if test:repeat,r = test.groups()

            for z in range(int(repeat)):
                for p in e[1]:#.split('+'):
                    if r != p:
                        repeat=1
                        test = coeff.match(p)
                        if test:repeat,p = test.groups()
                        for z in range(int(repeat)):
                            save.append((p,r,{'rxn':c,'cat1':cat[0],'cat2':cat[1]}))
                            nodes.extend([r,p])



    G = nx.DiGraph() #multidigraph increases the score
    G.add_edges_from( save )

    return G













from progressbar import ProgressBar,Bar

import datetime
import powerlaw

sample = 100
ss = lambda x: set(np.random.permutation(vocs)[:x])
info = re.compile(r'(\d[.\d]+)')



def pset (n):
    np.random.seed(seed=n)
    comb = []
    for i in range(sample):
        comb.append(' '.join(set(ss(n))))

    comb = set(comb)
    print n
    return [ i.split() for i in comb ]



def perm(myspecs):
    try:
        run = {}

        myeqns = subset(eqns,myspecs)
        myG = makeG(myeqns[1])
        #print len(myeqns[1]),len(myspecs),len(myG.nodes())
        ifo = info.findall(nx.info(myG))
        run['species']=myG.nodes()
        run['VOC']=myspecs
        run['nodes']=ifo[0]
        run['edges']=ifo[1]
        run['indegree']=ifo[2]
        run['outdegree']=ifo[3]
        run['transivity']=nx.transitivity(myG)
        run['density']=nx.density(myG)
        run['ndin'] = myG.in_degree()
        run['ndout']= myG.out_degree()

        #np.random.seed(seed=42)
        '''
        UG = myG.to_undirected()
        run['smsig']=nx.smallworld.sigma(UG, niter=100, nrand=10, seed=42)
        run['smomg']=nx.smallworld.omega(UG, niter=100, nrand=10, seed=42)
        '''
        '''
        np.random.seed(seed=42)
        dg = np.zeros(len(myG.nodes()))
        for i in dict(run['ndout']).values():
            dg[i]+=1
        for i in dict(run['ndin']).values():
            dg[i]+=1

        dg = np.array(dg).astype(float)
        dg.sort()
        dg = dg/len(myG.nodes())

        pwr = powerlaw.Fit(dg,discrete = True,)

        run['log_exp'] = pwr.distribution_compare('lognormal_positive', 'exponential')
        run['pow_exp'] = pwr.distribution_compare('power_law', 'exponential')
        run['pow_log'] = pwr.distribution_compare('power_law', 'lognormal_positive')

        run['pow.D'] =  pwr.power_law.D
        run['pow.a'] =  pwr.power_law.alpha
        run['pow.s'] =  pwr.power_law.sigma
        run['log.D'] =  pwr.lognormal.D
        run['exp.D'] =  pwr.exponential.D
        '''

        #https://www.nature.com/articles/s41467-019-08746-5




        for i in fn.columns:
            dc = fn.loc[list(myG.nodes())][i].fillna(0).astype(int).to_dict()
            #nx.set_node_attributes(myG,str(i),dict(dc))
            nx.set_node_attributes(myG, values=dc, name=i)
            run[i]=nx.numeric_assortativity_coefficient(myG,i)



        return run

    except Exception as e:
        print e
        return False

    print '.'

rxns = []
import multiprocessing as mp
pl = mp.Pool()
print mp.cpu_count()-1
print 'assign'
for i in pl.map(pset,range(1,len(vocs),1)):
    rxns.extend(i)



print 'start'
print len(rxns)
print datetime.datetime.now()
#results = pl.map(perm,rxns)
amap = [pl.apply_async(perm,args=(x,)) for x in rxns]
bar = ProgressBar()
results = [p.get() for p in bar(amap)]
print datetime.datetime.now()

results = filter(None,results) #identity function removes falsely values [] {} 0 false

print len(results)
print 'saving'
pl.close()
print 'saved'
'''
results =np.load('global_graph.npy')
'''
from scipy.stats.stats import pearsonr




#nodees
data = []
for i in results:

    data.append([i['nodes'],i['edges'],len(i['VOC'])])
data = np.array(data)
df = pd.DataFrame(data,columns = ['nodes','edges','vocs'])
df = df.astype(float)
df.sort_values('nodes', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
df.to_csv('nodeedge_%s_%s.csv'%(','.join(df.min().values.astype(str)),','.join(df.max().values.astype(str))))


#nodees
data = []
for i in results:

    data.append([i['indegree'],i['outdegree'],i['edges']])
data = np.array(data)
df = pd.DataFrame(data,columns = ['indegree','outdegree','edges'])
df = df.astype(float)
df.sort_values('indegree', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
df.sort_values('outdegree', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
df.to_csv('degreecorr_%s_%s.csv'%(','.join(df.min().values.astype(str)),','.join(df.max().values.astype(str))))
print 'degree', pearsonr(df.indegree.values,df.outdegree.values)

#nodees
data = []
for i in results:

    data.append([i['transivity'],i['density'],i['nodes']])
data = np.array(data)
df = pd.DataFrame(data,columns = ['transivity','density','nodes'])
df = df.astype(float)
df.sort_values('transivity', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
df.sort_values('density', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
df.to_csv('transdense_%s_%s.csv'%(','.join(df.min().values.astype(str)),','.join(df.max().values.astype(str))))
print 'transdense'

#nodees
data = []
for i in results:

    data.append([i[j] for j in fn.columns])
data = np.array(data)
df = pd.DataFrame(data,columns = fn.columns)
df = df.astype(float)
df.to_csv('assortivity.csv')
print 'assort'



G = makeG(subset(eqns,vocs)[1])
din = {}
dout ={}
for n in G.nodes():
    din[n]=[]
    dout[n]=[]


for i in results:

    for j in i['ndin']:
        j=j[0]
        din[j].append(i['ndin'][j])
    for j in i['ndout']:
        j=j[0]
        dout[j].append(i['ndout'][j])

degprof = [din,dout]



print 'savedprof'
np.save('degprof.npy',degprof)
print 'saved'



np.save('global_graph.npy', results)

print 'use this for tsne'
