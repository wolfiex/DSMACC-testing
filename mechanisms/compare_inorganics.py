import re 
import pandas as pd


class mechanism:
    '''reactions and rates in kpp file'''
    
    def __init__(self,filename):
        f = ''.join(tuple(open(filename))).strip('\s')
        f = re.sub(r'([\t ])', '', f)
        self.eqns = re.findall(r'\}(.*);',f)
        self.rate = [i.split(':')[1] for i in self.eqns]
        self.rcts = [set(i.split(':')[0].split('=')[0].split('+')) for i in self.eqns]
        self.prod = [set(i.split(':')[0].split('=')[1].split('+')) for i in self.eqns]
        self.len  = len(self.eqns)
    
    
    def compare (self,mech):
        same = []
        different = [] 
        exclusive_mine = []
        
        for i in xrange(self.len):
            found = False
            newrate=0
            for j in xrange(mech.len):
                if self.rcts[i] == mech.rcts[j]:
                    
                    if self.prod[i] == mech.prod[j]:
                        found = True
                        newrate=mech.rate[j]
                        #print self.rcts[i],self.prod[i], self.rate[i], mech.rate[j]
                        
                        
            if found : 
                if self.rate[i] == newrate: 
                    same.append(self.eqns[i])
                else:
                    different.append([self.rcts[i],self.prod[i], self.rate[i], newrate])
            
            else: exclusive_mine.append(self.eqns[i])
                    
        return {'exclusive':exclusive_mine, 'match':same,'change': different}    
            
            
        
        new
new = mechanism('33inorganics.kpp')
old = mechanism('32inorganics.kpp')

df = pd.DataFrame(old.compare(new)['change'])
df.columns = ['rct','prod','rateold','ratenew']
df.ratenew = df.ratenew.map(lambda x: x.replace('D','E'))

sameD = df[df.ratenew==df.rateold][['rct','prod']] 

