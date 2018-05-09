from scipy.io import FortranFile

import os,sys,time,re
import numpy as np


obs=False
groups = None
debug=False #'for boradcast'

for i in sys.argv[1:]:
    if i=='--obs':
        if rank==0:
            obs = int(tuple(open('include.obs'))[0].strip().replace('!obs:',''))
            print 'observations being used, number of obs: ',int(obs)
    if '.h5' in i :
        filename = i.strip()    
    if '--debug' in i:
        debug = True
        
print obs,filename 



if filename:

        ###read args 
        extend = True 
        rewind = False

        
        if not debug: 
            os.system(' touch temp.txt && rm temp.txt')
            debug = '>>temp.txt'
            
            
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
            return [names.replace(' ',''),np.array(data)]

        from progressbar import ProgressBar
        pbar = ProgressBar()

        import h5py
        hf = h5py.File(filename, 'a')
        #ics = []
        #ics.extend([hf['icspecs'],hf['icconst']])           
        
        
        
        ###extend????
        #[ics.append(i) for i in hf['icruns']]
        
        
        #ics = np.array(ics)
        
        head= hf.attrs['ictime'] + '\n' + '!'.join(['%15s'%i for i in hf['icspecs']])+ '\n' + '!'.join(['%15s'%i for i in hf['icconst']]) 
        
        
        ############################################            
        ###hf.attrs['ictime']=1000
        ##################### DEL
        
        print 'duration' , hf.attrs['ictime']
        
        np.savetxt('Init_cons.dat', hf['icruns'], fmt='%15e', delimiter='!', newline='\n', header= head,comments='')  

        groups = [[int(item.attrs['id']),item.name] for item in hf.values() if isinstance(item, h5py.Group)]
       

        lgroups = len(groups)
       

        
        for n in xrange(lgroups):
                
                g = groups[n]
                
                
                          
                #set the model
                model='model'
                if '-' in g[1]: 
                    if runsaved: model='save/exec/%s/model'%(g[1].split('-')[-1])
                    else:  description = g[1].split('-')[0]
                    
                
                #run cmd
                version = os.popen('./%s 0 0 --version'%(model)).read()
                run ='./%s %s %d %s'%(model,int(g[0]),obs,debug)
                print '\n'+ run, ' of version ' , version ;
                
                ##the actual run
                start = time.strftime("%s");os.system(run)
                wall = int(time.strftime("%s")) - int(start)

                
                #return data
                data = {'wall':wall,'group':g[1],'vers':version.strip(),'id':g[0]}
                      

                #next task        
                n+=(ncpus-1)


                for i in pbar(xrange(lgroups)):
                
                        #blocking recieve! 
                        req = data      
                        #req.Wait()
                        g = hf[req['group']]

                        print 'Finished' , req, '. Cleaning and Saving.'
                        
                        g.attrs['version'] = req['vers']
                        
                        for dataset in ['spec','rate','flux']:
                            data = readfun('%s.%s'%(req['id'],dataset))     
                            
                            print data[1].shape,len(data[
                            0].split(','))#remove non/zero results through mask 
                         
                            dataarr = data[0].split(',')
                            mask = data[1].sum(axis=0)
                            if dataset != 'spec':
                                #only save reaction which contain species 
                                match = re.compile(r'\b(\w+)\b')
                                fltr=set(fltr)
                                keep = [len(set(match.findall(i))-fltr)==0 for i in dataarr]
                                
                                mask *= np.array(keep)
                            
                            mask = np.where(mask)
          
                            fltr = np.array(dataarr)[mask]
                            
                            
                            g.attrs[dataset + u'head']  = ','.join(fltr)
                            data[1]  = np.squeeze(data[1][...,mask],axis = 1)

                            try: g[dataset]
                            except:extend=False
                            
                            if not extend :
                                g.create_dataset(dataset, data=data[1] , chunks=True,maxshape=(None,None))
                            else:    
                                print 'already saved'
                                #print g[dataset]
                                #g[dataset] = g[dataset].extend(data[1])     ### if exists extend this 
                                
                                #use lines below
                                #g[dataset].resize((g[dataset].shape[0] + data[1].shape[0]),axis=0)
                                #g[dataset][-data[1].shape[0]:] = data[1]
                        ### move status bar to here !!! 
                        #print g[dataset]
                        
                    
                    
                    #print req,g.items()
                    
                
                

        hf.close()
        print 'written' , filename
         




