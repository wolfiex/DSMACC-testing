import re,os

tol= 90
glist = [eval(i) for i in tuple(open('centrality/newsubgroups.txt'))]
#glist = filter(lambda x:(int(x[1])>tol) & (int(x[1])<101),glist)

inorganics = ''.join(open('src/background/inorganic_mcm.kpp','r').readlines())
inorganics = re.findall(r'\b([\w\d]+)\s*=\s*IGNORE',inorganics)
inorganics.append('CO')

'''
flist = [ filter(lambda x:  x not in inorganics, i[2].split('-')) for i in glist]
flist = filter(lambda x: len(x)>1,flist)
'''
flist = filter(lambda x: len(x)>1,glist)

flatlist = [i for j in flist for i in j]


import numpy as np
data = np.load('lhsgroupfract.npy')

data = data[0]

#data[xrange(0,len(data),len(flatlist)),0]

means = dict([[j,np.array(data[xrange(i,len(data),len(flatlist)),0]).mean()] for i,j in enumerate(flatlist)])

std = dict([[j,np.array(data[xrange(i,len(data),len(flatlist)),0]).std()] for i,j in enumerate(flatlist)])



import matplotlib.pyplot as plt

rmlist = []

lumplist = []
splitlist_day = dict()
splitlist_night = dict()

col = ['red','green','blue','orange','black','cyan','magenta','purple',
'yellow','pink','grey','maroon','yellow','pink','grey','maroon','yellow','pink','grey','maroon','navy']



os.system(' rm centrality/p_*.pdf' )

day = range(0,8)+range(17,32)+range(41,56)+range(65,72)
night = range(8,17)+range(32,41)+range(56,65)
daynight =[day,night]

for j in flist:

    plt.figure()
    percent  =  ''
    dummy=[]
    for n,i in enumerate(j):
        for sun in [1,0]:#day night
            d = means[i][daynight[sun]]

            m = d.mean()
            md = [m]*len(d)
            sd = d.std()
            s = std[i][daynight[sun]]

            lw = m-s-sd
            hw = m+s+sd

            x = range(len(d))

            #print i, s.mean(), sd
            
            
            if sun == 0 :
                            splitlist_day[i]=m
            else:
                            splitlist_night[i]=m

            if m == 0 :
                print 'precursor or dead', i,sun
                rmlist.append(i)
                continue

            #fill band
            #plt.fill_between(x,lw,hw,color=col[n],                alpha=0.2,label=None)

            #line
            percent = '%.8f '%(m*100)

            plt.plot(x,d, label=i+' %d +- %e %s'%(float(percent),s.std(),['day','night'][sun]),c=col[n],alpha=0.8)
            #plt.plot(x,md, label=i,c=col[n])

            
            
        dummy.append(i)
    if len(dummy)>1:
        lumplist.append(dummy)


    plt.ylim(ymin =0,ymax=1)
    plt.legend()
    plt.xticks([])
    plt.yticks([])

    plt.title(' '.join(j))
    plt.savefig('centrality/p_'+'_'.join(j)+'.pdf')
    plt.clf()

splitlist = dict()
for i in flatlist:
    dummy  = '(ISDAY * %.3e + ISNIGHT * %.3e)'%(splitlist_day[i],splitlist_night[i]) 
    splitlist[i]  = dummy.replace('e','D').replace("'",'"')
    


with open('lhsgrouplimited.txt','w') as f:
    f.write(('lumplist = %s ;\n'%lumplist).replace("'",'"'))
    f.write(('keys = %s ;\n'%splitlist.keys()).replace("'",'"'))
    f.write('values = %s ;\n'%(splitlist.values()))
    f.write(('specval = Dict(zip(keys,["( $i )" for i in values]))').replace("'",'"'))


print 'montage'

os.system('montage centrality/p_*.pdf -geometry 800x800+0+0 groups.png')
