  F90        = ifort  #-L/usr/local/netcdf-ifort/lib -I/usr/local/netcdf-ifort/include/ -lnetcdff #mpifort #ifort
  FC         = ifort  #-L/usr/local/netcdf-ifort/lib -I/usr/local/netcdf-ifort/include/ -lnetcdff # mpifort #ifort
  #F90FLAGS  = -Cpp --pca
  # F90FLAGS   = -Cpp --chk a,e,s,u --pca --ap -O0 -g --trap
  # FDEP ?= 'depos.dat'         # data file variable for makedepos script
  # FEMI ?= 'emiss.dat'         # data file variable for makedepos script
  # FKPP ?= 'inorganic organic' # kpp input file variable for makedepos scrpit
  # FSTD  ?= 1                  # option to extend standard vd to all species
  # export FDEP, FEMI, FKPP, FSTD
  # MODELKPP ?= '--custom'
  F90FLAGS   = -assume bscc -cpp -mcmodel large -O0 -fpp -g -traceback   -heap-arrays  -ftz -implicitnone -fp-model strict #-fp-stack-check -check bounds -check arg_temp_created -check all #-warn all # -openmp
  

##############################################################################

#do not use -heap arrays in omp or parallel 

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
	ulimit -s unlimited #unlimit stack size

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
	rm -f .nfs*
	rm -f *model*
	rm -f run_
	rm -f *.old
	rm -rf DATA*
	rm -rf Outputs
	rm -f params
	rm -f *.png
	rm -f *.pyo

tuv: # compile tuv!
	rm -rf DATAJ1/ DATAE1/ DATAS1/ params
	cp -rf TUV_5.2.1/DATA* TUV_5.2.1/params .
	-cd TUV_5.2.1 && make clean && make && cd ../

large: # functions to deal with large mechanisms that wont compile !
	./src/large_mechanisms.py model_Jacobian*.f90
	./src/large_mechanisms.py model_Linear*.f90
	./src/large_mechanisms.py model_Rates.f90

#use make change mechanism='<path to mech>'
change: # changes organic in model.kpp , define new mech by typing mechanism = <mech name here> before running this command!
	ls && python ./src/mechparse.py $(mechanism)
	sed -i '6s!.*!#INCLUDE ./$(mechanism)!' src/model.kpp
	echo $(mechanism) 'updated in /src/model.kpp at line 6'


./Outputs:
	mkdir Outputs

new: distclean update_submodule tuv
	./src/sfmakedepend
	mkdir Outputs
	python -O -m py_compile AnalysisTools/explore_dsmacc.py
	mv AnalysisTools/explore_dsmacc.pyo explore.pyo

kpp: clean | ./Outputs #ini  # makes kpp using the model.kpp file in src!
	touch model
	$(eval export KPP_PATH=$(shell pwd)/src/kpp/kpp-2.2.3_01)
	$(eval export KPP_HOME=$(shell pwd)/src/kpp/kpp-2.2.3_01)
	#$(eval export KPP_HOME=$(shell pwd)/src/kpp/kpp-2.2.3_01)
	$(eval export PATH=$(KPP_PATH)/bin:$(PATH))
	@echo $(KPP_PATH)
	rm model
	cd $(KPP_PATH)/src && make
	python src/background/makemodeldotkpp.py $(MODELKPP)
	cp src/constants.f90 ./model_constants.f90
	-$(KPP_PATH)/bin/kpp model.kpp

kpp_custom: clean | ./Outputs  # makes kpp using the model.kpp file in src!
	touch model
	rm model
	cd src/kpp/kpp*/src && make
	python src/background/makemodeldotkpp.py --custom
	cp src/constants.f90 ./model_constants.f90
	-./src/kpp/kpp-2.2.3_01/bin/kpp model.kpp
	

ini: # generate kpp files with emission and deposition data
	cd ./mechanisms && perl makedepos.pl $(FKPP) $(FDEP) $(FSTD) && \
	perl makeemiss.pl $(FKPP) $(FEMI) && cd ..

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
