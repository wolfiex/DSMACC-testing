
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
