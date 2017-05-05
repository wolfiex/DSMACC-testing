# DSMACC-testing
Dan's version of the Dynamically Simple Model For Atmospheric Chemical Complexity --- still in development/testing

##Cite
Emmerson, KM; Evans, MJ (2009) Comparison of tropospheric gas-phase
chemistry schemes for use within global models, *ATMOS CHEM PHYS*,
**9(5)**, pp1831-1845 [doi:
10.5194/acp-9-1831-2009](http://dx.doi.org/10.5194/acp-9-1831-2009) .

## New user
Run `make new` to clean everything and update latest TUV.

## Updating the submodule (TUV and KPP)
This needs to be done to include contents here. 
Can be accomplished through `git submodule init;
git submodule update` or typing `make update_submodule`

## Compiling 
1.`make distclean && make new` to clear all, else use `make clear` or `make clean` 
2. Download mechanism from mcm website and place into mechanisms/organic.kpp
3. Add any emissions into emissions.kpp (these can be disabled in ICs)
4. Adjust deposition constant in ./makedepos.pl if needed (currently being updated)
5. Run kpp and make by typing `make kpp`
6. `make`

## How to run
1. Create Init cons csv file (methane.csv as a template) 
 .. * different columns are different runs
 ..* depos and emiss are deposition / emission constants, set 1 to enable 0 do disable 
 ..* run names are useful, see + depos etc for examples. 

2. Run `python begin.py` after setting the number of processes inside
..* this makes Init_cons.dat
..* generates run files. sdout is in run.sdout, individual run.nc
..* concatenates nc files including initial conditions, and run time into one grouped netcdf
..* to see the form of this have a look inside begin, or read_dsmacc

3. to view files:
..* ipython, then type `run AnalysisTools/read_dsmacc <ncfilename>` for interactive play
..* run the PDF_concentrations.py file for a time series plot of all the runs (diagnostic purposes) - see .pdf files



## Updating the rate constants
Rate-constant simplification through the use of a symbolic engine has been applied. This reduces computation and allows the setting of  parameters for fixed numeric constants (see KDEC bug). An example of some equations below.

| Rate Cefficient | Original-eqn | Simplified-eqn |
| :---         |     :---:      |          ---: |
| krd   |  kd0/kdi    |   5.79e\-23\*m\*exp(4000\/temp) |
|  ncd  |   0.75-1.27*(log10(fcd))  | 1.41   |
|  kbpan  |  (kd0*kdi)*fd/(kd0+kdi) |  fd\*kd0\*kdi\/(kd0 + kdi)  |
|  kr1  |   k10/k1i  |  3.32e\-18\*m\*temp\*\*(\-1.3)  |
|  f1  |   	10**(log10(fc1)/(1+(log10(kr1)/nc1)**2))  | 10\*\*(-0.07\/(1 + log10(kr1)\*\*2\/nc1**2))   |
|  kmt12  |    (k120*k12i*f12)/(k120+k12i) |  2e\-12\*f12\*k120\/(k120 + 2e\-12)  |


To do this place your new rate file in the src folder, run simplfy_rates.py and update the constants.f90 code to inculde the newly generates .def and .var files

## Notes:

### Dependancies:
+ Ifort (Intel)
+ Netcdf4 (python)
+ Anacondas Python (continuum.io)
+ icc & bison for kpp
+ perl

### Changes:
+ Reorganised code / removed unnecessary loops
+ CH4 intiation fix 
+ removed multiline serial read and replaced with initation program 
+ repaced initial conditions with csv file
+ added the output to netcdf (needs netcdf libraries)
+ added emission / deposition switches
+ improved makefile 
+ MCM TUV 5 updated
+ simplification of rate constants
+ start multiple parallel runs
+ peters hardwired photolysis rate generator
+ depos default + manual override
