import re,multiprocessing 
import pandas as pd 
global data,r,tuvdata,i,remapping

data  = tuple(open('FJX_j2j.dat'))[1:-1]
r = re.compile(r"\b[A-z][\-\w\)\.\(]*")
r2 = re.compile(r"\b[A-z][\-\w\)\.\(]*\b")
i = re.compile(r"[0-9]+\b")
skip =  re.compile("-[^>]")

ncores = 4 

tuveqnstart = 49

inmcm = {'10': '41',
 '11': '4',
 '12': '6',
 '13': '5',
 '14': '13*.99',
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
    selection = [ii.replace(" ",'') for ii in match[2:-1]]
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
        
def sort (x):
    match = r2.findall(x.replace('(','z1').replace(')','z2').replace(' )',')'))
    reaction = match[0].replace(' ','').replace('z1','(').replace('z2',')') + ' -> '
    selection = [ii.replace(' ','').replace('z1','(').replace('z2',')') for ii in match[1:]]
    selection.sort()
    reaction += ' + '.join(selection)
    return reaction

#sort by most occurring tuv number

fastjx = multiprocessing.Pool(ncores).map(fjx_eqn,data)
fjxdict= dict(fastjx)
tuvdata = tuple(open('../../../TUV_5.2.1/INPUTS/MCMTUV'))[tuveqnstart-1:-1]

tuv = dict(filter(lambda x: x!=None, multiprocessing.Pool(ncores).map(tuv_eqn,tuvdata)))

#read and update with mcm jvals 
mcm2t = [i.split(':') for i in tuple(open('MCM331.db'))]

mcm2tuv = pd.DataFrame(mcm2t, columns = ['j','coeff','rct'])

mcm2tuv['tuvrnno'] = [int(str(tuv[sort(ii[1:-1])]).replace(' ','')) for ii in  mcm2tuv.rct]

mcm2tuv.j = [int(i) for i in mcm2tuv.j]

mcm2tuv.coeff = [i.replace(' ','') for i in mcm2tuv.coeff]

def flexmcmtotuv(x):
    name = x.split('*')
    loc = mcm2tuv[mcm2tuv['j']==int(name[0])]
   
    try: coeff = float(name[1])
    except: coeff = 1
    
    try:
        coeff = coeff + float(loc['coeff'])
    except: None
    
    if coeff != 1: 
        coeff = '*' + str(coeff) 
    else:
        coeff = ''   
    return   str(int(loc['tuvrnno'])) + coeff  
       
fast2tuv =dict(zip(inmcm.keys(), [flexmcmtotuv(x) for x in inmcm.values()   ]))

fast2tuv['50'] = 131
fast2tuv['51'] = 132


mapping = [
        
['O','O(3P)'],['ClNO3','ClONO2'],['ClNO2','ClONO'],['HO','OH'],['BrNO3','BrONO2'],['BrNO2','BrONO']


]
#fast, tuv
direct_mapping = {
26:94,
36:9,
37:119,
38:110,
39:111,
40:112,
41:113,
42:102,
43:105,
44:106,
50:131,
56:132,
77:69,
84:41,


}


remapping = [ [re.compile(r"\b"+i[0]+r"\b"), i[1]] for i in mapping ]

def ismatch (x):
    try: return tuv[x[1]]
    except:
        idn= x[0]        
        x=x[1]
        try: return fast2tuv[str(idn)]
        except: 
            for i in remapping:
                
                x = i[0].sub(i[1],x).split('->')
                
                p = x[1].split('+')
                p.sort()
                x[1]= '+'.join(p)
                x = '->'.join(x)
                print x 
        
        try:  return tuv[x]    
        except:
            #try direct mapping 
            try:  return direct_mapping[int(idn)]
            
            except:
                return None




for x in fastjx: ismatch(x)



found  = multiprocessing.Pool(ncores).map(ismatch,fastjx)


toadd =[6,25,34,66,70,93,94,94,96,97,99,100,104,105]
for i in enumerate(found,1): print i 







results = filter(lambda x: x[1]!=None, enumerate(found,1 ))


string = '''
SELECT CASE(jl)
'''

for i in results:
    n1= int(str(i[1]).split('*')[0])
    try: coeff = str(i[1]).split('*')[1] + ' * '
    except: coeff=''
    n2= int(str(i[0]).split('*')[0])
    string += '''
    CASE(%3d) !%s
        j(%3d) = %s seval(szabin,theta,tmp,tmp2,b,c,d)!%s
        ''' %(n2, fjxdict[n2], n1, coeff,tuvdata[n1][5:-1] )


string += '\nEND SELECT'

with open('../../../TUV_5.2.1/GC11.inc','w') as f: f.write(string)




missing = [ [n,fjxdict[n]] for n in toadd]



