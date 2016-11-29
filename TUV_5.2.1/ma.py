def running_mean(x, N):
    import numpy
    cumsum = numpy.cumsum(numpy.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / N

import numpy as np
data = np.loadtxt('wlweight.dat',float,'#')
lrm = 10
rm = running_mean(data[:,1],lrm)
ma = np.zeros((len(data)))
ma[lrm-1:] = rm
np.savetxt('weightz500x0.dat',(np.transpose([data[:,0],ma])))
rm = running_mean(data[:,2],lrm)
ma = np.zeros((len(data)))
ma[lrm-1:] = rm
np.savetxt('weightz500x50.dat',(np.transpose([data[:,0],ma])))