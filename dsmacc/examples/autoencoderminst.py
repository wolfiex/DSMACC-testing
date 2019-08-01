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


(x_train, y_train), (x_test, y_test) = mnist.load_data()
nelement = x_train.shape[0]

indim = x_train.shape[1]*x_train.shape[2]
inshape = x_train.shape[1]

x_train = x_train.reshape(x_train.shape[0], x_train.shape[1]*x_train.shape[2]) / 255
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1]*x_test.shape[2]) / 255

#https://stats.stackexchange.com/questions/190148/building-an-autoencoder-in-tensorflow-to-surpass-pca

l_big = 512
l_mid = 128
l_lat = 2

epochs =5
m = Sequential()
m.add(Dense(l_big,  activation='elu', input_shape=(indim,)))
m.add(Dense(l_mid,  activation='elu'))
m.add(Dense(l_lat,    activation='linear', name="bottleneck"))
m.add(Dense(l_mid,  activation='elu'))
m.add(Dense(l_big,  activation='elu'))
m.add(Dense(indim,  activation='sigmoid'))
m.compile(loss='mean_squared_error', optimizer = Adam())

hist = m.fit(x_train, x_train, batch_size=indim, epochs=epochs, verbose=1,
                validation_data=(x_test, x_test))

encoder = Model(m.input, m.get_layer('bottleneck').output)
Zenc = encoder.predict(x_train)  # bottleneck representation
Renc = m.predict(x_train)        # reconstruction

plt.title('Autoencoder')
plt.scatter(Zenc[:5000,0], Zenc[:5000,1], c=y_train[:5000].reshape(5000), s=8, cmap='tab20')
plt.gca().get_xaxis().set_ticklabels([])
plt.gca().get_yaxis().set_ticklabels([])

plt.tight_layout()
plt.show()

plt.figure(figsize=(9,3))
toPlot = (x_train,  Renc)
for i in range(10):
    for j in range(2):
        ax = plt.subplot(3, 10, 10*j+i+1)
        plt.imshow(toPlot[j][i,:].reshape(inshape,inshape), interpolation="nearest",
                   vmin=0, vmax=1)
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

plt.tight_layout()
plt.show()
