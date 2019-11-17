
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import matplotlib.pyplot as plt
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors as Descriptors
import numpy as np

fngroups=pd.read_csv('functionalgroups_regexmatched.csv')
sm = pd.read_csv('vankrevelenratios.csv')

fngroups.set_index('name',inplace=True)
sm.set_index('name',inplace=True)

sm = sm[sm.smiles.astype('str')!='nan']
sm = sm.sort_index()


smiles = sm.smiles.values.astype('str')
species = sm.index
fngroups = fngroups.loc[species]


print (fngroups.columns ,len(species))

#inorganics dont have smiles strings, lets remove these
#fngroups = fngroups.loc[map(lambda x: type(x)==str,fngroups.smiles),:]
#species = fngroups.index.values
#species.sort()

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

df = {}
df['smiles']= smiles
df['names']= sm.index

names = 'vec_spec,vec_smiles,finger_mqn,finger_maccs,embed_fn '.split(',')




counter = 0
for i in  [vec_spec,vec_smiles,finger_mqn,finger_maccs,embed_fn]:
    #i = np.array([np.nan_to_num(q) for q in i])
#for i in [embed_fn,,embed_graph ]:

    df[names[counter]] = np.array([np.nan_to_num(q) for q in i])

    counter += 1

df['fnnames'] = fngroups.columns
df['fngroups'] = (fngroups>0).astype(int).values

import pickle

def save_obj(obj, name ):
    with open( name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open( name + '.pkl', 'rb') as f:
        return pickle.load(f)

save_obj(df,'all_fingerprints')
