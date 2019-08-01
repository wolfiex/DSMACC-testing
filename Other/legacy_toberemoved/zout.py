icfile='icname'

filename = '1_.spec'
h5file = 'test.h5'



from scipy.io import FortranFile
import numpy as np
import h5py,time, os,sys
sys.exit('old')

### make new hdf file
try: os.remove(h5file)
except : None
hf = h5py.File( h5file, 'w')
hf.attrs[u'file_name']  = icfile
hf.attrs[u'icsstr'] = 'fdsadgfd.sa\dsa'
hf.attrs[u'startTime'] = time.strftime("Started at:%A %d %B %Y   %H:%M")


def readfun(filename):
    '''
    reads unformatted fortran files 
    ''' 
    f = FortranFile('Outputs/'+filename, 'r')
    names = ''.join(f.read_reals('c'))
    data = []
    while True:
            try:
                data.append(f.read_reals(dtype=np.float_))
            except TypeError:
                break
        #array = np.reshape(array, (nspecs,-1))

    f.close()
    return [names.replace(' ',''),data]
    
    
    

class GroupClass:
    ''' A class containing group data'''
    def __init__(self,run_id,name,description,obs=False,saved=False):
        self.obs=obs
        self.description = description 
        self.name=name.split('-')[0][:10] # name truncated to 10 char
        self.run_id = '%d'%(run_id+1)
        self.model = './model'
        
        if '-' in name: 
            model = name.split('-')[1]
            #check if model exists in saved folder
            if os.path.isdir("/saved/exec/"+model):
                self.model='save/exec/%s/model'%(model)



def simulate (group):
    '''
    starts the simulation
    
    inputs:
        saved
        obs 
        description
        run_id
        name
        
    calc:
        walltime
        flux
    
    simres:
        spechead
        ratehead
        spec
        rate
    '''
    wall=0
    run ='./%s %s %s %d'%(group.model, group.name, group.run_id,group.obs)
    try:    
        g = hf.create_group(group.name)
        g.attrs[u'description']  = group.description
        g.attrs[u'id']  = group.run_id
        g.attrs[u'model']  = group.model
        g.attrs[u'observations']  = group.obs
        
        
        start = time.strftime("%s")
        
        print run
        os.system(run)
        
        wall = int(time.strftime("%s")) - int(start)
        
        for dataset in ['spec','rate']:
            data = readfun('%s.%s'%(group.name,dataset))
            g.attrs[dataset + u'head']  = data[0]
            g.create_dataset(dataset, data=data[1], chunks=True)
            
        
        
    
        
    except Exception as e:
        print 'Failure on '+ run + e
    
    g.attrs[u'wall']  = wall

''' hf = h5py.File( h5file, 'r')
group1 = hf.get('group1')
group1.items()
'''


g = GroupClass(0,'hi','bye')
simulate(g)


hf.close()



