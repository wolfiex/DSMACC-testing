#INLINE F90_GLOBAL
  REAL(dp) :: PRESS, LAT, LON, O3COL, JO1D, JNO2,DEPOS
  REAL(dp) :: JDAY, JREPEAT, ALBEDO, SAREA, RP1
  INTEGER :: INIT_TIME, NOX(NVAR)
  REAL(dp):: CONSTRAIN(NVAR)
  INTEGER :: const_method(NSPEC+10)
  REAL(dp), allocatable :: SPIN_CONST(:) ! constrain array for spinup
  CHARACTER(LEN=15) :: spec_name(NSPEC+10)!10000
  LOGICAL :: SPEC_CH4, SPEC_H2
  INTEGER :: IntTime,daycounter,SPINUP
  LOGICAL :: CONSTRAIN_NOX, SAVE_LEGACY
  LOGICAL :: CONSTRAIN_RUN, LAST_POINT, OUTPUT_LAST
  INTEGER, PARAMETER :: OUTPUT_UNIT = 24
  INTEGER, PARAMETER :: ERROR_UNIT = 0
  INTEGER, PARAMETER :: SPEC_UNIT = 10
  INTEGER, PARAMETER :: RATE_UNIT = 12
  INTEGER, PARAMETER :: jmax= 8100, szabin=19

  character(len=3) :: mechanism
  REAL(dp), allocatable :: output_s(:,:),output_r(:,:)
!Photolysis variables
  include './params'
  INTEGER :: TUVvers = 1
  REAL(8) ::            bs(szabin,kj), cs(szabin,kj),ds(szabin,kj)
  REAL(4) ::            svj_tj(kt,kj), szas(kt), jfactno2, jfacto1d
!End photolysis variables
#ENDINLINE {above lines go into MODULE KPP_ROOT_Global}

