import glob
import multiprocessing as mp
from collections import Counter


f = glob.glob('lhsgroup/*.day') + glob.glob('lhsgroup/*.night')


def function(a):

    d=tuple(open(a))

    return list(['-'.join(set(i.strip().split('-'))) for i in d])


q = function(f[0])


pool = mp.Pool(16)



A =[]

r = pool.map_async(function, f, callback=A.extend)
r.wait()

print 'joining'
l = (i for j in A for i in j)


with open('grouplhscollected.txt','w') as fl:
        items = Counter(l).items()
        items = sorted(items,key=lambda x:x[1],reverse=True)
        print items[:20]
        for i in items:
            fl.write('%d,%d,%s\n'%(i[1],100.*(i[1]/float(len(f))),i[0]))
