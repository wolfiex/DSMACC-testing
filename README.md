# DSMACC-testing

The heavily edited and improved version of the Dynamically Simple Model for Atmospheric Chemical
Complexity (DSMACC), as used in the Thesis:

Understanding the Atmosphere using graph theory, visualisation and machine learning 

by Daniel Ellis. 


## Cite
### If any of the code from this repository, please cite the codebase as follows:
<pending final changes to be made>

### Additionally the original work for the DSMACC model was accomplished by Emmerson and Evans, which should also be cited:

Emmerson, KM; Evans, MJ (2009) Comparison of tropospheric gas-phase
chemistry schemes for use within global models, *ATMOS CHEM PHYS*,
**9(5)**, pp1831-1845 [doi:
10.5194/acp-9-1831-2009](http://dx.doi.org/10.5194/acp-9-1831-2009) .




## Install




## testing
To test run `make test` or `pytest dsmacc/test/`. 



## Model debugging
f90 model output is presented in the temp.txt file. This should be your first point of call for problems with no visible output. 

It is then important to check that an initial conditions file `Init_cons.dat` has been created, and that the model has been compiled. Try `./model 0 0 --version` and `./model 0 0` to run the first set of initial conditions. 



### Compiler Notes
The intel compiler is preferable, although the makefile has been rewritten to fall back to gfortran should this not be available. In the rare case where ifort is installed, but not functional, you may have to either comment `#intel := $(shell command -v ifort 2> /dev/null)` within the Makefile (which disables the switch) or uninstall it for gfortran to be used. 






#---------------------------------------------



# dsmacc python library 
- python 3 hassle
- test scripts
- used to run parallel instances
- create constraints to observations
- preparse kpp mechanisms
- diagnostics and read tools



## reformat kppfiles
- `make kpp`
or 
-`python -m dsmacc.parsekpp.reformat.py`
(then use the ncurses interface - arrow keys, space and enter)

## Create a new run - and execute
-`python -m dsmacc.run -r -c`
(run, create)

## Run last modified intial conditions file (useful for testing)
-`python -m dsmacc.run -r -c -l`
(run, create, last)

## Spinup until steady state
- set spinup time in ics
- `python -m dsmacc.run -r -c -s`


## Observation constrains
- create the required files in format.... 
- `python -m dsmacc.observations.constrain <csvfilenamewithdata>`
- `python -m dsmacc.run -r -c -o`
























Try the wiki - also in progress but contains some debug tips.





TUV repository updated with thanks to @pb866

## Setting up files
1. Download organic mechanism from mcm.york.ac.uk. 
2. Place file in mechanisms folder (and optionally add a version name: `VERS='TroposphericChemistry'`
3. Reformat this to keep KPP happy. Use `make reformat` or `python -m dsmacc.parsekpp.reformat` for a quick format with additional deposition rates of 1/day.
4. run `make kpp`
5. run `make` to compile.

## Running a model
1. Set up the initial conditions csv file
2. To quickrun the model type `make run` or `python -m dsmacc.run -c -r`



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

### Parallel h5py - not enabled as none of the york hpc clusters have been configured to do this 
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



## Makefile
Type `make man` to see a description of available functions.

