  F90        = ifort  #-L/usr/local/netcdf-ifort/lib -I/usr/local/netcdf-ifort/include/ -lnetcdff #mpifort #ifort
  FC         = ifort  #-L/usr/local/netcdf-ifort/lib -I/usr/local/netcdf-ifort/include/ -lnetcdff # mpifort #ifort
  #F90FLAGS  = -Cpp --pca
  # F90FLAGS   = -Cpp --chk a,e,s,u --pca --ap -O0 -g --trap
  F90FLAGS   = -assume bscc -cpp -mcmodel medium -O0 -fpp  #-openmp
##############################################################################
#colour
black="\033[90m"
red="\033[91m"
green="\033[92m"
yellow="\033[93m"
blue="\033[94m"
purple="\033[95m"
cyan="\033[96m"
white="\033[97m"
nocol="\033[0m"
#################

PROG = model

# complete list of all f90 source files
SRCS1 = $(wildcard model_*.f90)
SRCS2 = $(wildcard TUV_5.2.1/*.f)

# the object files are the same as the source files but with suffix ".o"
OBJS1 := $(SRCS1:.f90=.o)
OBJS2 := $(SRCS2:.f=.o)

MAKEFILE_INC = depend.mk

# If you don't have the perl script sfmakedepend, get it from:
# http://www.arsc.edu/~kate/Perl
F_makedepend = ./src/sfmakedepend --file=$(MAKEFILE_INC)
perl = /usr/bin/perl #perl path

all: $(PROG) # default make cmd !

# the dependencies depend on the link
# the executable depends on depend and also on all objects
# the executable is created by linking all objects
$(PROG): depend $(OBJS1) $(OBJS2)
	perl -p -i -e 's/\!\s*EQUIVALENCE/EQUIVALENCE/g' model_Global.f90;
	$(F90) $(F90FLAGS) $(OBJS1) $(OBJS2) -o $@

# update file dependencies
depend $(MAKEFILE_INC): $(SRCS1) $(SRCS2)
	$(F_makedepend) $(SRCS1) $(SRCS2)

clean: # remove others
	rm -f $(OBJS1) *model* *.mod *.log *~ depend.mk.old *.o *.sdout *.tee #$(OBJS2)

clear: # remove temp and run files only !
	rm -f *.nc *.sdout run_* del* *.pdf *.spec *.rate *.names Outputs/*

distclean: clean clear # clean all !
	rm -f $(PROG)
	rm -f depend.mk*
	rm -f *.nc
	rm -f *.dat
	rm -f *.o
	rm -f *model*
	rm -f run_
	rm -f *.old
	rm -rf DATA*
	rm -rf Outputs
	rm -f params
	rm -f *.png

tuv: # compile tuv!
	rm -rf DATAJ1/ DATAE1/ DATAS1/ params
	cp -rf TUV_5.2.1/DATA* TUV_5.2.1/params .
	cd TUV_5.2.1 && make clean && make && cd ../

large: # functions to deal with large mechanisms that wont compile !
	./src/large_mechanisms.py model_Jacobian*.f90
	./src/large_mechanisms.py model_Linear*.f90
	./src/large_mechanisms.py model_Rates.f90

#use make change mechanism='<path to mech>'
change: # changes orgnaic in model.kpp , define new mech by typing mechanism = <mech name here> before running this command!
	ls && python ./src/mechparse.py $(mechanism)
	sed -i '6s!.*!#INCLUDE ./$(mechanism)!' src/model.kpp
	echo $(mechanism) 'updated in /src/model.kpp at line 6'


./Outputs:
	mkdir Outputs

new: distclean update_submodule tuv
	./src/sfmakedepend
	mkdir Outputs	

kpp: clean | ./Outputs  # makes kpp using the model.kpp file in src!
	touch model
	rm model
	cd src/kpp/kpp*/src && make
	cd mechanisms && ./makedepos.pl && cd ../
	./src/background/makemodeldotkpp.py
	cp src/constants.f90 ./model_constants.f90
	./src/kpp/kpp-2.2.3_01/bin/kpp model.kpp
	rm -rf *.kpp

kpp_custom: clean | ./Outputs  # makes kpp using the model.kpp file in src!
	touch model
	rm model
	cd src/kpp/kpp*/src && make
	cd mechanisms && ./makedepos.pl && cd ../
	./src/background/makemodeldotkpp.py --custom
	cp src/constants.f90 ./model_constants.f90
	./src/kpp/kpp-2.2.3_01/bin/kpp model.kpp
	rm -rf *.kpp

tidy: # removes fortran files from main directory whist retaining model and run data!
	rm model_* *.mod del* *.del

%.o: %.f90
	$(F90) $(F90FLAGS) $(LINCLUDES) -c $<
TUV_5.2.1/%.o: %.f
	$(F90) $(F90FLAGS) $(LINCLUDES) -c $<

## section to run a server and display results on web page
ropaserver: # creates a ropa file from latest nc file and displays on server!
	python ./AnalysisTools/ropatool/ropa_tool.py *.nc
	make displayropa

displayropa: # runs a server for timeout period!
	cd AnalysisTools/ropatool/ && timeout 3600 python -m SimpleHTTPServer 8000
	make killserver




killserver: # kills a running server on port 8000!
	fuser -k 8000/tcp

#man cmd list
man: # print each make function in list!
	perl -lne 's/#/\n\t\t\$(blue)/;s/!/\$(nocol)\n/;print $1 if /([^\.]{2,99}):\s(.*)/;' Makefile

#downloads required submodules
update_submodule: # print each make function in list!
	git submodule init
	git submodule update

#save model for multi use -  make save name=<yourmodelname>
savemodel:
	rm -rf ./save/exec/$(name)
	mkdir ./save/exec/$(name)
	python	./src/background/movetotemp.py $(name)
  
#lists all models
lsmodels: 
	ls ./save/exec
    
#removes a saved model - make rmmodel name=<yourmodelname>
rmmodel:
	rm -rf ./save/exec/$(name)

# list of dependencies (via USE statements)
include depend.mk
# DO NOT DELETE THIS LINE - used by make depend
model_Global.o: params
model_Global.o: model_Parameters.o
model_Initialize.o: model_Global.o model_Parameters.o
model_Integrator.o: model_Global.o model_Jacobian.o model_LinearAlgebra.o
model_Integrator.o: model_Parameters.o model_Rates.o
model_Jacobian.o: model_JacobianSP.o model_Parameters.o
model_LinearAlgebra.o: model_JacobianSP.o model_Parameters.o
model_Main.o: src/initialisations.inc
model_Main.o: model_Global.o model_Integrator.o model_Monitor.o
model_Main.o: model_Parameters.o model_Rates.o model_Util.o model_constants.o
model_Model.o: model_Global.o model_Integrator.o model_Jacobian.o
model_Model.o: model_LinearAlgebra.o model_Monitor.o model_Parameters.o
model_Model.o: model_Precision.o model_Rates.o model_Util.o
model_Parameters.o: model_Precision.o
model_Rates.o: model_Global.o model_Parameters.o model_constants.o
model_Util.o: model_Global.o model_Integrator.o model_Monitor.o
model_Util.o: model_Parameters.o
model_constants.o: tuv_old/MCM3.inc src/rate_coeff/new_rate.inc.var
model_constants.o: src/rate_coeff/new_rate.inc.def TUV_5.2.1/MCM331.inc params
model_constants.o: model_Global.o model_Precision.o
constants.mod: model_constants.o
