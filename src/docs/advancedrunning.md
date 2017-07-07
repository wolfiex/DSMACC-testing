
## Selecting custom mechanisms
1. For any mechanism, when you run `make kpp` it will ask you what .kpp
   mechanism (from the ./mechanisms folder) you wish to compile.
2. Choose all mechanisms needed- if multiple add a space between each selection.
3. If only one mechanism is selected, and this contains the word 'organic', then inorganic.kpp shall also automatically be included. 
4. These is also a custom option available from the makemodeldotkpp.py file. 
5. If you want to use the _model.kpp_ file from the _src_ folder, use
   `make kpp MODELKPP='--custom'`, which will copy _model.kpp_ from the
   _src_ folder to the main folder.




## Running with multiple models
1. Making a new model model and ensure it works
2. Type `make savemodel name=<yournamehere>` with what you wish to refer
   to your model with in the future
3. In your Initial conditions, at the description add your model name
   after a hyphen, e.g., myrun-mcm_new
4. Run using the saved flag `./begin.py -saved`

* only use a hyphen when providing a model name



## Alias run shortcuts
For those who do not know, aliases are shortcuts for command line functions and code snipets. For seasoned DSMACC users it may be easier to use these shortcuts than to have to type out the full commands all the time. To use these an alias must be included in your .bashrc or .profile file. Use of combinatory aliases should however be used with caution! 

Examples of some potentially useful commands are: 
106 alias b="python begin.py"
107 alias d="cd ~/DSMACC-testing"
108 alias k="make kpp && make"
109 alias ics="cd ~/DSMACC-testing/InitCons"
110 alias m="cd ~/DSMACC-testing/mechanisms"




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

