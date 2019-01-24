# -*- coding: utf-8 -*-
import time,re
import h5py,re,dask,os,sys
import numpy as np
import dask.array as da
import dask.dataframe as dd
import time
import progressbar

glist = [eval(i.strip()) for i in tuple(open('centrality/newsubgroups.txt'))]

# dtol = 90
#glist = filter(lambda x:int(x[1])>tol,glist)

inorganics = ''.join(open('src/background/inorganic_mcm.kpp','r').readlines())
inorganics = re.findall(r'\b([\w\d]+)\s*=\s*IGNORE',inorganics)
inorganics.append('CO')


flist = [ filter(lambda x:  x not in inorganics, i) for i in glist]
flist = filter(lambda x: len(x)>1,flist)

print len(flist), 'clusters'


#######

fl = 'lhs.h5'
maxtsps = int(144/2.)*3
desired = 24
tslst = range(1,(3*144)+1,6)#maxtsps/desired)
setsgroup= 4



run = True


data = [[]]*len(flist)
bar = progressbar.ProgressBar()

with h5py.File(fl,'r') as hf:
        groups = list(filter(lambda x: type(x[1])==h5py._hl.group.Group, hf.items()))
        print 'every '+str(setsgroup)+' groups'
        for gr in bar(groups[::setsgroup]):

            g=gr[1]
            if run:
                shead = g.attrs['spechead'].split(',')
                fhead = g.attrs['fluxhead'].split(',')

            spec = dd.from_array(g.get('spec')[1:,:],chunksize=50000, columns = shead)
            flux = dd.from_array(g.get('flux')[1:,:],chunksize=50000,columns = fhead)



            if run:

                #spec = spec.set_index('TIME', sorted=True)
                M =  spec.M.mean()
                spec = spec/M
                #flux = flux.set_index('TIME', sorted=True)

                shead = g.attrs['spechead'].split(',')
                fcol = g.attrs['fluxhead']

                products = [i.split('+') for i in re.findall(r'-->([A-z0-9+]*)',fcol)]
                prodloss = {k: {'loss':[],'prod':[]} for k in shead}
                ### reaction prodloss arrays
                for idx in xrange(len(products)):
                    for i in products[idx]:
                        try:prodloss[i]['prod'].append(idx)
                        except:None
                run = False

            print 'group ',g
            for gn,g in enumerate(flist):
                        sm = (spec.loc[tslst,g]).sum(axis=1).compute()*M
                        fx = [flux.loc[:,flux.columns[prodloss[s]['prod']]].sum(axis=1) for s in g]
                        sm = sum(fx)
                        for i,s in enumerate(g):
                            frac = fx[i]/sm
                            frac = frac.loc[tslst].compute()
                            std =  frac.std()
                            mean = frac.mean()

                            data[gn].append([frac,std,mean])
                        
                        #print g,gn


np.save('lhsgroupfract.npy',data)









fdsafdsaf=k



groups = eval(tuple(open('centrality/lhscollection.txt'))[2])



print groups[1]

a = new('cri22.h5')
maxtsps = len(ts)-144
desired = 24
tslst = range(144,len(ts),maxtsps/desired)
newts = ts[tslst]
percentstd = .05


print 'Percentage Tolerance %d%%'%(percentstd*100)
html = '''
<style>

@font-face {
    font-family: 'Datalegreya-Gradient';
    src: url('./Downloads/Datalegreya-Gradient.otf');
    font-weight: normal;
    font-style: normal;

}

body {
    background-color: #222;
    -webkit-font-feature-settings: "kern" on, "liga" on, "calt" on;
    -moz-font-feature-settings: "kern" on, "liga" on, "calt" on;
    -webkit-font-feature-settings: "kern" on, "liga" on, "calt" on;
    -ms-font-feature-settings: "kern" on, "liga" on, "calt" on;
    font-feature-settings: "kern" on, "liga" on, "calt" on;
    font-variant-ligatures: common-ligatures discretionary-ligatures contextual;
}

body {
    color:#ff9900
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;

}
body,h3,h4,h5,p{color:#ff9900;font-family: 'Datalegreya-Gradient', sans-serif;

text-align: center;}

p{
    font-family: 'Datalegreya-Gradient', sans-serif;
    /*color:#00ffdc;*/
    height:24;
    text-align: center;


}



</style>
<body>


<p>d|1a|0t|3a|2l|1e|2g|1r|3e|2y|1a|2 fd|2sfdsf</p>
{mean:13} h|1e|2l|3l|3o|0 |0w|1o|2r|1l|1d|3 {33    [-]  }{99   [+]}
<br>
<br><br>



'''
lumpfull =[]


grouplist=[]
groupcoeff=[]
M= M.compute()
for gn,g in enumerate(groups):
    print g
    #sm = np.log10(spec.loc[newts,g]).sum(axis=1)
    sm = (spec.loc[newts,g]).sum(axis=1).compute()*M
    html+='<h4> lmp %02d </h4>\n'%(gn+1)
    dummygroup=[]
    dummy = []
    fx = [flux.loc[:,prod(s)].sum(axis=1) for s in g]
    sm = sum(fx)
    for i,s in enumerate(g):
        #frac = np.log10(spec.loc[newts,s])/sm
        frac = fx[i]/sm
        frac = frac.loc[newts].compute()

        std =  frac.std()
        mean = frac.mean()
        inlim = ''
        if std>percentstd:
            print std,s,gn
            inlim = 'style="color:powderblue;"'


        line = list(' |'.join([str(int(i*4)) for i in list(frac)]))
        dummy.append([s,float(mean),float(std)])
        dummygroup.append(s)
        groupcoeff.append([s,'%.08f'%(mean)])
        count = 4
        for c in (s+'  %d%%'%(100*mean)).lower():
            line[count] = c
            count+=3

        html += '<!--%s-->\n<p %s>{std:%02d percent} §%s {%02.1f °[-]  }{%02.1f °[+]}</p>\n'%(s,inlim,100.*std,''.join(line),100.*frac.min(),100.*frac.max())
    if inlim == '':
        grouplist.append(dummygroup)


    lumpfull.append(dummy)
    html+='\n'


html+='</body>'
#print html

with open('test.html','w') as f:
    f.write(html)

with open('lump.mech','w') as f:
    f.write('lumplist = '+ str(grouplist).replace("'",'"'))
    f.write('\nlumpcoeff = '+ str(groupcoeff).replace("'",'"'))
