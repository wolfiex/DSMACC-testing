#!/usr/bin/python
''' 
Simplifying the rate coefficients of DSMACC using the sympy symbolic simplification library

Creates a Param definition file, and a variable definition file. 


daniel.ellis@york.ac.uk 2017
'''


from sympy import * 
import re, numpy,sys

## Rate file we wish to open
filename = sys.argv[1]#'new_rate.inc'
data = tuple(open(filename))





#convert data to string for regex
nonreal,string= [],'';
for i in data: string+= i; datalower=str(string).lower()

#get constants
constants = re.findall(r'\b(\w+)\b\s*=',datalower)
for i in constants + ['temp','m','o2','h2o','LOG10']:  exec(i + '= symbols("%s")'%i)
#dictionary of coefficients
coeff_d = dict([[j,i] for i,j in enumerate(constants)])

#equations associated with rates
eqns = [ re.sub(r'(\d)[d]([\W\d])', r'\1e\2' , eq ) for eq in  re.findall( r'\b\w+\b\s*=\s*([\S ]+)\n', datalower)] #keep the pesky space in the brackets - python re is still weird




## First pass from equation simplification 
#- this round identifies equations that are exclusively numeric
for i,j in enumerate(eqns): 
    const = constants[i]
    try:
        spfd = False
        exec( 'dummy  =  N(%s,3)' %(j))
        exec( 'if (dummy.is_real): spfd = True')
        if spfd:  locals()[const]= dummy
        else:  nonreal.append(const)
    except NameError as e:
        nonreal.append(const)

## Second pass 
for name in nonreal:

     # if a kr rate constants simplify using unedited combinations of equations from variables. 
     if 'kr' in name:
         cffs = re.findall(r'\b([A-z]\w*)\b',eqns[coeff_d[name]])
         for i in cffs+[name]:
            try:
                exec('%s = symbols("%s")'%(i.upper(),i.upper()))
                exec( '%s = %s'%(i.upper(),eqns[coeff_d[i]] ))
            except KeyError:
                None
         exec('%s = str(N(expand(%s),3))'%(name.upper(),eqns[coeff_d[name]].upper()))
      
     # otherwise simplify without substituting any other coefficients 
     else:
         j = eqns[coeff_d[name]]
         exec('%s = symbols("%s")'%(name.upper(),name.upper()))
         try:
            exec( '%s  =  N(%s,3)' %(name,upper(),j))
         except NameError as e:
            neweqn = re.sub(r'mpmath.log10\(('+'|'.join(nonreal)+')\)',r'LOG10(\1)',j.replace('log10','mpmath.log10'))
            exec( '%s = N((%s),3)' %(name.upper(),neweqn))

          
for i in nonreal: locals()[i] = str(locals()[i.upper()]) # overwrite original labels with new values  
        
        
       
    
import pandas as pd
#check if numeric and get values 

def numeric(x): 
    try: float(x); return True; 
    except: return False
    
values = [str(locals()[i]) for i in constants]
fixed = [numeric(i) for i in values]

#Create a table from the data
df = pd.DataFrame([eqns,values,fixed],columns=constants,index=['original','simplified','parameter']).T

## split into variable and fixed rate constants
save = df[df.parameter]
variable = df[df.parameter==False]

definitions = 'Real(dp) :: '+ ','.join(variable.index) + '\n' 
for i in save.iterrows():
    definitions += 'Real(dp),PARAMETER ::'+ i[0]+' = '+ i[1].simplified + '\n'

variables = ''
for i in variable.iterrows():
    variables +=  i[0]+' = '+ i[1].simplified.lower() + '\n'


with open(filename+'.def', 'w') as f:
    f.write(definitions)
with open(filename+'.var', 'w') as f:
    f.write(variables)


print 'completed' 

