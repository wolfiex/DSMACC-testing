import os,sys
from zhdf import *
import matplotlib.pyplot as plt

from sklearn import preprocessing
scaler = preprocessing.StandardScaler()

from sklearn.decomposition import PCA
from sklearn import manifold

from optics import OPTICS

a = new(sys.argv[1])
a.rm_spinup()

df = a.spec.compute().iloc[144/2:144/2+144]

print df.head()

cmapn = 'viridis_r'

scaled_df = scaler.fit_transform(np.log10(1e-20 + df))
scaled_df = pd.DataFrame(scaled_df, columns=df.columns)


pca = PCA(n_components=2)
principalComponents = pca.fit_transform(scaled_df.T)
pdf = pd.DataFrame(data = principalComponents, columns = ['x','y'], index= df.columns)


tsne = manifold.TSNE(n_components=2, perplexity= 120, init='pca',early_exaggeration=5, random_state=0)
tsneComponents = tsne.fit_transform(scaled_df.T)
pdf['xt'] = tsneComponents[:,0]
pdf['yt'] = tsneComponents[:,1]
#https://towardsdatascience.com/clustering-using-optics-cac1d10ed7a7
# optics - dbscan with a reachability graph  OPTICS (Ordering Points to Identify Cluster Structure)
clust = OPTICS(min_samples=25, xi=.055, min_cluster_size=None)
opt = clust.fit_predict(pdf)

# ['Pastel1', 'Pastel2', 'Paired', cmapn,'Dark2', 'Set1', 'Set2', 'Set3','tab10', 'tab20', 'tab20b', 'tab20c']
print opt,opt.max()


pdf['c'] = opt

os.system('rm CDR_*')
##############


fig,ax = plt.subplots()#figure(frameon=False)
ax.axis('off')
fig.patch.set_visible(False)
pdf.plot(ax = ax, kind = 'scatter',x='x',y='y',s=1,c=opt ,cmap = cmapn)
plt.tight_layout()
fig.savefig("CDR_pca.png", dpi = (600))


fig,ax = plt.subplots()#figure(frameon=False)
ax.axis('off')
fig.patch.set_visible(False)
pdf.plot(ax = ax, kind = 'scatter',x='xt',y='yt',s=1,c=opt ,cmap = cmapn)
plt.tight_layout()
fig.savefig("CDR_tsne.png", dpi = (600))

f = open('CDR_groups.txt','w')

for id in range(-1,opt.max()+1):

    if id not in list(set(pdf['c'])): continue
    print id

    f.write('%2d %s\n'%(id,'-'.join(pdf[pdf['c'] == id].index)))

    fig,ax = plt.subplots()#figure(frameon=False)
    ax.axis('off')
    fig.patch.set_visible(False)
    sel = scaled_df[pdf[pdf['c'] == id].index]
    sel.plot( ax = ax, legend = False)
    plt.tight_layout()
    fig.savefig("CDR_scaled_%s.png"%id, dpi = (600))
    #plt.show()

    fig,ax = plt.subplots()#plt.figure(frameon=False)
    ax.axis('off')
    fig.patch.set_visible(False)
    sel = np.log10(df[pdf[pdf['c'] == id].index])
    sel.plot( ax = ax, legend = False)
    plt.tight_layout()
    fig.savefig("CDR_l10fdsaconc_%s.png"%id, dpi = (600))
    #plt.show()



f.close()


'''
pdf.plot(kind = 'scatter',x='x',y='y',s=1,c=opt ,cmap = cmapn)
np.log10(df[pdf[pdf['c'] == 1].index]).plot()
scaled_df[pdf[pdf['c'] == 1].index].plot()

plt.show()
'''

print 'fi'
