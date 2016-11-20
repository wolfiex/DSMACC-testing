*= This file contains the following subroutines, related to reading/loading
*= the product (cross section) x (quantum yield) for photo-reactions of
*= organic radical compounds in MCM-GECKO, which were not yet present in TUV5.2:
*=
*=     mr01 through mr04

*=============================================================================*

      SUBROUTINE mr01(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! C1 Criegee radical

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  methyleneperoxy Criegee intermediate photolysis:                         =*
*=        CH2OO + hv -> HCHO + O(3P)                                         =*
*=                                                                           =*
*=  Cross section:  IUPAC                                                    =*
*=  Quantum yield:  IUPAC                                                    =*
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
!      REAL sig
      INTEGER ierr, idumx, idumy
      INTEGER iw

      j = j+1
      jlabel(j) = 'CH2OO -> HCHO + O(3P)'

* cross sections
      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/RAD/CH2OO_iup.abs',
     $     STATUS='old')
      do i = 1, 5
        read(kin,*)
      enddo

      n  = 36
      DO i = 1, n
        READ(kin,*) idumx, idumy
        x1(i) = FLOAT(idumx)
        y1(i) = FLOAT(idumy)*1E-20
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
!      qy = 1.

* combine:
      DO iw = 1, nw - 1
        DO i = 1, nz
          sq(j  ,i,iw) = yg(iw)! xs * qy
        ENDDO
      ENDDO

      END

* =============================================================================

      SUBROUTINE mr02(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! C2 Criegee radical

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  acetaldehyde oxide Criegee intermediate photolysis:                      =*
*=        CH3CHOO + hv -> CH3CHO + O(3P)                                     =*
*=                                                                           =*
*=  Cross section:  Smith et al. (2014)                                      =*
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
!      REAL sig
      INTEGER ierr
      INTEGER iw

      j = j+1
      jlabel(j) = 'CH3CHOO -> CH3CHO + O(3P)'

* cross sections
      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/RAD/CH3CHOO_Smi14.abs',
     $     STATUS='old')
      do i = 1, 6
        read(kin,*)
      enddo

      n  = 288
      DO i = 1, n
        READ(kin,*) x1(i), y1(i)
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
!      qy = 1.

* combine:
      DO iw = 1, nw - 1
        DO i = 1, nz
          sq(j  ,i,iw) = yg(iw)! xs * qy
        ENDDO
      ENDDO

      END

* =============================================================================

      SUBROUTINE mr03(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! n-C3 Criegee radical

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  propionaldehyde oxide Criegee intermediate photolysis:                   =*
*=       C2H5CHOO + hv -> C2H5CHO + O(3P)                                    =*
*=                                                                           =*
*=  Cross section: Liu et al. (2014)                                         =*
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
      REAL dum!,sig
      INTEGER ierr,idum
      INTEGER iw

      j = j+1
      jlabel(j) = 'C2H5CHOO + hv -> C2H5CHO + O(3P)'

* cross sections
      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/RAD/C2H5CHOO_Liu14.abs',
     $     STATUS='old')
      do i = 1, 8
        read(kin,*)
      enddo

      n  = 23
      DO i = 1, n
        READ(kin,*) idum, y1(i), dum
        x1(i) = float(idum)
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
!      qy = 1.

* combine:
      DO iw = 1, nw - 1
        DO i = 1, nz
          sq(j  ,i,iw) = yg(iw)! xs * qy
        ENDDO
      ENDDO

      END

* =============================================================================

      SUBROUTINE mr04(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! i-C3 Criegee radical

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  propionaldehyde oxide Criegee intermediate photolysis:                   =*
*=       (CH3)2COO + hv -> CH3COCH3 + O(3P)                                  =*
*=                                                                           =*
*=  Cross section: Liu et al. (2014)                                         =*
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
      REAL dum!,sig
      INTEGER ierr,idum
      INTEGER iw

      j = j+1
      jlabel(j) = '(CH3)2COO + hv -> CH3COCH3 + O(3P)'

* cross sections
      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/RAD/CH32COO_Liu14.abs',
     $     STATUS='old')
      do i = 1, 8
        read(kin,*)
      enddo

      n  = 23
      DO i = 1, n
        READ(kin,*) idum, y1(i), dum
        x1(i) = float(idum)
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
!      qy = 1.

* combine:
      DO iw = 1, nw - 1
        DO i = 1, nz
          sq(j  ,i,iw) = yg(iw)! xs * qy
        ENDDO
      ENDDO

      END

* =============================================================================