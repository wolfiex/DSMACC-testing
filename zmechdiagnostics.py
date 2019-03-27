

def mechcomp(mechs,what='spec',n_subplot = 4):
        '''Compare PDF diagnostic for two differnt runs/mechanisms'''
        if type(mechs) != type([]):mechs = [mechs]

        print ('creating a comparison pdf of '+what)
        from matplotlib.backends.backend_pdf import PdfPages
        from matplotlib.pyplot import tick_params,setp,tight_layout,ylabel,xlabel,savefig,close
        import progressbar

        bar = progressbar.ProgressBar()

        linestyles = ['-', ':', '--', '-.']
        data = []
        for i in mechs:
            exec('data.append(i.%s.compute())'%what)

        #data.sort_index(axis=1,inplace=True)# arrange alphabetically
        crossover = set(data[0])
        for i in data[1:]:
            crossover = crossover & set(list(i.columns))
        crossover = sorted(list(set(crossover)))


        pp = PdfPages('compare_%s.pdf'%('_'.join([i.groupname for i in mechs])))

        for i in bar(xrange(0, len(crossover), n_subplot+1)):
            spselect = crossover[i:i+n_subplot]

            Axes = data[0][spselect].plot(subplots=True)
            for l,d in enumerate(data[1:]):
                d[spselect].plot(ax = Axes,linestyle = linestyles[-1*(l+1)],alpha =.8 , subplots=True)

            tick_params(labelsize=6)

            #y ticklabels
            [setp(item.yaxis.get_majorticklabels(), 'size', 7) for item in Axes.ravel()]
            #x ticklabels
            [setp(item.xaxis.get_majorticklabels(), 'size', 5) for item in Axes.ravel()]
            #y labels
            [setp(item.yaxis.get_label(), 'size', 10) for item in Axes.ravel()]
            #x labels
            [setp(item.xaxis.get_label(), 'size', 10) for item in Axes.ravel()]

            tight_layout()
            ylabel('mix ratio')

            #plt.locator_params(axis='y',nbins=2)

            savefig(pp, format='pdf')
            close('all')

        pp.close()
        print ('PDF out')
        close('all')



def pdiff(base,lump,what='spec',n_subplot = 4):
        '''
        Calculate the percentage difference between two returns
        '''
        print ('creating a comparison pdf of '+what)
        from matplotlib.backends.backend_pdf import PdfPages
        from matplotlib.pyplot import tick_params,setp,tight_layout,ylabel,xlabel,savefig,close
        import progressbar

        bar = progressbar.ProgressBar()

        linestyles = ['-', ':', '--', '-.']
        data = []
        for i in [base,lump]:
            exec('data.append(i.%s.compute())'%what)

        crossover = set(data[0])
        crossover = crossover & set(list(data[1].columns))
        crossover = sorted(list(set(crossover)))

        pp = PdfPages('pdiff_%s.pdf'%('_'.join([i.groupname for i in [base,lump]])))

        for i in bar(xrange(0, len(crossover), n_subplot+1)):
            spselect = crossover[i:i+n_subplot]

            df = 100*(data[1][spselect]/data[0][spselect])
            Axes = df.plot(subplots=True)

            tick_params(labelsize=6)

            #y ticklabels
            [setp(item.yaxis.get_majorticklabels(), 'size', 7) for item in Axes.ravel()]
            #x ticklabels
            [setp(item.xaxis.get_majorticklabels(), 'size', 5) for item in Axes.ravel()]
            #y labels
            [setp(item.yaxis.get_label(), 'size', 10) for item in Axes.ravel()]
            #x labels
            [setp(item.xaxis.get_label(), 'size', 10) for item in Axes.ravel()]

            tight_layout()
            ylabel('mix ratio')
            #plt.locator_params(axis='y',nbins=2)
            savefig(pp, format='pdf')
            close('all')

        pp.close()
        print ('PDF out')
        close('all')





def lumpdiagnostics(original,lumped,filename= 'lump.mech'):
    exec(''.join(tuple(open(filename))).replace('\n',';\n'))
    ts=original.ts
    for i,lump in enumerate(lumplist):
         ax = original.spec.loc[ts,lump].compute().plot.area(alpha=0.2)
         lumped.spec.loc[ts,'LMP%d'%(i+1)].compute().plot(ax = ax,c= 'blue',style='^-')
         print (i+1,lumped.spec.loc[ts,'LMP%d'%(i+1)].compute().mean(), original.spec.loc[ts,lump].compute().mean().sum())

         breakme = raw_input('enter for next')
         if breakme=='break':break
         plt.clf()
