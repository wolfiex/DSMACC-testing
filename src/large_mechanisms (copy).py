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
               'X(1) = X(1) -JVS(5807)*X(5807)\nend do\n\n',
               'X(1) = X(1)  / (JVS(1))\n']
               
               
        elif 'REAL(kind=dp) :: UV(NVAR)' in line or 'REAL(kind=dp) :: X(NVAR)' in line: 
            return [line, 'REAL(kind=dp) :: j_DUMMY\n' , 'INTEGER :: I\n']
            
            
        '''
        elif len(line) > c_lim:
            
            continuation,counter = [],0

            #for divisions
            if '/' in line: 
                split = line.split('/')
                line = split[0]
                print 'this line contains a division, splitting'

            
            while counter+c_lim < len(line) :
                


                linesegment = line[counter:counter+c_lim]
                #update line length
                for match in re.finditer('[+-]', linesegment):continue
                previous = counter    
                loc = match.start()
                counter += loc

                continuation.append( '    &'+linesegment[ : loc] +'&\n')

                
                if (len(continuation) > l_lim):
                    #if not (re.match('.*=\s+\(.*', continuation[0])) and  dummy
                    if (re.match('.*=\s+.*', continuation[0])) and  dummy :
                            if (re.match('.*=\s+\(.*', continuation[0])):
                                continuation[-1] = continuation[-1].replace('&\n',')\n')
                                continuation.append( 'j_DUMMY = (0.0 &\n') 
                            else:  
                                continuation[-1] = continuation[-1].replace('&\n','\n')
                                continuation.append( 'j_DUMMY = 0.0 &\n') 
                            dummy = False;  print 'using j_DUMMY variable'
                          

                    elif dummy:   
                             
                        sys.exit( 'too many continuation lines' )          
                
                
            if len(line[ counter : ].replace(' ','')) >0: continuation.append( '    &'+line[ counter : ] +'&\n')
            

            
            continuation[0]= continuation[0].replace('    &','\n')
            continuation[-1] = continuation[-1].replace('&\n','')
            
            if len(continuation) > l_lim: 
                name = line.split('=')[0]
                continuation.append( '\n%s = %s + j_DUMMY\n' %(name,name))
                try: continuation.append('\n%s = %s / %s\n' %(name,name, split[1]))
                except:None
            else: 
                try: continuation.append(' / %s\n' %(split[1]))
                except:None
            
            
                
            print '------------------------'
            #for item in  continuation: print item
            print len(continuation), continuation[0][:18]
            return continuation     
       
        ''' 
        
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
        current = output[line]
        if bool(re.match('.*RO2.*=.*&.*', str(current))): 
            print 'RO2 found',current
            strip = True
        if strip:
            if 'CALL' in current: 
                strip=False
                string = '' 
                for i in checker(data.replace('&','').replace('\n','').replace(' ',''),c_lim = 2000): 
                    string+= i 
                string = re.sub(r"&\n    &", "\n    RO2=RO2", string)
                #limit to how many functions attached?
                print 'fdsfds',len(string.split('\n'))
                output[line]= string +'\n'+ current

            else: 
                data += current# checker(current.replace('&','').replace('\n',''))
                output[line]=''
                

    
    #output = multiprocessing.Pool(ncores).map(checker,data)
     
newdata=['! parsed by large_mechanisms.py D.Ellis 2017\n']
for item in output: newdata.extend(item)   

f=open(file_name,'w')
f.writelines(newdata)
f.close()

print 'parsed ', file_name


