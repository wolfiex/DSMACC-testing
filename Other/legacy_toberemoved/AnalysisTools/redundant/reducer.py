import re
import multiprocessing
import pandas as pd

''' program to search for duplicates in Linear algebra file and simplify '''
''' outcome was that there are not really any duplicates'''


min_limit = 0


data = open('model_LinearAlgebra.f90').read()#.split('SUBROUTINE KppSolve ')
#section
m = re.findall ( r'SUBROUTINE KppSolve\s(.*?)SUBROUTINE KppSolve', data, re.DOTALL)
#link
l = re.sub(r'\s*\&[\s\\n]+\&\s*','', str(m))
#rows
r= l.split('\\n')
#seperated reactions
reactions = [re.split('[=/]', i.replace(' ',''))for i in r ]


def seperate(x):
    length = len(x)
    if (length < 2):  return set([])
    else: 
        #print len(re.split('\)', x[1])) #cant use ( as some are multiplied
        return set(re.split('\-', x[1]))

        #')'.join(seperate(reactions[-5]))
               
# items
items = multiprocessing.Pool(2).map( seperate , reactions ) 
#link array for replacements
simplify = []




while True: 


    multiples = lambda(x): [[v for v in x & y if v] for y in items]      

    matches = [multiples(i) for i in items]
    
    

    combinations= [[len(y) for y in x] for x in matches]

    maxlen= pd.Series([sorted(y,reverse=True)[1] for y in combinations])

    maxlen = maxlen[maxlen>min_limit]

    maxlen.sort(ascending=False)


    if len(maxlen)==0: break

    group_id = maxlen.index[0]

    max_item = pd.Series(combinations[group_id])

    max_item.sort(ascending=False)

    match_id = max_item.index[1]



    replace =  set(matches[group_id][match_id])
    counter = len(simplify)
    

    items[group_id] = set(list(items[group_id] ^ replace) + ['+sim%s'%counter])
    items[match_id] = set(list(items[match_id] ^ replace) + ['+sim%s'%counter])
    
    items.append(replace)#incase further matches appear within here
    
    simplify.append(list(replace))
    print counter, len(replace)



for i in xrange(len(reactions)): 
    if (len(reactions[i])>1 ):  
        items[i] = list(items[i])
        items[i].sort(reverse=True)
        '''
        if items[i][-2][0]=='(': #formatting fix
            dummy = items[i][0]
            items[i][0] = items[i][-2]
            items[i][-2]= dummy 
            items[i].append('')
        '''
        reactions[i][1] = '-'.join(items[i])    

        dummy = reactions[i][0] + ' = ' + reactions[i][1]
        try: reactions[i] = dummy + '/' + reactions[i][2]
        except: reactions[i] = dummy 
    else: reactions[i] = reactions[i][0]

updated = '\n'.join(['SUBROUTINE KppSolve'] + reactions ) + ' SUBROUTINE KppSolve'


datanew = re.split( r'SUBROUTINE KppSolve\s', data)
datanew[1] = updated

datanew = '\n'.join(datanew)
f = open('testfile.f90','w')
f.write(datanew)
f.close()

