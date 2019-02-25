# DSMACC-testing

Dan's version of the Dynamically Simple Model for Atmospheric Chemical
Complexity --- still in development/testing

Try the wiki - also in progress but contains some debug tips.


## Cite
Emmerson, KM; Evans, MJ (2009) Comparison of tropospheric gas-phase
chemistry schemes for use within global models, *ATMOS CHEM PHYS*,
**9(5)**, pp1831-1845 [doi:
10.5194/acp-9-1831-2009](http://dx.doi.org/10.5194/acp-9-1831-2009) .


TUV repository updated with thanks to @pb866

## Setting up files
1. Download organic mechanism from mcm.york.ac.uk. 
2. Place file in mechanisms folder (and optionally add a version name: `VERS='TroposphericChemistry'`
3. Reformat this to keep KPP happy. Use `make reformat` or `python -m dsmacc.parsekpp.reformat` for a quick format with additional deposition rates of 1/day.
4. run `make kpp`
5. run `make` to compile.

## Running a model
1. Set up the initial conditions csv file




## Install

#### General
To install we may use the (Yet Another Markup Language) file.

```
export MPICC=\`which mpicc\` &&
export CC=mpicc &&
conda-env create -f meta.yaml
```

And to use this, we run (or add within our .bashrc):

`source activate dsmacc-env`


### Parallel Libraries

If parallel installs fail, remove the conda installs, then follow the instructions below.

#### mpi4py
First we make sure the correct modules are loaded:
`module load intel-mpi/intel/....`

Set the loaded version of MPI to be used with mpi4py
`export MPICC=\`which mpicc\``

Then run `pip install mpi4py`

### Parallel h5py
1 Build hdf5 library with the following flags (note many clusters dont seem to do this for some reason)
`$./configure --enable-parallel --enable-shared`
Note that --enable-shared is required.

```
$ h5cc -showconfig
```

```
$ export CC=mpicc
$ python setup.py configure --mpi [--hdf5=/path/to/parallel/hdf5]
$ python setup.py build
```

Notes :
- Cannot constrain to 0 due to spinup conditions, either use giant sink
or FIX species [util.inc]





If mpirun failes with [] then run has failed.



# Updates to run procedures
Compile and prep as before, these changes only affect the running.
Filenames may have to be manually changed for the time being, .... sorry.

To create ics: `python run.py -c`

This makes a hdf5 file containing all your information.


To run: `python run.py -s`

If the env variable NCPUS is set, it uses this for an mpi run of the model, else a serial run is set. On earth, each queue automatically  sets the NCPUS environment variable.

To read: in ipython `run zhdf;  a = new('yourfilename.hdf'); a.specs / rates / flux`



Custom mydepos definition file in src - change depos without having to run kpp, just make

# Install and run kpp as before! Run / read model using above

## New user
Run `make new` to clean everything, update latest TUV, and download KPP. __In order to
initialise all submodules correctly, you need to have a clean repository.__

## Updating the submodule (TUV and KPP)
This needs to be done to include contents here.
Can be accomplished through `git submodule init;
git submodule update` or typing `make update_submodule`


## Documentation Contents

1. [**How to compile**](src/docs/compile.md)
2. [**How to run**](src/docs/run.md)
3. [ErrorCodes](src/docs/errors.md)
4. [**How to plot**](src/docs/view_results.md)
5. [Advanced features](src/docs/advancedrunning.md)
6. [Constrain to obs.](http://htmlpreview.github.io/?https://github.com/wolfiex/DSMACC-testing/blob/master/src/docs/constrain_obs.html)
7. [Updating TUV](src/docs/newtuv.md)
8. [GeosCHEM](src/docs/geoschem.md)
9. [Changes](src/docs/changes.md)



## Makefile
Type `make man` to see a description of available functions.


## Optional extras
- [x] MCM subset selector in mechanisms - this uses an init cons file to
  generate the smallest mechanism required by the model.
- [x] read DSMACC output routine in analysis tools.
- [x] plot all concentrations / reaction rates as a PDF for diagnostics
  in analysis tools and ropa tool
- [x] animated ropa plotter (alternatively you can use the online version -
  link to be added soon)


## Notes:

### Dependancies:
+ Ifort (Intel)
+ Netcdf4 (python)
+ Anacondas Python (continuum.io)
+ icc & bison for kpp
+ perl
