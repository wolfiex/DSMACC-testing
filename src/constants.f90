MODULE constants
  USE model_Precision, ONLY: dp
  USE model_global, ONLY: jmax, szabin
  IMPLICIT NONE
  PRIVATE dp

  INTEGER, PARAMETER :: mnsp=250, mre=2000
  INTEGER  :: i
  real(dp):: DFRACT
  ! variables for zenith routine which calculates zenith angle
  REAL(dp) :: theta, secx, cosx
! generic reaction rate variables
! variables for calculation of photolysis reaction rates
! maximum array size of J is jmax
! Use programme TUV2DSMACC (https://github.com/pb866/TUV_DSMACC.git)
! to determine maximum array size.
! Current settings:
! -    0 -  999: inorganics (use for halogens as well)
! - 1000 - 1999: aldehydes
! - 2000 - 2999: ketones
! - 3000 - 2999: dicarbonyls
! - 4000 - 4999: mono-nitrates and other mono-nitrogen compounds
! - 5000 - 5999: polynitrates and polypernitrates
! - 6000 - 6999: hydroperoxides and PAAs
! - 7000 - 7999: Criegee intermediates
! - 8000 - 8100: Polyfunctional chromophores
! Old MCM labelling from the MCM website still available
  REAL(dp) :: l(jmax), mm(jmax), nn(jmax), j(jmax)=0.
  REAL(dp) :: kalkpxy,kalkoxy
  INTEGER  :: k

!remove these just for testing lumping
real(dp)::hchocoeff, prodhcho , prodch3o,ch3ocoeff 



  INCLUDE './src/rate_coeff/new_rate.inc.def'
CONTAINS

!**************************************************************************

  SUBROUTINE mcm_constants(time, temp, M, N2, O2, RO2, H2O)
! calculates rate constants from arrhenius informtion
    USE model_global,  ONLY:LAT, LON, JDAY, SZAS, SVJ_TJ, bs,cs,ds, &
      jfactno2, TUVvers, jmax, szabin, jfacto1d, output_unit
    REAL(dp) :: time, temp, M, N2, O2, RO2, H2O, THETA, TIME2, LAT2
    REAL(dp) :: y,dy,x,tmp(szabin),tmp2(szabin),b(szabin),c(szabin),d(szabin)

    INTEGER :: i,jl,n
    INTEGER :: LK
    include './params'

! Time2 is local time in hours
    Time2=mod(Time/(60.*60.), 24.)
   
  

    IF (TIME2 .LT. 0) TIME2=TIME2+24.
    LAT2=LAT

    THETA=ZENANG(int(jday)+int((time-time2)/(60.*60.*24.)),Time2,LAT2)*180./PI
    WRITE (OUTPUT_UNIT,*) jday, time, time2, theta
! ************************************************************************
! define generic reaction rates.
! ************************************************************************
! constants used in calculation of reaction rates
!M  = 2.55E+19
    N2 = 0.79*M
    O2 = 0.2095*M

    kalkoxy=6.00d-14*EXP(-550.0/temp)*o2
    kalkpxy=1.50d-14*EXP(-200.0/temp)*o2


! -------------------------------------------------------------------
! simple + complex reactions
! -------------------------------------------------------------------

! MCM -> extract -> kpp + include generic rate coeff -> rename
    INCLUDE './src/rate_coeff/new_rate.inc.var'

! ************************************************************************
! define photolysis reaction rates from cubic splines of the TUV output
! ************************************************************************

    IF (theta .le. 90) then

      DO jl=1,kj
        DO i=1,szabin
          tmp(i)=szas(i)
          tmp2(i)=svj_tj(i,jl)

          b(i)=bs(i,jl)
          c(i)=cs(i,jl)
          d(i)=ds(i,jl)
        ENDDO

        SELECT CASE (TUVvers)
         CASE(0)
          INCLUDE './tuv_old/MCM3.inc'
         CASE(1)
          INCLUDE './TUV_5.2.1/MCM331.inc'
         CASE(2)
          INCLUDE './TUV_5.2.1/MCM4.inc'
         CASE(3)
          INCLUDE './TUV_5.2.1/GC11.inc'
         CASE DEFAULT
          STOP "Select TUV case between 0 and 3."
        END SELECT

      ENDDO

     ELSE
      DO i=1,jmax
        j(i)=0.
      ENDDO
    ENDIF


    IF (jfactno2 .eq. 0) jfactno2=1.
    IF (jfacto1d .eq. 0) jfacto1d=1.

    DO i=1,jmax
      IF (i .ne. 1) then
        j(i)=j(i)*jfactno2
       ELSE
        j(i)=j(i)*jfacto1d
      ENDIF
    ENDDO

    DO i=1,jmax
      IF (j(i) .lt. 0.e0) j(i)=0.d0
    ENDDO




  END SUBROUTINE mcm_constants


  REAL FUNCTION UPTAKE(GAMMA,TEMP,AREA,MASS)
! INPUT GAMMA=UPTAKE COEFFICIENT (0..1)
!       TEMP=TEMPERTURE(K)
!       AREA=SURFACE AREA (M^2/M^3)
!       MASS=MOLECULAR MASS OF MOLECULE
!       R=BOLTZMAN'S CONSTANT
!       RP=RADIUS OF PARTICLE (M)
!       DG=GAS-PHASE DIFFUSION COEFFICIENT (M^2 S-1)
    REAL*8 GAMMA, TEMP, AREA, MASS
    REAL*8 V, V2, R, DG
    R=8.314
    DG=2.47D-5
!     DG TAKEN FROM MOZUREVICH ET EL 1987
    V2=3*R*TEMP/MASS
    V=(8*V2/(3*3.1415))**0.5
!      UPTAKE=(((RP/DG)+(4/(GAMMA*V)))**-1)*AREA
    UPTAKE=v*AREA*GAMMA/4
  END FUNCTION UPTAKE



  FUNCTION ZENANG(Nday,Time,Geolat)
    REAL(dp) :: Geolat , Time
    INTEGER :: Nday
    REAL(dp) :: ZENANG
    INTENT (IN) Geolat , Time
! Local variable
    REAL :: arg , dec , georad , w,torad
!     REAL :: SOLDEC
!-----------------------------------------------------------------------
!     a function to calculate the solar zenith angle for a given day,
!     nday, local time, ntime & geographical latitude, geolat.
!     the solar zenith angle, also called the zenith distance, is the
!     angle between the local zenith and the line joining the observer
!     and the sun.!     it is returned in radians.
!-----------------------------------------------------------------------
!     the hour angle, w, changes by 15 degrees for every hour, it is 0
!     at local noon. it is computed here in radians.
!     the declination, dec, is the angular position of the sun at
!     solar noon with respect to the plane of the equator, north is
!     positive, it is a function of the time of year.
!     it is required in radians.
!-----------------------------------------------------------------------
!     calculate the hour angle in radians.
    torad=4.0*ATAN(1.0)/180.
    w = torad*15.0*(Time-12.)
!     calculate declination in radians.
    dec = SOLDEC(Nday)
!     geographic latitude in degrees converted to radians.
    georad = Geolat*torad
!     we know the geographical latitude, so from a simple geometrical
!     relationship we can now calculate the solar zenith angle.
    arg = SIN(dec)*SIN(georad) + COS(dec)*COS(georad)*COS(w)
    ZENANG = ACOS(arg)
!-----------------------------------------------------------------------
  END FUNCTION ZENANG


  FUNCTION SOLDEC(Nday)
    IMPLICIT NONE
! Dummy arguments
    INTEGER :: Nday
    REAL :: SOLDEC, pi
    INTENT (IN) Nday
! Local variables
    REAL :: dayang
    REAL :: REAL
    PI=3.14159265
!----------------------------------------------------------------------
!     a function to calculate the solar declination using the
!     relation given by j. w. spencer, fourier series representation
!     of the position of the sun, search vol. 2 (5), pp. 172, 1971.
!     the declination, dec, is the angular position of the sun at
!     solar noon with respect to the plane of the equator, north is
!     positive, it is a function of the time of year.
!     it is returned in radians.
!-----------------------------------------------------------------------
!     nday is the day number, 1 on january 1st, 365 on december 31st.
!     dayang is the day angle, dayang=2*pi*(nday-1)/365, in radians,
!     from spencer.
!-----------------------------------------------------------------------

!     calculate day angle in radians.
    dayang = 2.0*pi*REAL(Nday-1)/365.0

!     calculate declination in radians.
    SOLDEC = (0.006918-0.399912*COS(dayang)+0.070257*SIN(dayang)      &
      & -0.006758*COS(2.0*dayang)+0.000907*SIN(2.0*dayang)       &
      & -0.002697*COS(3.0*dayang)+0.00148*SIN(3.0*dayang))
!-----------------------------------------------------------------------
  END FUNCTION SOLDEC


  double precision function seval(n, u, x, y, b, c, d)
!======================================================================
!  this subroutine evaluates the cubic spline function
!    seval = y(i) + b(i)*(u-x(i)) + c(i)*(u-x(i))**2 + d(i)*(u-x(i))**3
!    where  x(i) .lt. u .lt. x(i+1), using horner's rule
!  if  u .lt. x(1) then  i = 1  is used.
!  if  u .ge. x(n) then  i = n  is used.
!  input..
!    n = the number of data points
!    u = the abscissa at which the spline is to be evaluated
!    x,y = the arrays of data abscissas and ordinates
!    b,c,d = arrays of spline coefficients computed by spline
!  if  u  is not in the same interval as the previous call, then a
!  binary search is performed to determine the proper interval.
!========================================================================
    integer n
    double precision  u, x(n), y(n), b(n), c(n), d(n)
    integer i, j, k
    double precision dx
    data i/1/
    IF ( i .ge. n ) i = 1
    IF ( u .lt. x(i) ) go to 10
    IF ( u .le. x(i+1) ) go to 30

!  binary search
    10 i = 1
    j = n+1
    20 k = (i+j)/2

    IF ( u .ge. x(k) )  then
      i = k
     ELSE
      j = k
    END IF

    IF ( j .gt. i+1 ) go to 20

!  evaluate spline
    30 dx = u - x(i)
    seval = y(i) + dx*(b(i) + dx*(c(i) + dx*d(i)))
    return
  END function seval

  subroutine polint(f,a,n,x,r)
!----------------------------------------------------------
! service program for fintr
!----------------------------------------------------------
    real*8 r,al,x,a,f
    integer  i,j,k,l,n
    dimension f(n),a(n)
    r=0.0
    DO 1 j=1,n
      al=1.0
      DO 2 i=1,n
        IF (i-j) 3,2,3
3         al=al*(x-a(i))/(a(j)-a(i))
2         continue
1         r=r+al*f(j)
    return
  END subroutine polint


END MODULE constants
