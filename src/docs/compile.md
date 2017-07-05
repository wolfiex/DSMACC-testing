## An example of how to use KPP
#### Generates required f90 files for DSMACC


```
make kpp
```
This opens a list of available kpp files in the mechanisms folder. Select either one, or multiple by supplying a space between each selection. 


![ ](img/kppmech)


#### If run correctly this should produce no errors. 
Duplicate warnings will run, although may become problematic when trying to select an equation later on. Use the subset selector to eliminate these. 


![ ](img/kpp)




## Compiling
1. **Clear the directory.** If you are just starting or want a clean slate use `make distclean && make new` to clear all. 
Otherwise you can opt for `make clear or make clean` to remove the .f90/other files

2. **Download mechanism** from mcm website and save it in the mechanisms folder. If you wish to compile it with the inorganics.kpp for the MCM, please include the `_organics` tag in the name. All mechanism files require the `.kpp ` extention. 

3. Emissions/ Deposition may be adjusted <include something about peters script>. These can be enabled/disabled during runtime with the FEMISS and DEPOS flags in the Initial Conditions. 

4. **Create model.kpp and run kpp using `make kpp`**. Here you shall be tempted to select which mechanism/mechanisms you require. 

5. **Compile DSMACC** with `make`

\* If there is an error with the params file, tuv may not have been compiled (ie make new was not run). To fix this type `make tuv`  followed by `make`. 


