MODULE constants
USE model_Precision, ONLY: dp
IMPLICIT NONE
PRIVATE dp

INTEGER, PARAMETER :: mnsp=250, mre=2000
INTEGER i
! variables for zenith routine which calculates zenith angle
REAL(dp) theta, secx, cosx
! generic reaction rate variables
REAL(dp) kro2no, kro2ho2, kapho2, kapno, kro2no3, kno3al, kdec, &
krosec, kalkoxy, kalkpxy, kroprim, kch3o2, k298ch3o2
! variables for calculation of kfpan and kbpan
REAL(dp) kfpan, kbpan, kbppn
REAL(dp) kc0, kci, krc, fcc, nc, fc
REAL(dp) kd0, kdi, krd, fcd, ncd, fd
REAL(dp) kppn0, kppni, krppn, fcppn, ncppn, fppn
! variables for calculation of kmt01
REAL(dp) kmt01
REAL(dp) k10, k1i, kr1, fc1, f1
! variables for calculation of kmt02
REAL(dp) kmt02
REAL(dp) k20, k2i, kr2, fc2, f2
! variables for calculation of kmt03
REAL(dp) kmt03
REAL(dp) k30, k3i, kr3, fc3, f3
! variables for calculation of kmt04
REAL(dp) kmt04
REAL(dp) k40, k4i, kr4, fc4, f4
! variables for calculation of kmt05
REAL(dp) kmt05
! variables for calculation of kmt06
REAL(dp) kmt06
! variables for calculation of kmt07
REAL(dp) kmt07
REAL(dp) k70, k7i, kr7, fc7, f7
! variables for calculation of kmt08
REAL(dp) kmt08
REAL(dp) k80, k8i, kr8, fc8, f8
! variables for calculation of kmt09
REAL(dp) kmt09
REAL(dp) k90, k9i, kr9, fc9, f9
! variables for calculation of kmt10
REAL(dp) kmt10
REAL(dp) k100, k10i, kr10, fc10, f10
! variables for calculation of kmt11
REAL(dp) kmt11
REAL(dp) k1,k2,k3,k4
! variables for calculation of kmt12
REAL(dp) kmt12
REAL(dp) k0, ki, x, ssign,f
! variables for calculation of kmt13
REAL(dp) kmt13
REAL(dp) k130, k13i, kr13, fc13, f13
! variables for calculation of kmt14
REAL(dp) kmt14
REAL(dp) k140, k14i, kr14, fc14, f14
! variables for calculation of kmt15
REAL(dp) kmt15
! variables for calculation of kmt16
REAL(dp) kmt16
REAL(dp) k160, k16i, kr16, fc16, f16
! variables for calculation of kmt17
REAL(dp) kmt17
! variables for calculation of photolysis reaction rates
! J increased to 1100. Upto 1000 for inorganics/organics, 1000 onwards halogens
REAL(dp)  l(1500), mm(1500), nn(1500), j(1500)
INTEGER k
REAL(dp)NC13,NC14,K150,K15I,KR15,NC15,FC15,F15,NC16,K170,K17I,KR17,FC17,F17
REAL(dp)KMT18,NC17,F12,FC12,KR12,K120,NC12, NC9,NC10,K12I,NC7,NC8,NC3,NC4,NC1,NC2,K14ISOM1

CONTAINS

!**************************************************************************

SUBROUTINE mcm_constants(time, temp, M, N2, O2, RO2, H2O)
! calculates rate constants from arrhenius informtion
USE model_Global,  ONLY:LAT, LON, JDAY, SZAS, SVJ_TJ, bs,cs,ds, jfactno2, new_tuv, jfacto1d,output_unit
REAL(dp) time, temp, M, N2, O2, RO2, H2O, THETA, TIME2, LAT2
REAL*8 y,dy,x,tmp(19), tmp2(19),b(19),c(19),d(19)

integer i,n,jl
INTEGER LK
include './TUV_5.2.1/params'

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
! rate_coeff.inc

!INCLUDE 'rate_coeff.inc'
INCLUDE './src/old_rate.inc'
INCLUDE './src/new_rate.inc' !update the old constants whilst keeping the
!redundant ones

! ************************************************************************
! define photolysis reaction rates from cubic splines of the TUV output
! ************************************************************************

if (theta .le. 90) then
    n=19

    do jl=1,kj
    do i=1,19
    tmp(i)=szas(i)
    tmp2(i)=svj_tj(i,jl)

    b(i)=bs(i,jl)
    c(i)=cs(i,jl)
    d(i)=ds(i,jl)
    enddo


if (new_tuv) then
  SELECT CASE (jl)
    CASE(  2)
      j(   1) = seval(n,theta,tmp,tmp2,b,c,d) ! O3 -> O2 + O(1D)
    CASE(  3)
      j(   2) = seval(n,theta,tmp,tmp2,b,c,d) ! O3 -> O2 + O(3P)
    CASE(  5)
      j(   3) = seval(n,theta,tmp,tmp2,b,c,d) ! H2O2 -> 2 OH
    CASE(  6)
      j(   4) = seval(n,theta,tmp,tmp2,b,c,d) ! NO2 -> NO + O(3P)
    CASE(  7)
      j(   5) = seval(n,theta,tmp,tmp2,b,c,d) ! NO3 -> NO + O2
    CASE(  8)
      j(   6) = seval(n,theta,tmp,tmp2,b,c,d) ! NO3 -> NO2 + O(3P)
    CASE( 12)
      j(   7) = seval(n,theta,tmp,tmp2,b,c,d) ! HNO2 -> OH + NO
    CASE( 13)
      j(   8) = seval(n,theta,tmp,tmp2,b,c,d) ! HNO3 -> OH + NO2
    CASE( 22)
      j(  11) = seval(n,theta,tmp,tmp2,b,c,d) ! CH2O -> H + HCO
    CASE( 23)
      j(  12) = seval(n,theta,tmp,tmp2,b,c,d) ! CH2O -> H2 + CO
    CASE( 24)
      j(  13) = seval(n,theta,tmp,tmp2,b,c,d) ! CH3CHO -> CH3 + HCO
    CASE( 27)
      j(  14) = seval(n,theta,tmp,tmp2,b,c,d) ! C2H5CHO -> C2H5 + HCO
    CASE( 30)
      j(  41) = seval(n,theta,tmp,tmp2,b,c,d) ! CH3OOH -> CH3O + OH
    CASE( 32)
      j(  51) = seval(n,theta,tmp,tmp2,b,c,d) ! CH3ONO2 -> CH3O + NO2
    CASE( 35)
      j(  52) = seval(n,theta,tmp,tmp2,b,c,d) ! C2H5ONO2 -> C2H5O + NO2
    CASE( 36)
      j(  53) = seval(n,theta,tmp,tmp2,b,c,d) ! n-C3H7ONO2 -> C3H7O + NO2
    CASE( 39)
      j(  54) = seval(n,theta,tmp,tmp2,b,c,d) ! CH3CHONO2CH3 -> CH3CHOCH3 + NO2
    CASE( 41)
      j(  56) = seval(n,theta,tmp,tmp2,b,c,d)*0.750 ! CH3COCH2(ONO2) -> CH3COCH2(O.) + NO2
      j(  57) = seval(n,theta,tmp,tmp2,b,c,d)*0.250 ! CH3COCH2(ONO2) -> CH3COCH2(O.) + NO2
    CASE( 42)
      j(  55) = seval(n,theta,tmp,tmp2,b,c,d) ! C(CH3)3(ONO2) -> C(CH3)3(O.) + NO2
    CASE( 52)
      j(  18) = seval(n,theta,tmp,tmp2,b,c,d) ! CH2=C(CH3)CHO -> CH2=CCH3 + CHO
    CASE( 55)
      j(  19) = seval(n,theta,tmp,tmp2,b,c,d) ! CH2=C(CH3)CHO -> CH2=C(CH3)CO + H
    CASE( 56)
      j(  20) = seval(n,theta,tmp,tmp2,b,c,d) ! HPALD -> Products
    CASE( 58)
      j(  24) = seval(n,theta,tmp,tmp2,b,c,d) ! CH3COCH=CH2 -> C2H3 + CH3CO
    CASE( 59)
      j(  23) = seval(n,theta,tmp,tmp2,b,c,d) ! CH3COCH=CH2 -> C3H6 + CO
    CASE( 63)
      j(  21) = seval(n,theta,tmp,tmp2,b,c,d) ! CH3COCH3 -> CH3CO + CH3
    CASE( 65)
      j(  22) = seval(n,theta,tmp,tmp2,b,c,d) ! CH3COCH2CH3 -> CH3CO + CH2CH3
    CASE( 68)
      j(  33) = seval(n,theta,tmp,tmp2,b,c,d) ! CHOCHO -> 2 HO2 + 2 CO
    CASE( 69)
      j(  31) = seval(n,theta,tmp,tmp2,b,c,d) ! CHOCHO -> H2 + 2 CO
    CASE( 70)
      j(  32) = seval(n,theta,tmp,tmp2,b,c,d) ! CHOCHO -> CH2O + CO
    CASE( 71)
      j(  34) = seval(n,theta,tmp,tmp2,b,c,d) ! CH3COCHO -> CH3CO + HCO
    CASE( 72)
      j(  35) = seval(n,theta,tmp,tmp2,b,c,d) ! CH3COCOCH3 -> Products
    CASE( 81)
      j(1008) = seval(n,theta,tmp,tmp2,b,c,d) ! Cl2 -> Cl + Cl
    CASE( 92)
      j(1006) = seval(n,theta,tmp,tmp2,b,c,d) ! ClONO2 -> Cl + NO3
    CASE( 93)
      j(1007) = seval(n,theta,tmp,tmp2,b,c,d) ! ClONO2 -> ClO + NO2
    CASE(113)
      j(1003) = seval(n,theta,tmp,tmp2,b,c,d) ! Br2 -> Br + Br
    CASE(114)
      j(1002) = seval(n,theta,tmp,tmp2,b,c,d) ! BrO -> Br + O
    CASE(115)
      j(1001) = seval(n,theta,tmp,tmp2,b,c,d) ! HOBr -> OH + Br
    CASE(120)
      j(1005) = seval(n,theta,tmp,tmp2,b,c,d) ! BrONO2 -> BrO + NO2
    CASE(121)
      j(1004) = seval(n,theta,tmp,tmp2,b,c,d) ! BrONO2 -> Br + NO3
    CASE(130)
      j(  15) = seval(n,theta,tmp,tmp2,b,c,d) ! n-C3H7CHO -> n-C3H7 + CHO
    CASE(131)
      j(  16) = seval(n,theta,tmp,tmp2,b,c,d) ! n-C3H7CHO -> C2H4 + CH2CHOH
    CASE(136)
      j(  17) = seval(n,theta,tmp,tmp2,b,c,d) ! i-C3H7CHO -> i-C3H7 + CHO
  END SELECT



else !old tuv hard wiring





SELECT CASE (jl)

 CASE(2)
        j(1)=seval(n,theta,tmp, tmp2, b,c,d) ! O3->O1D

 CASE(3)
        j(2)=seval(n,theta,tmp, tmp2, b,c,d) ! O3->O3P

 CASE(11)
        j(3)=seval(n,theta,tmp, tmp2, b,c,d) ! H2O2->2*OH

 CASE(4)
        j(4)=seval(n,theta,tmp, tmp2, b,c,d) ! NO2->NO+O3P

 CASE(5)
        j(5)=seval(n,theta,tmp, tmp2, b,c,d) ! NO3->NO+O2

 CASE(6)
        j(6)=seval(n,theta,tmp, tmp2, b,c,d) ! NO3->NO2+O3P

 CASE(12)
        j(7)=seval(n,theta,tmp, tmp2, b,c,d) ! HNO2->OH+NO

 CASE(13)
        j(8)=seval(n,theta,tmp, tmp2, b,c,d) ! HNO3->NO2+OH

 CASE(14)
        j(1300)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(15)
        j(11)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(16)
        j(12)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(17)
        j(13)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(20)
        j(14)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(75)
        j(15)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(76)
        j(16)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(77)
        j(17)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(62)
        j(18)=seval(n,theta,tmp, tmp2, b,c,d)*0.5
        j(19)=seval(n,theta,tmp, tmp2, b,c,d)*0.5

 CASE(25)
        j(21)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(87)
        j(22)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(61)
        j(23)=seval(n,theta,tmp, tmp2, b,c,d)*0.5
        j(24)=seval(n,theta,tmp, tmp2, b,c,d)*0.5

 CASE(21)
        j(31)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(23)
        j(32)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(22)
        j(33)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(24)
        j(34)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(60)
        j(35)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(26)
        j(41)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(27)
        j(51)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(64)
        j(52)=seval(n,theta,tmp, tmp2, b,c,d)
        j(54)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(91)
        j(53)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(94)
        j(55)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(67)
        j(56)=seval(n,theta,tmp, tmp2, b,c,d)*0.75
        j(57)=seval(n,theta,tmp, tmp2, b,c,d)*0.25
!!!!!!!!!!Halogens !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

 CASE(72)
        j(1001)=seval(n,theta,tmp, tmp2, b,c,d) ! HOBr

 CASE(73)
        j(1002)=seval(n,theta,tmp, tmp2, b,c,d) ! BrO

 CASE(74)
        j(1003)=seval(n,theta,tmp, tmp2, b,c,d) ! Br2

 CASE(50)
        j(1004)=seval(n,theta,tmp, tmp2, b,c,d) ! BrNO3->Br+NO3

 CASE(51)
        j(1005)=seval(n,theta,tmp, tmp2, b,c,d) ! BrNO3->BrO+NO2

 CASE(30)
        j(1006)=seval(n,theta,tmp, tmp2, b,c,d) ! ClNO3->Cl+NO3

 CASE(31)
        j(1007)=seval(n,theta,tmp, tmp2, b,c,d) ! ClNO3->ClO+NO2

 CASE(58)
        j(1008)=seval(n,theta,tmp, tmp2, b,c,d) ! Cl2->2Cl

END SELECT


 end if



    enddo

else
    do i=1,1500
    j(i)=0.
    enddo
endif


if (jfactno2 .eq. 0) jfactno2=1.
if (jfacto1d .eq. 0) jfacto1d=1.

do i=1,1500
if (i .ne. 1) then
    j(i)=j(i)*jfactno2
else
    j(i)=j(i)*jfacto1d
endif
enddo

do i=1,1500
if (j(i) .lt. 0.e0) j(i)=0e0
enddo


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
if ( i .ge. n ) i = 1
if ( u .lt. x(i) ) go to 10
if ( u .le. x(i+1) ) go to 30

!  binary search
10 i = 1
j = n+1
20 k = (i+j)/2

if ( u .ge. x(k) )  then
    i = k
else
    j = k
end if

if ( j .gt. i+1 ) go to 20

!  evaluate spline
30 dx = u - x(i)
seval = y(i) + dx*(b(i) + dx*(c(i) + dx*d(i)))
return
end function seval

subroutine polint(f,a,n,x,r)
!----------------------------------------------------------
! service program for fintr
!----------------------------------------------------------
real*8 r,al,x,a,f
integer  i,j,k,l,n
dimension f(n),a(n)
r=0.0
do 1 j=1,n
al=1.0
do 2 i=1,n
if (i-j) 3,2,3
3        al=al*(x-a(i))/(a(j)-a(i))
2     continue
1     r=r+al*f(j)
return
end subroutine polint


END MODULE constants
