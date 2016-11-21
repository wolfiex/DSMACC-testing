*= This file contains the following subroutines, related to reading/loading
*= the product (cross section) x (quantum yield) for photo-reactions of
*= dicarbonyls in MCM-GECKO, which were not yet present in TUV5.2:
*=
*=     mk01 through mk21

*=============================================================================*

      SUBROUTINE mk01(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! diethyl ketone

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  CHOCH=CHCHO photolysis:                                                  =*
*=        C2H5COC2H5 + hv -> products                                        =*
*=                                                                           =*
*=  Cross section:  see options below                                        =*
*=  Quantum yield:  estimated (0.85:0.15)                                    =*
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
      REAL A, lc, w

      INTEGER mabs

      j = j+1
      jlabel(j) = 'C2H5COC2H5 -> 2 C2H5 + CO'
      j = j+1
      jlabel(j) = 'C2H5COC2H5 -> C2H5CO + C2H5'


      IF(vers==1)THEN
        mabs = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
       ELSEIF(vers==2)THEN
        mabs = 4
       ELSEIF(vers==0) THEN
        mabs = 1
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(mabs.EQ.1) THEN
        WRITE(kout,'(A)')
     &       ' C2H5COC2H5 cross sections from Martinez et al. 1992.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' C2H5COC2H5 cross sections from Horowitz. 1999.'
       ELSEIF(mabs.EQ.3) THEN
        WRITE(kout,'(A)')
     &       ' C2H5COC2H5 cross sections from Koch et al. 2008.'
       ELSEIF(mabs.EQ.4) THEN
        WRITE(kout,'(A)')
     &  ' C2H5COC2H5 cross sections from T-dep. gaussian approximation.'
       ELSE
        STOP "'mabs' not defined for C2H5COC2H5 photolysis."
      ENDIF


      IF(mabs==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/ABS/Martinez.abs',
     $       STATUS='old')
        do i = 1, 4
          read(kin,*)
        enddo

        n  = 96
        DO i = 1, n
          READ(kin,*) idum, dum, dum, dum, y1(i)
          x1(i) = FLOAT(idum)
          y1(i) = y1(i)*1.E-20
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==2) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/DEK_Hor99.abs',
     $       STATUS='old')
        do i = 1, 7
          read(kin,*)
        enddo

        n  = 2196
        DO i = 1, n
          READ(kin,*) x1(i), y1(i)
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs>=3) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/DEK_Koch08.abs',
     $       STATUS='old')
        do i = 1, 6
          read(kin,*)
        enddo

        n  = 159
        DO i = 1, n
          READ(kin,*) x1(i), y1(i)
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

      qy1 = 0.85
      qy2 = 0.15


* combine:
      DO iw = 1, nw - 1
        sig = yg(iw)
        DO i = 1, nz
          IF(mabs==4 .AND. wc(iw)>=230. .AND. wc(iw)<=330.) THEN
            A   = 4.77e-20 + 4.87e-23*tlev(i)
            lc  = 273.7    + 0.0186  *tlev(i)
            w   =  25.1    + 0.0101  *tlev(i)
            sig = A * exp(-((wc(iw)-lc)/w)**2)
          ENDIF
          sq(j-1,i,iw) = sig * qy1
          sq(j  ,i,iw) = sig * qy2
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mk02(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! methyl n-propyl ketone

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  C3H7COCH3 photolysis:                                                    =*
*=        C3H7COCH3 + hv -> Norish type I + II products                      =*
*=                                                                           =*
*=  Cross section:  see options below                                        =*
*=  Quantum yield:  estimates based on Calvert et al. 2011 book              =*
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

      INTEGER i, n, n1, n2, n3
      REAL x1(kdata),x2(kdata),x3(kdata)
      REAL y1(kdata),y2(kdata),y3(kdata)

* local

      REAL yg(kw), yg1(kw), yg2(kw), yg3(kw), dum
      REAL qy1, qy2, qy3, qy4
      REAL sig
      INTEGER ierr
      INTEGER iw
      REAL A, lc, w

      INTEGER mabs

      j = j+1
      jlabel(j) = 'C3H7COCH3 -> CH3CO + C3H7'
      j = j+1
      jlabel(j) = 'C3H7COCH3 -> C3H7CO + CH3'
      j = j+1
      jlabel(j) = 'C3H7COCH3 -> C3H7 + CO + CH3'
      j = j+1
      jlabel(j) = 'C3H7COCH3 -> CH3C(OH)=CH2 + CH2=CH2'


      IF(vers==1)THEN
        mabs = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
       ELSEIF(vers==2)THEN
        mabs = 2
       ELSEIF(vers==0) THEN
        mabs = 1
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(mabs.EQ.1) THEN
        WRITE(kout,'(A)')
     &       ' C3H7COCH3 cross sections from Martinez et al. 1992.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &  ' C3H7COCH3 cross sections from T-dep. gaussian approximation.'
       ELSE
        STOP "'mabs' not defined for C3H7COCH3 photolysis."
      ENDIF

* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/ABS/Martinez.abs',
     $     STATUS='old')
      do i = 1,4
         read(kin,*)
      enddo

      n = 96
      DO i = 1, n
         READ(kin,*) x1(i),dum,dum,y1(i),dum
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

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/2pentanone.yld',
     $     STATUS='old')
      do i = 1,6
         read(kin,*)
      enddo

      n  = 4
      n1 = n
      n2 = n
      n3 = n
      DO i = 1, n
         READ(kin,*) x1(i), y1(i), y2(i), y3(i)
         x2(i) = x1(i)
         x3(i) = x1(i)
      ENDDO
      CLOSE(kin)

         CALL addpnt(x1,y1,kdata,n1,x1(1)*(1.-deltax),0.058)
         CALL addpnt(x1,y1,kdata,n1,               0.,0.058)
         CALL addpnt(x1,y1,kdata,n1,x1(n1)*(1.+deltax),0.2)
         CALL addpnt(x1,y1,kdata,n1,           1.e+38,0.2)
         CALL inter2(nw,wl,yg1,n1,x1,y1,ierr)
         IF (ierr .NE. 0) THEN
            WRITE(*,*) ierr, jlabel(j-1)
            STOP
         ENDIF

         CALL addpnt(x2,y2,kdata,n2,x2(1)*(1.-deltax),0.007)
         CALL addpnt(x2,y2,kdata,n2,               0.,0.007)
         CALL addpnt(x2,y2,kdata,n2,x2(n2)*(1.+deltax),0.025)
         CALL addpnt(x2,y2,kdata,n2,           1.e+38,0.025)
         CALL inter2(nw,wl,yg2,n2,x2,y2,ierr)
         IF (ierr .NE. 0) THEN
            WRITE(*,*) ierr, jlabel(j-1)
            STOP
         ENDIF

         CALL addpnt(x3,y3,kdata,n3,x3(1)*(1.-deltax),0.05)
         CALL addpnt(x3,y3,kdata,n3,               0.,0.05)
         CALL addpnt(x3,y3,kdata,n3,x3(n3)*(1.+deltax),0.05)
         CALL addpnt(x3,y3,kdata,n3,           1.e+38,0.05)
         CALL inter2(nw,wl,yg3,n3,x3,y3,ierr)
         IF (ierr .NE. 0) THEN
            WRITE(*,*) ierr, jlabel(j-1)
            STOP
         ENDIF


* combine xs and qy:
      DO iw = 1, nw - 1
        sig = yg(iw)
        qy1 = yg1(iw)
        qy2 = yg2(iw)
        qy3 = yg3(iw)
        IF(wc(iw)<=254.) THEN
          qy4 = 0.39
         ELSEIF(wc(iw)>=313.) THEN
          qy4 = 0.28
         ELSE
          qy4 = 0.39 - (wc(iw)-254.) * (0.11/59.)
        ENDIF
        DO i = 1, nz
          IF(mabs==2 .AND. wc(iw)>=240. .AND. wc(iw)<=330.) THEN
            A   = 4.72e-20 + 4.87e-23*tlev(i)
            lc  = 274.16   + 0.0186  *tlev(i)
            w   =  25.1    + 0.0101  *tlev(i)
            sig = A * exp(-((wc(iw)-lc)/w)**2)
          ENDIF
          sq(j-3,i,iw) = sig * qy1
          sq(j-2,i,iw) = sig * qy2
          sq(j-1,i,iw) = sig * qy3
          sq(j  ,i,iw) = sig * qy4
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mk03(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! methyl n-butyl ketone

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  C4H9COCH3 photolysis:                                                    =*
*=        C4H9COCH3 + hv -> CH3CH=CH2 + CH2=C(OH)CH3                         =*
*=                                                                           =*
*=  Cross section:  McMillan (1966)                                          =*
*=  Quantum yield:  estimates based on Calvert et al. 2011 book              =*
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

      INTEGER i, n, n1, n2
      REAL x1(kdata), x2(kdata)
      REAL y1(kdata), y2(kdata)

* local

      REAL yg(kw), yg0(kw), yg1(kw)
      REAL sig, qy, eta
      INTEGER ierr, idum
      INTEGER iw

      INTEGER myld

      j = j+1
      jlabel(j) = 'C4H9COCH3 + hv -> CH3CH=CH2 + CH2=C(OH)CH3'


* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/2hexanone.abs',
     $     STATUS='old')
      do i = 1,6
         read(kin,*)
      enddo

      n = 68
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

      IF(vers==1)THEN
        myld = 1
       ELSEIF(vers==2)THEN
        myld = 2
       ELSEIF(vers==0) THEN
        myld = 1
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' C4H9COCH3 quantum yields without quenching',
     &       ' from Calvert et al. 2011 book.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' C4H9COCH3 quantum yields with quenching',
     &       ' from Calvert et al. 2011 book.'
       ELSE
        STOP "'myld' not defined for C4H9COCH3 photolysis."
      ENDIF

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/2hexanone.yld',
     $     STATUS='old')
      do i = 1,7
         read(kin,*)
      enddo

      n  = 72
      n1 = n
      n2 = n
      DO i = 1, n
        READ(kin,*) idum, y1(i), y2(i)
        x1(i) = FLOAT(idum)
        x2(i) = x1(i)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x1,y1,kdata,n1,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n1,               0.,0.)
      CALL addpnt(x1,y1,kdata,n1,x1(n1)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n1,           1.e+38,0.)
      CALL inter2(nw,wl,yg0,n1,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j-1)
        STOP
      ENDIF

      CALL addpnt(x2,y2,kdata,n2,x2(1)*(1.-deltax),0.)
      CALL addpnt(x2,y2,kdata,n2,               0.,0.)
      CALL addpnt(x2,y2,kdata,n2,x2(n2)*(1.+deltax),0.)
      CALL addpnt(x2,y2,kdata,n2,           1.e+38,0.)
      CALL inter2(nw,wl,yg1,n2,x2,y2,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j-1)
        STOP
      ENDIF


* combine xs and qy:
      DO iw = 1, nw - 1
        sig = yg(iw)
        IF(myld == 1) THEN
          qy = yg0(iw)
         ELSEIF(myld == 2) THEN
          eta = MAX(0.,yg0(iw)/yg1(iw) - 1.)
        ENDIF
        DO i = 1, nz
          qy = yg1(iw)*(1.+eta)/(1.+eta*airden(i)/2.465e19)
          sq(j  ,i,iw) = sig * qy
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mk04(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! ethyl n-propyl ketone

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  C3H7COC2H5 photolysis:                                                   =*
*=        C3H7COC2H5 + hv -> products                                        =*
*=                                                                           =*
*=  Cross section:  Horrowitz (1999) unpublished data                        =*
*=  Quantum yield:  estimates based on Calvert et al. 2011 book              =*
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
      PARAMETER(kdata=2500)

      INTEGER i, n
      REAL x1(kdata)
      REAL y1(kdata)

* local

      REAL yg(kw)
      REAL qyI, qy1, qy2, qy3, qy4
      REAL sig
      INTEGER ierr
      INTEGER iw

      j = j+1
      jlabel(j) = 'C3H7COC2H5 -> C2H5CO + C3H7'
      j = j+1
      jlabel(j) = 'C3H7COC2H5 -> C3H7CO + C2H5'
      j = j+1
      jlabel(j) = 'C3H7COC2H5 -> C3H7 + CO + C2H5'
      j = j+1
      jlabel(j) = 'C3H7COC2H5 -> C2H5C(OH)=CH2 + CH2=CH2'



* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/3hexanone.abs',
     $     STATUS='old')
      do i = 1,7
         read(kin,*)
      enddo

      n = 2318
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
      qyI = 0.61
      qy4 = 0.21

* combine xs and qy:
      DO iw = 1, nw - 1
        sig = yg(iw)
        IF(wc(iw)<=290.) THEN
          qy3 = 0.45*qyI
          qy1 = (qyI-qy3)/13*8
          qy2 = (qyI-qy3)/13*5
         ELSE
          qy3 = 0.25*qyI
          qy1 = (qyI-qy3)/13*8
          qy2 = (qyI-qy3)/13*5
        ENDIF
        DO i = 1, nz
          sq(j-3,i,iw) = sig * qy1
          sq(j-2,i,iw) = sig * qy2
          sq(j-1,i,iw) = sig * qy3
          sq(j  ,i,iw) = sig * qy4
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mk05(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! MIPK

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  MIPK photolysis:                                                         =*
*=        MIPK + hv -> products                                              =*
*=                                                                           =*
*=  Cross section:  estimated same as MIBK                                   =*
*=  Quantum yield:  estimates based on Calvert et al. 2011 book              =*
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
      REAL qyI, qy1, qy2, qy3, qy4, qydum
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      j = j+1
      jlabel(j) = 'MIPK -> CH3CO + i-C3H7'
      j = j+1
      jlabel(j) = 'MIPK -> i-C3H7CO + CH3'
      j = j+1
      jlabel(j) = 'MIPK -> i-C3H7 + CO + CH3'
      j = j+1
      jlabel(j) = 'MIPK -> CH2=CHOH + CH3CH=CH2'



* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/MIBK.abs',
     $     STATUS='old')
      do i = 1,6
         read(kin,*)
      enddo

      n = 111
      DO i = 1, n
         READ(kin,*) idum, y1(i)
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


* combine xs and qy:
      DO iw = 1, nw - 1
        sig = yg(iw)
        DO i = 1, nz
          CALL qyacet(wc(iw),tlev(i),airden(i),qy3,qydum)
          qy3 = min(1., max(0.,qy3))
          IF(wc(iw)<=254.) THEN
            qy4 = 0.36
           ELSEIF(wc(iw)>313.) THEN
            qy4 = 0.0
           ELSE
            qy4 = 0.36 - (wc(iw)-254.) * (0.35/59.)
          ENDIF
          qyI = max(0.,0.75 - qy3 - qy4)
          qy1 = qyI*6/7
          qy2 = qyI/7
          sq(j-3,i,iw) = sig * qy1
          sq(j-2,i,iw) = sig * qy2
          sq(j-1,i,iw) = sig * qy3
          sq(j  ,i,iw) = sig * qy4
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mk06(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! MIBK

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  MIBK photolysis:                                                         =*
*=        MIBK + hv -> products                                              =*
*=                                                                           =*
*=  Cross section:  Yujing and Mellouki 2000                                 =*
*=  Quantum yield:  estimates based on Calvert et al. 2011 book              =*
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
      REAL qy1, qy2, qy3, qy4
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER myld

      j = j+1
      jlabel(j) = 'MIBK -> CH3CO + i-C4H9'
      j = j+1
      jlabel(j) = 'MIBK -> i-C4H9CO + CH3'
      j = j+1
      jlabel(j) = 'MIBK -> i-C4H9 + CO + CH3'
      j = j+1
      jlabel(j) = 'MIBK -> CH3C(OH)=CH2 + CH3CH=CH2'

      IF(vers==1)THEN
        myld = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
       ELSEIF(vers==2)THEN
        myld = 2
       ELSEIF(vers==0) THEN
        myld = 3
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' MIBK quantum yields estimates (0.34*0.7/0.3) from',
     &       ' GECKO-A database.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' MIBK quantum yields estimates (0.35/0.15)',
     &       ' based on Calvert et al. 2011 book.'
       ELSEIF(myld.EQ.3) THEN
        WRITE(kout,'(2A)')
     &       ' MIBK quantum yields estimates (0.21/0.15)',
     &       ' based on Calvert et al. 2011 book.'
       ELSE
        STOP "'myld' not defined for MIBK photolysis."
      ENDIF


* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/MIBK.abs',
     $     STATUS='old')
      do i = 1,6
         read(kin,*)
      enddo

      n = 111
      DO i = 1, n
         READ(kin,*) idum, y1(i)
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

      IF(myld==1) THEN
        qy1 = 0.34*0.3
        qy2 = 0.
        qy3 = 0.
        qy4 = 0.34*0.7
       ELSEIF(myld==2) THEN
        qy1 = 0.035
        qy2 = 0.035
        qy3 = 0.08
        qy4 = 0.35
       ELSEIF(myld==3) THEN
        qy1 = 0.035
        qy2 = 0.035
        qy3 = 0.08
        qy4 = 0.21
      ENDIF


* combine xs and qy:
      DO iw = 1, nw - 1
        sig = yg(iw)
        DO i = 1, nz
          sq(j-3,i,iw) = sig * qy1
          sq(j-2,i,iw) = sig * qy2
          sq(j-1,i,iw) = sig * qy3
          sq(j  ,i,iw) = sig * qy4
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mk07(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! 4-Me-2-hexanone

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  4-Me-2-hexanone photolysis:                                              =*
*=        4-Me-2-hexanone + hv -> Norish type II products                    =*
*=                                                                           =*
*=  Cross section:  estimated same as 5-Me-2-hexanone                        =*
*=  Quantum yield:  estimates based on Calvert et al. 2011 book and MIPK     =*
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
      REAL qy, qy1, qy2, qyrat
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER myld

! channels I - III ignored: qy(I-III)/qy(IVa/b) = 0.02 @ 42˚C
!     j = j+1
!     jlabel(j) = '4-Me-2-hexanone -> CH3CO + CH2CH(CH3)CH2CH3'
!     j = j+1
!     jlabel(j) = '4-Me-2-hexanone -> CH3CH2CH(CH3)CH2CO + CH3'
!     j = j+1
!     jlabel(j) = '4-Me-2-hexanone -> CH2CH(CH3)CH2CH3 + CO + CH3'
      j = j+1
      jlabel(j) = '4-Me-2-hexanone -> CH3C(OH)=CH2 + 2-butene'
      j = j+1
      jlabel(j) = '4-Me-2-hexanone -> CH3C(OH)=CH2 + 1-butene'

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
        WRITE(kout,'(2A)')
     &       ' 4-Me-2-hexanone quantum yields estimates',
     &       ' (0.34*0.7) from GECKO-A database.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' 4-Me-2-hexanone quantum yields estimated',
     &       ' same as qy IV of MIBK.'
       ELSE
        STOP "'myld' not defined for 4-Me-2-hexanone photolysis."
      ENDIF


* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/5Me2hexanone.abs',
     $     STATUS='old')
      do i = 1,6
         read(kin,*)
      enddo

      n = 111
      DO i = 1, n
         READ(kin,*) idum, y1(i)
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


* combine xs and qy:
      DO iw = 1, nw - 1
        sig = yg(iw)
        IF(myld==1) THEN
          qy  = 0.34*0.7
         ELSEIF(myld==2) THEN
          IF(wc(iw)<=254.) THEN
            qy = 0.36
           ELSEIF(wc(iw)>313.) THEN
            qy = 0.0
           ELSE
            qy = 0.36 - (wc(iw)-254.) * (0.35/59.)
          ENDIF
        ENDIF
        DO i = 1, nz
          qyrat = (-2.11e-3*wc(iw) + 0.7745)
     &          * 10**(171.92 * (1/317. - 1/tlev(i)))
          IF (wl(iw) <= 360.) THEN
            qy1 = qy / (1. + qyrat)
            qy2 = qy / (1. + 1./qyrat)
           ELSE
            qy1 = 0.
            qy2 = 0.
          ENDIF
          sq(j-1,i,iw) = sig * qy1
          sq(j  ,i,iw) = sig * qy2
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mk08(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! 5-Me-2-hexanone

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  5-Me-2-hexanone photolysis:                                              =*
*=        5-Me-2-hexanone + hv -> products                                   =*
*=                                                                           =*
*=  Cross section:  Yujing and Mellouki 2000                                 =*
*=  Quantum yield:  estimates based on Calvert et al. 2011 book              =*
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
      REAL qyI, qy1, qy2, qy3, qy4, qydum
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER myld

      j = j+1
      jlabel(j) = '5-Me-2-hexanone -> CH3CO + CH2CH2CH(CH3)2'
      j = j+1
      jlabel(j) = '5-Me-2-hexanone -> (CH3)2CHCH2CH2CO + CH3'
      j = j+1
      jlabel(j) = '5-Me-2-hexanone -> CH2CH2CH(CH3)2 + CO + CH3'
      j = j+1
      jlabel(j) = '5-Me-2-hexanone -> CH3C(OH)=CH2 + CH2=C(CH3)2'

      IF(vers==1)THEN
        myld = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
       ELSEIF(vers==2)THEN
        myld = 3
       ELSEIF(vers==0) THEN
        myld = 2
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' 5-Me-2-hexanone quantum yields estimates',
     &       ' (0.34*0.7/0.3) from GECKO-A database.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' 5-Me-2-hexanone quantum yields estimated',
     &       ' same as MIPK.'
       ELSEIF(myld.EQ.3) THEN
        WRITE(kout,'(2A)')
     &       ' 5-Me-2-hexanone quantum yields estimated',
     &       ' same as MIBK.'
       ELSEIF(myld.EQ.4) THEN
        WRITE(kout,'(2A)')
     &       ' 5-Me-2-hexanone quantum yields estimated',
     &       ' same as 4-Me-2-hexanone.'
       ELSE
        STOP "'myld' not defined for 5-Me-2-hexanone photolysis."
      ENDIF


* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/5Me2hexanone.abs',
     $     STATUS='old')
      do i = 1,6
         read(kin,*)
      enddo

      n = 111
      DO i = 1, n
         READ(kin,*) idum, y1(i)
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


* combine xs and qy:
      DO iw = 1, nw - 1
        sig = yg(iw)
        DO i = 1, nz
          IF(myld==1) THEN
            qy1 = 0.34*0.3
            qy2 = 0.
            qy3 = 0.
            qy4 = 0.34*0.7
           ELSEIF(myld==3) THEN
            qy1 = 0.035
            qy2 = 0.035
            qy3 = 0.08
            qy4 = 0.35
           ELSEIF(myld==2 .OR. myld==4) THEN
            IF(wc(iw)<=254.) THEN
              qy4 = 0.36
             ELSEIF(wc(iw)>313.) THEN
              qy4 = 0.0
             ELSE
              qy4 = 0.36 - (wc(iw)-254.) * (0.35/59.)
            ENDIF
            IF(myld==2) THEN
              CALL qyacet(wc(iw),tlev(i),airden(i),qy3,qydum)
              qy3 = min(1., max(0.,qy3))
              qyI = max(0.,0.75 - qy3 - qy4)
              qy2 = qyI/7
              qy1 = qyI*6/7
             ELSEIF(myld==4) THEN
              qy3 = 0.
              qy2 = 0.
              qy1 = 0.
            ENDIF
          ENDIF

          sq(j-3,i,iw) = sig * qy1
          sq(j-2,i,iw) = sig * qy2
          sq(j-1,i,iw) = sig * qy3
          sq(j  ,i,iw) = sig * qy4

        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mk09(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! di-isopropyl ketone

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  CH3CH(CH3)COCH(CH3)2 photolysis:                                         =*
*=        CH3CH(CH3)COCH(CH3)2 + hv -> Norish type I products                =*
*=                                                                           =*
*=  Cross section:  Yujing and Mellouki (2000)                               =*
*=  Quantum yield:  estimates based on Calvert et al. 2011 book              =*
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
      INTEGER ierr
      INTEGER iw

      j = j+1
      jlabel(j) = 'CH3CH(CH3)COCH(CH3)2 -> i-C3H7CO + i-C3H7'
      j = j+1
      jlabel(j) = 'CH3CH(CH3)COCH(CH3)2 -> 2 i-C3H7 + CO'


* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/di-isopropylket.abs',
     $     STATUS='old')
      do i = 1,6
         read(kin,*)
      enddo

      n = 111
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

      qy1 = 0.5
      qy2 = 0.5


* combine xs and qy:
      DO iw = 1, nw - 1
        sig = yg(iw)
        DO i = 1, nz
          sq(j-1,i,iw) = sig * qy1
          sq(j  ,i,iw) = sig * qy2
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mk10(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! c-C4H6O

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  cyclobutanone photolysis:                                                =*
*=        c-C4H6O + hv ->  products                                          =*
*=                                                                           =*
*=  Cross section:  Calvert et al. 2008/2011 book                            =*
*=  Quantum yield:  estimates based on Calvert et al. 2011 book              =*
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

      INTEGER i, n, n1, n2, n3
      REAL x1(kdata),x2(kdata),x3(kdata)
      REAL y1(kdata),y2(kdata),y3(kdata)

* local

      REAL yg(kw), yg1(kw), yg2(kw)
      REAL qy1, qy2, qy3, qyII, qyrat
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      j = j+1
      jlabel(j) = 'c-C4H6O + hv -> C2H4 + CH2=C=O'
      j = j+1
      jlabel(j) = 'c-C4H6O + hv -> C3H6 + CO'
      j = j+1
      jlabel(j) = 'c-C4H6O + hv -> c-C3H6 + CO'


* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/cC4H6O.dat',
     $     STATUS='old')
      do i = 1,9
         read(kin,*)
      enddo

      n  = 63
      n1 = n
      n2 = n
      n3 = n
      DO i = 1, n
         READ(kin,*) idum, y1(i), y2(i), y3(i)
         x1(i) = float(idum)
         y1(i) = y1(i)*1e-20
         x2(i) = x1(i)
         x3(i) = x1(i)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x1,y1,kdata,n1,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n1,               0.,0.)
      CALL addpnt(x1,y1,kdata,n1,x1(n1)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n1,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n1,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
      ENDIF


* quantum yields

      CALL addpnt(x2,y2,kdata,n2,x2(1)*(1.-deltax),y2(1))
      CALL addpnt(x2,y2,kdata,n2,               0.,y2(1))
      CALL addpnt(x2,y2,kdata,n2,x2(n2)*(1.+deltax),y2(n2))
      CALL addpnt(x2,y2,kdata,n2,           1.e+38,y2(n2))
      CALL inter2(nw,wl,yg1,n2,x2,y2,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-2)
          STOP
      ENDIF

      CALL addpnt(x3,y3,kdata,n3,x3(1)*(1.-deltax),y3(1))
      CALL addpnt(x3,y3,kdata,n3,               0.,y3(1))
      CALL addpnt(x3,y3,kdata,n3,x3(n3)*(1.+deltax),y3(n3))
      CALL addpnt(x3,y3,kdata,n3,           1.e+38,y3(n3))
      CALL inter2(nw,wl,yg2,n3,x3,y3,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-1)
          STOP
      ENDIF


* combine xs and qy:
      DO iw   = 1, nw - 1
        sig   = yg(iw)
        qy1   = yg1(iw)
        qyII  = yg2(iw)
        qyrat = 3.77e4*0.96**wc(iw)
        qy2   = qyII/(1.+1./qyrat)
        qy3   = qyII/(1.+ qyrat)
        DO i = 1, nz
          sq(j-2,i,iw) = sig * qy1
          sq(j-1,i,iw) = sig * qy2
          sq(j  ,i,iw) = sig * qy3
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mk11(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! c-C6H10O

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  cyclobutanone photolysis:                                                =*
*=        c-C6H10O + hv ->  products                                         =*
*=                                                                           =*
*=  Cross section:  Iwasaki et al. 2008                                      =*
*=  Quantum yield:  estimates based on Calvert et al. 2011 book              =*
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

      REAL yg(kw), yg1(kw), yg2(kw), yg3(kw)
      REAL qy1, qy2, qy3
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      j = j+1
      jlabel(j) = 'c-C6H10O + hv -> 5-hexenal'
      j = j+1
      jlabel(j) = 'c-C6H10O + hv -> cyclopentane + CO'
      j = j+1
      jlabel(j) = 'c-C6H10O + hv -> 1-pentene + CO'


* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/cC6H10O.abs',
     $     STATUS='old')
      do i = 1,6
         read(kin,*)
      enddo

      n  = 23
      DO i = 1, n
         READ(kin,*) idum, y1(i)
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

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/cC6H10O_1.yld',
     $     STATUS='old')
      do i = 1,8
         read(kin,*)
      enddo

      n  = 59
      DO i = 1, n
         READ(kin,*) x1(i), y1(i)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),y1(n))
      CALL addpnt(x1,y1,kdata,n,           1.e+38,y1(n))
      CALL inter2(nw,wl,yg1,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
      ENDIF

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/cC6H10O_2.yld',
     $     STATUS='old')
      do i = 1,8
         read(kin,*)
      enddo

      n  = 48
      DO i = 1, n
         READ(kin,*) x1(i), y1(i)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),y1(1))
      CALL addpnt(x1,y1,kdata,n,               0.,y1(1))
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg2,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
      ENDIF

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/cC6H10O_3.yld',
     $     STATUS='old')
      do i = 1,8
         read(kin,*)
      enddo

      n  = 67
      DO i = 1, n
         READ(kin,*) x1(i), y1(i)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg3,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
      ENDIF


* combine xs and qy:
      DO iw = 1, nw - 1
        sig = yg(iw)
        qy1 = yg1(iw)
        qy2 = yg2(iw)
        qy3 = yg3(iw)
        IF(wc(iw)<=245.) THEN
          qy3 = max(0.,9.77e-3*wc(iw)-1.9646)
        ENDIF
        DO i = 1, nz
          sq(j-2,i,iw) = sig * qy1
          sq(j-1,i,iw) = sig * qy2
          sq(j  ,i,iw) = sig * qy3
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mk12(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! c-C5H8O

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  cyclopentanone photolysis:                                               =*
*=        c-C5H8O + hv ->  products                                          =*
*=                                                                           =*
*=  Cross section:  Calvert et al. 2008/2011 book                            =*
*=  Quantum yield:  estimates based on Calvert et al. 2011 book              =*
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
      REAL qy1, qy2, qy3, qyI, qyrat
      REAL sig
      INTEGER ierr
      INTEGER iw

      j = j+1
      jlabel(j) = 'c-C5H8O + hv -> 2 C2H4 + CO'
      j = j+1
      jlabel(j) = 'c-C5H8O + hv -> c-C4H8 + CO'
      j = j+1
      jlabel(j) = 'c-C5H8O + hv -> CH2=CHCH2CH2CHO'


* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/cC5H8O.abs',
     $     STATUS='old')
      do i = 1,8
         read(kin,*)
      enddo

      n  = 255
      DO i = 1, n
         READ(kin,*) x1(i), y1(i)
         y1(i) = y1(i)*1e-20
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


* combine xs and qy:
      DO iw   = 1, nw - 1
        sig   = yg(iw)
        IF(wc(iw)<=280.) THEN
          qyI = 0.9
          qy3 = 0.
         ELSEIF(wc(iw)>=330.) THEN
          qyI = 0.05
          qy3 = 0.85
         ELSE
          qyI = 0.9 - (wc(iw)-290.)*0.85/36.
          qy3 = (wc(iw)-290.)*0.85/36.
        ENDIF
        IF(wc(iw)>=240.) THEN
          qyrat = 0.64
         ELSE
          qyrat = 0.56
        ENDIF
        qy1   = qyI/(1.+ qyrat)
        qy2   = qyI/(1.+1./qyrat)
        DO i = 1, nz
          sq(j-2,i,iw) = sig * qy1
          sq(j-1,i,iw) = sig * qy2
          sq(j  ,i,iw) = sig * qy3
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mk13(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! c-C3H4O

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  cyclopropanone photolysis:                                               =*
*=        c-C3H4O + hv ->  products                                          =*
*=                                                                           =*
*=  Cross section:  Thomas and Rodiguez (1971)                               =*
*=  Quantum yield:  estimates based on Calvert et al. 2011 book              =*
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

      INTEGER i, n, n1, n2
      REAL x1(kdata), x2(kdata)
      REAL y1(kdata), y2(kdata)

* local

      REAL yg(kw), yg1(kw)
      REAL qy1, qy2, qy
      REAL sig
      INTEGER ierr
      INTEGER iw

      j = j+1
      jlabel(j) = 'c-C3H4O + hv -> C2H4 + CO'
      j = j+1
      jlabel(j) = 'c-C3H4O + hv -> further products'


* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/cC3H4O_calv.dat',
     $     STATUS='old')
      do i = 1,9
         read(kin,*)
      enddo

      n  = 122
      n1 = n
      n2 = n
      DO i = 1, n
         READ(kin,*) x1(i), y1(i), y2(i)
         y1(i) = y1(i)*1e-20
         x2(i) = x1(i)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x1,y1,kdata,n1,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n1,               0.,0.)
      CALL addpnt(x1,y1,kdata,n1,x1(n1)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n1,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n1,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
      ENDIF


* quantum yields

      CALL addpnt(x2,y2,kdata,n2,x2(1)*(1.-deltax),1.)
      CALL addpnt(x2,y2,kdata,n2,               0.,1.)
      CALL addpnt(x2,y2,kdata,n2,x2(n2)*(1.+deltax),0.)
      CALL addpnt(x2,y2,kdata,n2,           1.e+38,0.)
      CALL inter2(nw,wl,yg1,n2,x2,y2,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-2)
          STOP
      ENDIF


* combine xs and qy:
      DO iw = 1, nw - 1
        sig = yg(iw)
        IF(wc(iw)<=320.) THEN
          qy = 1.
         ELSEIF(wc(iw)>=370.) THEN
          qy = 0.9
         ELSE
          qy = 1. - (wc(iw)-320.)*0.1/50.
        ENDIF
        qy1 = yg1(iw)
        qy2 = qy - qy1
        DO i = 1, nz
          sq(j-1,i,iw) = sig * qy1
          sq(j  ,i,iw) = sig * qy2
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE mk14(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! EVK

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for CH3CH2COCH=CH  =*
*=  Ethyl vinyl ketone photolysis:                                           =*
*=           CH3CH2COCH=CH2 + hv -> Products                                 =*
*=                                                                           =*
*=  Cross section same as MVK from                                           =*
*= W. Schneider and G. K. Moorgat, priv. comm, MPI Mainz 1989 as reported by =*
*= Roeth, E.-P., R. Ruhnke, G. Moortgat, R. Meller, and W. Schneider,        =*
*= UV/VIS-Absorption Cross Sections and QUantum Yields for Use in            =*
*= Photochemistry and Atmospheric Modeling, Part 2: Organic Substances,      =*
*= Forschungszentrum Julich, Report Jul-3341, 1997.                          =*
*=                                                                           =*
*=  Quantum yield assumed unity                                              =*
*-----------------------------------------------------------------------------*
*=  PARAMETERS:                                                              =*
*=  NW     - INTEGER, number of specified intervals + 1 in working        (I)=*
*=           wavelength grid                                                 =*
*=  WL     - REAL, vector of lower limits of wavelength intervals in      (I)=*
*=           working wavelength grid                                         =*
*=  WC     - REAL, vector of center points of wavelength intervals in     (I)=*
*=           working wavelength grid                                         =*
*=  NZ     - INTEGER, number of altitude levels in working altitude grid  (I)=*
*=  TLEV   - REAL, temperature (K) at each specified altitude level       (I)=*
*=  AIRDEN - REAL, air density (molec/cc) at each altitude level          (I)=*
*=  J      - INTEGER, counter for number of weighting functions defined  (IO)=*
*=  SQ     - REAL, cross section x quantum yield (cm^2) for each          (O)=*
*=           photolysis reaction defined, at each defined wavelength and     =*
*=           at each defined altitude level                                  =*
*=  JLABEL - CHARACTER*lcl, string identifier for each photolysis         (O)=*
*=           reaction defined                                                =*
*=  lcl    - INTEGER, length of character for labels                         =*
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
      PARAMETER(kdata=50)

      INTEGER i, n
      REAL x(kdata), y(kdata)

* local

      REAL yg(kw)
      REAL qy, qy1, qy2, qy3
      INTEGER ierr, idum
      INTEGER iw

************************* ethyl vinyl ketone photolysis

      j = j+1
      jlabel(j) = 'CH3CH2COCH=CH2 -> C2H5 + C2H3CO'
      j = j+1
      jlabel(j) = 'CH3CH2COCH=CH2 -> C2H3 + C2H5CO'
      j = j+1
      jlabel(j) = 'CH3CH2COCH=CH2 -> 1-C4H8 + CO'


      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/EVK.abs',
     $     STATUS='old')
      DO i = 1, 4
        READ(kin,*)
      ENDDO
      n = 24
      DO i = 1, n
        READ(kin,*) idum, y(i)
        x(i) = float(idum)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x,y,kdata,n,x(1)*(1.-deltax),0.)
      CALL addpnt(x,y,kdata,n,               0.,0.)
      CALL addpnt(x,y,kdata,n,x(n)*(1.+deltax),0.)
      CALL addpnt(x,y,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x,y,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF

* quantum yield estimated same as MVK from
* Gierczak, T., J. B. Burkholder, R. K. Talukdar, A. Mellouki, S. B. Barone,
* and A. R. Ravishankara, Atmospheric fate of methyl vinyl ketone and methacrolein,
* J. Photochem. Photobiol A: Chemistry, 110 1-10, 1997.
* depends on pressure and wavelength, set upper limit to 1.0
* also recommended by IUPAC

* branching from IUPAC

      DO iw = 1, nw - 1
         DO i = 1, nz
            qy  = exp(-0.055*(wc(iw)-308.)) /
     $           (5.5 + 9.2e-19*airden(i))
            qy  = min(qy, 1.)
            qy1 = 0.2 * qy
            qy2 = 0.2 * qy
            qy3 = 0.6 * qy
            sq(j-2,i,iw) = yg(iw) * qy1
            sq(j-1,i,iw) = yg(iw) * qy2
            sq(j  ,i,iw) = yg(iw) * qy3
         ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE mk15(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! methyl 2-hydroxyethyl ketone

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  methyl 2-hydroxethyl ketone (CH3COC2H4OH) photolysis:                    =*
*=           CH3COC2H4OH  + hv -> CH3CO + CH2CH2OH                           =*
*=                                                                           =*
*=  Cross section:  Messaadia et al. (2012)                                  =*
*=  Quantum yield:  estimates based on hydroxyacetone, MEK, and 2-pentanone  =*
*=                                                                           =*
*-----------------------------------------------------------------------------*
*=  PARAMETERS:                                                              =*
*=  NW     - INTEGER, number of specified intervals + 1 in working        (I)=*
*=           wavelength grid                                                 =*
*=  WL     - REAL, vector of lower limits of wavelength intervals in      (I)=*
*=           working wavelength grid                                         =*
*=  WC     - REAL, vector of center points of wavelength intervals in     (I)=*
*=           working wavelength grid                                         =*
*=  NZ     - INTEGER, number of altitude levels in working altitude grid  (I)=*
*=  TLEV   - REAL, temperature (K) at each specified altitude level       (I)=*
*=  AIRDEN - REAL, air density (molec/cc) at each altitude level          (I)=*
*=  J      - INTEGER, counter for number of weighting functions defined  (IO)=*
*=  SQ     - REAL, cross section x quantum yield (cm^2) for each          (O)=*
*=           photolysis reaction defined, at each defined wavelength and     =*
*=           at each defined altitude level                                  =*
*=  JLABEL - CHARACTER*lcl, string identifier for each photolysis         (O)=*
*=           reaction defined                                                =*
*=  lcl    - INTEGER, length of character for labels                         =*
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
      PARAMETER(kdata=200)

      INTEGER i, n
      REAL x(kdata), y(kdata)

* local

      REAL yg(kw)
      REAL qy
      INTEGER ierr, idum
      INTEGER iw

************************* CH3COC2H4OH photolysis

      j = j+1
      jlabel(j) = 'CH3COC2H4OH -> CH3CO + CH2CH2OH'

* cross sections
      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/4OH2butanone.abs',
     $     STATUS='old')
      DO i = 1, 4
        READ(kin,*)
      ENDDO
      n = 146
      DO i = 1, n
        READ(kin,*) idum, y(i)
        x(i) = float(idum)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x,y,kdata,n,x(1)*(1.-deltax),0.)
      CALL addpnt(x,y,kdata,n,               0.,0.)
      CALL addpnt(x,y,kdata,n,x(n)*(1.+deltax),0.)
      CALL addpnt(x,y,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x,y,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* quantum yields

      qy = 0.34


* combine
      DO iw = 1, nw - 1
         DO i = 1, nz
            sq(j,i,iw) = yg(iw) * qy
         ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE mk16(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! methyl 1-hydroxyethyl ketone

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  methyl 1-hydroxethyl ketone (CH3COCH(OH)CH3) photolysis:                 =*
*=           CH3COCH(OH)CH3  + hv -> CH3CO + CH3CHOH                         =*
*=                                                                           =*
*=  Cross section:  Messaadia et al. (2012)                                  =*
*=  Quantum yield:  estimates based on hydroxyacetone, MEK, and 2-pentanone  =*
*=                                                                           =*
*-----------------------------------------------------------------------------*
*=  PARAMETERS:                                                              =*
*=  NW     - INTEGER, number of specified intervals + 1 in working        (I)=*
*=           wavelength grid                                                 =*
*=  WL     - REAL, vector of lower limits of wavelength intervals in      (I)=*
*=           working wavelength grid                                         =*
*=  WC     - REAL, vector of center points of wavelength intervals in     (I)=*
*=           working wavelength grid                                         =*
*=  NZ     - INTEGER, number of altitude levels in working altitude grid  (I)=*
*=  TLEV   - REAL, temperature (K) at each specified altitude level       (I)=*
*=  AIRDEN - REAL, air density (molec/cc) at each altitude level          (I)=*
*=  J      - INTEGER, counter for number of weighting functions defined  (IO)=*
*=  SQ     - REAL, cross section x quantum yield (cm^2) for each          (O)=*
*=           photolysis reaction defined, at each defined wavelength and     =*
*=           at each defined altitude level                                  =*
*=  JLABEL - CHARACTER*lcl, string identifier for each photolysis         (O)=*
*=           reaction defined                                                =*
*=  lcl    - INTEGER, length of character for labels                         =*
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
      PARAMETER(kdata=200)

      INTEGER i, n
      REAL x(kdata), y(kdata)

* local

      REAL yg(kw)
      REAL qy1, qy2
      INTEGER ierr, idum
      INTEGER iw
      INTEGER myld

************************* CH3COCH(OH)CH3 photolysis

      j = j+1
      jlabel(j) = 'CH3COCH(OH)CH3 -> CH3CO + CH3CHOH'
      j = j+1
      jlabel(j) = 'CH3COCH(OH)CH3 -> CH3CH(OH)CO + CH3'


      IF(vers==1)THEN
        myld = 1
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
        WRITE(kout,'(2A)')
     &       ' CH3COCH(OH)CH3 quantum yield same as hydroxyacetone.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(A)')
     &     ' CH3COCH(OH)CH3 quantum yield same as MEK.'
       ELSE
        STOP "'myld' not defined for CH3COCH(OH)CH3 photolysis."
      ENDIF

* cross sections
      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/3OH2butanone.abs',
     $     STATUS='old')
      DO i = 1, 4
        READ(kin,*)
      ENDDO
      n = 133
      DO i = 1, n
        READ(kin,*) idum, y(i)
        x(i) = float(idum)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x,y,kdata,n,x(1)*(1.-deltax),0.)
      CALL addpnt(x,y,kdata,n,               0.,0.)
      CALL addpnt(x,y,kdata,n,x(n)*(1.+deltax),0.)
      CALL addpnt(x,y,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x,y,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* quantum yields

      IF(myld==1) THEN
        qy1 = 0.31
        qy2 = 0.29
       ELSEIF(myld==2) THEN
        qy1 = 0.34
        qy2 = 0.00
      ENDIF

* combine
      DO iw = 1, nw - 1
         DO i = 1, nz
            sq(j-1,i,iw) = yg(iw) * qy1
            sq(j  ,i,iw) = yg(iw) * qy2
         ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE mk17(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! 3-hydroxy-3-methyl-2-butanone

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  3-hydroxy-3-methyl-2-butanone (CH3COC(CH3)2OH) photolysis:               =*
*=           CH3COCH(OH)CH3  + hv -> CH3CO + CH3CHOH                         =*
*=                                                                           =*
*=  Cross section:  Messaadia et al. (2012)                                  =*
*=  Quantum yield:  estimates based on hydroxyacetone, MEK, 2-pentanone,     =*
*=                  methyl isopropyl ketone, and di-isopropyl ketone         =*
*=                                                                           =*
*-----------------------------------------------------------------------------*
*=  PARAMETERS:                                                              =*
*=  NW     - INTEGER, number of specified intervals + 1 in working        (I)=*
*=           wavelength grid                                                 =*
*=  WL     - REAL, vector of lower limits of wavelength intervals in      (I)=*
*=           working wavelength grid                                         =*
*=  WC     - REAL, vector of center points of wavelength intervals in     (I)=*
*=           working wavelength grid                                         =*
*=  NZ     - INTEGER, number of altitude levels in working altitude grid  (I)=*
*=  TLEV   - REAL, temperature (K) at each specified altitude level       (I)=*
*=  AIRDEN - REAL, air density (molec/cc) at each altitude level          (I)=*
*=  J      - INTEGER, counter for number of weighting functions defined  (IO)=*
*=  SQ     - REAL, cross section x quantum yield (cm^2) for each          (O)=*
*=           photolysis reaction defined, at each defined wavelength and     =*
*=           at each defined altitude level                                  =*
*=  JLABEL - CHARACTER*lcl, string identifier for each photolysis         (O)=*
*=           reaction defined                                                =*
*=  lcl    - INTEGER, length of character for labels                         =*
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
      PARAMETER(kdata=200)

      INTEGER i, n
      REAL x(kdata), y(kdata)

* local

      REAL yg(kw)
      REAL qy
      INTEGER ierr, idum
      INTEGER iw

************************* CH3COCH(OH)CH3 photolysis

      j = j+1
      jlabel(j) = 'CH3COC(CH3)2OH -> CH3CO + (CH3)2COH'


* cross sections
      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/3OH3Me2butanone.abs',
     $     STATUS='old')
      DO i = 1, 4
        READ(kin,*)
      ENDDO
      n = 151
      DO i = 1, n
        READ(kin,*) idum, y(i)
        x(i) = float(idum)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x,y,kdata,n,x(1)*(1.-deltax),0.)
      CALL addpnt(x,y,kdata,n,               0.,0.)
      CALL addpnt(x,y,kdata,n,x(n)*(1.+deltax),0.)
      CALL addpnt(x,y,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x,y,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* quantum yields

      qy = 0.34

* combine
      DO iw = 1, nw - 1
         DO i = 1, nz
            sq(j,i,iw) = yg(iw) * qy
         ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE mk18(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! Ketene

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  Ketene (CH2=C=O) photolysis:                                             =*
*=           CH2=C=O + hv -> CO2 + CO + H2                                   =*
*=                                                                           =*
*=  Cross section:  Laufer and Keller (1971)                                 =*
*=  Quantum yield:  Calvert et al. (2011)                                    =*
*=                                                                           =*
*-----------------------------------------------------------------------------*
*=  PARAMETERS:                                                              =*
*=  NW     - INTEGER, number of specified intervals + 1 in working        (I)=*
*=           wavelength grid                                                 =*
*=  WL     - REAL, vector of lower limits of wavelength intervals in      (I)=*
*=           working wavelength grid                                         =*
*=  WC     - REAL, vector of center points of wavelength intervals in     (I)=*
*=           working wavelength grid                                         =*
*=  NZ     - INTEGER, number of altitude levels in working altitude grid  (I)=*
*=  TLEV   - REAL, temperature (K) at each specified altitude level       (I)=*
*=  AIRDEN - REAL, air density (molec/cc) at each altitude level          (I)=*
*=  J      - INTEGER, counter for number of weighting functions defined  (IO)=*
*=  SQ     - REAL, cross section x quantum yield (cm^2) for each          (O)=*
*=           photolysis reaction defined, at each defined wavelength and     =*
*=           at each defined altitude level                                  =*
*=  JLABEL - CHARACTER*lcl, string identifier for each photolysis         (O)=*
*=           reaction defined                                                =*
*=  lcl    - INTEGER, length of character for labels                         =*
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
      PARAMETER(kdata=200)

      INTEGER i, n1, n2
      REAL x1(kdata),x2(kdata)
      REAL y1(kdata),y2(kdata)

* local

      REAL yg(kw),yg1(kw)
      INTEGER ierr, idum
      INTEGER iw

************************* Ketene photolysis

      j = j+1
      jlabel(j) = 'CH2=C=O -> CO2 + CO + H2'


* read data

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/Ketene.dat',
     $     STATUS='old')
      DO i = 1, 9
        READ(kin,*)
      ENDDO
      n1 = 151
      n2 = n1
      DO i = 1, n1
        READ(kin,*) idum, y1(i), y2(i)
        x1(i) = float(idum)
        x2(i) = x1(i)
        y1(i) = y1(i)*1.E-20
      ENDDO
      CLOSE(kin)


* cross sections

      CALL addpnt(x1,y1,kdata,n1,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n1,               0.,0.)
      CALL addpnt(x1,y1,kdata,n1,x1(n1)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n1,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n1,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
      ENDIF


* quantum yields

      CALL addpnt(x2,y2,kdata,n2,x2(1)*(1.-deltax),y2(1))
      CALL addpnt(x2,y2,kdata,n2,               0.,y2(1))
      CALL addpnt(x2,y2,kdata,n2,x2(n2)*(1.+deltax),0.)
      CALL addpnt(x2,y2,kdata,n2,           1.e+38,0.)
      CALL inter2(nw,wl,yg1,n2,x2,y2,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-2)
          STOP
      ENDIF


* combine
      DO iw = 1, nw - 1
         DO i = 1, nz
            sq(j,i,iw) = yg(iw) * yg1(iw)
         ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE mk19(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! Methylketene

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  Methylketene (CH3CH=C=O) photolysis:                                     =*
*=           CH3CH=C=O + hv -> C2H4 + CO                                     =*
*=                                                                           =*
*=  Cross section:  Chong and Kistiakowsky (1964)                            =*
*=  Quantum yield:  Calvert et al. (2011)                                    =*
*=                                                                           =*
*-----------------------------------------------------------------------------*
*=  PARAMETERS:                                                              =*
*=  NW     - INTEGER, number of specified intervals + 1 in working        (I)=*
*=           wavelength grid                                                 =*
*=  WL     - REAL, vector of lower limits of wavelength intervals in      (I)=*
*=           working wavelength grid                                         =*
*=  WC     - REAL, vector of center points of wavelength intervals in     (I)=*
*=           working wavelength grid                                         =*
*=  NZ     - INTEGER, number of altitude levels in working altitude grid  (I)=*
*=  TLEV   - REAL, temperature (K) at each specified altitude level       (I)=*
*=  AIRDEN - REAL, air density (molec/cc) at each altitude level          (I)=*
*=  J      - INTEGER, counter for number of weighting functions defined  (IO)=*
*=  SQ     - REAL, cross section x quantum yield (cm^2) for each          (O)=*
*=           photolysis reaction defined, at each defined wavelength and     =*
*=           at each defined altitude level                                  =*
*=  JLABEL - CHARACTER*lcl, string identifier for each photolysis         (O)=*
*=           reaction defined                                                =*
*=  lcl    - INTEGER, length of character for labels                         =*
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
      PARAMETER(kdata=200)

      INTEGER i, n1, n2
      REAL x1(kdata),x2(kdata)
      REAL y1(kdata),y2(kdata)

* local

      REAL yg(kw),yg1(kw),dum
      INTEGER ierr, idum
      INTEGER iw

************************* CH3COCH(OH)CH3 photolysis

      j = j+1
      jlabel(j) = 'CH3CH=C=O -> C2H4 + CO'


* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/methylketene.abs',
     $     STATUS='old')
      DO i = 1, 8
        READ(kin,*)
      ENDDO
      n1 = 136
      DO i = 1, n1
        READ(kin,*) x1(i), y1(i)
        y1(i) = y1(i)*1.E-20
      ENDDO
      CLOSE(kin)

      CALL addpnt(x1,y1,kdata,n1,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n1,               0.,0.)
      CALL addpnt(x1,y1,kdata,n1,x1(n1)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n1,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n1,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
      ENDIF


* quantum yields

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/Ketene.dat',
     $     STATUS='old')
      DO i = 1, 9
        READ(kin,*)
      ENDDO
      n2 = 151
      DO i = 1, n2
        READ(kin,*) idum, dum, y2(i)
        x2(i) = float(idum)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x2,y2,kdata,n2,x2(1)*(1.-deltax),y2(1))
      CALL addpnt(x2,y2,kdata,n2,               0.,y2(1))
      CALL addpnt(x2,y2,kdata,n2,x2(n2)*(1.+deltax),0.)
      CALL addpnt(x2,y2,kdata,n2,           1.e+38,0.)
      CALL inter2(nw,wl,yg1,n2,x2,y2,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-2)
          STOP
      ENDIF


* combine
      DO iw = 1, nw - 1
         DO i = 1, nz
            sq(j,i,iw) = yg(iw) * yg1(iw)
         ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE mk20(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! Generic unbranched ketones

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  RCOR'  photolysis:                                                       =*
*=           RCOR'+ hv -> R + R'CO                                           =*
*=                                                                           =*
*=  Cross section:  Chong and Kistiakowsky (1964)                            =*
*=  Quantum yield:  Calvert et al. (2011)                                    =*
*=                                                                           =*
*-----------------------------------------------------------------------------*
*=  PARAMETERS:                                                              =*
*=  NW     - INTEGER, number of specified intervals + 1 in working        (I)=*
*=           wavelength grid                                                 =*
*=  WL     - REAL, vector of lower limits of wavelength intervals in      (I)=*
*=           working wavelength grid                                         =*
*=  WC     - REAL, vector of center points of wavelength intervals in     (I)=*
*=           working wavelength grid                                         =*
*=  NZ     - INTEGER, number of altitude levels in working altitude grid  (I)=*
*=  TLEV   - REAL, temperature (K) at each specified altitude level       (I)=*
*=  AIRDEN - REAL, air density (molec/cc) at each altitude level          (I)=*
*=  J      - INTEGER, counter for number of weighting functions defined  (IO)=*
*=  SQ     - REAL, cross section x quantum yield (cm^2) for each          (O)=*
*=           photolysis reaction defined, at each defined wavelength and     =*
*=           at each defined altitude level                                  =*
*=  JLABEL - CHARACTER*lcl, string identifier for each photolysis         (O)=*
*=           reaction defined                                                =*
*=  lcl    - INTEGER, length of character for labels                         =*
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

* local

      REAL    qy,sig
      REAL    A,lc,w
      INTEGER CN
      INTEGER iz,iw

************************* CH3COCH(OH)CH3 photolysis

      j = j+1
      jlabel(j) = 'C3-Ketone -> products'
      j = j+1
      jlabel(j) = 'C4-Ketone -> products'
      j = j+1
      jlabel(j) = 'C5-Ketone -> products'
      j = j+1
      jlabel(j) = 'C6-Ketone -> products'
      j = j+1
      jlabel(j) = 'C7-Ketone -> products'
      j = j+1
      jlabel(j) = 'C8-Ketone -> products'
      j = j+1
      jlabel(j) = 'C9-Ketone -> products'
      j = j+1
      jlabel(j) = 'C10-Ketone -> products'
      j = j+1
      jlabel(j) = 'C11-Ketone -> products'
      j = j+1
      jlabel(j) = 'C12-Ketone -> products'
      j = j+1
      jlabel(j) = 'C13-Ketone -> products'
      j = j+1
      jlabel(j) = 'C14-Ketone -> products'
      j = j+1
      jlabel(j) = 'C15-Ketone -> products'
      j = j+1
      jlabel(j) = 'C16-Ketone -> products'
      j = j+1
      jlabel(j) = 'C17-Ketone -> products'
      j = j+1
      jlabel(j) = 'C18-Ketone -> products'
      j = j+1
      jlabel(j) = 'C19-Ketone -> products'
      j = j+1
      jlabel(j) = 'C20-Ketone -> products'


* cross sections are parameterised with Gaussian fit
*
* sig (CN, wl, T) = A(CN,T)*exp{-[(wl - lc(CN,T)) / w(CN,T)]**2}
* variables:  CN = carbon number; wl wavelength; T = temperature
* parameters: A = amplitude; lc = centre wavelength; w = curve width
*
* with (A(CN, T) / 1E-20 cm2) = 4.845e-3 * (T/K) + 2.364*ln(CN) + 1.035
*      (lc(CN, T) / nm)       = 1.71e-2  * (T/K) + 1.718 * CN   + 265.344
*       w(CN, T)              = 9.8e-3   * (T/K) - 0.728 * CN   + 29.367


* quantum yields

      qy = 0.75


* combine
      DO iw = 1, nw - 1
         DO iz = 1, nz
           DO CN = 3,20
             A   = (4.845e-3 * tlev(iz) + 2.364*log(float(CN)) + 1.035)
     &             *1.e-20
             lc  = 1.71e-2   * tlev(iz) + 1.718 * CN   + 265.344
             w   = 9.8e-3    * tlev(iz) - 0.728 * CN   + 29.367
             sig = A*exp(-((wc(iw) - lc) / w)**2)
             sq(j-20+CN,iz,iw) = sig * qy
           ENDDO
         ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE mk21(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! alpha-branched ketones (with Norish II)

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  alpha-branched ketone photolysis:                                        =*
*=                                                                           =*
*=  Cross section:  same as DIPK                                             =*
*=  Quantum yield:  same as MIBK                                             =*
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
      REAL qy1, qy2, qy3, qy4
      REAL sig
      INTEGER ierr
      INTEGER iw

      j = j+1
      jlabel(j) = 'a-br. Ket. -> R1CO + R2'
      j = j+1
      jlabel(j) = 'a-br. Ket. -> R2CO + R1'
      j = j+1
      jlabel(j) = 'a-br. Ket. -> R1 + R2 + CO'
      j = j+1
      jlabel(j) = 'a-br. Ket. -> enol + 1-alkene'


* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/KET/di-isopropylket.abs',
     $     STATUS='old')
      do i = 1,6
         read(kin,*)
      enddo

      n = 111
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

      qy1 = 0.035
      qy2 = 0.035
      qy3 = 0.08
      qy4 = 0.35


* combine xs and qy:
      DO iw = 1, nw - 1
        sig = yg(iw)
        DO i = 1, nz
          sq(j-3,i,iw) = sig * qy1
          sq(j-2,i,iw) = sig * qy2
          sq(j-1,i,iw) = sig * qy3
          sq(j  ,i,iw) = sig * qy4
        ENDDO
      ENDDO

      END

* ============================================================================*