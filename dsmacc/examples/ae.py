from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pylab as plt
import numpy as np
import seaborn as sns; sns.set()

import keras
from keras.models import Sequential, Model
from keras.layers import Dense
from keras.optimizers import Adam

from keras.datasets import cifar10,mnist


#https://stats.stackexchange.com/questions/190148/building-an-autoencoder-in-tensorflow-to-surpass-pca

class isoae:
    def __init__(
        self,
        indim,
        l_big = 512,
        l_mid = 128,
        l_lat = 2,
        epochs= 100,
        activation = 'sigmoid' #elu
        ):

        m = Sequential()
        m.add(Dense(l_big,  activation=activation, input_shape=(indim,)))
        m.add(Dense(l_mid,  activation=activation))
        m.add(Dense(l_lat,    activation='linear', name="bottleneck"))
        m.add(Dense(l_mid,  activation=activation))
        m.add(Dense(l_big,  activation=activation))
        m.add(Dense(indim,  activation='sigmoid'))
        m.compile(loss='mean_squared_error', optimizer = Adam())
        self.m = m
        self.indim = indim


    def train(self,x_train):
        assert x_train.shape[1] == self.indim
        self.hist = m.fit(x_train, x_train, batch_size=indim, epochs=epochs, verbose=1,
                validation_data=(x_test, x_test))
        self.encoder = Model(m.input, m.get_layer('bottleneck').output)

    def predict(self,x_train):
        self.predict = encoder.predict(x_train)  # bottleneck representation
        self.reconstruct = m.predict(x_train)        # reconstruction


    def plot(self,x_train):
        self.predict(x_train)

        plt.title('Autoencoder')
        plt.scatter(self.predict[:,0], self.predict[:,1], c='blue', s=8, cmap='tab20')
        plt.gca().get_xaxis().set_ticklabels([])
        plt.gca().get_yaxis().set_ticklabels([])
        plt.tight_layout()
        plt.show()
