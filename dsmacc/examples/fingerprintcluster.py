import pandas as pd
import numpy as np

import matplotlib
matplotlib.use("Agg")

import seaborn as sns
import pickle,os,sys


loc = '/work/home/dp626/DSMACC-testing/dsmacc/examples/outputs/'




#pandas.read_csv('mcm_emb.txt',skiprows=1,header=None,delimiter = ' ').c


d2 = pd.read_csv('mcm_emb2.txt',delimiter=' ')
d2.columns = 'x y'.split()

d100 = pd.read_csv('mcm_emb100.txt',delimiter=' ',skiprows=1,header=None,index_col=0)
d100.columns = range(100)



def save_obj(obj, name ):
    with open( name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open( name + '.pkl', 'rb') as f:
        return pickle.load(f)

data = load_obj('./fingerprintgen/all_fingerprints')

gen = pd.read_csv('../datatables/gen_groups.csv')
gen.set_index('name',inplace = True)
gen = gen.loc[data['names']]
gen.drop('smiles',inplace = True,axis=1)
data['cat_protocol']= gen.values

fp =  pd.read_json('../datatables/fingerprint.json')
data['fingerprints'] = fp[data['names']].T.values

fn = pd.DataFrame(data['embed_fn '],index=data['names'],columns=data['fnnames'])

carb = pd.DataFrame([i.upper().count('C') for i in data['smiles']],index=data['names'],columns=['Carbons'])

ox = pd.DataFrame([i.upper().count('O') for i in data['smiles']],index=data['names'],columns=['Oxygens'])

check = pd.concat([fn[['Aromatic rings']]>0,gen,carb,ox],axis=1)

d100 = d100.loc[data['names']]
d2 = d2.loc[data['names']]

data['node2vec'] = d100.values
print(data.keys())

#### END LOAD #################





np.random.seed(seed=43110)

'''
['vec_smiles',
 'smiles',
 'finger_mqn',
 #'embed_fn ',
 'finger_maccs',
 'names',
 'vec_spec',
 'fnnames',
 'fingerprints'
 'fngroups']
 '''
 
  
##### FN ##############
 
import sklearn
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(check))
df_scaled.columns = check.columns
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import DBSCAN
from spectral_embedding import SpectralClustering

from ae import *
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from optics import OPTICS



def plot(x,y,title='',err =None,clust = 'blue',sserr=None):
    global item
    plt.title(title+': '+item)
    plt.scatter(x,y, c=clust, s=1, cmap='tab20')
    plt.gca().get_xaxis().set_ticklabels([])
    plt.gca().get_yaxis().set_ticklabels([])
    plt.tight_layout()
    plt.show()


def clust(out):
    x = np.array(out[:2]).T

    X = (x-np.min(x))/(np.max(x)-np.min(x))

    ssold = -1
    pkeep = [-1]*len(X)
    for samples in range(3,11):
        ms = int(2**samples)  #int(len(out[0])*2**samples)


        db = DBSCAN(eps=0.025, min_samples=ms,n_jobs=-1)
        op = OPTICS(min_samples=ms, max_eps=np.inf, metric='minkowski', p=2, metric_params=None, cluster_method='xi', eps=None, xi=0.009, predecessor_correction=False, min_cluster_size=None, algorithm='auto', leaf_size=30, n_jobs=-1)
        
        sp = SpectralClustering(n_clusters=2*samples,assign_labels="discretize",eigen_solver=None, random_state=None, n_init=10, gamma=1.0, affinity='rbf', n_neighbors=100, eigen_tol=0.0, degree=3, coef0=1, kernel_params=None, n_jobs=-1)



        pred = op.fit_predict(X)

        try:ss = silhouette_score(x,pred)
        except:
            print ('not enough samples, continue')
            continue
        print (ms,ss,max(pred) , 'optics')
        if ss > ssold:
            pkeep = pred
            ssold = ss

        pred = db.fit(X).labels_

        try:ss = silhouette_score(x,pred)
        except:
            print ('not enough samples, continue')
            continue
        print (ms,ss,max(pred) , 'dbscan')
        if ss > ssold:
            pkeep = pred
            ssold = ss
            
            
        pred = sp.fit(X).labels_    
        try:ss = silhouette_score(x,pred)
        except:
            print ('not enough samples, continue')
            continue
        print (2*samples,ss,max(pred) , 'spectral')
        if ss > ssold:
            pkeep = pred
            ssold = ss


    print ('best', max(pkeep), ssold)
    out = list(out)
    out.extend([pkeep,ssold])

    return out


def do_pca(data_subset):
        pca = PCA().fit(data_subset)
        err = np.cumsum(pca.explained_variance_ratio_)
        pca = PCA(n_components=2)
        pca_results = pca.fit_transform(data_subset)
        return pca_results[:,0],pca_results[:,1],'PCA',err

def do_tsne(data_subset,learning_rate=80,early_exaggeration=42.0,perplexity=80,n_iter=1000):
     #do_tsne(data_subset,learning_rate=200,early_exaggeration=42.0,perplexity=30,n_iter=300):

		tsne = TSNE(n_components=2,perplexity=perplexity,early_exaggeration=early_exaggeration,n_iter = n_iter)
		tsne_results = tsne.fit_transform(data_subset)
		return tsne_results[:,0],tsne_results[:,1],'t-SNE',None


def do_ae(dt):
    myae = ae(
            dt.shape[1],
            l_big = 16,
            l_mid = 8,
            l_lat = 2,
            epochs= 50,
            activation = 'tanh' #elu
            )
    myae.train(dt)
    myae.predict(dt)
    print (myae.hist.history)
    '''
    loss = MSE mean_squared_error.
     the average squared difference between the estimated values and the actual value.
     closer to zero is better

     val_loss is the value of cost function for your cross-validation data and loss is the value of cost function for your training data. On validation data, neurons using drop out do not drop random neurons. The reason is that during training we use drop out in order to add some noise for avoiding over-fitting. During calculating cross-validation, we are in the recall phase and not in the training phase. We use all the capabilities of the network.

     '''
    #myae.plot(dt)
    return myae.prediction[:,0], myae.prediction[:,1],'AE',myae.hist.history

print ('starting')


'''
plot(*clust(do_pca(dt)))

plot(*clust(do_tsne(dt)))

plot(*clust(do_ae(dt)))
'''

import sys
#    name = 'vec_smiles'

'node2vec,cat_protocol,vec_smiles,finger_mqn,fingerprints,finger_maccs,vec_spec,fngroups'

for name in sys.argv[1].split(','):#['cat_protocol','node2vec','vec_smiles',  'finger_mqn', 'embed_fn ', 'finger_maccs', 'vec_spec', 'fngroups']:


    item = name.split('_')[-1]

    dt = data[name]
    dt = np.array(dt).astype(float)
    dt[np.isnan(dt)]=0.


    for fn in [do_tsne,do_ae,do_pca]:



        out = clust(fn(dt))


        method = out[2]

        print (method,name,max(out[-2]))

        print (method)
        os.system('mkdir %s%s'%(loc,method))
        os.system('mkdir %s%s/%s'%(loc,method,item))
        os.system('rm %s%s/%s/*.p*'%(loc,method,item))

        X = check
        y = out[-2][:len(X)]
        df_scaled['Cluster'] = y

        #clf = RandomForestClassifier(n_estimators=100).fit(X, y)
        imp = []
        for i in [1,42,116,2019,43110]+list(range(100000,100000+4)):
            np.random.seed(seed=i)
            imp.append(RandomForestClassifier(n_estimators=100).fit(X, y).feature_importances_)

        imp = np.median(np.array(imp),axis=0)

        dataa = np.array([imp, X.columns]).T

        #columns = list(pd.DataFrame(dataa, columns=['Importance', 'Feature'])
                   #.sort_values("Importance", ascending=False)
                   #.head(len(df_scaled.columns)).Feature.values)

        legend = pd.DataFrame(dataa).sort_values(0,ascending=False)

        columns = legend[1].to_list()

        g = sns.barplot(x=0, y=1, data=legend)
        g.set(xlabel = 'Fractional importance' )
        g.set(title = 'Random Forrest ranked groups' )
        g.set(ylabel = '' )
        #plt.subplots_adjust(left=0.5, right=0.5)
        plt.tight_layout()
        plt.savefig('outputs/%s/%s/legend.png'%(method,item))
        #plt.show()
        plt.clf()


        tidy = df_scaled[columns+['Cluster']].melt(id_vars='Cluster')

        t1 = tidy[:]
        t1['v']=1
        topc = list(t1.groupby('Cluster').count().sort_values('v',ascending=False).index)[0:12]

        if len(topc)>11:
            topc = filter(lambda x: x!= -1,topc)

        print (topc)

        for cn in topc:

            g = sns.barplot(x='Cluster', y='value', hue='variable', data=tidy[tidy.Cluster==cn])

            plt.legend().set_visible(False)
            g.set_ylim(0,np.max(tidy.value))
            g.set(xticklabels=[])
            g.set(yticklabels=[])
            g.set(xlabel = '' )
            g.set(title = 'Cluster %s'%cn )
            g.set(ylabel = '' )
            plt.tight_layout()
            plt.savefig('outputs/%s/%s/%02d.png'%(method,item,cn),transparent=True)
            plt.clf()
            print (cn)




        '''big'''
        flab = []
        for i in out[-2]:
            dm = ''
            if i in topc:
                dm = str(i)
            flab.append(dm)

        print ('totalplot')
        try:
            g = sns.scatterplot(x=out[0], y=out[1],
                                alpha=0.5,
                                 hue=flab,
                                 size=0.2,#['-'*int(i=='') for i in flab],
                                 palette="Set2"
                                 )
        except:
                    g = sns.scatterplot(x=out[0], y=out[1],
                                        alpha=0.5,
                                         hue=np.array(flab,dtype=int),
                                         size=.2,#['-'*int(i=='') for i in flab],
                                         palette="Set2"
                                         )

        g.set(xlabel = '' )
        g.set(title = 'Name: %s , Silhouette score: %.2e'%(out[2],out[5]) )
        g.set(ylabel = '' )
        plt.tight_layout()
        plt.savefig('outputs/%s/%s_all.pdf'%(method,item),transparent=True)
        plt.clf()
        '''
        if out[2] == 'PCA':
            out[3] = out[3][1]
        if out[2] == 'AE':
            out[3] = out[3][-1]
        else:
            out[3] = 0
        '''
        out.append(flab)
        pd.DataFrame([i[:len(data['names'])] for i in np.array(out)[[0,1,4,6]]],index= 'x y label filterlab'.split(), columns = data['names']).T.to_csv('outputs/%s/%s_data.csv'%(method,item))

        os.system('cd %s%s/%s && montage *.png  -geometry 600x600+1+1 -tile 3x4 group.png'%(loc,method,item))
