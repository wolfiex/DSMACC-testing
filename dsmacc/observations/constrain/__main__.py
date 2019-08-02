from . import *

cfarray =  np.asfortranarray(np.array(get_spline()))

splinef.writeobs(cfarray)


ratestring = "!obs:%d\n"%len(cfarray)

ratestring+='''
!! Constrain from observations
!USE model_Global,       ONLY: CONSTRAIN,CFACTOR,spcf,obs
!DFRACT = mod(((DAYCOUNTER*dt)/86400.) + mod(JDAY,1.),1.)

if (DFRACT .ge. 0) then
'''

#generator to increase nubmers
def count(n):
       num = 1
       while num < n:
           yield num
           num += 1

c = count(len(cfarray))
n=next

'''
BVOC = ['C5H8','APINENE','BPINENE','LIMONENE']
ANTH = ['C2H6','C3H8','IC4H10','NC4H10','CHEX','IC5H12','M2PE','NC5H12','NC6H14','NC7H16','NC8H18','NC9H20','NC10H22','NC11H24','NC12H26']
NOX = ['NOEMISS']
CO = ['CO']
AROM = ['BENZENE','TOLUENE','EBENZ','OXYL','MXYL','IPBENZ','PBENZ','METHTOL','PETHTOL','TM135B','OETHTOL','TM124B','TM123B','DIME35EB']
ALKE = ['C2H4','C3H6','C2H2','TBUT2ENE','BUT1ENE','MEPROPENE','CBUT2ENE','C4H6','TPENT2ENE','CPENT2ENE']
METHANE = ['CH4']
'''
constrain =[]

for i in names:
    if i in ['NOX','nox','NOx','NOY','NOy','noy']:
        ratestring += "\n TNOX_OLD = CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(n(c),n(c),n(c),n(c))
    elif i in ['DEPOS','depos']:
        ratestring += "\n DEPOS = 10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(n(c),n(c),n(c),n(c))
    elif i in ['SAREA','sarea']:
        ratestring += "\n SAREA = SAFAC*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(n(c),n(c),n(c),n(c))
    elif i in ['TEMP','temp']:
        ratestring += "\n TEMP = 10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(n(c),n(c),n(c),n(c))
    elif i in ['H2O','h2o']:
        ratestring += "\n H2O = CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(n(c),n(c),n(c),n(c))

    else:
        ratestring += "\n C(ind_%s)= CFACTOR*10**seval(27,dfract,spcf(obs,:),spcf(%d,:),spcf(%d,:),spcf(%d,:),spcf(%d,:))"%(i,n(c),n(c),n(c),n(c))
        ratestring += '\n CONSTRAIN(ind_%s) = C(ind_%s)\n'%(i,i)
        constrain.append('CONSTRAIN(ind_%s)'%i)


ratestring += '''
ELSE
! Unconstrain species
    '''
for c in constrain:
    ratestring+='''
        %s =0'''%c

ratestring+='\nEND IF'
print ratestring


with open('./include.obs','w') as f:
    f.write(ratestring)


print ' '.join(names)

print 'Re-running make!   (needed)'
os.system('make')
