import glob
import numpy as np
import networkx as nx
import os

os.system('rm centrality/circle_* ')
files = glob.glob('centrality/*.gexf')

try:
    from xml.dom import minidom

    doc = minidom.parse('centrality/template.svg')  # parseString also exists
    x = [c.getAttribute('cx') for c in doc.getElementsByTagName('circle')]
    y = [c.getAttribute('cy') for c in doc.getElementsByTagName('circle')]
    id = [c.getAttribute('class').replace('id_','') for c in doc.getElementsByTagName('circle')]
    doc.unlink()
    print 'read template'

    for f in files:
        print f

        G = nx.read_gexf(f)

        attrs = {}
        for i in range(len(x)):
            attrs[id[i]] = {'x':float(x[i]),'y':float(y[i])}

        nx.set_node_attributes(G, attrs)

        nx.write_gexf(G,'centrality/template_'+f.split('/')[-1])









except:


    f=files[0]



    G = nx.read_gexf(f)

    sorteddeg = sorted(dict(G.degree()).items(), key=lambda kv: kv[1],reverse=True)
    sdl = len(sorteddeg)
    fract = 2*np.pi/sdl
    idx = []


    groups = 60
    scale = 1000

    for i in range(groups):
        idx.extend(range(i,sdl,groups))

    angle = 0
    attrs = {}
    for i in idx:
        angle+=fract
        attrs[sorteddeg[i][0]] = {'x':float(scale*(np.cos(angle))),'y':float(scale*(np.sin(angle)))}

    nx.set_node_attributes(G, attrs)

    nx.write_gexf(G,'centrality/circle_'+f.split('/')[-1])
