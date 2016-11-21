*= This file contains the following subroutines, related to reading/loading
*= the product (cross section) x (quantum yield) for photo-reactions of
*= dicarbonyls in MCM-GECKO, which were not yet present in TUV5.2:
*=
*=     mb01 through mb04

*=============================================================================*

      SUBROUTINE mb01(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! butenedial

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  CHOCH=CHCHO photolysis:                                                  =*
*=        HC(O)CH=CHCHO + hv -> 3H-furan-2-one                               =*
*=                                                                           =*
*=  Cross section:  trans-butenedial (see options below)                     =*
*=  Quantum yield:  trans-butenedial (see options below)                     =*
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

      REAL yg(kw), yg1(kw), dum
      REAL qy
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs, myld

      j = j+1
      jlabel(j) = 'CHOCH=CHCHO -> 3H-furan-2-one'


      IF(vers==1)THEN
        mabs = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
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
        WRITE(kout,'(A)')
     &       ' CHOCH=CHCHO cross sections from SAPRC-99.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' CHOCH=CHCHO cross sections from IUPAC.'
       ELSE
        STOP "'mabs' not defined for CHOCH=CHCHO photolysis."
      ENDIF

      IF(vers==1)THEN
        myld = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
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
     &       ' CHOCH=CHCHO quantum yields from SAPRC-99.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' CHOCH=CHCHO quantum yields from IUPAC.'
       ELSE
        STOP "'myld' not defined for CHOCH=CHCHO photolysis."
      ENDIF


      IF(mabs==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DICAR/butenedial1',
     $       STATUS='old')
        do i = 1, 6
          read(kin,*)
        enddo

        n  = 56
        DO i = 1, n
          READ(kin,*) idum, y1(i), dum
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==2) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DICAR/ButDial_iup.abs',
     $       STATUS='old')
        do i = 1, 5
          read(kin,*)
        enddo

        n  = 33
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
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

      IF(myld==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DICAR/butenedial1',
     $       STATUS='old')
        do i = 1, 6
          read(kin,*)
        enddo

        n  = 56
        DO i = 1, n
          READ(kin,*) idum, dum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg1,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
      ENDIF
      ENDIF


* combine:

      DO iw = 1, nw - 1
        sig = yg(iw)
        IF(myld==1) THEN
          qy = yg1(iw)
         ELSEIF(myld==2) THEN
          !cis/trans conversion channel available from IUPAC (<0.4)
          IF(wc(iw)>248.) THEN
            qy = 0.012
           ELSE
            qy = 0.028
          ENDIF
        ENDIF
        DO i = 1, nz
          sq(j  ,i,iw) = sig * qy
        ENDDO
      ENDDO

      END

* =============================================================================

      SUBROUTINE mb02(nw,wl,wc,nz,tlev,airlev,j,sq,jlabel) ! 4-oxo-2-pentenal

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  CH3C(O)CH=CHCHO photolysis:                                              =*
*=        CH3C(O)CH=CHCHO + hv -> 5methyl-3H-furan-2-one                     =*
*=                                                                           =*
*=  Cross section:  4 oxo2pentenal Bierbach 94                               =*
*=  Quantum yield:  4 oxo2pentenal Bierbach 94                               =*
*-----------------------------------------------------------------------------*

      IMPLICIT NONE
      INCLUDE 'params'

* input

      INTEGER nw
      REAL wl(kw), wc(kw)

      INTEGER nz

      REAL tlev(kz)
      REAL airlev(kz)

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

      REAL yg(kw), yg1(kw), dum
      REAL qy1,qy2,qy3,qy4
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs, myld

      j = j+1
      jlabel(j) = 'CH3COCH=CHCHO + hv -> 5Me-3H-2-furanone'
      j = j+1
      jlabel(j) = 'CH3COCH=CHCHO + hv -> CH3 + CHOCH=CHCO'
      j = j+1
      jlabel(j) = 'CH3COCH=CHCHO + hv -> CH3COCH=CH2 + CO'
      j = j+1
      jlabel(j) = 'CH3COCH=CHCHO + hv -> maleic anhydride + HO2. + R.'
* further channel possible: cis/trans conversion with qy < 0.2 (see IUPAC)

      IF(vers==1)THEN
        mabs = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
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
        WRITE(kout,'(A)')
     &       ' CH3COCH=CHCHO cross sections from SAPRC-99.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' CH3COCH=CHCHO cross sections from IUPAC.'
       ELSE
        STOP "'mabs' not defined for CH3COCH=CHCHO photolysis."
      ENDIF

      IF(vers==1)THEN
        myld = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
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
     &       ' CH3COCH=CHCHO quantum yields from SAPRC-99.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' CH3COCH=CHCHO quantum yields from IUPAC.'
       ELSE
        STOP "'myld' not defined for CH3COCH=CHCHO photolysis."
      ENDIF

* cross sections:
* currently not distinguished between cis/trans
      IF(mabs == 1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DICAR/4oxo2pentenal1',
     $       STATUS='old')
        do i = 1, 6
          read(kin,*)
        enddo

        n = 56
        DO i = 1, n
          READ(kin,*) idum, y1(i), dum
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs == 2) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DICAR/4oPentenal_iup.abs',
     $       STATUS='old')
        do i = 1, 6
          read(kin,*)
        enddo

        n = 21
        DO i = 1, n
          READ(kin,*) idum, dum, dum, y1(i)
          x1(i) = FLOAT(idum)
          y1(i) = y1(i) * 1E-20
        ENDDO
        CLOSE(kin)
      ENDIF
      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-3)
          STOP
      ENDIF


* quantum yields from data file

      IF(myld == 1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DICAR/4oxo2pentenal1',
     $       STATUS='old')
        do i = 1, 6
          read(kin,*)
        enddo

        n = 56
        DO i = 1, n
          READ(kin,*) idum, dum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)
        CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
        CALL addpnt(x1,y1,kdata,n,               0.,0.)
        CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
        CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
        CALL inter2(nw,wl,yg1,n,x1,y1,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-3)
          STOP
        ENDIF
      ENDIF


* combine xs and qy:

      DO iw = 1, nw - 1
* cross section:
        sig = yg(iw)
* quantum yields:
        IF(myld == 1) THEN
          qy1 = yg1(iw)
          qy2 = 0.
          qy3 = 0.
          qy4 = qy1
         ELSEIF(myld==2) THEN
          qy1 = 0.05
          IF(wl(iw)<=308.) THEN
            qy2 = 0.3
            qy3 = 0.4
           ELSEIF(wl(iw)>=351.) THEN
            qy2 = 0.23
            qy3 = 0.33
           ELSE
            qy2 = 0.3 + (0.23-0.3)*(wl(iw)-308.)/(351.-308.)
            qy3 = 0.4 + (0.33-0.4)*(wl(iw)-308.)/(351.-308.)
          ENDIF
          qy4 = 0.
        ENDIF


         DO i = 1, nz
            sq(j-3,i,iw) = sig * qy1
            sq(j-2,i,iw) = sig * qy2
            sq(j-1,i,iw) = sig * qy3
            sq(j  ,i,iw) = sig * qy4
         ENDDO
      ENDDO

      END

* =============================================================================

      SUBROUTINE mb03(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! hexadienedial

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  CHOCH=CHCH=CHCHO photolysis:                                             =*
*=        HC(O)CH=CHCH=CHCHO + hv -> Z-3,4-Diformyl-cyclobutene              =*
*=                                                                           =*
*=  Cross section:  trans-butenedial (Bierbach 94)                           =*
*=  Quantum yield:  trans-butenedial (Bierbach 94)                           =*
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
      REAL qy
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs

      j = j+1
      jlabel(j) = 'CHOCH=CHCH=CHCHO + hv -> diformyl cyclobutene'


      IF(vers==1)THEN
        mabs = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
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
        WRITE(kout,'(A)')
     &       ' CHOCH=CHCH=CHCHO cross sections from Klotz et al. 1995.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' CHOCH=CHCH=CHCHO cross sections from Xiang and Zhu 2007.'
       ELSE
        STOP "'mabs' not defined for CHOCH=CHCH=CHCHO photolysis."
      ENDIF


      IF(mabs==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DICAR/EEhexadienedial1.prn',
     $       STATUS='old')
        do i = 1, 5
          read(kin,*)
        enddo

        n  = 13
        DO i = 1, n
          READ(kin,*) x1(i), y1(i), dum
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==2) THEN

        OPEN(UNIT=kin,
     $       FILE='DATAJ1/MCMext/DICAR/hexadienedial_X+Z07.abs',
     $       STATUS='old')
        do i = 1, 6
          read(kin,*)
        enddo

        n  = 29
        DO i = 1, n
          READ(kin,*) idum, y1(i),dum
          x1(i) = FLOAT(idum)
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

      qy = 0.1


* combine:

      DO iw = 1, nw - 1
        sig = yg(iw)
        DO i = 1, nz
          sq(j  ,i,iw) = sig * qy
        ENDDO
      ENDDO

      END

* =============================================================================

      SUBROUTINE mb04(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! 3-hexene-2,5-dione

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  CH3COCH=CHCOCH3 photolysis:                                              =*
*=        CH3COCH=CHCOCH3 + hv -> CH3CO + CH=CHCOCH3                         =*
*=                                                                           =*
*=  Cross section:  Liu et al. 1999 in acetonitrile                          =*
*=  Quantum yield:  estimated                                                =*
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
      INTEGER ierr
      INTEGER iw

      j = j+1
      jlabel(j) = 'CH3COCH=CHCOCH3 + hv -> CH3CO + CH=CHCOCH3'
* main fraction >~80% undergoes cis/trans-isomerisation

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DICAR/hexenedione.abs',
     $     STATUS='old')
      do i = 1, 9
        read(kin,*)
      enddo

      n  = 160
      DO i = 1, n
        READ(kin,*) x1(i), y1(i)
        y1(i) = y1(i)*1.E-20
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

      qy = 0.1


* combine:

      DO iw = 1, nw - 1
        sig = yg(iw)
        DO i = 1, nz
          sq(j  ,i,iw) = sig * qy
        ENDDO
      ENDDO

      END

* =============================================================================