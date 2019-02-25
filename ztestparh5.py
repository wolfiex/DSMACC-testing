import numpy as np
import h5py
from mpi4py import MPI
comm = MPI.COMM_WORLD   # Communicator which links all our processes together
rank = comm.rank        # Number which identifies this process.  Since we'll                         # have 4 processes, this will be in the range 0-3.
f = h5py.File('coords.hdf5', driver='mpio', comm=comm)
coords_dset = f['coords']
distances_dset = f.create_dataset('distances', (1000,), dtype='f4')
idx = rank*250  # This will be our starting index.  Rank 0 handles coordinate
# pairs 0-249, Rank 1 handles 250-499, Rank 2 500-749, and
# Rank 3 handles 750-999.
coords = coords_dset[idx:idx+250]
# Load process-specific data
result = np.sqrt(np.sum(coords**2, axis=1))
# Compute distances
distances_dset[idx:idx+250] = result
# Write process-specific data
f.close()
