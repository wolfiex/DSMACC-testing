'''
 run dsmacc/vis/ropa/__init__.py

'''
import numpy as np
import pandas as pd
import zhdf

self = zhdf.new('clfoch2.h5')
self.rm_spinup()


def group_hour(df,fn = np.mean,diurnal = False):
        try: df = df.compute()
        except:None


        df['group']= [str(i).split(':')[0] for i in df.index]
        df = df.groupby(by='group').agg(fn)
        if diurnal:
            day = range(24)
            hour = lambda x: x in range(24)
            df['hour'] = [int(i.split(' ')[-1]) for i in df.index]
            df = df[df['hour'].apply(hour)]
            df = df.groupby(['hour']).agg(fn)
        return df
        
'''
Inputs:
            spec   
            new class
            timestep
            
'''
import dsmacc 
        
spec = 'CH3CO3'
print spec
retdict = {"name":spec}


smileslist = dsmacc.__file__.replace('__init__.pyc','')+ 'datatables/smiles_mined.csv'
conc = np.log10(group_hour(self.spec[[spec,'SPINUP']].compute()))
vdot = np.log10(group_hour(self.vdot[[spec,'O3']].compute()))

retdict['concentration']= list(np.nan_to_num(conc)[:,0])
retdict['vdot']= list(np.nan_to_num(vdot)[:,0])

smiles = pd.read_csv(smileslist)
smiles = smiles[smiles.name == spec].smiles.values[0]
if smiles in [np.nan,'nan','NaN']: smiles = 'Inorganic'

retdict['smiles'] = smiles





pr = self.prod(spec)
ls = self.loss(spec)
 
pr1 = np.log10(group_hour(self.flux.loc[:,pr].compute()))
ls1 = np.log10(group_hour(self.flux.loc[:,ls].compute()))


retdict['production']= dict(zip(pr1.columns,pr1.T.values.tolist()))
retdict['loss']= dict(zip(ls1.columns,ls1.T.values.tolist()))

retdict['timesteps']= np.array(pr1.index).tolist()


import json

jarr = json.dumps(retdict)

with open('ropa.json','w') as f:
    f.write('data = %s'%jarr)


print ('Outputted ropa.json')