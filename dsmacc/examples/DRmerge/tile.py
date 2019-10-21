import glob,os,re

g = 'pca,spca,tsne,umap,vae,gae'.split(',')

t = "vec_spec,vec_smiles,embed_fn,finger_mqn,finger_maccs,embed_graph".split(
","
);



for gd in g:
     for td in t:
        fs =  glob.glob('plots/%s*%s*false*'%(td,gd))

        if gd == 'pca':

            fs=filter(lambda x: not 'spca' in x,fs)
            print 'pca',fs


        names = [i.split('false')[1].split('.png')[0] for i in fs]



        d = dict(zip(names, fs))


        get = [
        'Alcohol','Aldehyde',
        'Ketone', 'Aromatic rings',
        'Ether',  'Ester',

        'Nitrate','PAN',
        'Peroxyacyl rad','Hydroperoxide',
         #'Alkoxy rad',#// ,
          'Carb. Acid' , 'Criegee']


        bind  = [d[i].replace(' ','\ ') for i in get]


        os.system('montage %s -geometry 800x800+0+0 -crop -20-20 -background whitesmoke -tile 2x3 %s_%s.png'%(' '.join(bind),gd,td))









'''
['Per. Acid', 'Ether', 'vec_smiles_spca_c', 'Ester', 'Aldehyde', 'Alkoxy rad', 'Hydroperoxide', 'Carb. Acid', 'PAN', 'Peroxyacyl rad', 'Nitrate', 'Alcohol', 'Aromatic rings', 'Ketone', 'Criegee']


get = ['Alcohol','Aldehyde','Nitrate','PAN','Aromatic rings','Ketone']


bind  = [d[i].replace(' ','\ ') for i in get]


os.system('montage %s -geometry 800x800+0+0 -crop -20-20 -background whitesmoke -tile 2x3 %s_%s.png'%(' '.join(bind),g[1],t[1]))

#'Per. Acid',
'''
#'vec_smiles_spca_c'
