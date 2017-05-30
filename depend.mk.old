# DO NOT DELETE THIS LINE - used by make depend
model_Function.o: model_Parameters.o
model_Global.o: model_Parameters.o
model_Initialize.o: model_Global.o model_Parameters.o
model_Integrator.o: model_Function.o model_Global.o model_Jacobian.o
model_Integrator.o: model_LinearAlgebra.o model_Parameters.o model_Rates.o
model_Jacobian.o: model_JacobianSP.o model_Parameters.o
model_LinearAlgebra.o: model_JacobianSP.o model_Parameters.o
model_Main.o: src/initialisations.inc
model_Main.o: model_Global.o model_Integrator.o model_Monitor.o
model_Main.o: model_Parameters.o model_Rates.o model_Util.o model_constants.o
model_Model.o: model_Function.o model_Global.o model_Integrator.o
model_Model.o: model_Jacobian.o model_LinearAlgebra.o model_Monitor.o
model_Model.o: model_Parameters.o model_Precision.o model_Rates.o model_Util.o
model_Parameters.o: model_Precision.o
model_Rates.o: model_Global.o model_Parameters.o model_constants.o
model_Util.o: model_Global.o model_Integrator.o model_Monitor.o
model_Util.o: model_Parameters.o
model_constants.o: tuv_old/MCM3.inc src/rate_coeff/new_rate.inc.var
model_constants.o: src/rate_coeff/new_rate.inc.def TUV_5.2.1/MCM331.inc
model_constants.o: model_Global.o model_Precision.o
constants.mod: model_constants.o
