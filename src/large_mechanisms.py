'''
When large mechanisms are used with kpp, these often break the compiler consinuation line and character limits. 
It is therefore required that lines are split into smaller groupings. 

This is a program that does just that, abeit a bit crudely. 

Daniel Ellis 
daniel.ellis.research@googlemail.com 
daniel.ellis@york.ac.uk 
2017

'''


import os, sys, multiprocessing,re
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


file_name = sys.argv[1]

os.system('cp %s  %s.bak'%(file_name,file_name))#make a backup copy 

###################fn 
def checker (line, c_lim = 210 , l_lim = 200): 
        #c_lim = 210   #ff 7190# fix2048 #1400  #210 //continuation lines
        #l_lim = 200  ##511 character limit
        dummy=True #do not change
        
        #save 100s of lines of code
        if 'JUV(1)' in line:
            jval = re.findall('\d+', line)
            return ['do i = %d,%d\n'%(int(jval[0]),int(jval[-1])), 
               'JUV(1) = JUV(1)+ JVS(i)*UV(i)\nend do\n\n' ]
        
        elif 'X(1) = (X(1)' in line:        
            split = line.split('/')
            line = split[0]                   
            jval = re.findall('\d+', line)
            return ['do i = %d,%d\n'%(int(jval[0]),int(jval[-1])), 
               'X(1) = X(1) -JVS(i)*X(i)\nend do\n\n',
               'X(1) = X(1)  / (JVS(1))\n']
                      
               
               
        elif 'REAL(kind=dp) :: UV(NVAR)' in line or 'REAL(kind=dp) :: X(NVAR)' in line: 
            return [line, 'REAL(kind=dp) :: j_DUMMY\n' , 'INTEGER :: I\n']
            
        elif len(line) > c_lim:
            if '/' in line:
                line = line.replace(' ','')
                m = re.findall('=\((.*)\)/',line)[0]
                jval =re.findall(r'[+-]{1}[A-z0-9*\(\)]{1,40}', m)
                line1 = 'j_DUMMY'
                replace = [line1+'= 0.\n']+[line1 + '=' + line1 + i +'\n' for i in jval] 
                replace = replace+[line.replace(m,'j_DUMMY')+'\n']
                return replace

            else:
                split = line.split('=')
                line1 = split[0]                   
                jval =re.findall(r'[+-]{1}[A-z0-9*\(\)]{1,40}', split[1])
                print jval
                return [line1+'= 0.\n']+[line1 + '=' + line1 + i +'\n' for i in jval] 
    
        
            
        else: return [line]
   

######################################################################################################
####################################program run files#################################################
######################################################################################################

ncores=4



if 'Jacobian' in file_name or 'Linear' in file_name: 
    os.system ("/usr/bin/perl -p -i.bak -e 's/&[\n\r]//g;s/\s*&//g' %s"%file_name)#remove newlines using perl
    data = tuple(open(file_name))
    output = multiprocessing.Pool(ncores).map(checker,data)


else: # fix RO2 for non Jacobian or Linear Algebra Files  ie model.rates
    output = list(open(file_name))
    print 'else'
    strip = False
    data = ''
    
    for line in xrange(len(output)):
        current = output[line].replace(' ','')
        if bool(re.match('RO2.*=.*&.*', str(current))): 
            print 'RO2 found',current
            strip = True
        if strip:
            if 'CALL' in current: 
                strip=False
                string = 'RO2 = 0.\n'
                ro2data = re.findall( r'C\(ind_([A-z0-9]+)\)',data)
                for i in ro2data:
                    string += 'RO2 = RO2 + C(ind_%s) \n '%i
                output[line] = string + '\n' + output[line]

            else: 
                data += current
                output[line]=''
                

    
    #output = multiprocessing.Pool(ncores).map(checker,data)
     
newdata=['! parsed by large_mechanisms.py D.Ellis 2017\n']
for item in output: newdata.extend(item)   

f=open(file_name,'w')
f.writelines(newdata)
f.close()

print 'parsed ', file_name


