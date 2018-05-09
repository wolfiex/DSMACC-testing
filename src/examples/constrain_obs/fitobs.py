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


'''
import numpy as np
import splinef
import os

global names
names = []
copyto = '../../../'
matched= 'constraints_040617/*.csv'

def get_spline(match='*.csv',plot=True):
    #data is saved in 1-24
    import glob


    save=[]

    for filename in glob.glob(match):
        print filename
        myname = filename.split('/')[-1].split('_')[0]
        names.append(myname)

        scale = 1
        if '_pptv' in filename: scale = 1e-12
        if '_ppbv' in filename: scale = 1e-9


        data = tuple(open(filename))
        data = np.array([i.replace(' ','').split(',') for i in data])
        data = data.astype(np.float)

        #ensure x is forwards going - required by spline
        newdata = []
        old = 0
        for i in data:
            if i[0]>old: newdata.append(i)
            old = i[0]

        data = np.array(newdata)

        x=data[:,0]
        y=data[:,1]

        '''
        # update first and last values to ensure continuity
        x= np.insert(x,0,0)
        x =np.insert(x,len(x),24)
        mp = (y[-1]+y[0])/2
        y= np.insert(y,0,mp)
        y =np.insert(y,len(y),mp)

        '''

        x = [i/24. for i in x]
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
            plt.savefig(filename.replace('.csv','.png'))

        save.append(spyint)
        for j in coeff:
            save.append(j)

        #string = r"""C(ind_%s)= CFACTOR*10**seval(%s,DFRACT,(/%s/),  (/%s/), (/%s/), (/%s/), (/%s/) )"""%(len(modelfit),myname,modelfit,modelresult,coeff[0],coeff[1],coeff[])
    save.append(newx)
    return save

cfarray =  np.asfortranarray(np.array(get_spline(match=matched)))

splinef.writeobs(cfarray)


ratestring = "!obs:%d\n"%len(cfarray)

ratestring+='''
!! Constrain from observations
!USE model_Global,       ONLY: CONSTRAIN,CFACTOR,spcf,obs
DFRACT = mod(((DAYCOUNTER*dt)/86400.) + mod(JDAY,1.),1.)
'''

#generator to increase nubmers
def count(n):
       num = 1
       while num < n:
           yield num
           num += 1

c = count(len(cfarray))
n=next

BVOC = ['C5H8','APINENE','BPINENE','LIMONENE']
ANTH = ['C2H6','C3H8','IC4H10','NC4H10','CHEX','IC5H12','M2PE','NC5H12','NC6H14','NC7H16','NC8H18','NC9H20','NC10H22','NC11H24','NC12H26','BENZENE','TOLUENE','EBENZ','OXYL','MXYL','IPBENZ','PBENZ','METHTOL','PETHTOL','TM135B','OETHTOL','TM124B','TM123B','DIME35EB','C2H4','C3H6','C2H2','TBUT2ENE','BUT1ENE','MEPROPENE','CBUT2ENE','C4H6','TPENT2ENE','CPENT2ENE']
# ['C2H6','C3H8','IC4H10','NC4H10','CHEX','IC5H12','M2PE','NC5H12','NC6H14','NC7H16','NC8H18','NC9H20','NC10H22','NC11H24','NC12H26']
NOX = ['NOEMISS','NO2EMIS']
CO = ['CO']
LAROM = []
#['IPBENZ','PBENZ','METHTOL','PETHTOL','TM135B','OETHTOL','TM124B','TM123B','DIME35EB']
SAROM = []
#['BENZENE','TOLUENE','EBENZ','OXYL','MXYL']
ALKE = []
# ['C2H4','C3H6','C2H2','TBUT2ENE','BUT1ENE','MEPROPENE','CBUT2ENE','C4H6','TPENT2ENE','CPENT2ENE']
METHANE = ['CH4']

for i in names:
    if i in ['NOX','nox','NOx']:
        ratestring += "\n TNOX_OLD = CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(n(c),n(c),n(c),n(c))
    elif i in ['DEPOS','depos']:
        ratestring += "\n DEPOS = 10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(n(c),n(c),n(c),n(c))
    elif i in ['DILUTE','dilute']:
        ratestring += "\n DILUTE = 10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(n(c),n(c),n(c),n(c))
    elif i in ['BLH','blh']:
        ratestring += "\n BLH = 10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(n(c),n(c),n(c),n(c))
    elif i in ['SAREA','sarea']:
        ratestring += "\n SAREA = SAFAC*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(n(c),n(c),n(c),n(c))
    elif i in ['TEMP','temp']:
        ratestring += "\n TEMP = 10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(n(c),n(c),n(c),n(c))
    elif i in ['H2O','h2o']:
        ratestring += "\n H2O = CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(n(c),n(c),n(c),n(c))
    elif i in BVOC:
        ratestring += "\n C(ind_%s) = BVOCFAC*CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(i,n(c),n(c),n(c),n(c))
        ratestring += '\n CONSTRAIN(ind_%s) = C(ind_%s)\n'%(i,i)
    elif i in ANTH:
        ratestring += "\n C(ind_%s) = ANTHFAC*CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(i,n(c),n(c),n(c),n(c))
        ratestring += '\n CONSTRAIN(ind_%s) = C(ind_%s)\n'%(i,i)
    elif i in NOX:
        ratestring += "\n C(ind_%s) = NOXFAC*CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(i,n(c),n(c),n(c),n(c))
        ratestring += '\n CONSTRAIN(ind_%s) = C(ind_%s)\n'%(i,i)
    elif i in CO:
        ratestring += "\n C(ind_%s) = (COFAC*CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:)))+(1.3E-7*CFACTOR)"%(i,n(c),n(c),n(c),n(c))
        ratestring += '\n CONSTRAIN(ind_%s) = C(ind_%s)\n'%(i,i)   
    elif i in LAROM:
        ratestring += "\n C(ind_%s) = LAROMF*CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(i,n(c),n(c),n(c),n(c))
        ratestring += '\n CONSTRAIN(ind_%s) = C(ind_%s)\n'%(i,i)   
    elif i in SAROM:
        ratestring += "\n C(ind_%s) = SAROMF*CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(i,n(c),n(c),n(c),n(c))
        ratestring += '\n CONSTRAIN(ind_%s) = C(ind_%s)\n'%(i,i)   
    elif i in ALKE:
        ratestring += "\n C(ind_%s) = ALKEFAC*CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(i,n(c),n(c),n(c),n(c))
        ratestring += '\n CONSTRAIN(ind_%s) = C(ind_%s)\n'%(i,i)   
    elif i in METHANE:
        ratestring += "\n C(ind_%s) = (CH4FAC*CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:)))+(1.8E-6*CFACTOR)"%(i,n(c),n(c),n(c),n(c))
        ratestring += '\n CONSTRAIN(ind_%s) = C(ind_%s)\n'%(i,i)   
    else:
        ratestring += "\n C(ind_%s)= CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(i,n(c),n(c),n(c),n(c))
        ratestring += '\n CONSTRAIN(ind_%s) = C(ind_%s)\n'%(i,i)


print ratestring


with open(copyto+'include.obs','w') as f:
    f.write(ratestring)

os.system('mv spline.obs ../../../')

print ''

print ' '.join(names)


'''
Add to incude file with conditional
print*, dfract,seval(27,0.5_dp,spcf(obs,:),spcf(1,:),&
        spcf(2,:),spcf(3,:),spcf(4,:)), c(ind_O3),SHAPE(spcf)

'''
