# -*- coding: utf-8 -*-
from zhdf import *
import time

groups = eval(tuple(open('groupslimited.txt'))[1])



print groups[1]


a = new('cri22.h5')
maxtsps = len(a.ts)-144
desired = 24
tslst = range(144,len(a.ts),maxtsps/desired)
newts = a.ts[tslst]


html = '''
<style>

@font-face {
	font-family: 'Datalegreya-Gradient';
	src: url('./Downloads/Datalegreya-Gradient.otf');
	font-weight: normal;
	font-style: normal;

}

body {
	-webkit-font-feature-settings: "kern" on, "liga" on, "calt" on;
	-moz-font-feature-settings: "kern" on, "liga" on, "calt" on;
	-webkit-font-feature-settings: "kern" on, "liga" on, "calt" on;
	-ms-font-feature-settings: "kern" on, "liga" on, "calt" on;
	font-feature-settings: "kern" on, "liga" on, "calt" on;
	font-variant-ligatures: common-ligatures discretionary-ligatures contextual;
}

body {
	text-rendering: optimizeLegibility;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;

}
body,h3,h4,h5{font-family: 'Datalegreya-Gradient', sans-serif;

text-align: center;}

p{
	font-family: 'Datalegreya-Gradient', sans-serif;

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


for gn,g in enumerate(groups):
    print g
    sm = a.spec.loc[newts,g].sum(axis=1)
    html+='<h4> lmp %02d </h4>\n'%(gn+1)
    for s in g:
        frac = a.spec.loc[newts,s].compute()/sm.compute()
        line = list(' |'.join([str(int(i*4)) for i in list(frac)]))
        count = 4
        for c in s.lower():
            line[count] = c
            count+=3

        html += '<!--%s-->\n<p>{mean:%02d percent} §%s {%02.1f °[-]  }{%02.1f °[+]}</p>\n'%(s,100.*frac.mean(),''.join(line),100.*frac.min(),100.*frac.max())
    html+='\n'



html+='</body>'
print html
