import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from zhdf import new,loaddump,pool,ncores,da,progressbar,h5py
import numpy as np
import os
 




a = new('BaseRun_init.h5')

import time

from sklearn.manifold import TSNE

time_start = time.time()
tsne = TSNE(n_components=2, verbose=1, perplexity=100, n_iter=300)
tsne_results = tsne.fit_transform(a.adj[:,:,1])

print 't-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start)
