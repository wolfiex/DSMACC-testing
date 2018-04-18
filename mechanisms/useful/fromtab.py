from pandas import* 

names = read_csv('tabula-acp-15-9983-2015-supplement-3.csv')

data = read_csv('smiles_mined.csv')

n = [i.upper() for i in names.Name]

names.Name=n

syn = []
for i in np.array(data):

    if str(i[4])=='nan': continue
    else:
        for j in i[4].split(';'):
            syn.append([j.upper(),i[1]])
            
            

syn = dict(syn)


n2 = []
c = 0
d = ''
for i in n:
    try: 
        n2.append(syn[i])
        c+=1
        d += '%d,%s,1,%e\n'%(c,syn[i],float(names[names.Name==i].pptv)*1e-12)
    except Exception as e:
        q=1
        #print e,i,names[names.Name==i]
        #n2.append(i)
        
print ' '.join(n2)

with open('output.csv','w') as f:
    f.write(d)



