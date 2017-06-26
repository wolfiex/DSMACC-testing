import re,multiprocessing 
import pandas as pd 
global data,r,tuvdata,i,remapping

data  = tuple(open('FJX_j2j.dat'))[1:-1]
r = re.compile(r"\b[A-z][\-\w\)\(]*")
i = re.compile(r"[0-9]+\b")
skip =  re.compile(r".*\..*")

ncores = 4 

tuveqnstart = 49

inmcm = {'10': '41',
 '11': '4',
 '12': '6',
 '13': '5',
 '14': '13*0.99',
 '15': '7',
 '16': '8',
 '2': '2',
 '3': '1',
 '62': '13*0.01',
 '63': '23',
 '64': '24*0.5',
 '65': '24*0.5',
 '7': '11',
 '71': '34',
 '72': '33',
 '73': '31',
 '74': '32',
 '75': '22',
 '76': '21',
 '78': '41',
 '79': '41',
 '8': '12',
 '80': '41',
 '81': '41',
 '82': '41',
 '83': '41',
 '85': '41',
 '88': '41',
 '9': '3',
 '91': '41',
 '99': '41'} #FASTJX to MCM J 
 
 




def fjx_eqn (x):
    match = r.findall(x)
    id = int(i.search(x).group())
    reaction = match[0]+ ' -> '
    selection = match[2:-1]
    selection.sort()
    reaction += ' + '.join(selection)
    return [id,reaction]

def tuv_eqn (x):
        id = int(i.search(x).group())
        if skip.match(x): 
            print 'Ignoring: '+x.replace('\n','')
            return None
        match = r.findall(x)
        
        reaction = match[1]+ ' -> '
        selection = match[2:]
        selection.sort()
        reaction += ' + '.join(selection)
        return [reaction,id]


#sort by most occurring tuv number

fastjx = multiprocessing.Pool(ncores).map(fjx_eqn,data)


tuvdata = tuple(open('../../../TUV_5.2.1/INPUTS/MCMTUV'))[tuveqnstart-1:-1]

tuv = dict(filter(lambda x: x!=None, multiprocessing.Pool(ncores).map(tuv_eqn,tuvdata)))


mapping = [
['O','O(3P)'],['ClNO3','ClONO2'],['ClNO2','ClONO']


]

remapping = [ [re.compile(r"\b"+i[0]+r"\b"), i[1]] for i in mapping ]

def ismatch (x):
    try: return tuv[x[1]]
    except:
        x=x[1]
        for i in remapping:
                
                x = i[0].sub(i[1],x).split('->')
                
                p = x[1].split('+')
                p.sort()
                x[1]= '+'.join(p)
                x = '->'.join(x)
                print x 
        
        try:  return tuv[x]    
        except: return None




for x in fastjx: ismatch(x)



found  = multiprocessing.Pool(ncores).map(ismatch,fastjx)

