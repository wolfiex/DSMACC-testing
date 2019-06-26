OBJ   = cmn_fjx_mod.o fjx_sub_mod.o fjx_init_mod.o cld_sub_mod.o fjx72.o

FC    = ifort
FLAGS = -O2 -ip -fpp2 -W0 -assume byterecl

%.o: %.f
	$(FC) $(FLAGS) -c $<

jx    : $(OBJ)
	$(FC) $(FLAGS) -o JX70 $(OBJ)
