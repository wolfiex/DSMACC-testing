#INLINE F90_GLOBAL
  REAL(dp) :: PRESS, LAT, LON, O3COL, JO1D, JNO2,DEPOS
  REAL(dp) :: JDAY, JREPEAT, ALBEDO, SAREA, RP1
  INTEGER :: INIT_TIME, NOX(NVAR)
  REAL(dp):: CONSTRAIN(NVAR),const_method(NSPEC+10)
  CHARACTER(LEN=15) :: spec_name(NSPEC+10)!10000
  LOGICAL :: SPEC_CH4, SPEC_H2
  INTEGER :: IntTime,daycounter
  LOGICAL :: CONSTRAIN_NOX, SAVE_LEGACY
  LOGICAL :: CONSTRAIN_RUN, LAST_POINT, OUTPUT_LAST
  INTEGER, PARAMETER :: OUTPUT_UNIT = 24
  INTEGER, PARAMETER :: ERROR_UNIT = 0
  INTEGER, PARAMETER :: SPEC_UNIT = 10
  INTEGER, PARAMETER :: RATE_UNIT = 12
  Logical :: new_tuv = .True. 
  character(len=3) :: mechanism
  REAL(dp), allocatable :: output_s(:,:),output_r(:,:)
!Photolysis variables
  include './TUV5.2.1/params'
  REAL*8::bs(19,kj), cs(19,kj),ds(19,kj)
  REAL::svj_tj(kt,kj), szas(kt), jfactno2, jfacto1d
!End photolysis variables
#ENDINLINE {above lines go into MODULE KPP_ROOT_Global}

