from sympy import * 
import re, numpy

global data,constants,eqns

data = tuple(open('new_rate.inc'))
datalower=str(data).lower()


constants = re.findall(r'\b(\w+)\b\s*=',datalower)
constants.append('temp')
constants.append('m')
constants.append('o2')



eqns = [ re.sub(r'(\d)[d]([\W\d])', r'\1e\2' , eq ) for eq in re.findall( r'=\s*(\S+)\\n', datalower.replace('log10','mpmath.log10'))]

#eqns = [re.sub(r'log10\((.*[^\)])\)', r'log(\1,10)', eq) for eq in eqns]

for i in constants:
    exec(i + '= symbols("%s")'%i)

for i,j in enumerate(eqns): 
    print i
    try:
        exec( '%s  =  simplify(%s)' %(constants[i],j))
        exec('print ' + constants[i])
    except TypeError:
        continue

for i,j in enumerate(eqns): 
            print i
            try:
                exec( '%s  =  expand(%s)' %(constants[i],j))
                exec('print ' + constants[i])
            except TypeError:
                continue



log10=symbols('log10')
for i,j in enumerate(eqns): 
    print i
    exec( '%s  =  expand(%s)' %(constants[i],j.replace('mpmath.','')))
    exec('print ' + constants[i])


def review():
    for i in constants:
        exec('print ' + i)


from pandas import *

values = [locals()[i]for i in constants]

df = DataFrame([constants,values,eqns]).T
df

#replace *10** with D




