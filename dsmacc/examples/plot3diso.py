from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import keras
from keras.models import Sequential, Model
from keras.layers import Dense
from keras.optimizers import Adam

import numpy as np
np.warnings.filterwarnings('ignore')
import h5py,re,dask,os,sys
import dask.array as da
import dask.dataframe as dd

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from scipy.spatial import Delaunay
import matplotlib.tri as mtri

nox = []
o3=[]
ch4 = []

after = -2

with h5py.File('grid.h5','r') as hf:

            groups = list(filter(lambda x: type(x[1])==h5py._hl.group.Group, hf.items()))

            for g in groups:
                print (g[0])
                try:
                    g = g[1]
                    shead = g.attrs['spechead'].decode("utf-8").split(',')
                    spec = dd.from_array(g.get('spec')[:,:],chunksize=50000, columns = shead)

                    spec = spec/spec.M.mean()

                    nox.extend((spec.NO + spec.NO2).compute().values[after:])
                    o3.extend((spec.O3).compute().values[after:])
                    ch4.extend((spec.CH4).compute().values[after:])
                except:
                    print (type(g),g)


points = np.array([ch4,nox,o3]).T

def surf(points,darg = 'Qbb'):






    x = points[:,0]
    y = points[:,1 ]
    z = points[:,2]

    triang = mtri.Triangulation(x, y)
    #filter out long links

    tz = [[z[i] for i in j] for j in triang.triangles]
    ty = [[y[i] for i in j] for j in triang.triangles]
    tx = [[x[i] for i in j] for j in triang.triangles]


    triang.set_mask( [np.std(i)>(0.3*np.std(y)) for i in ty] )

    '''
    ec = []
    for e in triang.edges:
       if abs(e[1]-e[0])> 100:
            ec.append('red')
       else:
            ec.append('blue')
    '''
    ec = 'darkgrey'

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    # The triangles in parameter space determine which x, y, z points are
    # connected by an edge

    colormap = plt.get_cmap("Spectral")
    norm = matplotlib.colors.Normalize(vmin=min(z), vmax=max(z))



    ax.plot_trisurf(triang, z, alpha=.4, color=None, cmap= colormap, shade=True ,  linewidths=.3,edgecolors=ec)
    ax.scatter(x,y,z,s=2, c=colormap(norm(1.01*z)))
    plt.tick_params(
    axis='all',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off


    '''
    ax.dist = 30
    ax.azim = -140
    ax.set_xlim([0, 2])
    ax.set_ylim([0, 2])
    ax.set_zlim([0, 2])
    '''
    ax.set_xlabel('VOC')
    ax.set_ylabel('NOx')
    ax.set_zlabel('Ozone')
    ax.view_init(13,-45)#25, -151)
    plt.tight_layout()
    plt.show()



# Triangulate parameter space to determine the triangles
#tri = mtri.Triangulation(u, v)

lp = 1*np.log10(points)
surf(lp)

z = points[:,2]
colormap = plt.get_cmap("Spectral")
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(lp)
plt.scatter(x = X_train_pca[:,0],y = X_train_pca[:,1],c=z,cmap=colormap)
plt.show()

proj = pca.inverse_transform(X_train_pca)
surf(proj,darg = 'QJ')





#https://stats.stackexchange.com/questions/190148/building-an-autoencoder-in-tensorflow-to-surpass-pca

def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

nlp = lp#normalized(lp)

# Custom activation function
from keras.layers import Activation
from keras import backend as K
from keras.utils.generic_utils import get_custom_objects


def swish(x):
    return (K.sigmoid(x) * x)

get_custom_objects().update({'swish': Activation(swish)})



class isoae:
    def __init__(
        self,
        indim,
        l_big = 512,
        l_mid = 128,
        l_lat = 2,
        epochs= 200,
        activation = 'tanh', #elu
        activation1 = 'tanh',
        activationlast='linear'
        ):

        m = Sequential()
        m.add(Dense(l_big,  activation=activation, input_shape=(indim,)))
        m.add(Dense(l_mid,  activation=activation1))
        m.add(Dense(l_lat,    activation=activationlast, name="bottleneck"))
        m.add(Dense(l_mid,  activation=activation1))
        m.add(Dense(l_big,  activation=activation))
        m.add(Dense(indim,  activation=activationlast))
        m.compile(loss='mean_squared_error', optimizer = Adam())
        self.m = m
        self.indim = indim
        self.epochs=epochs


    def train(self,x_train):
        assert x_train.shape[1] == self.indim
        self.hist = self.m.fit(x_train, x_train, batch_size=self.indim, epochs=self.epochs, verbose=1,
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


ae = isoae(len(nlp[0]))
ae.train(nlp)
ae.predict(nlp)
X_train_ae = ae.predict
plt.scatter(x = X_train_ae[:,0],y = X_train_ae[:,1],c=z)
plt.show()

surf(ae.reconstruct)


ae = isoae(len(nlp[0]),activation ='linear',activation1='linear')
ae.train(nlp)
ae.predict(nlp)
X_train_ae = ae.predict
plt.scatter(x = X_train_ae[:,0],y = X_train_ae[:,1],c=z)
plt.show()

surf(ae.reconstruct)
