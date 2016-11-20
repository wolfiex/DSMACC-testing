*= This file contains the following subroutines, related to reading/loading
*= the product (cross section) x (quantum yield) for photo-reactions of
*= organic dinitrates in MCM-GECKO, which where not yet present in TUV5.2:
*=
*=     md01 through md06

*=============================================================================*

      SUBROUTINE md01(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! isopropylene dinitrate

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  CH3CH(NO3)CH2NO3 photolysis:                                             =*
*=        CH3CH(NO3)CH2NO3 + hv -> products                                  =*
*=                                                                           =*
*=  Cross section:  Barnes et al. (1993)                                     =*
*=  Quantum yield:  assumed unity with equal branching                       =*
*-----------------------------------------------------------------------------*

      IMPLICIT NONE
      INCLUDE 'params'

* input

      INTEGER nw
      REAL wl(kw), wc(kw)

      INTEGER nz

      REAL tlev(kz)
      REAL airden(kz)

* weighting functions

      CHARACTER(lcl) jlabel(kj)
      REAL sq(kj,kz,kw)

* input/output:

      INTEGER j

* data arrays

      INTEGER kdata
      PARAMETER(kdata=580)

      INTEGER i, n
      REAL x1(kdata)
      REAL y1(kdata)

* local

      REAL yg(kw)
      REAL qy1, qy2
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs


      j = j+1
      jlabel(j) = 'CH3CH(NO3)CH2NO3 -> CH3CH(NO3)CH2O + NO2'
      j = j+1
      jlabel(j) = 'CH3CH(NO3)CH2NO3 -> CH3CH(O.)CH2NO3 + NO2'


      IF(vers==1)THEN
        mabs = 1
       ELSEIF(vers==2)THEN
        mabs = 2
       ELSEIF(vers==0) THEN
        mabs = 2
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(mabs.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' CH3CH(NO3)CH2NO3 cross sections from least square fit',
     &       ' by Barnes et al.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &  ' CH3CH(NO3)CH2NO3 cross sections from data by Barnes et al.'
       ELSE
        STOP "'mabs' not defined for CH3CH(NO3)CH2NO3 photolysis."
      ENDIF


      IF(mabs==2) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DINIT/12PropNit.abs',
     $       STATUS='old')
        do i = 1, 6
          read(kin,*)
        enddo

        n  = 20
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

        CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
        CALL addpnt(x1,y1,kdata,n,               0.,0.)
        CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
        CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
        CALL inter2(nw,wl,yg,n,x1,y1,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
        ENDIF
      ENDIF


* quantum yields

      qy1 = 0.5
      qy2 = 0.5


* combine:

      DO iw = 1, nw - 1
        sig = exp(-5.99e-4*wc(iw)**2+0.2915*wc(iw)-79.24)
        IF(mabs==2 .AND. wc(iw)>=245. .AND. wc(iw)<=340.)THEN
          sig = yg(iw)
        ENDIF
        DO i = 1, nz
          sq(j-1,i,iw) = sig * qy1
          sq(j  ,i,iw) = sig * qy2
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE md02(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! 1,2-butylene dinitrate

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  CH3CH2CH(NO3)CH2NO3 photolysis:                                          =*
*=        CH3CH2CH(NO3)CH2NO3 + hv -> products                               =*
*=                                                                           =*
*=  Cross section:  Barnes et al. (1993)                                     =*
*=  Quantum yield:  assumed unity with equal branching                       =*
*-----------------------------------------------------------------------------*

      IMPLICIT NONE
      INCLUDE 'params'

* input

      INTEGER nw
      REAL wl(kw), wc(kw)

      INTEGER nz

      REAL tlev(kz)
      REAL airden(kz)

* weighting functions

      CHARACTER(lcl) jlabel(kj)
      REAL sq(kj,kz,kw)

* input/output:

      INTEGER j

* data arrays

      INTEGER kdata
      PARAMETER(kdata=580)

      INTEGER i, n
      REAL x1(kdata)
      REAL y1(kdata)

* local

      REAL yg(kw)
      REAL qy1, qy2
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs

      j = j+1
      jlabel(j) = 'C2H5CH(NO3)CH2NO3 -> C2H5CH(NO3)CH2O + NO2'
      j = j+1
      jlabel(j) = 'C2H5CH(NO3)CH2NO3 -> C2H5CH(O.)CH2NO3 + NO2'


      IF(vers==1)THEN
        mabs = 1
       ELSEIF(vers==2)THEN
        mabs = 2
       ELSEIF(vers==0) THEN
        mabs = 2
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(mabs.EQ.1) THEN
        WRITE(kout,'(2A)')
     &  ' CH3CH2CH(NO3)CH2NO3 cross sections from least square fit',
     &  ' by Barnes et al.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &  ' CH3CH2CH(NO3)CH2NO3 cross sections from data by Barnes et al.'
       ELSE
        STOP "'mabs' not defined for CH3CH2CH(NO3)CH2NO3 photolysis."
      ENDIF


      IF(mabs==2) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DINIT/12ButNit.abs',
     $       STATUS='old')
        do i = 1, 6
          read(kin,*)
        enddo

        n  = 20
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

        CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
        CALL addpnt(x1,y1,kdata,n,               0.,0.)
        CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
        CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
        CALL inter2(nw,wl,yg,n,x1,y1,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
        ENDIF
      ENDIF


* quantum yields

      qy1 = 0.5
      qy2 = 0.5


* combine:

      DO iw = 1, nw - 1
        sig = exp(-6.217e-4*wc(iw)**2+0.3025*wc(iw)-80.41)
        IF(mabs==2 .AND. wc(iw)>=245. .AND. wc(iw)<=340.)THEN
          sig = yg(iw)
        ENDIF
        DO i = 1, nz
          sq(j-1,i,iw) = sig * qy1
          sq(j  ,i,iw) = sig * qy2
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE md03(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! 2,3-butylene dinitrate

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  CH3CH(NO3)CH(NO3)CH3 photolysis:                                         =*
*=        CH3CH(NO3)CH(NO3)CH3 + hv -> CH3CH(NO3)CH(O.)CH3 + NO2             =*
*=                                                                           =*
*=  Cross section:  Barnes et al. (1993)                                     =*
*=  Quantum yield:  assumed unity                                            =*
*-----------------------------------------------------------------------------*

      IMPLICIT NONE
      INCLUDE 'params'

* input

      INTEGER nw
      REAL wl(kw), wc(kw)

      INTEGER nz

      REAL tlev(kz)
      REAL airden(kz)

* weighting functions

      CHARACTER(lcl) jlabel(kj)
      REAL sq(kj,kz,kw)

* input/output:

      INTEGER j

* data arrays

      INTEGER kdata
      PARAMETER(kdata=580)

      INTEGER i, n
      REAL x1(kdata)
      REAL y1(kdata)

* local

      REAL yg(kw)
!     REAL qy
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs

      j = j+1
      jlabel(j) = 'CH3CH(NO3)CH(NO3)CH3 -> RO. + NO2'


      IF(vers==1)THEN
        mabs = 1
       ELSEIF(vers==2)THEN
        mabs = 2
       ELSEIF(vers==0) THEN
        mabs = 2
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(mabs.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' CH3CH(NO3)CH(NO3)CH3 cross sections from',
     &       ' least square fit by Barnes et al.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' CH3CH(NO3)CH(NO3)CH3 cross sections from data',
     &       ' by Barnes et al.'
       ELSE
        STOP "'mabs' not defined for CH3CH(NO3)CH(NO3)CH3 photolysis."
      ENDIF


      IF(mabs==2) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DINIT/23ButNit.abs',
     $       STATUS='old')
        do i = 1, 6
          read(kin,*)
        enddo

        n  = 20
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

        CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
        CALL addpnt(x1,y1,kdata,n,               0.,0.)
        CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
        CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
        CALL inter2(nw,wl,yg,n,x1,y1,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
        ENDIF
      ENDIF


* quantum yields

!      qy = 1.0


* combine:

      DO iw = 1, nw - 1
        sig = exp(-5.74e-4*wc(iw)**2+0.2771*wc(iw)-77.47)
        IF(mabs==2 .AND. wc(iw)>=245. .AND. wc(iw)<=340.)THEN
          sig = yg(iw)
        ENDIF
        DO i = 1, nz
          sq(j  ,i,iw) = sig! * qy
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE md04(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! 1,4-dinitrooxy-2-butene

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  CH3CH(NO3)CH(NO3)CH3 photolysis:                                         =*
*=        CH2(NO3)CH=CHCH2NO3 + hv -> CH2(NO3)CH=CHCH2O + NO2                =*
*=                                                                           =*
*=  Cross section:  Barnes et al. (1993)                                     =*
*=  Quantum yield:  assumed unity                                            =*
*-----------------------------------------------------------------------------*

      IMPLICIT NONE
      INCLUDE 'params'

* input

      INTEGER nw
      REAL wl(kw), wc(kw)

      INTEGER nz

      REAL tlev(kz)
      REAL airden(kz)

* weighting functions

      CHARACTER(lcl) jlabel(kj)
      REAL sq(kj,kz,kw)

* input/output:

      INTEGER j

* data arrays

      INTEGER kdata
      PARAMETER(kdata=580)

      INTEGER i, n
      REAL x1(kdata)
      REAL y1(kdata)

* local

      REAL yg(kw)
!      REAL qy
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs

      j = j+1
      jlabel(j) = 'CH2(NO3)CH=CHCH2NO3 -> RO. + NO2'


      IF(vers==1)THEN
        mabs = 1
       ELSEIF(vers==2)THEN
        mabs = 2
       ELSEIF(vers==0) THEN
        mabs = 2
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(mabs.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' CH2(NO3)CH=CHCH2NO3 cross sections from',
     &       ' least square fit by Barnes et al.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' CH2(NO3)CH=CHCH2NO3 cross sections from data',
     &       ' by Barnes et al.'
       ELSE
        STOP "'mabs' not defined for CH2(NO3)CH=CHCH2NO3 photolysis."
      ENDIF


      IF(mabs==2) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DINIT/14Nit2Butene.abs',
     $       STATUS='old')
        do i = 1, 6
          read(kin,*)
        enddo

        n  = 18
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

        CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
        CALL addpnt(x1,y1,kdata,n,               0.,0.)
        CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
        CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
        CALL inter2(nw,wl,yg,n,x1,y1,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
        ENDIF
      ENDIF


* quantum yields

!      qy = 1.0


* combine:

      DO iw = 1, nw - 1
        sig = exp(-5.432e-4*wc(iw)**2+0.2631*wc(iw)-75.92)
        IF(mabs==2 .AND. wc(iw)>=245. .AND. wc(iw)<=330.)THEN
          sig = yg(iw)
        ENDIF
        DO i = 1, nz
          sq(j  ,i,iw) = sig! * qy
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE md05(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! 3,4-dinitrooxy-1-butene

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  CH3CH(NO3)CH(NO3)CH3 photolysis:                                         =*
*=        CH2=CHCH(NO3)CH2NO3 + hv -> CH2=CHCH(NO3)CH2O + NO2                =*
*=                                                                           =*
*=  Cross section:  Barnes et al. (1993)                                     =*
*=  Quantum yield:  assumed unity with equal branching                       =*
*-----------------------------------------------------------------------------*

      IMPLICIT NONE
      INCLUDE 'params'

* input

      INTEGER nw
      REAL wl(kw), wc(kw)

      INTEGER nz

      REAL tlev(kz)
      REAL airden(kz)

* weighting functions

      CHARACTER(lcl) jlabel(kj)
      REAL sq(kj,kz,kw)

* input/output:

      INTEGER j

* data arrays

      INTEGER kdata
      PARAMETER(kdata=580)

      INTEGER i, n
      REAL x1(kdata)
      REAL y1(kdata)

* local

      REAL yg(kw)
      REAL qy1, qy2
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs

      j = j+1
      jlabel(j) = 'CH2=CHCH(NO3)CH2NO3 -> C2H3CH(NO3)CH2O + NO2'
      j = j+1
      jlabel(j) = 'CH2=CHCH(NO3)CH2NO3 -> C2H3CH(O.)CH2NO3 + NO2'


      IF(vers==1)THEN
        mabs = 1
       ELSEIF(vers==2)THEN
        mabs = 2
       ELSEIF(vers==0) THEN
        mabs = 2
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(mabs.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' CH2=CHCH(NO3)CH2NO3 cross sections from',
     &       ' least square fit by Barnes et al.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' CH2=CHCH(NO3)CH2NO3 cross sections from data',
     &       ' by Barnes et al.'
       ELSE
        STOP "'mabs' not defined for CH2=CHCH(NO3)CH2NO3 photolysis."
      ENDIF


      IF(mabs==2) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DINIT/34Nit1Butene.abs',
     $       STATUS='old')
        do i = 1, 6
          read(kin,*)
        enddo

        n  = 20
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

        CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
        CALL addpnt(x1,y1,kdata,n,               0.,0.)
        CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
        CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
        CALL inter2(nw,wl,yg,n,x1,y1,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
        ENDIF
      ENDIF


* quantum yields

      qy1 = 0.5
      qy2 = 0.5


* combine:

      DO iw = 1, nw - 1
        sig = exp(-6.217e-4*wc(iw)**2+0.3025*wc(iw)-80.41)
        IF(mabs==2 .AND. wc(iw)>=245. .AND. wc(iw)<=340.)THEN
          sig = yg(iw)
        ENDIF
        DO i = 1, nz
          sq(j-1,i,iw) = sig * qy1
          sq(j  ,i,iw) = sig * qy2
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE md06(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! 1-methyl-cyclohexyl-1,2-dinitrate

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  1-methyl-cyclohexyl-1,2-dinitrate photolysis:                            =*
*=        C6H9-1-CH3-1,2-NO3 + hv -> products                                =*
*=                                                                           =*
*=  Cross section:  Wängberg et al. (1996)                                   =*
*=  Quantum yield:  assumed unity with equal branching                       =*
*-----------------------------------------------------------------------------*

      IMPLICIT NONE
      INCLUDE 'params'

* input

      INTEGER nw
      REAL wl(kw), wc(kw)

      INTEGER nz

      REAL tlev(kz)
      REAL airden(kz)

* weighting functions

      CHARACTER(lcl) jlabel(kj)
      REAL sq(kj,kz,kw)

* input/output:

      INTEGER j

* data arrays

      INTEGER kdata
      PARAMETER(kdata=580)

      INTEGER i, n
      REAL x1(kdata)
      REAL y1(kdata)

* local

      REAL yg(kw), dum
      REAL qy1, qy2
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs

      j = j+1
      jlabel(j) = 'C6H9-1-CH3-1,2-NO3 -> R1O. + NO2'
      j = j+1
      jlabel(j) = 'C6H9-1-CH3-1,2-NO3 -> R2O. + NO2'


      IF(vers==1)THEN
        mabs = 1
       ELSEIF(vers==2)THEN
        mabs = 1
       ELSEIF(vers==0) THEN
        mabs = 2
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(mabs.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' C6H9-1-CH3-1,2-NO3 cross sections from',
     &       ' Wangberg et al.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' C6H9-1-CH3-1,2-NO3 cross sections as plotted',
     &       ' in Calvert et al.'
       ELSE
        STOP "'mabs' not defined for C6H9-1-CH3-1,2-NO3 photolysis."
      ENDIF


      IF(mabs==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/MULT/Wangberg96.abs',
     $       STATUS='old')
        do i = 1, 9
          read(kin,*)
        enddo

        n  = 14
        DO i = 1, n
          READ(kin,*) idum, dum, dum, y1(i)
          x1(i) = FLOAT(idum)
          y1(i) = y1(i)*1.e-20
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==2) THEN

        OPEN(UNIT=kin,
     $       FILE  ='DATAJ1/MCMext/DINIT/1MecHex12DiNit_calv.abs',
     $       STATUS='old')
        do i = 1, 8
          read(kin,*)
        enddo

        n  = 111
        DO i = 1, n
          READ(kin,*) x1(i), y1(i)
          y1(i) = y1(i)*1.e-20
        ENDDO
        CLOSE(kin)
      ENDIF

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* quantum yields

      qy1 = 0.5
      qy2 = 0.5


* combine:

      DO iw = 1, nw - 1
        sig = yg(iw)
        DO i = 1, nz
          sq(j-1,i,iw) = sig * qy1
          sq(j  ,i,iw) = sig * qy2
        ENDDO
      ENDDO

      END

* ============================================================================*