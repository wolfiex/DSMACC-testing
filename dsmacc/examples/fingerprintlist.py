
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import matplotlib.pyplot as plt
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors as Descriptors


fngroups=pd.read_csv('~/DSMACC-testing/dsmacc/datatables/functionalgroups_regexmatched.csv')
sm = pd.read_csv('../datatables/vankrevelenratios.csv')

fngroups.set_index('name',inplace=True)
sm.set_index('name',inplace=True)

sm = sm[sm.smiles.astype('str')!='nan']
sm = sm.sort_index()



smiles = sm.smiles.values.astype('str')
species = sm.index
fngroups = fngroups.loc[species]



print (fngroups.columns ,len(species))

lf=klj

#inorganics dont have smiles strings, lets remove these
#fngroups = fngroups.loc[map(lambda x: type(x)==str,fngroups.smiles),:]

#species = fngroups.index.values
#species.sort()

graph = graph.loc[species]
#map(lambda x: x in species,graph.index),:]

#fngroups = fngroups.loc[map(lambda x: x in species,fngroups.index),:]
#smiles = fngroups.smiles.values

fngroups = fngroups[[u'PAN', u'Carb. Acid', u'Ester', u'Ether', u'Per. Acid',
       u'Hydroperoxide', u'Nitrate', u'Aldehyde', u'Ketone', u'Alcohol',
       u'Criegee', u'Alkoxy rad', u'Peroxalkyl rad', u'Peroxyacyl rad',
       u'Aromatic rings']]


#char to vector tokens
vectorizer = TfidfVectorizer(analyzer='char_wb')
vec_smiles = vectorizer.fit_transform(smiles).toarray()

vectorizer = TfidfVectorizer(analyzer='char_wb')
vec_spec = vectorizer.fit_transform(species).toarray()


#structure
embed_fn=np.nan_to_num(fngroups.values)
graph.fillna(0,inplace=True)
embed_graph=graph.values


#molecular fingerprint
#https://www.rdkit.org/UGM/2012/Landrum_RDKit_UGM.Fingerprints.Final.pptx.pdf
finger_mqn =[]
finger_morgan = []
finger_maccs = []
finger_ap = []

for i in smiles:
        mol = AllChem.MolFromSmiles(i)

        finger_mqn.append(np.array(Descriptors.MQNs_(mol)))
        finger_maccs.append(np.array(Descriptors.GetMACCSKeysFingerprint((mol))))
        #finger_morgan.append(np.array(Descriptors.GetMorganFingerprint((mol))))
        #finger_ap.append(np.array(Descriptors.GetAtomPairFingerprint((mol))))

###

df = pd.DataFrame()

names = 'vec_spec,vec_smiles,finger_mqn,finger_maccs,embed_graph,embed_fn '.split(',')



def n(z):
    z = np.array(z).astype(float)
    mn = np.min(z)
    mx = np.max(z)

    return (z-mn)/(mx-mn)

'''

counter = 0
for i in  [vec_spec,vec_smiles,finger_mqn,finger_maccs,embed_graph,embed_fn]:
    #i = np.array([np.nan_to_num(q) for q in i])
#for i in [embed_fn,,embed_graph ]:
    i = np.array(i)
    df.index = sm.index



    nfn =fngroups[[u'Carb. Acid',u'Ester',u'Ether', u'Per. Acid', u'Hydroperoxide',
u'Nitrate', u'Aldehyde', u'Ketone', u'Alcohol', u'Criegee',u'Alkoxy rad', u'Peroxalkyl rad', u'Peroxyacyl rad']].sum(axis=1).values

    nfn = nfn/nfn.max()

    df['Fngroups']=nfn

    pd.concat([df,fngroups,sm],axis=1).to_csv('compare_results.csv')
'''
