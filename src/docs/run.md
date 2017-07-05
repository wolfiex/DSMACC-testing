
## How to run

Ensure tuv is compiled, if in doubt run `make tuv` should no other error
  be apparent and the program hangs -

1. **Create Init cons csv** file in hte InitCons directory see (methane.csv as a template)

      * Different columns correspond to different runs
      
      * DEPOS and EMISS are deposition/emission constants; set concentration rows as 1 to enable,
        0 do disable
        
      * Run names are useful, see existing files as an example.
      
      
2. *Run `python begin.py`* after setting the number of processes inside
   this script - the default is 4.
  
      * This makes the `Init_cons.dat` as used by DSMACC
      
      * Run files are generated in the Outputs folder: sdout is in run.sdout, individual run.nc
      
      * Model output binary is concatenated into a single netCDF file. 
        
      * To see the form of this have a look inside begin.py or read_dsmacc.py
        in AnalysisTools

3. To view files: [see this](src/docs/view_results.md)
