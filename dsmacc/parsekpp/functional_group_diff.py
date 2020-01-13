'''
Crude indicator of fn group reaction styles
Does not take coeff into account
'''

from .reactiontypes import reformat_kpp
from .. import datatables
__tableloc__ = datatables.__file__

mechlist = ['formatted_China_GCGC']

if 1==1:

    reactions  = reformat_kpp(mechlist,findcat=True,join=False).values
    print(reactions)
    import pandas as pd

    df = pd.read_csv('./'+__tableloc__.replace('__init__.pyc','functionalgroups_regexmatched.csv'))

    '''
    s = set(s.loc[map(lambda x: 'c' in str(x).lower(),s.smiles.values),:].name.values)&set(['CH4'])
    '''

    ignore = 'OH,HO2,NO,NO2,NO3,Cl,CL,O,O3'.split(',')

    eqn = [[rxn[0],rxn[1]] for rxn in reactions]
#####
#presplit!



    pl={}
    prodloss = {}
    for i,j in enumerate(eqn):

        print(j)
        for r in j[0]:
            try:
                prodloss[r].append(i)
                pl[r][0].append(i)
            except:
                prodloss[r]=[i]
                pl[r]=[[],[]]


        for l in j[1]:
            try:
                prodloss[r].append(i)
                pl[r][1].append(i)
            except:
                prodloss[r]=[i]
                pl[r]=[[],[]]

    nodes =  list(prodloss.keys())

    fngroups = df

    fngroups.index = fngroups['name']

    matches = list(set(nodes) & set(fngroups.index))
    fng = ['PAN', 'Carb. Acid', 'Ester', 'Ether',
       'Per. Acid', 'Hydro peroxide', 'Nitrate', 'Aldehyde', 'Ketone',
       'Alcohol', 'Criegee', 'Alkoxy rad', 'Peroxalkyl rad','Aromatic rings','Carbons','Atoms']
    print(fngroups)
    fngroups = fngroups.loc[matches,fng].astype(float)

    print('pall',fngroups)
    print(100*fngroups.astype(bool).sum()/len(fngroups))


    percent = (fngroups.sum()/len(df)*100).apply(lambda x:'%.2f'%x+'%').to_latex()


    radicals = 'OH,NO,NO2,NO3,OH,HO2,HONO,CO,O3'.split(',')
    for r in radicals:
        fngroups[r]= 0
        fngroups.loc[r,r]=1


    print('eqn')

    line =[]
    fail=0
    for i in eqn:
        try:line.append((fngroups.loc[i[1]].sum() - fngroups.loc[i[0]].sum()).values)
        except:
            line.append(fngroups.loc['CO'].values)
            fail+=1

    print(fail)
    import matplotlib.pyplot as plt

    import numpy as np
    line = np.array(line).astype(float)
    res ={}







    reactivity =[[],[]]

    for z,fn in enumerate(fng):

        for p in [0,1]:
            d = []
            [d.extend([x[z] for x in line[list(set(pl[i][p]))]]) for i in fngroups.index[fngroups[fn]>0]]
            reactivity[p].append(d)

        vals = [np.mean(line[list(set(prodloss[i]))],axis=0) for i in fngroups.index[fngroups[fn]>0]]
        dfn = pd.DataFrame(vals, columns = fngroups.columns)
        dfl = dfn[:].mean()

        c = np.zeros(len(dfl))
        c[fng.index(fn)] = 1
        c[-len(radicals):]=3
        cols='#4d9de0-#e15554-#e1bc29-#3bb273-#7768ae'.split('-')
        #print cols,c
        clrs =np.array([tuple(int(cols[int(j)].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))  for j in c])/255.0

        # get reaction reactiontypes
        gp = set()
        for spe in fngroups.index[fngroups[fn]>0]:
            gp = gp | set(prodloss[spe])

        print(gp)

        from collections import Counter
        cnt = Counter([reactions[i][-2] for i in gp])


        print(clrs)

        dfl.plot(kind='bar', color = clrs)
        plt.ylim([-1,1])
        plt.subplots_adjust(bottom=0.3)
        #plt.show()
        plt.savefig('fng_'+fn+'.pdf')
        plt.clf()
        res[fn] = dfl.to_dict()



howreact = abs(pd.DataFrame(reactivity[0])[pd.DataFrame(reactivity[0])<0]).mean(axis=1)
howreact.index = fng
