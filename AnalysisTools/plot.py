#!/usr/local/anaconda/bin/python
# -*- coding: utf-8 -*-

###############################################################################

# Load python and system functions
import pandas as pd
import numpy as np
import netCDF4
from netCDF4 import Dataset
import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8') # output of UNICODE characters
sys.path.insert(0,os.path.expanduser("./py.fcn/"))
import matplotlib.pyplot as plt

# Load user-defined functions
from load import *

# Global variables
global spcM3, spcM4, rM3, rM4, xm, M

# Load mechanisms

# Load time, species and rate data of both mechanisms
# Change nc files and scenario name below:
time, xm, spcM3, rM3 = load('../save/ncfiles/DUN15M3dp.nc', 'DUN15', False)
time, xm, spcM4, rM4 = load('../save/ncfiles/DUN15M4dp.nc', 'DUN15', True)

# Define special lumped species
M = spcM4['M'].mean()
spcM3['NOx'] = spcM3['NO']+spcM3['NO2']
spcM4['NOx'] = spcM4['NO']+spcM4['NO2']

### Plots for species in moelcules/cm3
try:
    fname = argv[0]
except:
    fname = './IO/mlc.spc'
with open(fname) as f:
    spec = f.readlines()
# Remove whitespace characters and line breaks
spec = [x.strip() for x in spec]
print spec

for spc in spec:
    plot_mlc(spc)

### plot for species in mixing ratios
spec = ['O3','NO','NO2','NO3','NOx','HONO','HNO3','H2O2', \
    'cc11','cc12','cc13','cc21','cc22','cc23','cc25', \
    'cc31','cc33','cc4','cc5','cc0'] #, \
#    'newMLC1','newMLC2','newMLC3','newMLC4']
for spc in spec:
    plot_vmr(spc)

# spec = ['newMLC1','newMLC2','newMLC3','newMLC4']
# for spc in spec:
#     plot_new(spc)
# ### OH:HO2 ratio ###

ratM3 = spcM3['OH']/spcM3['HO2']
ratM4 = spcM4['OH']/spcM4['HO2']

fig = plt.figure()
fig.set_size_inches(6.,4.)
axes = plt.gca()
plt.rc('grid', linestyle=":", color='lightgrey')

plt.xticks(np.arange(0,xm,12))
plt.grid()
plt.xlabel('model time / hours')

plt.ylabel('[OH] / [HO$_2$]') #\n(F / cm$^{-3}$ s$^{-1}$)

plt.plot(time,ratM3,'g-',label=u'MCMv3.3.1')
plt.plot(time,ratM4,'b--',label=u'New Prot')

plt.legend(loc = 'upper center', prop={'size':12})
plt.tight_layout()
plt.savefig('DUN15/rat.pdf')
plt.close(fig)


# ### Mass by O:C ratio ###

# fig = plt.figure()
# fig.set_size_inches(6.,4.)
# axes = plt.gca()
# plt.rc('grid', linestyle=":", color='lightgrey')

# plt.xticks(np.arange(0,xm,12))
# plt.grid()
# plt.xlabel('model time / hours')
# ocM4 = spcM4['oc1']+spcM4['oc2']+spcM4['oc3']+spcM4['oc4']
# ord, mult = order(max(ocM4))
# plt.ylabel('[NMVOC] / 10$^{%i}\,$cm$^{-3}$' % ord) #\n(F / cm$^{-3}$ s$^{-1}$)

# plt.plot(time,spcM3['oc4']/mult,'g-',label=u'O:C ≥ 2 (MCMv3.3.1)')
# plt.plot(time,spcM4['oc4']/mult,'b--',label=u'O:C ≥ 2 (New Prot)')
# plt.plot(time,(spcM3['oc3']+spcM3['oc4'])/mult,'y-',label=u'1 ≤ O:C < 2 (MCMv3.3.1)')
# plt.plot(time,(spcM4['oc3']+spcM4['oc4'])/mult,'c--',label=u'1 ≤ O:C < 2 (New Prot)')
# plt.plot(time,(spcM3['oc2']+spcM3['oc3']+spcM3['oc4'])/mult,'r-',label=u'0.5 ≤ O:C < 1 (MCMv3.3.1)')
# plt.plot(time,(spcM4['oc2']+spcM4['oc3']+spcM4['oc4'])/mult,'k--',label=u'0.5 ≤ O:C < 1 (New Prot)')
# plt.plot(time,(spcM3['oc1']+spcM3['oc2']+spcM3['oc3']+spcM3['oc4'])/mult,'m-',label=u'O:C < 0.5 (MCMv3.3.1)')
# plt.plot(time,(spcM4['oc1']+spcM4['oc2']+spcM4['oc3']+spcM4['oc4'])/mult,color='skyblue',ls='--',label=u'O:C < 0.5 (New Prot)')

# plt.legend(loc = 'upper center', prop={'size':12})
# plt.tight_layout()
# plt.savefig('DUN15/oc.pdf')
# plt.close(fig)


# ### Mass by  O:C ratio as stacked area plot ###

# fig = plt.figure()
# fig.set_size_inches(6.,4.)
# plt.rc('grid', linestyle=":", color='lightgrey')
# axes = plt.gca()

# plt.xticks(np.arange(0,xm,12))
# plt.grid()
# plt.xlabel('model time / hours')
# plt.ylabel('c / cm$^{-3}$') #\n(F / cm$^{-3}$ s$^{-1}$)

# #plt.stackplot(time,spcM4['oc4'],spcM4['oc3'],spcM4['oc2'],spcM4['oc1'],colors=['b','c','k','skyblue'], \
# #    labels=[u'O:C ≥ 2 (New Prot)',u'1 ≤ O:C < 2 (New Prot)',u'0.5 ≤ O:C < 1 (New Prot)',u'O:C < 0.5 (New Prot)'])
# #plt.stackplot(time,spcM4['oc3'],label=u'1 ≤ O:C < 2 (New Prot)')
# #plt.stackplot(time,spcM4['oc2'],label=u'0.5 ≤ O:C < 1 (New Prot)')
# #plt.stackplot(time,spcM4['oc1'],label=u'O:C < 0.5 (New Prot)')

# plt.legend(loc = 'upper center', prop={'size':12})
# plt.tight_layout()
# plt.savefig('DUN15/oc_stack.pdf')
# plt.close(fig)


# ### Mass by chain length ###

# fig = plt.figure()
# fig.set_size_inches(6.,4.)
# axes = plt.gca()
# plt.rc('grid', linestyle=":", color='lightgrey')

# plt.xticks(np.arange(0,xm,12))
# plt.grid()
# plt.xlabel('model time / hours')
# cnM4 = spcM4['cn1']+spcM4['cn2']+spcM4['cn3']+spcM4['cn4']+spcM4['cn5'] \
#     +spcM4['cn6']+spcM4['cn7']+spcM4['cn8']+spcM4['cn9']+spcM4['cn0']
# ord, mult = order(max(cnM4))
# plt.ylabel('[NMVOC] / 10$^{%i}\,$cm$^{-3}$' % ord) #\n(F / cm$^{-3}$ s$^{-1}$)

# plt.plot(time,spcM3['cn0']/mult,'g-',label=u'CN ≥ 10')
# plt.plot(time,spcM4['cn0']/mult,'b--',label=u'CN ≥ 10')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9'])/mult,'y-',label=u'CN = 9')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9'])/mult,'c--',label=u'CN = 9')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8'])/mult,'r-',label=u'CN = 8')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8'])/mult,'k--',label=u'CN = 8')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7'])\
#     /mult,'m-',label=u'CN = 7')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7'])\
#     /mult,color='skyblue',ls='--',label=u'CN = 7')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7']\
#     +spcM3['cn6'])/mult,color='darkgreen',ls='-',label=u'CN = 6')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7']\
#     +spcM4['cn6'])/mult,color='orange',ls='--',label=u'CN = 6')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7']\
#     +spcM3['cn6']+spcM3['cn5'])/mult,color='blueviolet',ls='-',label=u'CN = 5')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7']\
#     +spcM4['cn6']+spcM4['cn5'])/mult,color='sandybrown',ls='--',label=u'CN = 5')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7']\
#     +spcM3['cn6']+spcM3['cn5']+spcM3['cn4'])/mult,color='olive',ls='-',label=u'CN = 4')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7']\
#     +spcM4['cn6']+spcM4['cn5']+spcM4['cn4'])/mult,color='m',ls='--',label=u'CN = 4')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7']\
#     +spcM3['cn6']+spcM3['cn5']+spcM3['cn4']+spcM3['cn3'])/mult,\
#     color='lightsteelblue',ls='-',label=u'CN = 3')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7']\
#     +spcM4['cn6']+spcM4['cn5']+spcM4['cn4']+spcM4['cn3'])/mult,\
#     color='indigo',ls='--',label=u'CN = 3')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7']\
#     +spcM3['cn6']+spcM3['cn5']+spcM3['cn4']+spcM3['cn3']+spcM3['cn2'])\
#     /mult,color='darkkhaki',ls='-',label=u'CN = 2')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7']\
#     +spcM4['cn6']+spcM4['cn5']+spcM4['cn4']+spcM4['cn3']+spcM4['cn2'])\
#     /mult,color='gold',ls='--',label=u'CN = 2')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7']\
#     +spcM3['cn6']+spcM3['cn5']+spcM3['cn4']+spcM3['cn3']+spcM3['cn2']\
#     +spcM3['cn1'])/mult,color='palevioletred',ls='-',label=u'CN = 1')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7']\
#     +spcM4['cn6']+spcM4['cn5']+spcM4['cn4']+spcM4['cn3']+spcM4['cn2']\
#     +spcM4['cn1'])/mult,color='wheat',ls='--',label=u'CN = 1')

# plt.legend(loc = 'upper center', prop={'size':12})
# plt.tight_layout()
# plt.savefig('DUN15/cn.pdf')
# plt.close(fig)


### new species

fig = plt.figure()
fig.set_size_inches(6.,4.)

df = spcM4[['newMLC1','newMLC2','newMLC3','newMLC4']]/M*1.0e12
df.index = time
df.plot(grid=True)

plt.savefig('DUN15/newMLC.pdf')
plt.close(fig)


### Mass by chain length (area plot) ###

fig = plt.figure(1)
fig.set_size_inches(6.,4.)

df = spcM3[['cn0','cn9','cn8','cn7','cn6','cn5','cn4','cn3','cn2','cn1']]/M*1.0e9
df.index = time
df.plot.area(color=['g','mediumseagreen','mediumturquoise','lawngreen','yellowgreen','olive','goldenrod','gold','palegoldenrod','peru'], \
    label=[u'CN ≥ 10 (MCMv3.3.1)',u'CN = 9 (MCMv3.3.1)',u'CN = 8 (MCMv3.3.1)',u'CN = 7 (MCMv3.3.1)',u'CN = 6 (MCMv3.3.1)', \
    u'CN = 5 (MCMv3.3.1)',u'CN = 4 (MCMv3.3.1)',u'CN = 3 (MCMv3.3.1)',u'CN = 2 (MCMv3.3.1)',u'CN = 1 (MCMv3.3.1)'],alpha=0.3, grid = True)


plt.savefig('DUN15/cnM3_stack.pdf')
plt.close(fig)


fig = plt.figure(2)
fig.set_size_inches(6.,4.)

df = spcM4[['cn0','cn9','cn8','cn7','cn6','cn5','cn4','cn3','cn2','cn1']]/M*1.0e9
df.index = time
df.plot.area(color=['blue','slateblue','darkviolet','m','fuchsia','violet','deeppink','red','orange','y'], \
    label=[u'CN ≥ 10 (New Prot)',u'CN = 9 (New Prot)',u'CN = 8 (New Prot)',u'CN = 7 (New Prot)',u'CN = 6 (New Prot)', \
    u'CN = 5 (New Prot)',u'CN = 4 (New Prot)',u'CN = 3 (New Prot)',u'CN = 2 (New Prot)',u'CN = 1 (New Prot)'], grid=True, alpha=0.3)

plt.savefig('DUN15/cnM4_stack.pdf')
plt.close(fig)


### Mass by O:C ratio (area plot) ###

fig = plt.figure(3)
fig.set_size_inches(6.,4.)

df = spcM3[['oc1','oc2','oc3','oc4']]/M*1.0e9
df.index = time
df.plot.area(color=['g','mediumseagreen','mediumturquoise','lawngreen'], \
    grid=True, alpha=0.3)

plt.savefig('DUN15/ocM3_stack.pdf')
plt.close(fig)


fig = plt.figure(4)
fig.set_size_inches(6.,4.)

df = spcM4[['oc1','oc2','oc3','oc4']]/M*1.0e9
df.index = time
df.plot.area(color=['blue','slateblue','darkviolet','m'], \
    alpha=0.3)

plt.savefig('DUN15/ocM4_stack.pdf')
plt.close(fig)

print 'Done.'
