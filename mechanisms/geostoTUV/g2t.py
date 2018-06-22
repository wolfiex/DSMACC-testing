''' A quick and dirty method for matching up TUV and mechanisms (Geos) 
2018 D Ellis
'''


import re 

gcfile = ' '.join(tuple(open('../gc_v11-02_Standard.eqn')))

gcphoto = re.findall(r'\n\s*(.*=.*):\s*J\((\d+)\);', gcfile)
gcphoto.sort(key = lambda x:int(x[1]))

tuvfile = ' '.join(tuple(open('../../TUV_5.2.1/INPUTS/MCMTUV')))

tuvphoto = re.findall(r'\s*[TF]\s*(\d+)\s(.*->.*)\n', tuvfile)


gcdict = re.findall(r'\n\s*([\w\d]+)\s*= IGNORE;\s*{([\w\d]+);', gcfile)
gcdict = dict(filter(lambda c: len(set(c))>1,gcdict))


tuv = []
for i in tuvphoto:
    row = i[1].replace(' ','').split('->')
    row = [set(j.split('+')) for j in row]
    
    tuv.append((row,i[0]))


output =[]
nocoeff = re.compile(r'(\d*)\.*\d*(\w[\w\d]*)')
gcdict ['O1D'] = 'O(1D)'
gcdict ['O'] = 'O(3P)'
for i in gcphoto:
       found = False
       
       row = i[0].replace(' ','').replace('+hv','').split('=')
       row = [set([nocoeff.sub(r'\1\2',k) for k in j.split('+')]) for j in row]
        
        
       for n,j in enumerate(tuv):
            if row == j[0]: 
                found = (i[1],i[0],tuvphoto[n][0],tuvphoto[n][1])
                break
            

       if not found:
           row = [set([nocoeff.sub(r'\2',k) for k in j]) for j in row]            
           for n,j in enumerate(tuv):
                if row == j[0]: 
                                found = (i[1],i[0],tuvphoto[n][0],tuvphoto[n][1])
                                break
        
       if not found:
           #row = [set([nocoeff.sub(r'\2',k) for k in j]) for j in row]
           for q in [0,1]:
               dummy = []
               for k in row[q]:
                  try: int(k)
                  except:
                    try: dummy.append(gcdict[k])
                    except: dummy.append(k)          
               row[q]=set(dummy)
               
           
        
           for n,j in enumerate(tuv):
                if row == j[0]: 
                    found = (i[1],i[0],tuvphoto[n][0],tuvphoto[n][1])
                    break
                    
                    
       if not found:
          print '\n %s \n'%str(i)
          #Manual selection
          dummy = []
          
          react = set(i[0].replace(' ','').replace('+hv','').split('=')[0])
          prod = set(i[0].replace(' ','').replace('+hv','').split('=')[1])
          
          for n,w in enumerate(tuv):
            if (w[0][0] == react) or (w[0][1]==prod) or (w[0][0] == row[0]) or (w[0][1]==row[1]):
                    dummy.append(tuvphoto[n])
          
          
          for w in enumerate(dummy):print '\t', w
          
          if len(dummy)>0:
            try:
                j= dummy[int(raw_input('  Enter number for match. A letter or blank means none of the above.\n'))]
                found = (i[1],i[0],j[0],j[1])
            except:None
            
          
          
          
       output.append(found)
       
       
with open('GC11.inc','w') as f:

    f.write('''SELECT CASE(jl)
    !geos
    !tuv
'''   )
          
    for n,i in enumerate(output):
        if i:             
          f.write('''    CASE(%3d) !%s
       j(%3d) =  seval(szabin,theta,tmp,tmp2,b,c,d)!%s\n\n'''%(int(i[0]),i[1],int(i[2]),i[3]))
        else:
          f.write('''    CASE(%3d) !%s
       0 \n!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown\n\n'''%(int(gcphoto[n][1]),gcphoto[n][0]))
        
            
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          

