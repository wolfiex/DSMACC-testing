name = "reformat"
from ..helperscripts import picker
import glob,sys,os,re,pathos
import pandas as pd
import numpy as np
from sympy import Symbol, expand, N

def iseqn (x):
    #find equations
    if (re.search(r'\{[\. \s\d]*\}', x)): 
        return True

def pool_eqn(x):
    #sort the reactions
    r,p=x[0].split('=')
    p=p.split('+')
    p.sort()
    r=r.split('+')
    r.sort()
    if co2:
        cdiff=sum([smiles[nocoeff.sub('',i)] for i in p])-sum([smiles[nocoeff.sub('',i)] for i in r])
        if cdiff<0: p.extend(['CO2']*abs(cdiff))
        else:  p.extend(['CO2']*cdiff)
        
    
    p='+'.join(p)
    r='+'.join(r)
    x[0] = r+'='+p
    #replace D and exp for sympy  re.sub(r'(\d)[dD]([+-\.\d])',r'\1e\2',  x[1].split('//')[0].replace('EXP','exp')
    x[1] =  x[1].split('//')[0].replace(';','')
    return x

def reformat_kpp(inorganics,depos,available_cores = 1,co2 = False,decayrate = (1./(24.*60.*60.))):
    '''
    
    co2 - adds co2 to MCM
    '''
    
    
    file_list = picker.Picker('mechanisms/*.kpp',remove=['mechanisms/','.kpp'],title = 'Select Mechanisms').getSelected()
    
    
    if co2:
        print 'edit co2 path'
        smilesdf = pd.read_csv('../src/background/smiles_mined.csv')
        smiles=pd.Series(smilesdf.smiles)
        smiles.index=smilesdf.name
        smiles['CO']='C'
        smiles['CO2']='C'
        smiles['DUMMY']=''
        smiles['NA']=''
        smiles =dict(zip(smiles.index,[str(i).upper().count('C') for i in smiles]))
        
    
    file_text = [open('mechanisms/%s.kpp'%i,'r').read() for i in file_list]
    
    if inorganics: 
        file_list.append('inorganics')
        file_text.append(open('src/background/inorganic_mcm.kpp','r').read())


    if file_list == ['inorganics']: sys.exit('You forgot to enter a file to reformat')

    fullstr='~'.join(file_text)
    
    
    
    inline = re.findall(r'[\n\b\s]#inline.+?#endinline',fullstr,re.IGNORECASE|re.M|re.S)

    minfull = re.sub(r' |\n|\t|\s|\r','', fullstr).upper()
    

    
    eqn = [i.split(':') for i in re.findall(r'[^/]{2}\s*\{[\.\W\s\d]*?\}([^;]+)' ,'   '+minfull,re.S|re.M)]
    
    
    nocoeff = re.compile(r'\b\d*\.*\d*([\W\d\w]+)\b')
    specs = []
    if co2:specs=['CO2']
    
    for e in eqn:specs.extend(re.findall(r"[\w']+", e[0]))
        
    specs = list(set((nocoeff.sub(r'\1',i) for i in specs)))
    specs.sort()
    
    
    if depos: 
        decayrate = '%.4e'%(decayrate)
        for i in specs:
            eqn.append([i + ' = DUMMY',decayrate])
            
    #replace RO2str
    ro2str ='\nRO2 = C(ind_'+ ') + C(ind_'.join(re.findall(r'ind_([\W\d\w]+?\b)',minfull,re.I))+')'
    
    for i in range(len(inline)):
        if 'RO2 =' in inline[i]:#re.match(r'\bRO2 *=',inline[i]):
            inline[i] = re.sub(r'RO2\s*=[\s&.\w\W]+C\(\s*ind_.+\)',ro2str,str(inline[i]),re.I|re.M|re.DOTALL)
            
    
    

    tofile = [
    '// reformatted by reformat.py', 
    '// contact: daniel.ellis.research@googlemail.com',
    '// filedata: %s'%(' + '.join(file_list)),
    '// %s species  %s reactions'%(len(specs),len(eqn)),
    '// Constant DEPOS = %s'%depos,
    ' ',
    '#INCLUDE atoms',
    ' ',
    '#DEFVAR'
    ]
    
    for i in specs:
        if i == 'DUMMY': continue
        tofile.append(i + ' = IGNORE;')
        
    tofile.extend([' ','#EQUATIONS'])
    
    for i,j in enumerate(eqn):
        if j[0][-1]=='=':j[0]+='DUMMY'
        tofile.append( '{%04d} %s : %s;'%(i,j[0],j[1]) )
        
    tofile.extend([' ','// inlineFNs'])
    

        
    
    ic_file = re.sub('\.\./InitCons/|\.csv|\.\./src/background','', '_'.join(file_list))

    line = re.compile(r"(.{1,75}[\s\n ])",re.M|re.S)# 75 char per line
    with open("mechanisms/formatted_"+ic_file+'_%s.kpp'%depos, 'w') as f:
        for l in tofile:
            
            
            #split into kpp happy lengths
            split = line.findall(l)
            
            if len(split)>1 :
                
                
                if re.match('\s*//.*', l):
                    f.write('\n//'.join(split)  )
                else : 
                    f.write('\n'.join(split) )
            else:
                f.write('\n'+l)  
                
        for i in inline:
            for l in i.split('\n'):
                split = line.findall(l)
                if len(split)>1 :f.write('&\n'.join(split) )
                else:f.write('\n'+l)                  
                        
        


    print "\n formatted_"+ic_file+' written'
        
        
        
    
    


if __name__ == '__main__':
    print 'lets go - quickstart with inorganics and depos'
    reformat_kpp(True, True)