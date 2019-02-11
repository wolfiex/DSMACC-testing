#INLINE F90_GLOBAL
  REAL(dp) :: PRESS, LAT, LON, O3COL, JO1D, JNO2, DEPOS, FORMLOS,DFRACT
  REAL(dp) :: JDAY, JREPEAT, ALBEDO, SAREA, RP1, BLH, DILUTE, CH4FAC,spinup
  REAL(dp) :: BVOCFAC, ANTHFAC, NOXFAC, COFAC, LAROMF, SAROMF, SAFAC, ALKEFAC
  INTEGER :: INIT_TIME, NOX(NVAR)
  REAL(dp):: CONSTRAIN(NVAR)
  INTEGER :: const_method(NSPEC+10)
  REAL(dp), allocatable :: spcf(:,:) !spline coeff
  CHARACTER(LEN=15) :: spec_name(NSPEC+10)!10000
  LOGICAL :: SPEC_CH4, SPEC_H2
  INTEGER :: IntTime,daycounter,obs
  LOGICAL :: CONSTRAIN_NOX, SAVE_LEGACY
  LOGICAL :: CONSTRAIN_RUN, LAST_POINT, OUTPUT_LAST
  INTEGER, PARAMETER :: OUTPUT_UNIT = 24
  INTEGER, PARAMETER :: ERROR_UNIT = 0
  INTEGER, PARAMETER :: SPEC_UNIT = 10
  INTEGER, PARAMETER :: RATE_UNIT = 12
  INTEGER, PARAMETER :: FLUX_UNIT = 14
  INTEGER, PARAMETER :: VDOT_UNIT = 16
  INTEGER, PARAMETER :: JACSP_UNIT = 18
  INTEGER, PARAMETER :: jmax= 8100, szabin=19

  !character(len=30) :: version
!Photolysis variables
  include './params'
  !INTEGER :: TUVvers
  REAL(8) ::            bs(szabin,kj), cs(szabin,kj),ds(szabin,kj)
  REAL(4) ::            svj_tj(kt,kj), szas(kt), jfactno2, jfacto1d
  !fastjx var
    REAL(kind=dp) :: JSCALE = 1.0d0
    INTEGER :: NJREACT
    integer, parameter :: JVN_ = 2000 ! see cmn_fjx_mod.F90
    character*50, dimension(JVN_) :: JLABELS
  
!End photolysis variables
!Custom Depos variables for easy changing
  include './src/mydepos.inc'
!End depos variables
#ENDINLINE {above lines go into MODULE KPP_ROOT_Global}
