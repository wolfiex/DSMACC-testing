'''
A cumelative page rank algorith for errors of a temporal network.
'''
import numpy as np
import operator


class Sparse3D:
      '''
      A 3 Dimentional sparse matrix represenatation.

      Autoinput:
          adjacency - n x n matrix of value items (items can be anything)
          names - list of names (e.g. G.nodes())

      onnone:
          value or object to return when a non-existant link is summoned.
      '''
      data = {}
      names = None
      log10log=[False,False]
      
      reversed = 0
      def __init__(self,adjacency_matrix = None, names = None, onnone=0):

            self.onnone = onnone

            if adjacency_matrix != None:
              vals=len(adjacency_matrix)
              if names!= None:
                assert(val == len(names))
                self.names = names
              else:
                self.names=range(val)

              for i in range(vals):
                  for j in range(vals):
                        dummy  = adjacency_matrix[i,j]
                        if dummy: self.data[(names[i],names[j])] = dummy

      def add(self, source,target, values):
          self.data[(source,target)] = values

      def read(self, source,target):
            try:
              value = self.data[(source,target)]
            except KeyError:
              value = self.onnone
            return value

      def reverse(self):
          self.reversed += 1
          self.data =  dict(zip([(X[1],X[0]) for X in list(self.data.keys())],self.data.values()))

      def get_rowkeys (self, fn = 'csc_keys'):
          fn = getattr(self,fn)
          self.rowkeys = [filter(lambda x: x[0] is i, fn()) for i in range(len(self.names))]
          
      def get_colkeys (self, fn = 'csc_keys'):
          '''
          goes into keys
          fn [keys, csc_keys, csc_keys]
          '''
          fn = getattr(self,fn)
          self.colkeys = [filter(lambda x: x[1] is i, fn()) for i in range(len(self.names))]
      
      
      def log10normalise(self,minlink = 0.001,zeronans = False):
          all_data = np.array(self.data.values()) 
          
          if not self.log10log[0]:
              all_data = np.log10(all_data)
              all_data[np.isinf(all_data)] = np.nan
              
              mn = np.nanmin(all_data)
              all_data -= mn
              mx = np.nanmax(all_data)
              all_data /= mx
              
              all_data = minlink + (1.-minlink)*all_data
              self.log10log[0]=True
              
          else: 
              print ('You already have the log 10 values!') 
          
          if zeronans and not self.log10log[1]: 
              all_data[np.isnan(all_data)] = 0. 
              self.log10log[1]=True
          
          all_data = dict(zip( self.data.keys(),all_data[:] ))
          self.data = all_data
          
      def to_numpy_matrix(self,elementnumber=0, parray = None): 
          ''' 
          Function to return an adjacency matrix for a certain timestep 
          Inputs:
              elementnumber [numerical index or 'teleport']
              parray - if teleporting we can specify a probability array for picking each timestep (more important times)
              
          Returns: 
             list (matrix, node names, elementnumber)
          '''
          n = len(self.names)
          rt = np.zeros((n,n))
          
          if elementnumber == 'teleport':
                try: self.number_timesteps
                except: self.number_timesteps = len(self.data.values()[0])
                tsrange = range(self.number_timesteps)
                        
          for i in self.data:
              if elementnumber == 'teleport':
                  #select a new teleportation link at random. 
                  elementnumber = np.random.choice(tsrange, replace=False, p=parray)
              rt[i[0],i[1]] = self.data[i][elementnumber]
              
          return (rt,self.names,elementnumber)
            
      def csc_keys(self):
          return sorted(self.data.keys(), key = operator.itemgetter(1,0)) #faster!
          #sorted(self.data.keys(), key=lambda x: x[1])
      def csr_keys(self):
          return sorted(self.data.keys(), key = operator.itemgetter(0,1))    
      def keys(self):
          return self.data.keys()   

      def init_pr(self):
          self.get_rowkeys()
          #from to normalise everything going out
          try: self.number_timesteps
          except: self.number_timesteps = len(self.data.values()[0])
          
          rsum =[]
          for columns in self.rowkeys:
          #data as a fraction of total weight incident on that node (fraction of influx)
              total = np.zeros(self.number_timesteps)
              for j in columns:
                  total += self.data[j]
              rsum.append(total)
              
              with np.errstate(divide='ignore'): # Ignore division by 0 on ranks/deg_out_beta
                  for j in columns:
                    dummy = self.data[j] /  total 
                    dummy[~np.isfinite(dummy)] = 0.
                    self.data[j] = dummy
              self.rsum = rsum
              
      def googley (self, timestep = 0 , alpha = 0.85, parray = None , personalization = None, nodelist=None, dangling=None):
            ''' 
            Create a google_matrix for our data. See networkx documentation for more information. 
              Inputs: 
                alpha - damping factor (float)
                timestep - [weight array index or 'teleport' or a random selection] (number|str)
                parray - probability array for time selection if using 'teleport' (list)
                personalisation - optional node weightings corresponding to importance (dict)
                '''
            try: self.number_timesteps
            except: self.number_timesteps = len(self.data.values()[0])
               
            n = len(self.names)
            if personalization is None:  p = np.repeat(1.0 / float(n), n)
            
            else:
                  p = np.array([personalization.get(n, 0) for n in self.names], dtype=float)
                  p /= p.sum()
            
            M = self.to_numpy_matrix(elementnumber=timestep,parray=parray)[0]
            # Assign dangling_weights to any dangling nodes (nodes with no out links)
            # Dangling nodes
            if dangling is None:
                dangling_weights = p
            else:
                # Convert the dangling dictionary into an array in nodelist order
                dangling_weights = np.array([dangling.get(n, 0) for n in nodelist],
                                            dtype=float)
                dangling_weights /= dangling_weights.sum()
            dangling_nodes = np.where(M.sum(axis=1) == 0)[0]

            # Assign dangling_weights to any dangling nodes (nodes with no out links)
            for node in dangling_nodes:
                M[node] = dangling_weights
                
            return M*alpha + (1 - alpha) * p

      def pr(self, timestep = 0 , alpha = 0.85, parray = None , personalization = None):
            M = self.googley(timestep , alpha, parray  , personalization )
            eigenvalues, eigenvectors = np.linalg.eig(M.T)
            ind = np.argmax(eigenvalues)
            # eigenvector of largest eigenvalue is at ind, normalized
            largest = np.array(eigenvectors[:, ind]).flatten().real
            norm = float(largest.sum())
            return dict(zip(self.names, map(float, largest / norm)))            
                  
          
              
def net2sparse(net_edges):
    '''
    Input:
        net_edges (pandas dataframe, columns: source->target)
    Output:
        Sparse3D object
    '''

    sp = Sparse3D()
    names = list(set([i for j in (k.split('->') for k in net_edges.columns) for i in j]))
    names.sort()
    sp.names = names

    names = dict(zip(names,range(len(names))))

    for c in net_edges.columns:
        col = net_edges[c]
        name = [names[x] for x in c.split('->')]

        dummy = col*(col>0)
        if dummy.max() > 0 :
            sp.add(name[0],name[1],dummy.values)

        dummy = abs(col*(col<0))
        if dummy.max() > 0 :
            sp.add(name[1],name[0],dummy.values)

    return sp
