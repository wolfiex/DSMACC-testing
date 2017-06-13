# DSMACC-testing

Dan's version of the Dynamically Simple Model for Atmospheric Chemical
Complexity --- still in development/testing


## Cite
Emmerson, KM; Evans, MJ (2009) Comparison of tropospheric gas-phase
chemistry schemes for use within global models, *ATMOS CHEM PHYS*,
**9(5)**, pp1831-1845 [doi:
10.5194/acp-9-1831-2009](http://dx.doi.org/10.5194/acp-9-1831-2009) .


## New user
Run `make new` to clean everything, update latest TUV, and download KPP. __In order to
initialise all submodules correctly, you need to have a clean repository.__

## Updating the submodule (TUV and KPP)
This needs to be done to include contents here.
Can be accomplished through `git submodule init;
git submodule update` or typing `make update_submodule`

## Compiling
1. Run `make distclean && make new` to clear all, else use `make clear`
or `make clean`
2. Download mechanism from mcm website and save as mechanisms/organic.kpp
3. Add any emissions into emissions.kpp (these can be disabled in InitCons)
4. Adjust deposition constants in ./makedepos.pl, if needed
5. Adjust call of mechanism (kpp) files in model.kpp
6. Compile TUV with `make tuv` in the main DSMACC folder, if needed
7. Run kpp by typing `make kpp`
8. Compile DSMACC with `make`

## Selecting custom mechanisms
1. For any mechanism, when you run `make kpp` it will ask you what .kpp
   mechanism (from the mech. folder) you wish to compile.
2. Choose all mechanisms needed separately (<Number> + <ENTER>) and exit
   with the last exit option (<last number> + <ENTER>) when finished.
3. If you use the default names `organic.kpp` and `inorganic.kpp`, you
   can run the make command with the `--default` option using:
   ```
   make kpp MODELKPP='--default'
   ```
   __(No spaces around equal sign of MODELKPP!)__
4. If you want to use the _model.kpp_ file from the _src_ folder, use
   `make kpp MODELKPP='--custom'`, which will copy _model.kpp_ from the
   _src_ folder to the main folder.


## How to run

- Ensure tuv is compiled, if in doubt run make tuv should no other error
  be apparent and the program hangs -

1. Create Init cons csv file (methane.csv as a template)
  * Different columns are different runs
  * DEPOS and EMISS are deposition/emission constants; set 1 to enable,
    0 do disable
  * Run names are useful, see depos etc for examples.
2. Run `python begin.py` after setting the number of processes inside
   the script
  * This makes Init_cons.dat
  * Generates run files: sdout is in run.sdout, individual run.nc
  * Concatenates nc files including initial conditions and run time into
    one grouped netcdf
  * To see the form of this have a look inside begin.py or read_dsmacc.py
    in AnalysisTools
3. To view files, run:
  * ipython, then type `run AnalysisTools/read_dsmacc.py <ncfilename>`
    for interactive play
  * Run the PDF_concentrations.py file for a time series plot of all the
    runs (diagnostic purposes) - see pdf files

## Running with multiple models
1. Making a new model model and ensure it works
2. Type `make savemodel name=<yournamehere>` with what you wish to refer
   to your model with in the future
3. In your Initial conditions, at the description add your model name
   after a hyphen, e.g., myrun-mcm_new
4. Run using the saved flag `./begin.py -saved`

* only use a hyphen when providing a model name



## Makefile
Type `make man` to see a description of available functions.


## Optional extras
- [x] MCM subset selector in mechanisms - this uses an init cons file to
  generate the smallest mechanism required by the model.
- [x] read DSMACC output routine in analysis tools.
- [x] plot all concentrations / reaction rates as a PDF for diagnostics
  in analysis tools
- [x] ropa tool in main folder (may change)
- [x] animated ropa plotter (alternatively you can use the online version -
  link to be added soon)



## Updating the rate constants
Rate-constant simplification through the use of a symbolic engine has been
applied. This reduces computation and allows the setting of  parameters for
fixed numeric constants (see KDEC bug). An example of some equations below.

| Rate Cefficient | Original-eqn | Simplified-eqn |
| :---         |     :---:      |          ---: |
| krd   |  kd0/kdi    |   5.79e\-23\*m\*exp(4000\/temp) |
|  ncd  |   0.75-1.27*(log10(fcd))  | 1.41   |
|  kbpan  |  (kd0*kdi)*fd/(kd0+kdi) |  fd\*kd0\*kdi\/(kd0 + kdi)  |
|  kr1  |   k10/k1i  |  3.32e\-18\*m\*temp\*\*(\-1.3)  |
|  f1  |   	10**(log10(fc1)/(1+(log10(kr1)/nc1)**2))  | 10\*\*(-0.07\/(1 + log10(kr1)\*\*2\/nc1**2))   |
|  kmt12  |    (k120*k12i*f12)/(k120+k12i) |  2e\-12\*f12\*k120\/(k120 + 2e\-12)  |


To do this place your new rate file in the src folder, run
simplfy_rates.py and update the constants.f90 code to inculde the newly
generates .def and .var files

## Notes:

### Dependancies:
+ Ifort (Intel)
+ Netcdf4 (python)
+ Anacondas Python (continuum.io)
+ icc & bison for kpp
+ perl

### Changes:
+ Reorganised code / removed unnecessary loops
+ CH4 initiation fix
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
