import mcm_tograph
from .. import datatables
__tableloc__ = datatables.__file__
import networkx as nx

import pandas as pd
name = 'formatted_China_GCGC'
G = mcm_tograph.getG([name])

fngroups = pd.read_csv('./'+__tableloc__.replace('__init__.pyc','functionalgroups_regexmatched.csv'))
fngroups.index = fngroups['name']

fngroups = fngroups[[u'PAN', u'Carb. Acid', u'Ester', u'Ether',
       u'Per. Acid', u'Nitrate', u'Aldehyde', u'Ketone',
       u'Alcohol', u'Criegee', u'Alkoxy rad', u'Peroxalkyl rad',
       u'Peroxyacyl rad','Aromatic rings','Carbons','Atoms']]


for c in fngroups.columns:
    # if unhashable type, different versions of nx changed the order for this.
    nx.set_node_attributes(G, dict(fngroups[c][list(G.nodes())].astype(str)),c)

#print nx.get_node_attributes(G,'PAN')

nx.write_gexf(G, name +".gexf")
print ('Written to : ',name +".gexf")
