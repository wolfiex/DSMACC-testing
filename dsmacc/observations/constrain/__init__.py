''' observation data array '''
''' read species 15a , matrix of values in init.
intial conditions flag add,

To compile f90 file:

export CFLAGS=''
export CXXFLAGS=''
export F77=gfortran
export FC=gfortran
export F90=gfortran
export FFLAGS=''
export CPP='gcc'
f2py --f90flags='-ffree-form -fPIC' -c splinecf.f90 -m splinef --f90exec=/usr/bin/gfortran

--verbose

ARGS =
1. location of filename

FILE FORMAT:
a csv containing all speices to be constrained
these must all be in capitals and have their units described (e.g. _PPBV), else they must be in mixing observations

'''


import numpy as np
import splinef
import os,sys

global names
names = []
loc = 'observations'
filename =  sys.argv[1]

os.system('mkdir '+loc)
os.system('mkdir '+loc+'/debug')
os.system('rm '+loc+'/debug/*.png') # remove prev diagnostic


def get_spline(plot=True,flatten=5):
    #data is saved in 1-24
    import pandas as pd
    save=[]
    global filename
    df = pd.read_csv(filename,index_col=0)
    df.index=pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    df['index'] = [int(i.hour) for i in df.index]

    df = df.groupby(['index']).mean()



    for filename in df.columns:
        myname = filename.split('_')[0]
        names.append(myname)

        scale = 1
        if '_PPTV' in filename: scale = 1e-12
        if '_PPBV' in filename: scale = 1e-9


        print (filename)

        data = df[filename].dropna()
        #data = np.array([i.replace(' ','').split(',') for i in data])

        #ensure x is forwards going - required by spline


        #missing values
        # take mean
        for i in range(24):

            if i not in data.index:
                data = data.append( pd.Series([data.loc[[i-1,i+1]].mean()],index=[i]) )
                print ('Interploating ',filename, i)

            data.sort_index(inplace=True)


        #### SMoothing
        for repeat in xrange(flatten):
            for i in range(len(data)):
                data.iloc[i] = data.iloc[[i-1,i,1+1]].mean(axis = 0)



        print data.index
        x= np.array(data.index)
        y= data.astype(np.float).values



        '''
        # update first and last values to ensure continuity
        x= np.insert(x,0,0)
        x =np.insert(x,len(x),24)
        mp = (y[-1]+y[0])/2
        y= np.insert(y,0,mp)
        y =np.insert(y,len(y),mp)
'''

        #day = 24.*60.*60.

        #x = [((i.hour*60 + i.minute)*60+i.second) for i in x]
        x=[i/24. for i in df.index]
        y = [np.log10(i*scale) for i in y]

        coeff = splinef.spline(x,y)

        newx = np.array([i/24. for i in xrange(25)])
        spyint = [splinef.seval(i,x,y,*coeff) for i in newx]

        newx = np.insert(newx,0,-.1)
        newx = np.insert(newx,len(newx),1.1)
        mp = (spyint[-2]+y[1])/2

        spyint[0] = mp
        spyint = np.insert(spyint,0,mp)
        spyint[-1] = mp
        spyint = np.insert(spyint,len(spyint),mp)



        coeff = splinef.spline(newx,spyint)
        modelfit = np.linspace(0,1,num=100,endpoint=True)
        modelresult = [splinef.seval(i,newx,spyint,*coeff) for i in modelfit]



        if plot:
            import matplotlib.pyplot as plt
            plt.clf()
            plt.plot(x, y, 'o', newx, spyint, '+', modelfit, modelresult, '--')
            plt.legend(['data', 'hourly', 'cubic'], loc='best')
            plt.title(filename)
            #plt.show()
            plt.savefig(loc+'/debug/'+filename+'.png')

        save.append(spyint)
        for j in coeff:
            save.append(j)

        #string = r"""C(ind_%s)= CFACTOR*10**seval(%s,DFRACT,(/%s/),  (/%s/), (/%s/), (/%s/), (/%s/) )"""%(len(modelfit),myname,modelfit,modelresult,coeff[0],coeff[1],coeff[])
    save.append(newx)
    return save


'''
Add to incude file with conditional
print*, dfract,seval(27,0.5_dp,spcf(obs,:),spcf(1,:),&
        spcf(2,:),spcf(3,:),spcf(4,:)), c(ind_O3),SHAPE(spcf)

'''
