    #@mprof(precision=4)    
    
    def calcFlux(self,timesteps=False, specs=False,io=None):
          
        ''' 
        Inputs: 
            timesteps = a list of all time values required
            specs = a list of all posible species we may be interested in
        
         
       
        '''
    
        if self.flux:        
            print '.flux already calculated, to recalculate reset by typing: \n <classname>.flux= False'
            return None
            
        else: 
            
            if not specs: 
                myspecs = xrange(len(self.reactants))
                specs = self.spec.columns
            else:
                dummy = []
                for a in specs:
                    dummy.extend([item for sublist in self.prodloss[a].values() for item in sublist])
                myspecs = list(set(dummy) )
            
            
                
            if timesteps:    
                timesteps = self.ts[timesteps]
                
                   
                print '-------------------------------------------'     
                print 'start %d x %d flux array'%(len(timesteps),len(myspecs))    
                
                
                '''
                @timing 
                def a():
                '''

                
                def frxn (x,spc): 
                    if x == []: return 'empty'
                    
                    rn = re.compile(r'\s*([\.\d]*)(\D[\d\D]*)')   
                    rt = []
                    for a in x:
                        for j in xrange(len(a)):
                            
                            coeff=1.
                            try:
                                coeff*=float(rn.sub( r'\1', x[j]))
                                a[j] = rn.sub( r'\2', a[j])
                            except: None          
                        #prod multiple columns
                        
                        try:              
                            rt.append( np.array(spc.loc[:,a].prod(axis=1)*coeff,dtype=np.float))
                        except Exception as e:
                            rt.append( np.array(spc.loc[:,a]*coeff,dtype=np.float))
                    return rt

                
                #async mps
                
                results = [pool.apply_async(frxn, args=(self.reactants[x],self.spec.loc[timesteps,:]),) for x in  np.array_split(myspecs,ncores)]
                
                #sys.exit()
                
                bar = progressbar.ProgressBar()           

                results = [p.get() for p in bar(results)] 
                results = np.array([i for j in results for i in j])
                
                
                self.flux = dd.from_pandas(pd.DataFrame(results,columns=timesteps,index=myspecs) ,chunksize=50000)
                #self.flux =
                
                
                #
                           
                print 'Flux array complete'
                 
            else:    
                print 'No timesteps selected.'
                
            #pool.close()
            return 'Done'   
            
            
