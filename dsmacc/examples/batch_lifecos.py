from __future__ import absolute_import
from __future__ import division
#from __future__ import print_function
import tensorflow as tf

def compute_cosine_distances(a, b):
    # x shape is n_a * dim
    # y shape is n_b * dim
    # results shape is n_a * n_b
    normalize_a = tf.nn.l2_normalize(a,1)
    normalize_b = tf.nn.l2_normalize(b,1)
    distance = 1 - tf.matmul(normalize_a, normalize_b, transpose_b=True)
    return distance

import numpy as np
import pandas as pd
np.warnings.filterwarnings('ignore')
import h5py,re,os,sys
import matplotlib.pyplot as plt


import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)

print sys.argv


sess = tf.Session()


inorganics = 'HCHO,CH4,O,O1D,H2O2,N2O5,HONO,HO2NO2,HSO3,H,O2,A,NA,SA,Cl,CL,SO2,SO3,H2,HNO3,O3,OH,HO2,NO,NO2,NO3'.split(',')
inorganics = [i+'->'+i for i in inorganics]


# qsub -J 1-301 -l nodes=1:ppn=100:100 -q x-large batchscript.sh
import time
time.sleep(60*int(sys.argv[2]))

hf = h5py.File(sys.argv[1],'r')
if True:
    print ('start')
    groups = list(filter(lambda x: type(x[1])==h5py._hl.group.Group, hf.items()))


    for gid in [int(sys.argv[2])+1]:
        g = groups[gid][1]
        qhead = g.attrs['jacsphead'].decode("utf-8").split(',')
        jacobian = pd.DataFrame(g.get('jacsp')[:,:],columns=qhead)


        jacobian.drop('TIME', axis = 1, inplace = True)
        rhead = filter(lambda x: len(set(x.split('->')))==1,jacobian.columns)
        rhead = filter(lambda x: x not in inorganics, rhead)
        specs = [i.split('-')[0] for i in rhead]
        ordered = dict(zip(range(len(specs)),specs))


        #normalisev.
        life = np.nan_to_num(np.log10(-1/jacobian[rhead])).T
        hf.close()
        csm = sess.run(compute_cosine_distances(life,life))


        index = []
        cosine = []
        euclid = []



        length = len(rhead)
        print length

        for s1 in range(length):
            if s1%10 ==0 :print 'progress',float(s1) / length
            tmp1 = np.array([life[s1]],dtype = 'float32')

            for s2 in range(length):
                    if s1==s2:break
                    tmp2 = np.array([life[s2]], dtype = 'float32')
                    index.append([ordered[s1]+'_'+ordered[s2]])
                    cosine.append(csm[s1,s2])
                    euclid.append(tf.norm(tmp1-tmp2, ord='euclidean'))


        df = pd.DataFrame(index)
        df['euclid']=sess.run(euclid)
        df['cosine']=cosine


        df.to_csv('REDUCE/lifecos_%03d.csv'%int(sys.argv[2]))


        print '--'
        break


print 'fi'
