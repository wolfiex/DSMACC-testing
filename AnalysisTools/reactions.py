import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
global mixedform


full = tuple(open('full_mcm.kpp'))

species,reactions=[],[]


for item in full:
    if 'IGNORE' in item:
        item=item.replace(' ','').split('=')[0]
        species.append(item)
    

location = dict(zip(species,xrange(len(species))))
mixedform = [[] for i in species]
count = [1 for i in species]
    
for item in full:
    if '.}' in item: 
        item = item.split('}')[1].replace(' ','')
        item = item.split(':')[0].strip('\t')
        reactions.append(item)
        
        item = item.split('=')
        prod = item[1].split('+')
        prod = [location[i] for i in prod]
        
        for element in item[0].split('+'): 
            index = location[element]
            
            mixedform[index] = mixedform[index] + prod  
            count[index]+=1   
            
mixedform = [set(i) for i in mixedform]



def get_produced (indexno):

    z = mixedform[indexno]

    while True:
        x = z
        y=[]
        for i in x: y.extend(mixedform[i])
        y = set(y)

        z = set(list(z)+list(y))
        x = y ^ z 
        

        
        if x == set(): break
        
    return z



spec_list = [get_produced(i) for i in xrange(len(species))]
    
spec_length = [len(i) for i in spec_list]

spec_count =[sum([count[j] for j in i]) for i in spec_list] 




order = pd.Series(spec_length)
order.sort_values(inplace=True)

count_ordered = [spec_count[i] for i in order.index]
 

plt.plot(order, count_ordered)
#plt.xlabel('number of species spawned')
#plt.ylabel('number of edges associated with these')


#plt.show()


order2 = pd.Series(spec_length)
#order2.index = species
order2.sort_values(inplace=True)
name=order2.index
order2.plot()
#plt.xticks(name,rotation=90, fontsize = 5)
plt.ylabel('Number of secondary species')
plt.xlabel('species name')

plt.show()


ratio = [spec_count[i] / 0.0001+spec_length[i] for i in xrange(len(spec_length))]
    
ratiodf = pd.Series(ratio)
ratiodf.index = species
ratiodf.sort_values(inplace=True)
ratiodf.plot()

#plt.xticks(name,rotation=90, fontsize = 5)
plt.ylabel('links/nodes')
plt.xlabel('primary species name')

plt.show()




