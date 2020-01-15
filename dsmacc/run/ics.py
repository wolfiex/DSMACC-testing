

def create_ics(fileic=False,    last=False,    keepx=True , postime = False ,spin = False):
    print ("\033]0;creating ics\007")
    import h5py,glob,os,sys,re
    import numpy as np

    file_list = glob.glob('InitCons/*.csv')
    file_list.sort(key=os.path.getmtime)#getmtime - modified getctime-created

    print (file_list)
    if fileic:
        print (fileic)
        ic_file = fileic
    elif (last) :
        ic_file = file_list[-1]
    else:
        print ('Select file to open: \n\n')
        for i,f in enumerate(file_list): print (i , ' - ', f.replace('InitCons/','').replace('.csv',''))
        ic_file = file_list[int(input('Enter Number \n'))]

    if ('.csv' not in ic_file):  ic_file += '.csv'
    print ('selected',ic_file)

    ic_open= tuple(open(ic_file))
    run_names = np.array([i for i in enumerate(ic_open[2].strip().split(',')[3:])])
    descriptions = np.array([i for i in enumerate(ic_open[1].strip().split(',')[3:])])

    data = np.array([i.strip().split(',') for i in ic_open]).T


    lon = None
    jday = None

    for i,j in enumerate(data[1]):
        if (j in ['LON','lon','Lon']): lon = i
        elif (j in ['JDAY','jday','Jday','JDay']): jday = i
        elif (j in ['SPINUP','spinup']): spinup = i

    try:spinup = (data[3:,spinup].astype(float) + data[3:,jday].astype(float)*60*60*24)  #.astype('M8[s]')
    except:spinup = [0]*data.shape[1]




    for run in range(3,data.shape[0]):
        localtime = float(data[run,lon])/360.
        print ('Adjusting jday to localtime by %.2f hours for model: %s'%(localtime*24,run_names[run-3][1]))
        data[run,jday]= '%.4f'%(float(data[run,jday])-localtime)

    time = data[3,3]
    print(time)

    time = time.replace('-','')
    if spin:#and not postime:
        time = '-'+time


    data = data[1:,4:]

    print (data)

    ##make ics
    #np.savetxt('Init_cons.dat', data, fmt='%15s', delimiter='!', newline='\n', header='%s'%time,comments='')

    #comment out runs
    if not keepx: numbered = filter(lambda x: x[1][0] not in 'xX', numbered)

    ### make new hdf file
    h5file = ic_file.replace('InitCons/','').replace('.csv','.h5')

    try: os.remove(h5file)
    except : None

    hf = h5py.File( h5file, 'w')
    hf.attrs[u'file_name']  = ic_file

    hf.attrs[u'startTime'] = ''#time.strftime("%A %d %B %Y   %H:%M")

    print([u''+i for i in data[0]])

    hf.attrs[u'ictime'] = time
    hf.create_dataset(  name = 'icspecs',data = data[0].astype('S15'),dtype='S15',shuffle=True, chunks=True, compression="gzip", compression_opts=9)
    hf.create_dataset(  name = 'icconst',data = data[1].astype(np.float).astype(np.int) ,dtype='I',shuffle=True, chunks=True, compression="gzip", compression_opts=9)
    hf.create_dataset(  name = 'icruns',data = np.array(data[2:]).astype(np.float) ,dtype=np.float,shuffle=True, chunks=True, compression="gzip", compression_opts=9)




    for i,group in enumerate(run_names):

            g = hf.create_group(group[1])
            g.attrs[u'description']  = ''
            g.attrs[u'id']  = group[0].astype('S')
            g.attrs[u'model']  = 'model for now'
            g.attrs[u'observations']  = 'check for obs flag'
            g.attrs[u'walltime']  = False
            g.attrs[u'spinup']  = spinup[i]




            '''
            g.attrs[u'spec_head']=''
            g.attrs[u'rate_head']=''
            g.create_dataset(  name = 'spec',data = [] , dtype='f',shuffle=True, chunks=True, compression="gzip", compression_opts=9)
            g.create_dataset(  name = 'rate',data = [] , dtype='f',shuffle=True, chunks=True, compression="gzip", compression_opts=9)
            '''






    hf.close()


    #try: os.environ['NCPUS']
    #except:  print 'serial'
    #h5dump file.h5
    print ("\033]0;   \007")
    return h5file
