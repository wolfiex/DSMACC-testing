
smileslist = tuple(open('smiles_mined.csv'))

newlist = []

   
match= '=N,O,OO,C(=O),C(O)O,C(O)OO,OC(O)O,S,SS'.split(',')

matchend= 'F,Cl,Br,I,NO,ONO,OONO,NO2,ONO2,OONO2,C(O)OONO2,N,C#N,OH,OOH,CHO,C(O)OH,C(O)OOH,OC(O)OH,SO4,SO5,SO6,SO7,SO3,S'.split(',')

#namematch='NH2,NH,=NH'

match.sort(key=lambda item: (-len(item),item))
matchend.sort(key=lambda item: (-len(item),item))


for row in smileslist[1:]:
    row=row.split(',')
    if row[2]== '':
        #print row[1]
        continue
    smiles = row[2]
    array = []
    for m in matchend:
        if row[2][-len(m):] == m:
            array.append(m)
            row[2]=row[2].replace(m,'x')
        else: array.append('')
        
            
    for m in match:
        if m in row[2]:
            array.append(m)
            row[2]=row[2].replace(m,'x')
        else: array.append('')
            
   
            
    newlist.append([row[1],smiles,array])
    
if 1: 
    import pandas as pd
    import numpy as np
    groups = pd.DataFrame([i[2] for i in newlist])
    
    groups.columns = ['-'+i for i in matchend]+['-'+i+'-' for i in match]
    groups.index= [i[0] for i in newlist]
    
    import seaborn as sns; sns.set()
    import matplotlib.pyplot as plt
    plotgroup = groups!=''
    
    plotgroup = plotgroup.loc[:,plotgroup.sum() >0]
    
    
    
    ax = sns.heatmap(plotgroup.multiply(np.array(plotgroup.sum(axis=1)),axis=0))#,cmap='YlGnBu')
   
    #plotgroup.sum().plot(ax=ax)
    
    plt.show()    
    
