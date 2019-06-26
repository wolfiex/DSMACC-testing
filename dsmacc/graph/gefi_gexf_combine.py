'''
Combine the positions of the gephi run with the original gexf file
for use in JS viz
'''

from xml.dom import minidom
import sys
import networkx as nx


doc = minidom.parse(sys.argv[1])  # parseString also exists
#path_strings = [path.getAttribute('d') for path
#                in doc.getElementsByTagName('path')]

x,y,n = [],[],[]
for node in doc.getElementsByTagName('circle'):
    x.append(node.getAttribute('cx'))
    y.append(node.getAttribute('cy'))
    n.append(node.getAttribute('class').replace('id_',''))




print x,n

G = nx.read_gexf(sys.argv[2])

nx.set_node_attributes(G, dict(zip(n,x)),'fx')
nx.set_node_attributes(G, dict(zip(n,y)),'fy')

import json

jsondata = nx.json_graph.node_link_data(G)
with open('withlocation.json', 'w') as f:
    json.dump(jsondata,f)


doc.unlink()
