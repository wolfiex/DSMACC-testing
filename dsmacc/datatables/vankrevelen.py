from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import rdmolops
import numpy as np
import pandas as pd

my_smiles_string = 'C1=CC(=C(C=C1C(CN)O)O)O'

def get_ratio(my_smiles_string):
    try:
        my_mol = Chem.MolFromSmiles(my_smiles_string)
        #print(rdMolDescriptors.CalcMolFormula(my_mol))

        my_mol= Chem.AddHs(my_mol)
        atoms = [ i.GetSymbol() for i in my_mol.GetAtoms()]
        admatrix = rdmolops.GetAdjacencyMatrix( my_mol )
        bonds = [ ''.join(set( [atoms[b.GetBeginAtomIdx()],atoms[b.GetEndAtomIdx()]] )) for b in my_mol.GetBonds() ]

        hydrogen = bonds.count('HC')
        oxygen = bonds.count('CO')

        return (hydrogen,oxygen)
    except:
        return (0,0)

df = pd.read_csv( 'smiles_mined.csv'     )

df.index = df.name
df=df[['smiles']]


vankrevelen = np.array(map(get_ratio ,  df.smiles.values)).astype(float)

df['oxygen'] = vankrevelen[:,1]
df['hydrogen'] = vankrevelen[:,0]

df['ocratio'] = df['oxygen']/(df['oxygen']+df['hydrogen'])
df['hcratio'] = df['hydrogen']/(df['oxygen']+df['hydrogen'])


df.to_csv('vankrevelenratios.csv')

'''
import matplotlib.pyplot as plt


df.plot(kind='scatter', x='ocratio' ,y='hcratio')
plt.show()

import seaborn as sns
sns.set(style="whitegrid")

ax = sns.swarmplot(x=df['ocratio'])
plt.show()
'''
