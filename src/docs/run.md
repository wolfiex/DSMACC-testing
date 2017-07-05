
## How to run

- Ensure tuv is compiled, if in doubt run `make tuv` should no other error
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

