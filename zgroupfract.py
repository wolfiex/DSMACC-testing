from zhdf import *
import time

groups = eval(tuple(open('groupslimited.txt'))[1])



print groups[1]


a = new('cri22.h5')

for g in groups:
    print g
    sm = a.spec[g].sum(axis=1)
    for s in g:
        frac = (a.spec[s]/sm).compute()
        print s, frac.mean()
        frac.plot()
        
    #time.sleep(11 )  
    input('')  
    plt.clf()
    
    print '' 