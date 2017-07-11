
### Plot function for new runs only

def plot_new(spc):

    print 'plotting',spc,'...'
    fig = plt.figure()
    fig.set_size_inches(6.,4.)
    axes = plt.gca()
    plt.rc('grid', linestyle=":", color='lightgrey')

    plt.xticks(np.arange(0,xm,12))
    plt.grid()
    plt.xlabel('model time / hours')

    ord, mult = order(max(spcM4[spc]))
    #s =pd.Series(spcM4[spc])
    #s.index=time
    #s.to_csv('test.dat',sep=' ')

    plt.ylabel('[%s] / 10$^{%i}\,$cm$^{-3}$' % (spc, ord)) #\n(F / cm$^{-3}$ s$^{-1}$)

    plt.plot(time,spcM4[spc]/mult,'b--')

    plt.legend(loc = 'upper center', prop={'size':12})
    plt.tight_layout()
    file = 'DUN15/new_'+spc+'.pdf'
    plt.savefig(file)
    plt.close(fig)


### Plot function for concentratrations in molecules/cm3

def plot_mlc(spc):

    print 'plotting',spc,'...'
    fig = plt.figure()
    fig.set_size_inches(6.,4.)
    axes = plt.gca()
    plt.rc('grid', linestyle=":", color='lightgrey')

    plt.xticks(np.arange(0,xm,12))
    plt.grid()
    plt.xlabel('model time / hours')

    ord, mult = order(max(spcM4[spc]))
    #s =pd.Series(spcM4[spc])
    #s.index=time
    #s.to_csv('test.dat',sep=' ')

    plt.ylabel('[%s] / 10$^{%i}\,$cm$^{-3}$' % (spc, ord)) #\n(F / cm$^{-3}$ s$^{-1}$)

    plt.plot(time,spcM3[spc]/mult,'g-',label=u'MCMv3.3.1')
    plt.plot(time,spcM4[spc]/mult,'b--',label=u'New Prot')

    plt.legend(loc = 'upper center', prop={'size':12})
    plt.tight_layout()
    file = 'DUN15/'+spc+'.pdf'
    plt.savefig(file)
    plt.close(fig)


### Plot function for mixing ratios

def plot_vmr(spc):

    print 'plotting',spc,'...'

    concM3 = spcM3[spc]/M
    concM4 = spcM4[spc]/M
    ord, mult = order(max(concM4))

    if (max(concM4) > 5.e-7):
        unit = 'ppm$_{\mathrm{v}}$'
        concM3 = concM3*1.e6
        concM4 = concM4*1.e6
    elif (max(concM4) > 5.e-10):
        unit = 'ppb$_{\mathrm{v}}$'
        concM3 = concM3*1.e9
        concM4 = concM4*1.e9
    else:
        unit = 'ppt$_{\mathrm{v}}$'
        concM3 = concM3*1.e12
        concM4 = concM4*1.e12

    fig = plt.figure()
    fig.set_size_inches(6.,4.)
    axes = plt.gca()
    plt.rc('grid', linestyle=":", color='lightgrey')

    plt.xticks(np.arange(0,xm,12))
    plt.grid()
    plt.xlabel('model time / hours')

    #s =pd.Series(spcM4[spc])
    #s.index=time
    #s.to_csv('test.dat',sep=' ')

    plt.ylabel('[%s] / %s' % (spc, unit)) #\n(F / cm$^{-3}$ s$^{-1}$)

    plt.plot(time,concM3,'g-',label=u'MCMv3.3.1')
    plt.plot(time,concM4,'b--',label=u'New Prot')

    # plt.legend(loc = 'upper center', prop={'size':12})
    plt.tight_layout()
    file = 'DUN15/'+spc+'.pdf'
    plt.savefig(file)
    plt.close(fig)
