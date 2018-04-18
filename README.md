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
