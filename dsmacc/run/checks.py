
def checkmatch(start,  model='model',
        ignore = ['TEMP', 'LAT', 'LON', 'JDAY', 'H2O', 'ALBEDO', 'PRESS', 'NOx', 'DEPOS', 'FEMISS', 'SPINUP','NOX']
        ):
        '''
        A function to check if the species within the ics file match those of the compiled model!
        '''
        import h5py,re,os

        with h5py.File(start, 'r') as f:
            icspecs = [i.decode('utf-8') for i in f['icspecs']]
            specs = re.split(r'\s+',os.popen('./%s 0 0 --species'%(model)).read())
            specs.extend(ignore)

            diff = set(icspecs)-set(specs)
        diff = list(filter(lambda x: x[0] != 'X',diff))
        return diff

def coreupdate(ncores,start):
        '''
        A function to adjust the number of cores needed.
        '''
        import h5py,sys

        with h5py.File(start, 'r') as f:
            runs = len([1 for item in list(f.values()) if isinstance(item, h5py.Group)]) + 1

        if ncores > runs:
            print('Scaling down the cores to ',runs)
            ncores = runs


        return ncores
