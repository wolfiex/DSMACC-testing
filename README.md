# DSMACC-testing
Dan's version of the Dynamically Simple Model For Atmospheric Chemical Complexity

##Cite
Emmerson, KM; Evans, MJ (2009) Comparison of tropospheric gas-phase
chemistry schemes for use within global models, *ATMOS CHEM PHYS*,
**9(5)**, pp1831-1845 [doi:
10.5194/acp-9-1831-2009](http://dx.doi.org/10.5194/acp-9-1831-2009) .


## Compiling 
0. run `make distclean`
1. Download mechanism from mcm website and place into organic.kpp
2. Add any emmitions into emissions.kpp (these can be disabled)
3. Adjust deposition constant in ./makedepos.pl if needed
4. Run kpp and make by typing `make kpp`

## How to run
1. Create Init cons csv file (methane.csv as a template) 
..* different columns are different runs
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




### To do:
+ Modularise
+ add omp statements to kpp?
+ tidy
+ fix netcfd write problems
