'''
Vary inputs, or use a latin hypercube for two inputs
'''
import pandas as pd
import numpy as np
import pyDOE,argparse


parser = argparse.ArgumentParser()
parser.add_argument('--linspace' , action = 'store', dest='lns')
parser.add_argument('--lhc' , action = 'store', dest='lhc')
parser.add_argument('--basename' , action = 'store', dest='base')
args = parser.parse_args()

if args.base==None: args.base='base.csv'

df = pd.read_csv(args.base,header=2)
spindex = dict(zip(df.Species,df.index))

print type(args),args.lhc

def write(df):
    df.to_csv('formatted.csv',index=False)
    
    with open('formatted.csv','r+') as f:
        file_data = f.read()
        f.seek(0, 0)
        f.write('Commissioned for Pete Edwards \n%s\n'%(','.join(df.columns))+file_data)
        

if args.lns and args.lhc == None:
    fract = np.array(args.lns.split(',')).astype('int')
    fract = np.linspace(*fract)
    print fract
    cycle = set(df.loc[df.Index=='ii','Species']) ^ set(list(df.Species)) ^ set(['O3','H2'])

    for i in cycle:
        counter = 0 
        for j in fract:
            counter+=1
            
            copy = np.array(df.BaseRun[:])
            copy[spindex[i]] = j 
            df['%s_%s'%(i,counter)] = copy
        
    write(df)

elif args.lns==None and args.lhc:
    inf = np.array(args.lhc.split(','))

    index = [spindex[i] for i in inf[[0,3]] ]
    lhc = pyDOE.lhs(2,samples=int(inf[-1])).T
    lhc [0] = lhc[0]*(int(inf[2])-int(inf[1])) + int(inf[1])
    lhc [1] = lhc[1]*(int(inf[5])-int(inf[4])) + int(inf[4])
    
    print lhc
    for i in xrange(int(inf[-1])):
        
            df['%s'%(i)] = np.array(df.BaseRun[:])
        
    df.loc[index,[str(y) for y in xrange(int(inf[-1]))]]=lhc
    
    write(df)
    
    
else:
    print '''
    run with one of args:
    --linspace=from,to,npoints  (--linspace=0,10,20)
    --lhc=spec1,min1,max1,spec2,min2,max2,nsamples  (--lhc=NOX,0,5,BVOS,0,22,100)
    '''

print 'END'




#print parser.parse_args()
 
''' 
 #
 # Replace line 
 # 62 os.system("./InitCons/makeics.pl %s"%ic_file)
 # with:
 
ic_open= tuple(open(ic_file))
run_names = np.array([i for i in enumerate(ic_open[2].strip().split(',')[3:])])
descriptions = np.array([i for i in enumerate(ic_open[1].strip().split(',')[3:])])

data = np.array([i.strip().split(',') for i in ic_open]).T
time = data[3,3]
data = data[1:,4:]

##make ics 
np.savetxt('Init_cons.dat', data, fmt='%15s', delimiter='!', newline='\n', header='%s'%time,comments='')

'''
