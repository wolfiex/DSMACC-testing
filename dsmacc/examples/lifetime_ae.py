from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import keras
from keras.models import Sequential, Model
from keras.layers import Dense,Embedding
from keras.optimizers import Adam

import numpy as np
import pandas as pd
np.warnings.filterwarnings('ignore')
import h5py,re,os,sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from scipy.spatial import Delaunay
import matplotlib.tri as mtri

import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)

def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)


# Custom activation function
from keras.layers import Activation
from keras import backend as K
from keras.utils.generic_utils import get_custom_objects


def swish(x):
    return (K.sigmoid(x) * x)

get_custom_objects().update({'swish': Activation(swish)})

class rateae:
    def __init__(
        self,
        indim,
        l_big = 256,
        l_mid = 64,
        l_lat = 2,
        epochs= 5,
        activation = 'swish', #elu
        activation1 = 'swish',
        activationlast='softmax',
        emb_size = 2
        ):

        m = Sequential()
        m.add(Dense(l_big,  activation=activation, input_shape=(indim,)))
        m.add(Dense(l_mid,  activation=activation1))
        m.add(Dense(l_lat,    activation=activationlast, name="bottleneck"))

        #m.add(Embedding(input_dim=indim,output_dim=emb_size, input_length=2, name="embedding"))

        m.add(Dense(l_mid,  activation=activation1))
        m.add(Dense(l_big,  activation=activation))
        m.add(Dense(indim,  activation=activationlast))
        m.compile(loss='mean_squared_error', optimizer = Adam())
        self.m = m
        self.indim = indim
        self.epochs=epochs


    def train(self,x_train):
        assert x_train.shape[1] == self.indim
        self.hist = self.m.fit(x_train, x_train, batch_size=self.indim, epochs=self.epochs, verbose=0,
                validation_data=(x_train, x_train))
        self.encoder = Model(self.m.input, self.m.get_layer('bottleneck').output)

    def predict(self,x_train):
        self.predict = self.encoder.predict(x_train)  # bottleneck representation
        self.reconstruct = self.m.predict(x_train)        # reconstruction


    def plot(self,x_train):
        self.predict(x_train)

        plt.title('Autoencoder')
        plt.scatter(self.predict[:,0], self.predict[:,1], c='blue', s=8, cmap='tab20')
        plt.gca().get_xaxis().set_ticklabels([])
        plt.gca().get_yaxis().set_ticklabels([])
        plt.tight_layout()
        plt.show()

#autoencoder.save_weights('autoencoder.h5')

def norm(Y):
    n = Y.min()
    x = Y.max()
    Y -= n
    return Y/(n+x)

rest = []

with h5py.File(sys.argv[1],'r') as hf:
    print 'start'
    groups = list(filter(lambda x: type(x[1])==h5py._hl.group.Group, hf.items()))
    test = 5#len(groups)-2
    for gid in range(len(groups)):
        g = groups[gid][1]
        qhead = g.attrs['jacsphead'].decode("utf-8").split(',')
        rate = pd.DataFrame(g.get('jacsp')[:,:],columns=qhead)

        if gid == 0:
            rate.drop('TIME', axis = 1, inplace = True)
            rhead = filter(lambda x: len(set(x.split('->')))==1,rate.columns)
            ae = rateae(len(rhead))#len(rhead))

        #normalisev.
        life = np.nan_to_num(np.log10(abs(rate[rhead])))
        if gid<test:
            for r in life:

                ae.train(norm(life))
            print ( gid/test  )
        else:
            xt = np.zeros((len(rhead),1))
            X_train_ae = ae.encoder.predict(life)
            rest.append(X_train_ae)


            np.save('autolife.npy',dict(zip(rhead,X_train_ae)))
            plt.scatter(x = X_train_ae[:,0],y = X_train_ae[:,1],c=life.mean(axis=1),s=.5)
            plt.show()

            if gid>test+3: break

dfs= fdsa

from sklearn.decomposition import PCA
pca = PCA(n_components=2,svd_solver='full')
X_pca = pca.fit_transform(life)
plt.scatter(X_pca[:,0],X_pca[:,1])
plt.show()
