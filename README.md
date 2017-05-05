# DSMACC-testing
Dan's version of the Dynamically Simple Model For Atmospheric Chemical Complexity --- still in development/testing

##Cite
Emmerson, KM; Evans, MJ (2009) Comparison of tropospheric gas-phase
chemistry schemes for use within global models, *ATMOS CHEM PHYS*,
**9(5)**, pp1831-1845 [doi:
10.5194/acp-9-1831-2009](http://dx.doi.org/10.5194/acp-9-1831-2009) .

## New user
Run `make new` to clean everything and update latest TUV.

## Updating the submodule (TUV)
This needs to be done to include contents here. 
Can be accomplished through `git submodule init
git submodule update` or typing `make update_submodule`

## Compiling 
0. run `make distclean`
1. If not done so already, go into the TUV folder, type `make clean && make`
2. Download mechanism from mcm website and place into organic.kpp
3. Add any emmitions into emissions.kpp (these can be disabled)
4. Adjust deposition constant in ./makedepos.pl if needed
5. Run kpp and make by typing `make kpp`

## How to run
1. Create Init cons csv file (methane.csv as a template) 
 .. * different columns are different runs
 ..* depos and emiss are deposition / emission constants, set 1 to enable 0 do disable 
 ..* run names are useful, see +depos etc for examples. 

2. Run `python begin.py <youricfile.csv>` after setting the number of processes inside
..* this makes Init_cons.dat
..* generates run files. sdout is in run.sdout, individual run.nc
..* concatenates nc files including initial conditions, and run time into one grouped netcdf
..* to see the form of this have a look inside begin, or read_dsmacc

3. to view files:
..* ipython, then type read_dsmacc <ncfilename> for interactive play
..* run the PDF_concentrations.py file for a time series plot of all the runs (diagnostic purposes) - see .pdf files

### Notes:

## Updating the rate coefficients
A method to symplify the rate coefficients using a symbolic engine has been applied. This not only reduces the amount of computation that has to be done by the computer, but also allows for the constraint of fixed numerical rate constants as parameters (see KDEC bug). 

| Rate Cefficient | Original-eqn | Simplified-eqn |
| :---         |     :---:      |          ---: |
| git status   | git status     | git status    |
| git diff     | git diff       | git diff      |


To do this place your new rate file in the src folder, run simplfy_rates.py and update the constants.f90 code to inculde the newly generates .def and .var files

### Dependancies:
+ Ifort (Intel)
+ Netcdf
+ anacondas python (continuum.io)
**Ensure you build kpp in the kpp folder

### Changes:
+ Reorganised code / removed unnecessary loops
+ CH4 intiation fix 
+ removed multiline serial read and replaced with initation program 
+ repaced initial conditions with csv file
+ added the output to netcdf (needs netcdf libraries)
+ added emission / deposition switches
+ improved makefile 
+ MCM TUV 5 updated
