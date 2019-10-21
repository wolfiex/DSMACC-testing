import multiprocessing as mp
import sys,os

def run(x):
	print(x)
	os.system('npm start index.html "%s"'%x)


data = []

for i in range(6):
	for k in 'pca,spca,tsne,umap,vae,gae'.split(','):
		for s in ['ocratio','Fngroups',0]:
			data.append('%s#%s#%s#%s'%(i,k,s,''))



#mp.Pool().map(run,data)
#
#

data=[]

for i in range(6):
	for k in 'pca,spca,tsne,umap,vae,gae'.split(','):
		for f in [   "Carb. Acid",
  "Ester",
  "Ether",
  "Per. Acid",
  "Hydroperoxide",
  "Nitrate",
  "Aldehyde",
  'PAN',
  "Ketone",
  "Alcohol",
  "Criegee",
  "Alkoxy rad",
  "Peroxyacyl rad",
  "Aromatic rings",
  "Carbons"]:
			data.append('%s#%s#%s#%s'%(i,k,0,f))



#mp.Pool().map(run,data)


data=[]

for i in range(6):
	for k in 'pca,spca,tsne,umap,vae,gae'.split(','):
		for c in ["Carbons"]:
			data.append('%s#%s#%s#%s'%(i,k,c,''))



#mp.Pool().map(run,data)
