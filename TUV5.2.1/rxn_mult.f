*= This file contains the following subroutines, related to reading/loading
*= the product (cross section) x (quantum yield) for photo-reactions of
*= organic compounds with multiple chromphores in MCM-GECKO,
*= which where not yet present in TUV5.2:
*=
*=     mm01 through mm06

*=============================================================================*

      SUBROUTINE mm01(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! NMEK, nitroxymethyl ethyl ketone

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  nitroxymethyl ethyl ketone photolysis:                                   =*
*=        C2H5COCH2NO3 + hv -> C2H5COCH2O + NO2                              =*
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
      jlabel(j) = 'C2H5COCH2NO3 -> C2H5COCH2O + NO2'


      IF(vers==1)THEN
        mabs = 2
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
     &       ' C2H5COCH2NO3 cross sections from least square fit',
     &       ' by Barnes et al.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &  ' C2H5COCH2NO3 cross sections from data by Barnes et al.'
       ELSE
        STOP "'mabs' not defined for C2H5COCH2NO3 photolysis."
      ENDIF


      IF(mabs==2) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/MULT/NMEK_Bar93.abs',
     $       STATUS='old')
        do i = 1, 4
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

!        qy = 1.0


* combine:

      DO iw = 1, nw - 1
        IF(mabs==1) THEN
          sig = exp(-1.011e-3*wc(iw)**2+0.5437*wc(iw)-116.9)
         ELSEIF(mabs==2) THEN
          sig = yg(iw)
        ENDIF

        DO i = 1, nz
          sq(j,i,iw) = sig! * qy
        ENDDO

      ENDDO

      END

* ============================================================================*

      SUBROUTINE mm02(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! M1NEK, methyl 1-nitroxyethyl ketone

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  methyl 1-nitroxyethyl ketone photolysis:                                 =*
*=        CH3COCH(NO3)CH3 + hv -> CH3COCH(O.)CH3 + NO2                       =*
*=                                                                           =*
*=  Cross section:  Barnes et al. (1993)                                     =*
*=  Quantum yield:  see options below                                        =*
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
      REAL qy
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs, myld


      j = j+1
      jlabel(j) = 'CH3COCH(NO3)CH3 + hv -> CH3COCH(O.)CH3 + NO2'


      IF(vers==1)THEN
        mabs = 2
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
     &       ' CH3COCH(NO3)CH3 cross sections from least square fit',
     &       ' by Barnes et al.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &  ' CH3COCH(NO3)CH3 cross sections from data by Barnes et al.'
       ELSE
        STOP "'mabs' not defined for CH3COCH(NO3)CH3 photolysis."
      ENDIF


      IF(vers==1)THEN
        myld = 2
       ELSEIF(vers==2)THEN
        myld = 2
       ELSEIF(vers==0) THEN
        myld = 2
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(A)')
     &  ' CH3COCH(NO3)CH3 quantum yields estimated 1 (Calvert et al.).'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(A)')
     & ' CH3COCH(NO3)CH3 quantum yields estimated 0.75 (Muller et al.).'
       ELSE
        STOP "'myld' not defined for CH3COCH(NO3)CH3 photolysis."
      ENDIF


      IF(mabs==2) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/MULT/M1NEK_Bar93.abs',
     $       STATUS='old')
        do i = 1, 4
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

      IF(myld==1) THEN
        qy = 1.0
       ELSEIF(myld==2) THEN
        qy = 0.75
      ENDIF


* combine:

      DO iw = 1, nw - 1
        IF(mabs==1) THEN
          sig = exp(-1.044e-3*wc(iw)**2+0.578*wc(iw)-123.5)
         ELSEIF(mabs==2) THEN
          sig = yg(iw)
        ENDIF

        DO i = 1, nz
          sq(j,i,iw) = sig * qy
        ENDDO

      ENDDO

      END

* ============================================================================*

      SUBROUTINE mm03(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! 2-oxo-cyclohexyl nitrate

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  2-oxo-cyclohexyl nitrate photolysis:                                     =*
*=        C6H9-2-=O-1-NO3 + hv -> RO. + NO2                                  =*
*=                                                                           =*
*=  Cross section:  Wängberg et al. (1996)                                   =*
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

      REAL yg(kw), dum
!     REAL qy
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs

      j = j+1
      jlabel(j) = 'C6H9-2-=O-1-NO3 + hv -> RO. + NO2'


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
     &       ' C6H9-2-=O-1-NO3 cross sections from',
     &       ' Wangberg et al.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' C6H9-2-=O-1-NO3 cross sections as plotted',
     &       ' in Calvert et al.'
       ELSE
        STOP "'mabs' not defined for C6H9-2-=O-1-NO3 photolysis."
      ENDIF


      IF(mabs==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/MULT/Wangberg96.abs',
     $       STATUS='old')
        do i = 1, 11
          read(kin,*)
        enddo

        n  = 14
        DO i = 1, n
          READ(kin,*) idum, dum, y1(i), dum
          x1(i) = FLOAT(idum)
          y1(i) = y1(i)*1.e-20
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==2) THEN

        OPEN(UNIT=kin,
     $       FILE  ='DATAJ1/MCMext/MULT/2oxo-cHexNit_calv.abs',
     $       STATUS='old')
        do i = 1, 8
          read(kin,*)
        enddo

        n  = 94
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

!     qy = 1.0


* combine:

      DO iw = 1, nw - 1
        sig = yg(iw)
        DO i = 1, nz
          sq(j,i,iw) = sig! * qy
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mm04(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! 2-hexanone-5-hydroperoxide

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  2-hexanone-5-hydroperoxide photolysis:                                   =*
*=        CH3COCH2CH2CH(OOH)CH3 + hv -> RO. + OH                             =*
*=                                                                           =*
*=  Cross section:  Jorand et al. (2000)                                     =*
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
      PARAMETER(kdata=100)

      INTEGER i, n
      REAL x1(kdata)
      REAL y1(kdata)

* local

      REAL yg(kw)
!     REAL qy
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      j = j+1
      jlabel(j) = 'CH3COCH2CH2CH(OOH)CH3 + hv -> RO. + OH'


      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/MULT/2oxo5oohHex.abs',
     $     STATUS='old')
      do i = 1, 6
        read(kin,*)
      enddo

      n  = 81
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


* quantum yields

!      qy = 1.0


* combine:

      DO iw = 1, nw - 1
        sig = yg(iw)
        DO i = 1, nz
          sq(j,i,iw) = sig! * qy
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mm05(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! oxohexyl-hydroperoxide

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  oxohexyl-hydroperoxide photolysis:                                       =*
*=        oxohexyl-hydroperoxide + hv -> RO. + OH                            =*
*=                                                                           =*
*=  Cross section:  Jorand et al. (2000)                                     =*
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
      PARAMETER(kdata=100)

      INTEGER i, n
      REAL x1(kdata)
      REAL y1(kdata)

* local

      REAL yg(kw)
!     REAL qy
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      j = j+1
      jlabel(j) = 'oxohexyl-hydroperoxide + hv -> RO. + OH'


      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/MULT/oxo+oohHex.abs',
     $     STATUS='old')
      do i = 1, 7
        read(kin,*)
      enddo

      n  = 81
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


* quantum yields

!      qy = 1.0


* combine:

      DO iw = 1, nw - 1
        sig = yg(iw)
        DO i = 1, nz
          sq(j,i,iw) = sig! * qy
        ENDDO
      ENDDO

      END

* ============================================================================*