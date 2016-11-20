import rpy2.robjects as ro
import os, multiprocessing
import pandas as pd
import numpy as np 
from scipy.io import FortranFile
from rpy2.robjects import pandas2ri
pandas2ri.activate()



ro.r("library('lhs')")
ro.r("library('DiceKriging')")






def readfbin(filename):
    f = FortranFile(filename, 'r')
    array = f.read_reals(dtype=float)
    #array = np.reshape(array, (zangles,-1))
    f.close()
    return array
    
    
inputs = pd.DataFrame(ro.r("lhc<-randomLHS(1000,5)"),columns = ['sza','albedo','temp','alt','o3col'])

inputs['sza'] *= 90
inputs['sza'] += 0

inputs['albedo'] *= 1
inputs['albedo'] += 0

inputs['temp'] *= 320-190
inputs['temp'] += +190

inputs['alt'] *= 80
inputs['alt'] += 0

inputs['o3col'] *= 273-50
inputs['o3col'] += 50



data = []; print inputs


def jammy (selection):
    finame= 'run'+str(selection[0])+'.bin'
    selection = selection[1]    
    os.system('touch %s && ./tuv %s %s %s %s %s %s  > sdout.bin'%(finame,finame,selection.alt,selection.albedo,selection.o3col,selection.temp,selection.sza))
    return readfbin(finame)
    

data = multiprocessing.Pool(8).map( jammy , inputs.iterrows() )       





df=pd.DataFrame(data).T 
df.columns= inputs.index





def see_j (val):

    jval = inputs
    jval['value'] = df.ix[val]


    ro.globalenv['jval'] = jval

    ro.r('plot(jval)')

#http://mbostock.github.io/d3/talk/20111116/iris-splom.html
# trellis interactive


os.system('rm *.bin')


'''
      import dill                            #pip install dill --user

      filename= 'globalsave.pkl'

      dill.dump_session(filename)

   
           
   
        import dill           
        import rpy2.robjects as ro
        import os, multiprocessing
        import pandas as pd
        import numpy as np 
        from scipy.io import FortranFile
        from rpy2.robjects import pandas2ri
        pandas2ri.activate()

        # and to load the session again:
        filename= 'globalsave.pkl'
        dill.load_session(filename)

'''

           
