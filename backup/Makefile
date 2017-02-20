/usr.  F90        = ifort  #-L/usr/local/netcdf-ifort/lib -I/usr/local/netcdf-ifort/include/ -lnetcdff #mpifort #ifort
  FC         = ifort  #-L/usr/local/netcdf-ifort/lib -I/usr/local/netcdf-ifort/include/ -lnetcdff # mpifort #ifort
  #F90FLAGS  = -Cpp --pca
  # F90FLAGS   = -Cpp --chk a,e,s,u --pca --ap -O0 -g --trap
  F90FLAGS   = -cpp -mcmodel medium -O0 -fpp  #-openmp
##############################################################################

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

all: $(PROG)

# the dependencies depend on the link
# the executable depends on depend and also on all objects
# the executable is created by linking all objects
$(PROG): depend $(OBJS1) $(OBJS2)
	$(F90) $(F90FLAGS) $(OBJS1) $(OBJS2) -o $@

# update file dependencies
depend $(MAKEFILE_INC): $(SRCS1) $(SRCS2)
	$(F_makedepend) $(SRCS1) $(SRCS2)

clean:
	rm -f $(OBJS) *.mod *.log *~ depend.mk.old *.o *.sdout

clear:
	rm -f *.nc *.sdout run_* del* *.pdf *.spec *.rate *.names Outputs/*

distclean: clean
	rm -f $(PROG)
	rm -f depend.mk*
	rm -f *.nc
	rm -f *.dat
	rm -f *.o
	rm -f model_*
	rm -f run_

tuv:
	cd TUV_5.2.1 && make clean && make && cd ../

large:
	./src/large_mechanisms.py model_Jacobian*.f90
	./src/large_mechanisms.py model_Linear*.f90
	./src/large_mechanisms.py model_Rates.f90

#use make change mechanism='<path to mech>'
change:
	ls && python ./src/mechparse.py $(mechanism)
	sed -i '6s!.*!#INCLUDE ./$(mechanism)!' src/model.kpp
	echo $(mechanism) 'updated in /src/model.kpp at line 6'


kpp: clean
	cd mechanisms && ./makedepos.pl && cd ../
	cp src/model.kpp ./
	cp src/constants.f90 ./model_constants.f90
	./src/kpp-2.2.3/bin/kpp model.kpp
	rm -rf *.kpp

tidy:
	rm model_* *.mod del* *.del

%.o: %.f90
	$(F90) $(F90FLAGS) $(LINCLUDES) -c $<
TUV_5.2.1/%.o: %.f
	$(F90) $(F90FLAGS) $(LINCLUDES) -c $<

# list of dependencies (via USE statements)
include depend.mk
# DO NOT DELETE THIS LINE - used by make depend
model_Global.o: TUV_5.2.1/params
model_Global.o: model_Parameters.o
model_Initialize.o: model_Global.o model_Parameters.o
model_Integrator.o: model_Global.o model_Jacobian.o model_LinearAlgebra.o
model_Integrator.o: model_Parameters.o model_Rates.o
model_Jacobian.o: model_JacobianSP.o model_Parameters.o
model_LinearAlgebra.o: model_JacobianSP.o model_Parameters.o
model_Main.o: src/initialisations.inc
model_Main.o: model_Global.o model_Integrator.o model_Monitor.o
model_Main.o: model_Parameters.o model_Rates.o model_Util.o
model_Model.o: model_Global.o model_Integrator.o model_Jacobian.o
model_Model.o: model_LinearAlgebra.o model_Monitor.o model_Parameters.o
model_Model.o: model_Precision.o model_Rates.o model_Util.o
model_Parameters.o: model_Precision.o
model_Rates.o: model_Global.o model_Parameters.o
model_Util.o: model_Global.o model_Integrator.o model_Monitor.o
model_Util.o: model_Parameters.o
