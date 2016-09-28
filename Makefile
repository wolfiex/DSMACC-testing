  F90        = ifort  -L/usr/local/netcdf-ifort/lib -I/usr/local/netcdf-ifort/include/ -lnetcdff #mpifort #ifort
  FC         = ifort  -L/usr/local/netcdf-ifort/lib -I/usr/local/netcdf-ifort/include/ -lnetcdff # mpifort #ifort
  #F90FLAGS  = -Cpp --pca
  # F90FLAGS   = -Cpp --chk a,e,s,u --pca --ap -O0 -g --trap
  F90FLAGS   = -cpp  -mcmodel medium -O0 -fpp  #-openmp
##############################################################################

PROG = model 

# complete list of all f90 source files
SRCS1 = $(wildcard model_*.f90) constants.f90
SRCS2 = $(wildcard tuv_old/*.f)

# the object files are the same as the source files but with suffix ".o"
OBJS1 := $(SRCS1:.f90=.o) 
OBJS2 := $(SRCS2:.f=.o)

MAKEFILE_INC = depend.mk

# If you don't have the perl script sfmakedepend, get it from:
# http://www.arsc.edu/~kate/Perl
F_makedepend = ./sfmakedepend --file=$(MAKEFILE_INC)

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

distclean: clean
	rm -f $(PROG)
	rm -f depend.mk* 
	rm -f *.nc
	rm -f *.dat
	rm -f *.o 
	rm -f model_*
	rm -f run_*

kpp:clean
	./makedepos.pl
	./kpp-2.2.3/bin/kpp model.kpp
	make all 
	

# all object files *.o depend on their source files *.f90
# the object files are created with the "-c" compiler option
%.o: %.f90
	$(F90) $(F90FLAGS) $(LINCLUDES) -c $<
tuv_old/%.o: %.f
	$(F90) $(F90FLAGS) $(LINCLUDES) -c $<
# list of dependencies (via USE statements)
include depend.mk
# DO NOT DELETE THIS LINE - used by make depend
constants.o: old_rate.inc
constants.o: model_Global.o model_Precision.o
driver.o: initialisations.inc
driver.o: constants.o model_Global.o model_Integrator.o model_Monitor.o
driver.o: model_Parameters.o model_Rates.o model_Util.o
model_Global.o: model_Parameters.o
model_Initialize.o: model_Global.o model_Parameters.o
model_Integrator.o: model_Global.o model_Jacobian.o model_JacobianSP.o
model_Integrator.o: model_LinearAlgebra.o model_Parameters.o model_Precision.o
model_Integrator.o: model_Rates.o
model_Jacobian.o: model_JacobianSP.o model_Parameters.o
model_LinearAlgebra.o: model_JacobianSP.o model_Parameters.o
model_Main.o: initialisations.inc
model_Main.o: constants.o model_Global.o model_Integrator.o model_Monitor.o
model_Main.o: model_Parameters.o model_Rates.o model_Util.o
model_Model.o: model_Global.o model_Integrator.o model_Jacobian.o
model_Model.o: model_LinearAlgebra.o model_Monitor.o model_Parameters.o
model_Model.o: model_Precision.o model_Rates.o model_Util.o
model_Parameters.o: model_Precision.o
model_Rates.o: constants.o model_Global.o model_Parameters.o
model_Util.o: model_Global.o model_Integrator.o model_Monitor.o
model_Util.o: model_Parameters.o
