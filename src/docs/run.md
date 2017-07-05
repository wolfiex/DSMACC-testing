## An example of how to run DSMACC
#### Start the Run script. This will open a selection menu showing all available initial conditions files. Please select which one you wish to run. 

**Optional flags are: **

-saved : (advanced) runs model using saved versions when -modelname is provided

-keepx : does not ignore runs marked with an X in the beginning

-icsonly : does not run the model, merely creates an intial conditions file for legacy reasons.


```python
python begin.py
```

![ ](img/begin)



#### Running Screen
A progress bar and initialisation conditions have been added for convenience. These should fill up when model is running. If the model stalls for a long period of time, the likelyness is that tuv may not have been compiled properly. 



![ ](img/running)


## How to run (old doc info)

Ensure tuv is compiled, if in doubt run `make tuv` should no other error
  be apparent and the program hangs -




1. **Create Init cons csv** file in the InitCons directory 

      * See (methane.csv as a template)

      * Different columns correspond to different runs
      
      * DEPOS and EMISS are deposition/emission constants; set concentration rows as 1 to enable,
        0 do disable
        
      * Run names are useful, see existing files as an example.
      
      
      
      
      
2. **Run `python begin.py`** 

      * set the number of processes inside this script - the default is 4.
  
      * This makes the `Init_cons.dat` as used by DSMACC
      
      * Run files are generated in the Outputs folder: sdout is in run.sdout, individual run.nc
      
      * Model output binary is concatenated into a single netCDF file. 
        
      * To see the form of this have a look inside begin.py or read_dsmacc.py
        in AnalysisTools



3. To view files: [see this](src/docs/view_results.md)
