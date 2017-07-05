
## GEOSCHEM
Globchem files are included in the mechanisms directory. Photolysis rates for v11 are mapped in the TUV folder as GC11 and are taken from the fastjx engine, whose input file is located in src/background/geos...

Newer globchem.eqns files need to have the photolysis array (PHOTOL(x)) renamed as J(x) and checked that the eqns in GC11.inc are correct. 

There are several methods to run this, although using the make kpp_custom? flag may be easiest provided all the other files are correctly assembled. 

Additionally all the '+ hv' parts of the reactions must be removed. This can be done using `perl -p -i -e 's/\+\h*hv//g' mechanisms/geoschem/globchem.eqn` from the main directory. 

You must create a GC11 file in tuv using /src/background/g\*/c\*.py 

 

