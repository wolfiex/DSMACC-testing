*= This file contains the following subroutines, related to reading/loading
*= the product (cross section) x (quantum yield) for photo-reactions of
*= aldehydes in MCM-GECKO, which were not yet present in TUV5.2:
*=
*=     ma01 through ma21

*=============================================================================*

      SUBROUTINE ma01(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! n-C3H7CHO

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide product (cross section)x(quantum yield) for n-C3H7CHO photolysis =*
*=          n-C3H7CHO + hv -> products (Norish type I + II)                  =*
*=                                                                           =*
*=  Cross section and quantum yield from IUPAC                               =*
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
      PARAMETER(kdata=580)

      INTEGER i, n, n1
      REAL x1(kdata), x1oh(kdata)
      REAL y1(kdata), y1oh(kdata)

* local

      REAL yg(kw),yg1(kw),ygoh(kw)
      REAL qy1, qy2, qy0, eta, qyoh
      REAL sig,sigoh
      INTEGER ierr, idum
      INTEGER iw

      INTEGER myld

* Norish type I:
      j = j+1
      jlabel(j) = 'n-C3H7CHO -> n-C3H7 + CHO'
* Norish type II:
      j = j+1
      jlabel(j) = 'n-C3H7CHO -> C2H4 + CH2CHOH'
* test OH substituted butyraldehyde:
      j = j+1
      jlabel(j) = 'ALD4OHqy -> NI products'
      j = j+1
      jlabel(j) = 'ALD4OHqy -> NII products'
      j = j+1
      jlabel(j) = 'ALD4OHoh -> NI products'
      j = j+1
      jlabel(j) = 'ALD4OHoh -> NII products'


      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/nC3H7CHO_iup.abs',
     $     STATUS='old')
      do i = 1, 5
         read(kin,*)
      enddo

      n = 106
      DO i = 1, n
         READ(kin,*) idum, y1(i)
         x1(i) = FLOAT(idum)
         y1(i) = y1(i)*1.e-20
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,ygoh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* quantum yields

* 1: Moortgat 99
* 2: IUPAC (Tadic et al. 01)

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
     &       ' n-C3H7CHO quantum yields from Moortgat 1999.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' n-C3H7CHO quantum yields from IUPAC.'
       ELSE
        STOP "'myld' not defined for n-C3H7CHO photolysis."
      ENDIF


      IF(myld==1) THEN
        qy1 = 0.19
        qy2 = 0.06
       ELSEIF(myld==2) THEN
        qy0 = 0.21
        qy2 = 0.1
      ENDIF

      qyOH = 0.75


* pressure dependence

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/nC3H7CHO_Chen02.yld',
     $     STATUS='old')
      do i = 1, 4
         read(kin,*)
      enddo

      n = 11
      DO i = 1, n
         READ(kin,*) idum, y1(i)
         x1(i) = FLOAT(idum)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),qy0)
      CALL addpnt(x1,y1,kdata,n,               0.,qy0)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),qy0)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,qy0)
      CALL inter2(nw,wl,yg1,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-1)
          STOP
      ENDIF


* combine:

      DO iw = 1, nw - 1
         sig = yg(iw)
         eta = MAX(0.,yg1(iw)/qy0-1.)
         sigoh = ygoh(iw)
         WRITE(19,*) wc(iw),sig,sigoh
         DO i = 1, nz
           qy1 = qy0*(1.+eta)/(1.+eta*airden(i)/2.465e19)
           sq(j-5,i,iw) = sig * qy1
           sq(j-4,i,iw) = sig * qy2
           sq(j-3,i,iw) = sigoh * qy1
           sq(j-2,i,iw) = sigoh * qy2
           IF(qy1+qy2 > 0.) THEN
             sq(j-1,i,iw) = sigoh * qyoh*qy1/(qy1+qy2)
             sq(j  ,i,iw) = sigoh * qyoh*qy2/(qy1+qy2)
            ELSE
             sq(j-1,i,iw) = 0.
             sq(j  ,i,iw) = 0.
           ENDIF
         ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma02(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! i-C3H7CHO

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide product (cross section)x(quantum yield) for i-C3H7CHO photolysis =*
*=          i-C3H7CHO + hv -> i-C3H7 + CHO                                   =*
*=                                                                           =*
*=  Cross section and quantum yield as given below in source code            =*
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
      PARAMETER(kdata=580)

      INTEGER i, n
      REAL x1(kdata), x2(kdata)
      REAL y1(kdata), y2(kdata)

* local

      REAL yg(kw), yg1(kw), dum
      REAL qy
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs, myld

* only Norish type I for i-C3H7CHO!
      j = j+1
      jlabel(j) = 'i-C3H7CHO + hv -> i-C3H7 + CHO'


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
     &       ' i-C3H7CHO cross sections from Martinez et al. 1992.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' i-C3H7CHO cross sections from IUPAC.'
       ELSE
        STOP "'mabs' not defined for i-C3H7CHO photolysis."
      ENDIF

      IF(vers==1)THEN
        myld = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
       ELSEIF(vers==2)THEN
        myld = 4
       ELSEIF(vers==0) THEN
        myld = 4
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(A)')
     &       ' i-C3H7CHO quantum yields from Desai et al. 1986.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' i-C3H7CHO quantum yields from Calvert book, opt. 1.'
       ELSEIF(myld.EQ.3) THEN
        WRITE(kout,'(A)')
     &       ' i-C3H7CHO quantum yields from Calvert book, opt. 2.'
       ELSEIF(myld.EQ.4) THEN
        WRITE(kout,'(A)')
     &       ' i-C3H7CHO quantum yields from IUPAC.'
       ELSE
        STOP "'myld' not defined for i-C3H7CHO photolysis."
      ENDIF

* cross sections

      IF(mabs==1) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/i_butyraldehyde_R.prn',
     $       STATUS='old')
        do i = 1, 3
           read(kin,*)
        enddo

        n = 101
        DO i = 1, n
           READ(kin,*) x1(i), y1(i), dum
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==2) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/iC3H7CHO_iup.abs',
     $       STATUS='old')
        do i = 1, 5
           read(kin,*)
        enddo

        n = 121
        DO i = 1, n
           READ(kin,*) idum, y1(i)
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
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* quantum yields
! myld 3 needs adjustments of zero-pressure qy!

      IF(myld==1) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/i_butyraldehyde_R.prn',
     $       STATUS='old')
        do i = 1, 3
           read(kin,*)
        enddo

        n = 101
        DO i = 1, n
           READ(kin,*) x1(i), dum, y1(i)
        ENDDO
        CLOSE(kin)

       ELSEIF(myld==2 .OR. myld==3) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/iC3H7CHO_calv.yld',
     $       STATUS='old')
        do i = 1, 6
           read(kin,*)
        enddo

        n = 73
        DO i = 1, n
           READ(kin,*) idum, dum, y1(i),y2(i)
           x1(i) = FLOAT(idum)
           x2(i) = x1(i)
        ENDDO
        CLOSE(kin)

       ELSEIF(myld==4) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/iC3H7CHO_iup.yld',
     $       STATUS='old')
        do i = 1, 7
           read(kin,*)
        enddo

        n = 11
        DO i = 1, n
           READ(kin,*) idum, y1(i)
           x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

      ENDIF

      IF(myld==3)THEN
        CALL addpnt(x2,y2,kdata,n,x2(1)*(1.-deltax),0.)
        CALL addpnt(x2,y2,kdata,n,               0.,0.)
        CALL addpnt(x2,y2,kdata,n,x2(n)*(1.+deltax),0.)
        CALL addpnt(x2,y2,kdata,n,           1.e+38,0.)
        CALL inter2(nw,wl,yg1,n,x2,y2,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
        ENDIF
       ELSE
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

*combine
      DO iw = 1, nw - 1
         sig = yg (iw)
         qy  = yg1(iw)
         DO i = 1, nz
            sq(j  ,i,iw) = sig * qy
         ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma03(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! pinonaldehyde

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide product (cross section)x(quantum yield) for                      =*
*=  pinonaldehyde photolysis                                                 =*
*=          pinonaldehyde + hv -> R + CO + HO2                               =*
*=                                                                           =*
*=  Cross section from IUPAC                                                 =*
*=  Quantum yield see options below                                          =*
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

      INTEGER myld


      j = j+1
      jlabel(j) = 'pinonaldehyde -> R + CO + HO2'

* 1: EUPHORE chamber experiments (RADICAL 2002)
* 2: Jaoui and Kamens 2003
* 3: approximate average

      IF(vers==1)THEN
        myld = 1
       ELSEIF(vers==2)THEN
        myld = 1
       ELSEIF(vers==0) THEN
        myld = 3
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' Pinonaldehyde quantum yields',
     &       ' from EUPHORE chamber experiments.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' Pinonaldehyde quantum yields',
     &       ' from Jaoui and Kamens 2003.'
       ELSEIF(myld.EQ.3) THEN
        WRITE(kout,'(2A)')
     &       ' Pinonaldehyde quantum yields',
     &       ' as approximate average of opt. 1 and 2.'
       ELSE
        STOP "'myld' not defined for pinonaldehyde photolysis."
      ENDIF


      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DICAR/Pinonaldehyde_iup.abs',
     $     STATUS='old')
      do i = 1, 5
         read(kin,*)
      enddo

      n = 14
      DO i = 1, n
         READ(kin,*) x1(i), y1(i)
         y1(i) = y1(i) * 1E-20
      ENDDO
      CLOSE(kin)

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-1)
          STOP
      ENDIF


* quantum yields
      IF(myld == 1) THEN
        qy = 0.14
       ELSEIF(myld == 2) THEN
        qy = 0.4
       ELSEIF(myld == 3) THEN
        qy = 0.25
      ENDIF


* combine:

      DO iw = 1, nw - 1
         sig = yg(iw)
         DO i = 1, nz
            sq(j,i,iw) = sig * qy
         ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma04(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! n-C4H9CHO

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for n-C4H9CHO      =*
*=  photolysis:                                                              =*
*=         n-C4H9CHO + hv -> Norish type I + II products                     =*
*=                                                                           =*
*=  Cross section:  see options below in the source code                     =*
*=  Quantum yield:  see options below in the source code                     =*
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

      INTEGER i, n, n1
      REAL x1(kdata), x1oh(kdata)
      REAL y1(kdata), y1oh(kdata)


* local

      REAL yg(kw), yg1(kw), yg2(kw), ygoh(kw), dum
      REAL qy1, qy2, qy3, qy0, eta, ptorr,qyoh
      REAL sig, sigoh
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs, myld


      j = j+1
      jlabel(j) = 'n-C4H9CHO + hv -> C4H9 +  CHO'
      j = j+1
      jlabel(j) = 'n-C4H9CHO + hv -> CH3CH=CH2 +  CH2=CHOH'
      j = j+1
      jlabel(j) = 'n-C4H9CHO + hv -> 2-methylcyclobutanol'

      j = j+1
      jlabel(j) = 'C5nALDOHqy + hv -> NI products'
      j = j+1
      jlabel(j) = 'C5nALDOHqy + hv -> NII products'
! 3rd cyclisation channel for OH-subst. C5 n-aldehydes will be estimated with
! scaled value from the corresponding C8 compound

      j = j+1
      jlabel(j) = 'C5nALDOHoh + hv -> NI products'
      j = j+1
      jlabel(j) = 'C5nALDOHoh + hv -> NII products'
      j = j+1
      jlabel(j) = 'C5nALDOHoh + hv -> cycl. product'


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
     &       ' n-C4H9CHO cross sections from Zhu 99.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' n-C4H9CHO cross sections from Tadic et al. 2001.'
       ELSE
        STOP "'mabs' not defined for n-C4H9CHO photolysis."
      ENDIF

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
        WRITE(kout,'(A)')
     &       ' n-C4H9CHO quantum yields from Zhu 99.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' n-C4H9CHO quantum yields from Calvert et al. 2011 book.'
       ELSEIF(myld.EQ.3) THEN
        WRITE(kout,'(A)')
     &       ' n-C4H9CHO quantum yields from Tadic et al. 2001.'
       ELSE
        STOP "'myld' not defined for n-C4H9CHO photolysis."
      ENDIF


      IF(mabs==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/n_pentanal_rad',
     $       STATUS='old')

        do i = 1, 3
          read(kin,*)
        enddo

        n = 23
        DO i = 1, n
          READ(kin,*) x1(i), y1(i), dum
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==2) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/Tadic.abs',
     $       STATUS='old')

        do i = 1, 5
          read(kin,*)
        enddo

        n = 121
        DO i = 1, n
          READ(kin,*) x1(i), dum, y1(i)
        ENDDO
        CLOSE(kin)
      ENDIF

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j-2)
        STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,ygoh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* quantum yields

      IF(myld==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/n_pentanal_rad',
     $       STATUS='old')

        do i = 1, 3
          read(kin,*)
        enddo

        n = 23
        DO i = 1, n
          READ(kin,*) x1(i), dum, y1(i)
        ENDDO
        CLOSE(kin)

       ELSEIF(myld==2) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/pentanal_calv.yld',
     $       STATUS='old')

        do i = 1, 4
          read(kin,*)
        enddo

        n = 66
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)
      ENDIF

      IF(myld<=2) THEN
        CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
        CALL addpnt(x1,y1,kdata,n,               0.,0.)
        CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
        CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
        CALL inter2(nw,wl,yg1,n,x1,y1,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-1)
          STOP
        ENDIF
      ENDIF

      qyoh = 0.75

* pressure dependency

      IF(myld<=2) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/valeraldehyde_C+Z98.yld',
     $       STATUS='old')

        do i = 1, 4
          read(kin,*)
        enddo

        n = 11
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

        CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
        CALL addpnt(x1,y1,kdata,n,               0.,0.)
        CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
        CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
        CALL inter2(nw,wl,yg2,n,x1,y1,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
        ENDIF
      ENDIF


* combine:

      DO iw = 1, nw - 1
        sig = yg(iw)
        sigoh = ygoh(iw)
        IF(myld<=2) THEN
          qy0 = yg1(iw)
          qy2 = 0.19
          qy3 = 0.00
          eta = MAX(0.,yg2(iw)/qy0-1.)
        ENDIF
        DO i = 1, nz
          IF(myld<=2) THEN
            qy1 = qy0*(1.+eta)/(1.+eta*airden(i)/2.465e19)
           ELSEIF(myld==3) THEN
            ptorr = 760.*airden(i)/2.55e19
            qy1 = 0.13/(2.44 + 7.771E-4*ptorr)
            qy2 = 0.52/(2.44 + 7.771E-4*ptorr)
            qy3 = 0.35/(2.44 + 7.771E-4*ptorr)
          ENDIF
          sq(j-7,i,iw) = sig * qy1
          sq(j-6,i,iw) = sig * qy2
          sq(j-5,i,iw) = sig * qy3
          sq(j-4,i,iw) = sigoh * qy1
          sq(j-3,i,iw) = sigoh * qy2
          IF(qy1+qy2+qy3 > 0.) THEN
            sq(j-2,i,iw) = sigoh * qyoh*qy1/(qy1+qy2+qy3)
            sq(j-1,i,iw) = sigoh * qyoh*qy2/(qy1+qy2+qy3)
            sq(j  ,i,iw) = sigoh * qyoh*qy3/(qy1+qy2+qy3)
           ELSE
            sq(j-2,i,iw) = 0.
            sq(j-1,i,iw) = 0.
            sq(j  ,i,iw) = 0.
          ENDIF
        ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma05(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! i-C4H9CHO

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for i-C4H9CHO      =*
*=  photolysis:                                                              =*
*=         i-C4H9CHO + hv -> Norish type I + II products                     =*
*=                                                                           =*
*=  Cross section:  see options below in the source code                     =*
*=  Quantum yield:  see options below in the source code                     =*
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

      REAL yg(kw), yg1(kw), yg2(kw), dum
      REAL qy1, qy2, qy0, eta
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs, myld

      j = j+1
      jlabel(j) = 'i-C4H9CHO -> C4H9 + CHO'
      j = j+1
      jlabel(j) = 'i-C4H9CHO -> CH3CH=CH2 + CH2=CHOH'


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
        WRITE(kout,'(2A)')
     &       ' i-C4H9CHO 0 pressure cross sections from Zhu et al. 99',
     &       ' extented to 390nm as given in GECKO-A database.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' i-C4H9CHO 0 pressure cross sections from Zhu et al. 99',
     &       ' extented to 340nm as given in Calvert et al. (2008).'
       ELSEIF(mabs.EQ.3) THEN
        WRITE(kout,'(2A)')
     &       ' i-C4H9CHO cross sections from Lanza et al. 2008',
     &       ' extented to 390nm.'
       ELSEIF(mabs.EQ.4) THEN
        WRITE(kout,'(2A)')
     &       ' i-C4H9CHO cross sections averaged from Lanza et al.',
     &       ' 2008 and Calvert et al. 2011 data extented to 390nm.'
       ELSE
        STOP "'mabs' not defined for i-C4H9CHO photolysis."
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
        WRITE(kout,'(2A)')
     &       ' i-C4H9CHO 0 pressure quantum yields from Zhu et al. 99',
     &       ' extented to 390nm as given in GECKO-A database.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' i-C4H9CHO quantum yields with estimated quenching',
     &       ' above 310nm according to data in Calvert et al. (2008).'
       ELSE
        STOP "'myld' not defined for i-C4H9CHO photolysis."
      ENDIF


      IF(mabs==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/i_pentanal_rad',
     $       STATUS='old')
        do i = 1, 2
          read(kin,*)
        enddo

        n = 23
        DO i = 1, n
          READ(kin,*) idum, y1(i), dum
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==2) THEN

        OPEN(UNIT=kin,
     $       FILE='DATAJ1/MCMext/ALD/isovaleraldehyde_calv.dat',
     $       STATUS='old')
        do i = 1, 8
          read(kin,*)
        enddo

        n = 61
        DO i = 1, n
          READ(kin,*) idum, y1(i), dum, dum
          x1(i) = FLOAT(idum)
          y1(i) = y1(i) * 1.E-20
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==3) THEN

        OPEN(UNIT=kin,
     $       FILE='DATAJ1/MCMext/ALD/isovaleraldehyde_Lan08ext.abs',
     $       STATUS='old')
        do i = 1, 4
          read(kin,*)
        enddo

        n = 88
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==4) THEN

        OPEN(UNIT=kin,
     $       FILE='DATAJ1/MCMext/ALD/isovaleraldehyde_avrgext.abs',
     $       STATUS='old')
        do i = 1, 9
          read(kin,*)
        enddo

        n = 63
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
          y1(i) = y1(i) * 1.E-20
        ENDDO
        CLOSE(kin)
      ENDIF

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j-2)
        STOP
      ENDIF


* quantum yields

      IF(myld==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/i_pentanal_rad',
     $       STATUS='old')
        do i = 1, 2
          read(kin,*)
        enddo

        n = 23
        DO i = 1, n
          READ(kin,*) idum, dum, y1(i)
          x1(i) = FLOAT(idum)
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

       ELSEIF(myld==2) THEN

! yg1: qy1 at 1 atm; yg2: qy1 at 0 atm
        OPEN(UNIT=kin,
     $       FILE='DATAJ1/MCMext/ALD/isovaleraldehyde_qu.dat',
     $       STATUS='old')
        do i = 1, 11
          read(kin,*)
        enddo

        n  = 61
        n1 = n
        n2 = n
        DO i = 1, n
          READ(kin,*) idum, dum, y2(i), y1(i)
          x1(i) = FLOAT(idum)
          x2(i) = x1(i)
        ENDDO
        CLOSE(kin)

        CALL addpnt(x1,y1,kdata,n1,x1(1)*(1.-deltax),0.)
        CALL addpnt(x1,y1,kdata,n1,               0.,0.)
        CALL addpnt(x1,y1,kdata,n1,x1(n1)*(1.+deltax),0.)
        CALL addpnt(x1,y1,kdata,n1,           1.e+38,0.)
        CALL inter2(nw,wl,yg1,n1,x1,y1,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-1)
          STOP
        ENDIF

        CALL addpnt(x2,y2,kdata,n2,x2(1)*(1.-deltax),0.)
        CALL addpnt(x2,y2,kdata,n2,               0.,0.)
        CALL addpnt(x2,y2,kdata,n2,x2(n2)*(1.+deltax),y2(n))
        CALL addpnt(x2,y2,kdata,n2,           1.e+38,y2(n))
        CALL inter2(nw,wl,yg2,n2,x2,y2,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-1)
          STOP
        ENDIF

      ENDIF

* set minor pressure-independent pathway
      qy2 = 0.13

* combine:

      DO iw = 1, nw - 1
         sig = yg(iw)
         IF(myld==1) THEN
           qy1 = yg1(iw)
          ELSEIF(myld==2) THEN
           qy0 = yg1(iw)
           IF(qy0>=pzero) THEN
             eta = MAX(0.,yg2(iw)/qy0-1.)
            ELSE
             eta = 0.
           ENDIF
         ENDIF
         DO i = 1, nz
           IF(myld==2) qy1 = qy0*(1.+eta)/(1.+eta*airden(i)/2.465e19)
           sq(j-1,i,iw) = sig * qy1
           sq(j  ,i,iw) = sig * qy2
         ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE ma06(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! sec-C4H9CHO

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for sec-C4H9CHO    =*
*=  photolysis:                                                              =*
*=         sec-C4H9CHO + hv -> Norish type I + II products                   =*
*=                                                                           =*
*=  Cross section:  estimated same as i-C4H9CHO                              =*
*=  Quantum yield:  Calvert et al. (2011) book                               =*
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
      REAL qy0, qy1, qy2
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs, myld

      j = j+1
      jlabel(j) = 'sec-C4H9CHO -> C4H9 + CHO'
      j = j+1
      jlabel(j) = 'sec-C4H9CHO -> CH3CH=CHOH + CH2=CH2'


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
        WRITE(kout,'(2A)')
     &       ' sec-C4H9CHO cross sections estimated same as i-C4H9CHO',
     &       ' from GECKO-A database.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(2A)')
     &  ' sec-C4H9CHO cross sections estimated same as i-C4H9CHO',
     &  ' with average from Lanza et al. 2008 / Calvert et al. (2008).'
       ELSE
        STOP "'mabs' not defined for sec-C4H9CHO photolysis."
      ENDIF

      IF(vers==1)THEN
        myld = 3
       ELSEIF(vers==2)THEN
        myld = 3
       ELSEIF(vers==0) THEN
        myld = 3
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(A)')
     &       ' sec-C4H9CHO quantum yields from Calvert et al. (2011).'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' sec-C4H9CHO quantum yields from Calvert et al. (2011)',
     &       ' with estimated quenching.'
       ELSEIF(myld.EQ.3) THEN
        WRITE(kout,'(2A)')
     &       ' sec-C4H9CHO quantum yields from Calvert et al. (2011)',
     &       ' with estimated quenching for wavelength greater 310nm.'
       ELSE
        STOP "'myld' not defined for sec-C4H9CHO photolysis."
      ENDIF

* Absorption cross sections
* estimated same as i-C4H9CHO

      IF(mabs==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/i_pentanal_rad',
     $       STATUS='old')
        do i = 1, 2
          read(kin,*)
        enddo

        n = 23
        DO i = 1, n
          READ(kin,*) idum, y1(i), dum
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==2) THEN

        OPEN(UNIT=kin,
     $       FILE='DATAJ1/MCMext/ALD/isovaleraldehyde_avrgext.abs',
     $       STATUS='old')
        do i = 1, 9
          read(kin,*)
        enddo

        n = 63
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
          y1(i) = y1(i) * 1.E-20
        ENDDO
        CLOSE(kin)
      ENDIF

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j-2)
        STOP
      ENDIF

* quantum yields
* from Calvert et al. (2011) book
* with possible option for estimation of pressure dependence

* zero pressure qy:
      qy0 = 0.55
      qy2 = 0.15

      IF(myld>=2) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/CH3CHO/CH3CHO_pdep_iup13.yld',
     $       STATUS='old')
        do i = 1, 7
          read(kin,*)
        enddo
        n = 18
        DO i = 1, n
          READ(kin,*) idum, dum, y1(i)
          x1(i) = FLOAT(idum)
          y1(i) = y1(i)*1.E-21
        ENDDO
        CLOSE (kin)

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
         DO i = 1, nz
           IF(myld==2 .OR. (myld==3 .AND. wc(iw)>=310.)) THEN
             qy1 = MAX(0.,MIN(1.,1./(1./qy0+yg1(iw)*airden(i))))
            ELSE
             qy1 = qy0
           ENDIF
           sq(j-1,i,iw) = sig * qy1
           sq(j  ,i,iw) = sig * qy2
         ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE ma07(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! t-C4H9CHO/tALD

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for t-C4H9CHO      =*
*=  photolysis:                                                              =*
*=         t-C4H9CHO + hv -> HCO. +  t-C4H9.                                 =*
*=  Also provides values for generalised t-aldehydes with possible OH-subst. =*
*=                                                                           =*
*=  Cross section:  see options below in the source code                     =*
*=  Quantum yield:  see options below in the source code                     =*
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
      REAL x1(kdata), x2(kdata), x1oh(kdata)
      REAL y1(kdata), y2(kdata), y1oh(kdata)

* local

      REAL yg(kw), yg1(kw), yg2(kw), ygoh(kw), dum
      REAL qy, qy0, qyg1, qyg2, qyoh, eta
      REAL sig, sigoh
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs, myld

      j = j+1
      jlabel(j) = 't-C4H9CHO -> C4H9 + CHO'
      j = j+1
      jlabel(j) = 'tALD -> NI products'
      j = j+1
      jlabel(j) = 'tALD -> NII products'
      j = j+1
      jlabel(j) = 'tALDOHqy -> NI products'
      j = j+1
      jlabel(j) = 'tALDOHqy -> NII products'
      j = j+1
      jlabel(j) = 'tALDOHoh -> NI products'
      j = j+1
      jlabel(j) = 'tALDOHoh -> NII products'


      IF(vers==1)THEN
        mabs = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
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
     &       ' t-C4H9CHO 0 pressure cross sections from Zhu et al. 99',
     &       ' extented to 390nm as given in GECKO-A database.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' t-C4H9CHO 0 pressure cross sections from Zhu et al. 99',
     &       ' extented to 335nm as given in Calvert et al. (2008).'
       ELSE
        STOP "'mabs' not defined for t-C4H9CHO photolysis."
      ENDIF

      IF(vers==1)THEN
        myld = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
       ELSEIF(vers==2)THEN
        myld = 4
       ELSEIF(vers==0) THEN
        myld = 4
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' t-C4H9CHO 0 pressure quantum yields from Zhu et al. 99',
     &       ' extented to 390nm as given in GECKO-A database.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' t-C4H9CHO 0 pressure quantum yields from Zhu et al. 99',
     &       ' extented to 340nm as given in Calvert et al. (2008).'
       ELSEIF(myld.EQ.3) THEN
        WRITE(kout,'(2A)')
     &       ' t-C4H9CHO quantum yields from Zhu et al. 99',
     &       ' with estimated quenching.'
       ELSEIF(myld.EQ.4) THEN
        WRITE(kout,'(2A)')
     &       ' t-C4H9CHO quantum yields from Zhu et al. 99',
     &       ' with estimated quenching above 310nm.'
       ELSE
        STOP "'myld' not defined for t-C4H9CHO photolysis."
      ENDIF


      IF(mabs==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/t_pentanal_rad',
     $       STATUS='old')
        do i = 1, 3
          read(kin,*)
        enddo

        n = 23
        DO i = 1, n
          READ(kin,*) idum, y1(i), dum
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==2) THEN

        OPEN(UNIT=kin,
     $       FILE='DATAJ1/MCMext/ALD/pivaldehyde_calv.dat',
     $       STATUS='old')
        do i = 1, 8
          read(kin,*)
        enddo

        n = 61
        DO i = 1, n
          READ(kin,*) idum, y1(i), dum, dum
          x1(i) = FLOAT(idum)
          y1(i) = y1(i) * 1.E-20
        ENDDO
        CLOSE(kin)
      ENDIF

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j-2)
        STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,ygoh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* quantum yields

      IF(myld==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/t_pentanal_rad',
     $       STATUS='old')
        do i = 1, 3
          read(kin,*)
        enddo

        n = 23
        DO i = 1, n
          READ(kin,*) idum, dum, y1(i)
          x1(i) = FLOAT(idum)
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

       ELSE

        OPEN(UNIT=kin,
     $       FILE='DATAJ1/MCMext/ALD/pivaldehyde_calv.dat',
     $       STATUS='old')
        do i = 1, 8
          read(kin,*)
        enddo

        n = 61
        n1 = n
        n2 = n
        DO i = 1, n
          READ(kin,*) idum, dum, y2(i), y1(i)
          x1(i) = FLOAT(idum)
          x2(i) = x1(i)
        ENDDO
        CLOSE(kin)

        CALL addpnt(x1,y1,kdata,n1,x1(1)*(1.-deltax),0.)
        CALL addpnt(x1,y1,kdata,n1,               0.,0.)
        CALL addpnt(x1,y1,kdata,n1,x1(n1)*(1.+deltax),0.)
        CALL addpnt(x1,y1,kdata,n1,           1.e+38,0.)
        CALL inter2(nw,wl,yg1,n1,x1,y1,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
        ENDIF

        CALL addpnt(x2,y2,kdata,n2,x2(1)*(1.-deltax),0.)
        CALL addpnt(x2,y2,kdata,n2,               0.,0.)
        CALL addpnt(x2,y2,kdata,n2,x2(n2)*(1.+deltax),0.)
        CALL addpnt(x2,y2,kdata,n2,           1.e+38,0.)
        CALL inter2(nw,wl,yg2,n2,x2,y2,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
        ENDIF

      ENDIF

      qyoh = 0.75
      qyg1 = 0.45
      qyg2 = 0.13

* combine:

      DO iw = 1, nw - 1
        sig = yg(iw)
        sigoh = ygoh(iw)
        IF(myld==1) THEN
          qy = yg1(iw)
         ELSEIF(myld==2) THEN
          qy = yg2(iw)
         ELSEIF(myld>=3) THEN
          qy0 = yg1(iw)
          IF(qy0>=pzero) THEN
            eta = MAX(0.,yg2(iw)/qy0-1.)
           ELSE
            eta = 0.
          ENDIF
        ENDIF
        DO i = 1, nz
          IF(myld==3 .OR. (myld==4 .AND. wc(iw)>=310.)) THEN
            qy = qy0*(1.+eta)/(1.+eta*airden(i)/2.465e19)
          ENDIF
          sq(j-6,i,iw) = sig * qy
          sq(j-5,i,iw) = sig * qyg1
          sq(j-4,i,iw) = sig * qyg2
          sq(j-3,i,iw) = sigoh * qyg1
          sq(j-2,i,iw) = sigoh * qyg2
          IF(qyg1+qyg2 > 0.) THEN
            sq(j-1,i,iw) = sigoh * qyoh*qyg1/(qyg1+qyg2)
            sq(j  ,i,iw) = sigoh * qyoh*qyg2/(qyg1+qyg2)
           ELSE
            sq(j-1,i,iw) = 0.
            sq(j  ,i,iw) = 0.
          ENDIF
        ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE ma08(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! n-C5H11CHO

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for n-C5H11CHO     =*
*=  photolysis:                                                              =*
*=         n-C5H11CHO + hv -> Norish type I + II products                    =*
*=                                                                           =*
*=  Cross section:  see options below in the source code                     =*
*=  Quantum yield:  see options below in the source code                     =*
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

      INTEGER i, n, n1
      REAL x1(kdata), x1oh(kdata)
      REAL y1(kdata), y1oh(kdata)

* local

      REAL yg(kw), yg1(kw), yg2(kw), ygoh(kw), dum
      REAL qy1, qy2, qy3, qy0, eta, ptorr, qyoh
      REAL sig, sigoh
      INTEGER ierr, idum
      INTEGER iw

      INTEGER mabs, myld

      j = j+1
      jlabel(j) = 'n-C5H11CHO + hv -> C5H11 +  CHO'
      j = j+1
      jlabel(j) = 'n-C5H11CHO + hv -> C2H5CH=CH2 +  CH2=CHOH'
      j = j+1
      jlabel(j) = 'n-C5H11CHO + hv -> 2-ethylcyclobutanol'

      j = j+1
      jlabel(j) = 'C6nALDOHqy + hv -> NI products'
      j = j+1
      jlabel(j) = 'C6nALDOHqy + hv -> NII products'
! 3rd cyclisation channel for OH-subst. C6 n-aldehydes will be estimated with
! scaled value from the corresponding C8 compound

      j = j+1
      jlabel(j) = 'C6nALDOHoh + hv -> NI products'
      j = j+1
      jlabel(j) = 'C6nALDOHoh + hv -> NII products'
      j = j+1
      jlabel(j) = 'C6nALDOHoh + hv -> cycl. product'


      IF(vers==1)THEN
        mabs = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
       ELSEIF(vers==2)THEN
        mabs = 1
       ELSEIF(vers==0) THEN
        mabs = 1
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(mabs.EQ.1) THEN
        WRITE(kout,'(A)')
     &       ' n-C5H11CHO cross sections from Plagens et al. 1998.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &       " n-C5H11CHO cross sections from O'Connor et al. 2006."
       ELSEIF(mabs.EQ.3) THEN
        WRITE(kout,'(A)')
     &       " n-C5H11CHO cross sections from Jimenez et al. 2007."
       ELSE
        STOP "'mabs' not defined for n-C5H11CHO photolysis."
      ENDIF

      IF(vers==1)THEN
        myld = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
       ELSEIF(vers==2)THEN
        myld = 3
       ELSEIF(vers==0) THEN
        myld = 3
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(A)')
     &       ' n-C5H11CHO quantum yields from GECKO-A database.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' n-C5H11CHO quantum yields from Calvert book.'
       ELSEIF(myld.EQ.3) THEN
        WRITE(kout,'(A)')
     &       ' n-C5H11CHO quantum yields from Tadic et al. 2001.'
       ELSE
        STOP "'myld' not defined for n-C5H11CHO photolysis."
      ENDIF


      IF(mabs==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/hexanal_rad',
     $       STATUS='old')
        do i = 1, 2
          read(kin,*)
        enddo

        n = 89
        DO i = 1, n
          READ(kin,*) x1(i), y1(i), dum
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==2) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/nHexanal_OCon06.abs',
     $       STATUS='old')

        do i = 1, 5
          read(kin,*)
        enddo

        n = 64
        DO i = 1, n
          READ(kin,*) x1(i), y1(i)
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==3) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/nHexanal_Jim07.abs',
     $       STATUS='old')

        do i = 1, 5
          read(kin,*)
        enddo

        n = 73
        DO i = 1, n
          READ(kin,*) x1(i), y1(i), dum
        ENDDO
        CLOSE(kin)
      ENDIF

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,ygoh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* quantum yields


      IF(myld==2) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/nHexanal_calv11.yld',
     $       STATUS='old')

        do i = 1, 5
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
        CALL inter2(nw,wl,yg1,n,x1,y1,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
        ENDIF
      ENDIF

      qyoh = 0.75


* pressure dependency

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/hexanal_T+Z04.yld',
     $     STATUS='old')

      do i = 1, 4
        read(kin,*)
      enddo

      n = 11
      DO i = 1, n
        READ(kin,*) idum, y1(i)
        x1(i) = FLOAT(idum)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg2,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* combine:

      DO iw = 1, nw - 1
        sig = yg(iw)
        sigoh = ygoh(iw)
        IF(myld==1) THEN
          qy0 = 0.075
          qy2 = 0.175
          qy3 = 0.
         ELSEIF(myld==2) THEN
          qy0 = yg1(iw)
          qy2 = 0.29
          qy3 = 0.
        ENDIF
        IF(myld<=2) eta = MAX(0.,yg2(iw)/qy0-1.)
        DO i = 1, nz
          IF(myld<=2) THEN
            qy1 = qy0*(1.+eta)/(1.+eta*airden(i)/2.465e19)
           ELSEIF(myld==3) THEN
            ptorr = 760.*airden(i)/2.55e19
            qy1 = 0.21/(2.26 + 4.758E-4*ptorr)
            qy2 = 0.61/(2.26 + 4.758E-4*ptorr)
            qy3 = 0.18/(2.26 + 4.758E-4*ptorr)
          ENDIF
          sq(j-7,i,iw) = sig * qy1
          sq(j-6,i,iw) = sig * qy2
          sq(j-5,i,iw) = sig * qy3
          sq(j-4,i,iw) = sigoh * qy1
          sq(j-3,i,iw) = sigoh * qy2
          sq(j-2,i,iw) = sigoh * qy3
          IF(qy1+qy2+qy3 > 0.) THEN
            sq(j-1,i,iw) = sigoh * qyoh*qy1/(qy1+qy2+qy3)
            sq(j  ,i,iw) = sigoh * qyoh*qy2/(qy1+qy2+qy3)
           ELSE
            sq(j-1,i,iw) = 0.
            sq(j  ,i,iw) = 0.
          ENDIF
        ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma09(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! n-C6H13CHO

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for n-C6H13CHO     =*
*=  photolysis:                                                              =*
*=         n-C6H13CHO + hv -> Norish type I + II products                    =*
*=                                                                           =*
*=  Cross section:  see options below in the source code                     =*
*=  Quantum yield:  see options below in the source code                     =*
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

      INTEGER i, n, n1
      REAL x1(kdata), x1oh(kdata)
      REAL y1(kdata), y1oh(kdata)

* local

      REAL yg(kw), yg1(kw), yg2(kw), ygoh(kw)
      REAL qy1, qy2, qy3, qy0, eta, ptorr, qyoh
      REAL sig, sigoh
      INTEGER ierr, idum
      INTEGER iw

      INTEGER myld

      j = j+1
      jlabel(j) = 'n-C6H13CHO + hv -> C6H13 + CHO'
      j = j+1
      jlabel(j) = 'n-C6H13CHO + hv -> C3H7CH=CH2 + CH2=CHOH'
      j = j+1
      jlabel(j) = 'n-C6H13CHO + hv -> 2-propylcyclobutanol'

      j = j+1
      jlabel(j) = 'C7nALDOHqy + hv -> NI products'
      j = j+1
      jlabel(j) = 'C7nALDOHqy + hv -> NII products'
! 3rd cyclisation channel for OH-subst. C7 n-aldehydes will be estimated with
! scaled value from the corresponding C8 compound

      j = j+1
      jlabel(j) = 'C7nALDOHoh + hv -> NI products'
      j = j+1
      jlabel(j) = 'C7nALDOHoh + hv -> NII products'
      j = j+1
      jlabel(j) = 'C7nALDOHoh + hv -> cycl. product'

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
        WRITE(kout,'(A)')
     &       ' n-C6H13CHO quantum yields from Calvert book.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' n-C6H13CHO quantum yields from Tadic et al. 2001.'
       ELSE
        STOP "'myld' not defined for n-C6H13CHO photolysis."
      ENDIF


      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/nHeptanal.abs',
     $     STATUS='old')

      do i = 1, 5
        read(kin,*)
      enddo

      n = 11
      DO i = 1, n
        READ(kin,*) x1(i), y1(i)
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-1)
          STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,ygoh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* quantum yields
      IF(myld==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/nHeptanal_calv.yld',
     $       STATUS='old')

        do i = 1, 7
          read(kin,*)
        enddo

        n = 71
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

        CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
        CALL addpnt(x1,y1,kdata,n,               0.,0.)
        CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
        CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
        CALL inter2(nw,wl,yg1,n,x1,y1,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-2)
          STOP
        ENDIF


* pressure dependency

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/heptanal_T+Z04.yld',
     $       STATUS='old')

        do i = 1, 4
          read(kin,*)
        enddo

        n = 11
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

        CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
        CALL addpnt(x1,y1,kdata,n,               0.,0.)
        CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
        CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
        CALL inter2(nw,wl,yg2,n,x1,y1,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-2)
          STOP
        ENDIF
      ENDIF

      qyoh = 0.75


* combine:

      DO iw = 1, nw - 1
        sig = yg(iw)
        sigoh = ygoh(iw)
        IF(myld==1) THEN
          qy0 = yg1(iw)
          qy2 = 0.12
          qy3 = 0.00
          eta = MAX(0.,yg2(iw)/qy0-1.)
        ENDIF
        DO i = 1, nz
          IF(myld==1) THEN
            qy1 = qy0*(1.+eta)/(1.+eta*airden(i)/2.465e19)
           ELSEIF(myld==2) THEN
            ptorr = 760.*airden(i)/2.55e19
            qy1 = 0.10/(2.408 + 1.169E-3*ptorr)
            qy2 = 0.38/(2.408 + 1.169E-3*ptorr)
            qy3 = 0.52/(2.408 + 1.169E-3*ptorr)
          ENDIF
          sq(j-7,i,iw) = sig * qy1
          sq(j-6,i,iw) = sig * qy2
          sq(j-5,i,iw) = sig * qy3
          sq(j-4,i,iw) = sigoh * qy1
          sq(j-3,i,iw) = sigoh * qy2
          sq(j-2,i,iw) = sigoh * qy3
          IF(qy1+qy2+qy3 > 0.) THEN
            sq(j-1,i,iw) = sigoh * qyoh*qy1/(qy1+qy2+qy3)
            sq(j  ,i,iw) = sigoh * qyoh*qy2/(qy1+qy2+qy3)
           ELSE
            sq(j-1,i,iw) = 0.
            sq(j  ,i,iw) = 0.
          ENDIF
        ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma10(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! Glycidaldehyde

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for glycidaldehyde =*
*=  photolysis:                                                              =*
*=         Glycidaldehyde + hv ->  products                                  =*
*=                                                                           =*
*=  Cross section and quantum yield:  taken from Calvert et al. 2011         =*
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

* Ratio for both channels estimated from ratio of channel I + II
* from glycolaldehyde photolysis with overall quantum yield = 0.6
* (see Calvert et al. 2011 for total qy)
      j = j+1
      jlabel(j) = 'Glycidaldehyde + hv -> oxyranyl radical + CHO'
      j = j+1
      jlabel(j) = 'Glycidaldehyde + hv -> oxyrane + CO'


      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/Glycidaldehyde.abs',
     $     STATUS='old')

      do i = 1, 5
        read(kin,*)
      enddo

      n = 84
      DO i = 1, n
        READ(kin,*) idum, y1(i)
        x1(i) = FLOAT(idum)
        y1(i) = y1(i)*1.e-20
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


      DO iw = 1, nw - 1
        sig = yg(iw)
        qy1 = 0.6*0.89
        qy2 = 0.6*0.11
        DO i = 1, nz
          sq(j-1,i,iw) = sig * qy1
          sq(j  ,i,iw) = sig * qy2
        ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma11(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! CH3CH=CHCHO

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide product (cross section) x (quantum yield) for CH3CH=CHCHO        =*
*=  (crotonaldehyde) photolysis:                                             =*
*=       CH3CH=CHCHO + hv -> Products                                        =*
*=                                                                           =*
*=  Cross section: from Magneron et al.                                      =*
*=  Quantum yield: estimated 10 times that of acrolein                       =*
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
      PARAMETER(kdata=4500)

      INTEGER iw
      INTEGER i, n
      REAL x1(kdata)
      REAL y1(kdata)

* local

      REAL yg1(kw), yg2(kw)
      real qy, qym1, qy1, qy2, qy3
      REAL sig
      INTEGER ierr, idum

      INTEGER mabs, myld

**************** crotonaldehyde photodissociation

      j = j+1
      jlabel(j) = 'CH3CH=CHCHO -> CH3CH=CH + CHO'
      j = j+1
      jlabel(j) = 'CH3CH=CHCHO -> CH3CH=CH2 + CO'
      j = j+1
      jlabel(j) = 'CH3CH=CHCHO -> CH3CH=CHCO + H'

* cross section from
* UV-C: Lee et al. 2007
* UV/VIS:
* 1: published low res data by Magneron et al. 2002
* 2: unpublished high res data by Magneron et al. 1999

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
        WRITE(kout,'(A)')
     &  ' Crotonaldehyde cross section from published low res. data.'
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &  ' Crotonaldehyde cross section from unpublished high res. data.'
       ELSE
        STOP "'mabs' not defined for crotonaldehyde photolysis."
      ENDIF

* quantum yields estimated 10x acrolein
* Criegee channel replaced by CH3 fission
* 1: from JPL 2006
* 2: from Calvert et al. 2011

      IF(vers==1)THEN
        myld = 1
       ELSEIF(vers==2)THEN
        myld = 1
       ELSEIF(vers==0) THEN
        myld = 2
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' Crotonaldehyde quantum yields',
     &       ' estimated 10x acrolein with JPL data.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' Crotonaldehyde quantum yields',
     &       ' estimated 10x acrolein with Calvert et al. data.'
       ELSE
        STOP "'myld' not defined for crotonaldehyde photolysis."
      ENDIF


      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/crotonaldehyde_Lee07.abs',
     &     STATUS='OLD')
      DO i = 1, 6
        READ(kin,*)
      ENDDO
      n = 4368
      DO i = 1, n
        READ(kin,*) x1(i), y1(i)
      ENDDO
      CLOSE(kin)

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg1,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-1)
          STOP
      ENDIF


      IF(mabs==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/crotonaldehyde_Mag02.abs',
     &       STATUS='OLD')
        DO i = 1, 6
          READ(kin,*)
        ENDDO
        n = 68
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==2) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/crotonaldehyde_Mag99.abs',
     &       STATUS='OLD')
        DO i = 1, 6
          READ(kin,*)
        ENDDO
        n = 3202
        DO i = 1, n
          READ(kin,*) x1(i), y1(i)
        ENDDO
        CLOSE(kin)
      ENDIF

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg2,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-1)
          STOP
      ENDIF

* combine xs with qy:

      DO iw = 1, nw-1

* cross sections: combine UV-C and UV/VIS-data:
           IF(mabs==1) THEN
              IF(wc(iw)<=250.) THEN
                sig = max(0.,yg1(iw))
               ELSE
                sig = max(0.,yg2(iw))
              ENDIF
            ELSEIF(mabs==2) THEN
              IF(wc(iw)<=225.) THEN
                sig = max(0.,yg1(iw))
               ELSE
                sig = max(0.,yg2(iw))
              ENDIF
           ENDIF

        DO i = 1, nz

           if(airden(i) .gt. 2.6e19) then
              qy = 0.004
           elseif(airden(i) .gt. 8.e17 .and. airden(i) .lt. 2.6e19) then
             if(myld==1) then
               qym1 = 0.086 + 1.613e-17 * airden(i)
               qy = 0.004 + 1./qym1
              elseif(myld==2) then
               qym1 = -0.836+1.159e-17*airden(i)-2.166e-37*airden(i)**2
               qy = 1./qym1
             endif
           elseif(airden(i) .lt. 8.e17) then
             if(myld==1) then
              qym1 = 0.086 + 1.613e-17 * 8.e17
              qy = 0.004 + 1./qym1
              elseif(myld==2) then
               qym1 = -0.836+1.159e-17*8.e17-2.166e-37*8.e17**2
               qy = 1./qym1
             endif
           endif
* product distribution estimated from Calvert et al. 2011:
           qy  = MIN(10. * qy,1.) ! qy estimated 10 times higher than acrolein
           qy1 = qy*(-0.0173*(airden(i)/1.E19)**2
     &               +0.083*airden(i)/1.E19+0.0492)
           qy2 = qy*(0.0407*(airden(i)/1.E19)**2
     &               -0.1661*airden(i)/1.E19+0.8485)
           qy3 = qy*(-0.0217*(airden(i)/1.E19)**2
     &               +0.0788*airden(i)/1.E19+0.1029)
           sq(j-2,i,iw) = sig * qy1
           sq(j-1,i,iw) = sig * qy2
           sq(j  ,i,iw) = sig * qy3
        ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma12(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! 2-hexenal

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide product (cross section) x (quantum yield) for 2-hexeanal         =*
*=  photolysis:                                                              =*
*=       2-hexenal + hv -> Products                                          =*
*=                                                                           =*
*=  Cross section: see options below                                         =*
*=  Quantum yield: scaled to give j(total) ~ 3e-5 s-1                        =*
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
      PARAMETER(kdata=120)

      INTEGER iw
      INTEGER i, n
      REAL x1(kdata)
      REAL y1(kdata)

* local

      REAL yg(kw)
      real qy, qym1, qy1, qy2, qy3
      REAL sig
      INTEGER ierr, idum

      INTEGER mabs, myld

**************** 2-hexenal photodissociation

      j = j+1
      jlabel(j) = '2-hexenal -> 1-pentenyl radical + CHO'
      j = j+1
      jlabel(j) = '2-hexenal -> 1-pentene + CO'
      j = j+1
      jlabel(j) = '2-hexenal -> C3H7CH=CHCO + H'

* cross section from
* 1: O'Connor et al. 2006
* 2: Jiminez et al. 2007

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
        WRITE(kout,'(A)')
     &  " 2-hexenal cross section from O'Connor et al. 2006."
       ELSEIF(mabs.EQ.2) THEN
        WRITE(kout,'(A)')
     &  ' 2-hexenal cross section from Jiminez et al. 2007.'
       ELSE
        STOP "'mabs' not defined for 2-hexenal photolysis."
      ENDIF

* quantum yields estimated to give j~3e-5 s-1 on March 17
* Criegee channel replaced by R fission
* 1: from JPL 2006
* 2: from Calvert et al. 2011

      IF(vers==1)THEN
        myld = 1
       ELSEIF(vers==2)THEN
        myld = 1
       ELSEIF(vers==0) THEN
        myld = 2
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' 2-hexenal quantum yields',
     &       ' estimated with acrolein JPL data.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' 2-hexenal quantum yields',
     &       ' estimated with acrolein Calvert et al. data.'
       ELSE
        STOP "'myld' not defined for 2-hexenal photolysis."
      ENDIF

* cross sections
      IF(mabs==1) THEN
        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/hexenal_OCon06.abs',
     &       STATUS='OLD')
        DO i = 1, 6
          READ(kin,*)
        ENDDO

        n = 111
        DO i = 1, n
          READ(kin,*) idum, y1(i)
          x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

       ELSEIF(mabs==2) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/hexenal_Jim07.abs',
     &       STATUS='OLD')
        DO i = 1, 6
          READ(kin,*)
        ENDDO

        n = 81
        DO i = 1, n
          READ(kin,*) idum, y1(i)
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

* combine xs with qy:

      DO iw = 1, nw-1

        sig = yg(iw)

        DO i = 1, nz

           if(airden(i) .gt. 2.6e19) then
              qy = 0.004
           elseif(airden(i) .gt. 8.e17 .and. airden(i) .lt. 2.6e19) then
             if(myld==1) then
               qym1 = 0.086 + 1.613e-17 * airden(i)
               qy = 0.004 + 1./qym1
              elseif(myld==2) then
               qym1 = -0.836+1.159e-17*airden(i)-2.166e-37*airden(i)**2
               qy = 1./qym1
             endif
           elseif(airden(i) .lt. 8.e17) then
             if(myld==1) then
              qym1 = 0.086 + 1.613e-17 * 8.e17
              qy = 0.004 + 1./qym1
              elseif(myld==2) then
               qym1 = -0.836+1.159e-17*8.e17-2.166e-37*8.e17**2
               qy = 1./qym1
             endif
           endif
* product distribution estimated from Calvert et al. 2011:
           qy = MIN(12. * qy,1.) ! qy estimated 12 times higher than acrolein
           qy1 = qy*(-0.0173*(airden(i)/1.E19)**2
     &               +0.083*airden(i)/1.E19+0.0492)
           qy2 = qy*(0.0407*(airden(i)/1.E19)**2
     &               -0.1661*airden(i)/1.E19+0.8485)
           qy3 = qy*(-0.0217*(airden(i)/1.E19)**2
     &               +0.0788*airden(i)/1.E19+0.1029)
           sq(j-2,i,iw) = sig * qy1
           sq(j-1,i,iw) = sig * qy2
           sq(j  ,i,iw) = sig * qy3
        ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma13(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! caronaldehyde

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide product (cross section)x(quantum yield) for                      =*
*=  caronaldehyde photolysis                                                 =*
*=          caronaldehyde + hv -> R + CO + HO2                               =*
*=                                                                           =*
*=  Cross section from Hallquist et al. 1997                                 =*
*=  Quantum yield estimated same as pinonaldehyde                            =*
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

      INTEGER myld


      j = j+1
      jlabel(j) = 'caronaldehyde -> R + CO + HO2'

* qy same as pinonaldehyde:
* 1: EUPHORE chamber experiments (RADICAL 2002)
* 2: Jaoui and Kamens 2003
* 3: approximate average

      IF(vers==1)THEN
        myld = 1
       ELSEIF(vers==2)THEN
        myld = 1
       ELSEIF(vers==0) THEN
        myld = 3
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' Caronaldehyde quantum yields',
     &       ' from pinonaldehyde EUPHORE chamber experiments.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' Caronaldehyde quantum yields same as pinonaldehyde',
     &       ' from Jaoui and Kamens 2003.'
       ELSEIF(myld.EQ.3) THEN
        WRITE(kout,'(2A)')
     &       ' Caronaldehyde quantum yields',
     &       ' as approximate average of opt. 1 and 2.'
       ELSE
        STOP "'myld' not defined for caronaldehyde photolysis."
      ENDIF


      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/DICAR/caronaldehyde.abs',
     $     STATUS='old')
      do i = 1, 6
         read(kin,*)
      enddo

      n = 11
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
          WRITE(*,*) ierr, jlabel(j-1)
          STOP
      ENDIF


* quantum yields
      IF(myld == 1) THEN
        qy = 0.14
       ELSEIF(myld == 2) THEN
        qy = 0.4
       ELSEIF(myld == 3) THEN
        qy = 0.25
      ENDIF


* combine:

      DO iw = 1, nw - 1
         sig = yg(iw)
         DO i = 1, nz
            sq(j,i,iw) = sig * qy
         ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma14(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! C4H9CH(C2H5)CHO / alkyl-subst. ald.

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide the product (cross section) x (quantum yield) for                =*
*=  2-ethyl hexanal photolysis:                                              =*
*=         C4H9CH(C2H5)CHO + hv -> products                                  =*
*=                                                                           =*
*=  Cross section:  Fraire et al. (2011)                                     =*
*=  Quantum yield:  Fraire et al. (2011) @254nm                              =*
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

      INTEGER i, n, n1
      REAL x1(kdata), x1oh(kdata)
      REAL y1(kdata), y1oh(kdata)

* local

      REAL yg(kw), ygoh(kw), dum
      real qy1, qy2, qyg1, qyg2, qyoh
      REAL sig, sigoh
      INTEGER ierr, idum
      INTEGER iw

      j = j+1
      jlabel(j) = 'C4H9CH(C2H5)CHO -> C7H15 + CHO'
      j = j+1
      jlabel(j) = 'C4H9CH(C2H5)CHO -> C7H16 + CO'

      j = j+1
      jlabel(j) = 'AlkALD -> NI products'
      j = j+1
      jlabel(j) = 'AlkALD -> NII products'

      j = j+1
      jlabel(j) = 'AlkALDOHqy -> NI products'
      j = j+1
      jlabel(j) = 'AlkALDOHqy -> NII products'

      j = j+1
      jlabel(j) = 'AlkALDOHoh -> NI products'
      j = j+1
      jlabel(j) = 'AlkALDOHoh -> NII products'


* Absorption cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/2EthylHexanal.abs',
     $     STATUS='old')
      do i = 1, 5
        read(kin,*)
      enddo

      n = 33
      DO i = 1, n
        READ(kin,*) idum, y1(i), dum
        x1(i) = FLOAT(idum)
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
         WRITE(*,*) ierr, jlabel(j)
         STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,ygoh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF

* quantum yields
* measurements at 254nm extended to all other wavelength
* branching of qy1/qy2 of 0.8:0.2 assumed (total qy = 0.51)

* zero pressure qy:
      qy1  = 0.51*0.8
      qy2  = 0.51*0.2
      qyg1 = 0.45
      qyg2 = 0.13
      qyoh = 0.75


* combine:

      DO iw = 1, nw - 1
         sig = yg(iw)
         sigoh = ygoh(iw)
         DO i = 1, nz
           sq(j-7,i,iw) = sig * qy1
           sq(j-6,i,iw) = sig * qy2
           sq(j-5,i,iw) = sig * qyg1
           sq(j-4,i,iw) = sig * qyg2
           sq(j-3,i,iw) = sigoh * qyg1
           sq(j-2,i,iw) = sigoh * qyg2
           IF(qy1+qy2 > 0.) THEN
             sq(j-1,i,iw) = sigoh * qyoh*qyg1/(qyg1+qyg2)
             sq(j  ,i,iw) = sigoh * qyoh*qyg2/(qyg1+qyg2)
            ELSE
             sq(j-1,i,iw) = 0.
             sq(j  ,i,iw) = 0.
           ENDIF
         ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE ma15(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! CH3CH=C(CH3)CHO

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide product (cross section) x (quantum yield) for CH3CH=C(CH3)CHO    =*
*=  photolysis:                                                              =*
*=       CH3CH=C(CH3)CHO + hv -> Products                                    =*
*=                                                                           =*
*=  Cross section: Lanza et al. (2008)                                       =*
*=  Quantum yield: estimated 10 times that of acrolein                       =*
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
      PARAMETER(kdata=100)

      INTEGER iw
      INTEGER i, n, n1
      REAL x1(kdata), x1oh(kdata)
      REAL y1(kdata), y1oh(kdata)

* local

      REAL yg1(kw), ygoh(kw)
      real qy, qym1, qy1, qy2, qy3, qyoh
      REAL sig, sigoh
      INTEGER ierr, idum

      INTEGER myld

**************** 2-methyl crotonaldehyde photodissociation

      j = j+1
      jlabel(j) = 'CH3CH=C(CH3)CHO -> CH3CH=CCH3 + CHO'
      j = j+1
      jlabel(j) = 'CH3CH=C(CH3)CHO -> CH3CH=CHCH3 + CO'
      j = j+1
      jlabel(j) = 'CH3CH=C(CH3)CHO -> CH3CH=C(CH3)CO + H'

      j = j+1
      jlabel(j) = 'aMeC4uALDOHqy -> NI products'
      j = j+1
      jlabel(j) = 'aMeC4uALDOHqy -> alkene + CO'
      j = j+1
      jlabel(j) = 'aMeC4uALDOHqy -> acyl + H'

      j = j+1
      jlabel(j) = 'aMeC4uALDOHoh -> NI products'
      j = j+1
      jlabel(j) = 'aMeC4uALDOHoh -> alkene + CO'
      j = j+1
      jlabel(j) = 'aMeC4uALDOHoh -> acyl + H'


* quantum yields estimated 10x acrolein
* Criegee channel replaced by CH3 fission
* 1: acrolein from JPL 2006
* 2: acrolein from Calvert et al. 2011

      IF(vers==1)THEN
        myld = 1
       ELSEIF(vers==2)THEN
        myld = 1
       ELSEIF(vers==0) THEN
        myld = 2
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' 2-Me-crotonaldehyde quantum yields',
     &       ' estimated with acrolein JPL data.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' 2-Me-crotonaldehyde quantum yields',
     &       ' estimated with acrolein Calvert et al. data.'
       ELSE
        STOP "'myld' not defined for 2-Me-crotonaldehyde photolysis."
      ENDIF


* cross section

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/2Me2butenal.abs',
     &     STATUS='OLD')
      DO i = 1, 4
        READ(kin,*)
      ENDDO
      n = 84
      DO i = 1, n
        READ(kin,*) idum, y1(i)
        x1(i) = float(idum)
        y1(i) = y1(i)*1.E-20
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg1,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
         WRITE(*,*) ierr, jlabel(j)
         STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,ygoh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* combine xs with qy:

      qyoh = 0.75

      DO iw = 1, nw-1
        sig = yg1(iw)
        sigoh = ygoh(iw)
        DO i = 1, nz

           if(airden(i) .gt. 2.6e19) then
              qy = 0.004
           elseif(airden(i) .gt. 8.e17 .and. airden(i) .lt. 2.6e19) then
             if(myld==1) then
               qym1 = 0.086 + 1.613e-17 * airden(i)
               qy = 0.004 + 1./qym1
              elseif(myld==2) then
               qym1 = -0.836+1.159e-17*airden(i)-2.166e-37*airden(i)**2
               qy = 1./qym1
             endif
           elseif(airden(i) .lt. 8.e17) then
             if(myld==1) then
              qym1 = 0.086 + 1.613e-17 * 8.e17
              qy = 0.004 + 1./qym1
              elseif(myld==2) then
               qym1 = -0.836+1.159e-17*8.e17-2.166e-37*8.e17**2
               qy = 1./qym1
             endif
           endif
* product distribution as estimated 10 x acrolein from Calvert et al. 2011:
* fits of direct qy given behind do not match 0.0065 at 1 atm
           qy = MIN(10. * qy,1.)
           qy1 = qy*(-0.0173*(airden(i)/1.E19)**2
     &              +0.083*airden(i)/1.E19+0.0492)
           qy2 = qy*(0.0407*(airden(i)/1.E19)**2
     &              -0.1661*airden(i)/1.E19+0.8485)
           qy3 = qy*(-0.0217*(airden(i)/1.E19)**2
     &              +0.0788*airden(i)/1.E19+0.1029)
           sq(j-8,i,iw) = sig * qy1
           sq(j-7,i,iw) = sig * qy2
           sq(j-6,i,iw) = sig * qy3
           sq(j-5,i,iw) = sigoh * qy1
           sq(j-4,i,iw) = sigoh * qy2
           sq(j-3,i,iw) = sigoh * qy3
           IF(qy1+qy2+qy3 > 0.) THEN
             sq(j-2,i,iw) = sigoh * qyoh*qy1/(qy1+qy2+qy3)
             sq(j-1,i,iw) = sigoh * qyoh*qy2/(qy1+qy2+qy3)
             sq(j  ,i,iw) = sigoh * qyoh*qy3/(qy1+qy2+qy3)
            ELSE
             sq(j-2,i,iw) = 0.
             sq(j-1,i,iw) = 0.
             sq(j  ,i,iw) = 0.
           ENDIF
        ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma16(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! CH3C(CH3)=CHCHO

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide product (cross section) x (quantum yield) for CH3C(CH3)=CHCHO    =*
*=  photolysis:                                                              =*
*=       CH3C(CH3)=CHCHO + hv -> Products                                    =*
*=                                                                           =*
*=  Cross section: Lanza et al. (2008)                                       =*
*=  Quantum yield: estimated 10 times that of acrolein                       =*
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
      PARAMETER(kdata=100)

      INTEGER iw
      INTEGER i, n, n1
      REAL x1(kdata), x1oh(kdata)
      REAL y1(kdata), y1oh(kdata)

* local

      REAL yg1(kw), ygoh(kw)
      real qy, qym1, qy1, qy2, qy3, qyoh
      REAL sig, sigoh
      INTEGER ierr, idum

      INTEGER myld

**************** 3-methyl crotonaldehyde photodissociation

      j = j+1
      jlabel(j) = 'CH3C(CH3)=CHCHO -> (CH3)2C=CH + CHO'
      j = j+1
      jlabel(j) = 'CH3C(CH3)=CHCHO -> (CH3)2C=CH2 + CO'
      j = j+1
      jlabel(j) = 'CH3C(CH3)=CHCHO -> (CH3)2C=CHCO + H'

      j = j+1
      jlabel(j) = 'bMeC4uALDOHqy -> NI products'
      j = j+1
      jlabel(j) = 'bMeC4uALDOHqy -> alkene + CO'
      j = j+1
      jlabel(j) = 'bMeC4uALDOHqy -> acyl + H'

      j = j+1
      jlabel(j) = 'bMeC4uALDOHoh -> NI products'
      j = j+1
      jlabel(j) = 'bMeC4uALDOHoh -> alkene + CO'
      j = j+1
      jlabel(j) = 'bMeC4uALDOHoh -> acyl + H'


* quantum yields estimated 10x acrolein
* Criegee channel replaced by CH3 fission
* 1: acrolein from JPL 2006
* 2: acrolein from Calvert et al. 2011

      IF(vers==1)THEN
        myld = 1
       ELSEIF(vers==2)THEN
        myld = 1
       ELSEIF(vers==0) THEN
        myld = 2
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' 3-Me-crotonaldehyde quantum yields',
     &       ' estimated with acrolein JPL data.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &       ' 3-Me-crotonaldehyde quantum yields',
     &       ' estimated with acrolein Calvert et al. data.'
       ELSE
        STOP "'myld' not defined for 3-Me-crotonaldehyde photolysis."
      ENDIF


* cross section

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/3Me2butenal.abs',
     &     STATUS='OLD')
      DO i = 1, 4
        READ(kin,*)
      ENDDO
      n = 84
      DO i = 1, n
        READ(kin,*) idum, y1(i)
        x1(i) = float(idum)
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg1,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
         WRITE(*,*) ierr, jlabel(j)
         STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,ygoh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* combine xs with qy:

      qyoh = 0.75

      DO iw = 1, nw-1
        sig = yg1(iw)
        sigoh = ygoh(iw)
        DO i = 1, nz

           if(airden(i) .gt. 2.6e19) then
              qy = 0.004
           elseif(airden(i) .gt. 8.e17 .and. airden(i) .lt. 2.6e19) then
             if(myld==1) then
               qym1 = 0.086 + 1.613e-17 * airden(i)
               qy = 0.004 + 1./qym1
              elseif(myld==2) then
               qym1 = -0.836+1.159e-17*airden(i)-2.166e-37*airden(i)**2
               qy = 1./qym1
             endif
           elseif(airden(i) .lt. 8.e17) then
             if(myld==1) then
              qym1 = 0.086 + 1.613e-17 * 8.e17
              qy = 0.004 + 1./qym1
              elseif(myld==2) then
               qym1 = -0.836+1.159e-17*8.e17-2.166e-37*8.e17**2
               qy = 1./qym1
             endif
           endif
* product distribution as estimated 10 x acrolein from Calvert et al. 2011:
* fits of direct qy given behind do not match 0.0065 at 1 atm
           qy = MIN(10. * qy,1.)
           qy1 = qy*(-0.0173*(airden(i)/1.E19)**2
     &              +0.083*airden(i)/1.E19+0.0492)
           qy2 = qy*(0.0407*(airden(i)/1.E19)**2
     &              -0.1661*airden(i)/1.E19+0.8485)
           qy3 = qy*(-0.0217*(airden(i)/1.E19)**2
     &                +0.0788*airden(i)/1.E19+0.1029)
           sq(j-8,i,iw) = sig * qy1
           sq(j-7,i,iw) = sig * qy2
           sq(j-6,i,iw) = sig * qy3
           sq(j-5,i,iw) = sigoh * qy1
           sq(j-4,i,iw) = sigoh * qy2
           sq(j-3,i,iw) = sigoh * qy3
           IF(qy1+qy2+qy3 > 0.) THEN
             sq(j-2,i,iw) = sigoh * qyoh*qy1/(qy1+qy2+qy3)
             sq(j-1,i,iw) = sigoh * qyoh*qy2/(qy1+qy2+qy3)
             sq(j  ,i,iw) = sigoh * qyoh*qy3/(qy1+qy2+qy3)
            ELSE
             sq(j-2,i,iw) = 0.
             sq(j-1,i,iw) = 0.
             sq(j  ,i,iw) = 0.
           ENDIF
        ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma17(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! 2,4-hexadienal

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide product (cross section) x (quantum yield) for 2,4-hexadienal     =*
*=  photolysis:                                                              =*
*=       2,4-hexadienal + hv -> Products                                     =*
*=                                                                           =*
*=  Cross section: O'Connor et al. (2006)                                    =*
*=  Quantum yield: estimated 10*acrolein                                     =*
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
      PARAMETER(kdata=120)

      INTEGER iw
      INTEGER i, n, n1
      REAL x1(kdata), x1oh(kdata)
      REAL y1(kdata), y1oh(kdata)

* local

      REAL yg(kw), ygoh(kw)
      real qy, qym1, qy1, qy2, qy3, qyoh
      REAL sig, sigoh
      INTEGER ierr, idum

**************** 2-hexenal photodissociation

      j = j+1
      jlabel(j) = 'hexadienal -> 1-pentenyl radical + CHO'
      j = j+1
      jlabel(j) = 'hexadienal -> 1,3-pentadiene + CO'
      j = j+1
      jlabel(j) = 'hexadienal -> CH3CH=CHCH=CHCO + H'

      j = j+1
      jlabel(j) = 'uuALDOHqy -> NI products'
      j = j+1
      jlabel(j) = 'uuALDOHqy -> diene + CO'
      j = j+1
      jlabel(j) = 'uuALDOHqy -> acyl + H'

      j = j+1
      jlabel(j) = 'uuALDOHoh -> NI products'
      j = j+1
      jlabel(j) = 'uuALDOHoh -> diene + CO'
      j = j+1
      jlabel(j) = 'uuALDOHoh -> acyl + H'


* cross sections
      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/hexadienal.abs',
     &     STATUS='OLD')
      DO i = 1, 5
        READ(kin,*)
      ENDDO

      n = 111
      DO i = 1, n
        READ(kin,*) idum, y1(i)
        x1(i) = FLOAT(idum)
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
         WRITE(*,*) ierr, jlabel(j)
         STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,ygoh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF

* combine xs with qy:

      qyoh = 0.75

      DO iw = 1, nw-1

        sig = yg(iw)
        sigoh = ygoh(iw)

        DO i = 1, nz

           if(airden(i) .gt. 2.6e19) then
             qy = 0.004
            elseif(airden(i) .gt. 8.e17 .and. airden(i) .lt. 2.6e19)
     &        then
             qym1 = 0.086 + 1.613e-17 * airden(i)
             qy = 0.004 + 1./qym1
            elseif(airden(i) .lt. 8.e17) then
             qym1 = 0.086 + 1.613e-17 * 8.e17
             qy = 0.004 + 1./qym1
           endif
* product distribution estimated from Calvert et al. 2011:
           qy = MIN(10. * qy,1.) ! qy estimated 10 times higher than acrolein
           qy1 = qy*(-0.0173*(airden(i)/1.E19)**2
     &               +0.083*airden(i)/1.E19+0.0492)
           qy2 = qy*(0.0407*(airden(i)/1.E19)**2
     &               -0.1661*airden(i)/1.E19+0.8485)
           qy3 = qy*(-0.0217*(airden(i)/1.E19)**2
     &               +0.0788*airden(i)/1.E19+0.1029)
           sq(j-8,i,iw) = sig * qy1
           sq(j-7,i,iw) = sig * qy2
           sq(j-6,i,iw) = sig * qy3
           sq(j-5,i,iw) = sigoh * qy1
           sq(j-4,i,iw) = sigoh * qy2
           sq(j-3,i,iw) = sigoh * qy3
           IF(qy1+qy2+qy3 > 0.) THEN
             sq(j-2,i,iw) = sigoh * qyoh*qy1/(qy1+qy2+qy3)
             sq(j-1,i,iw) = sigoh * qyoh*qy2/(qy1+qy2+qy3)
             sq(j  ,i,iw) = sigoh * qyoh*qy3/(qy1+qy2+qy3)
            ELSE
             sq(j-2,i,iw) = 0.
             sq(j-1,i,iw) = 0.
             sq(j  ,i,iw) = 0.
           ENDIF
        ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma18(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! (CH3)2C(OH)CHO

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide product (cross section)x(quantum yield) for (CH3)2C(OH)CHO       =*
*=  photolysis                                                               =*
*=          (CH3)2C(OH)CHO + hv -> (CH3)2COH + CHO                           =*
*=                                                                           =*
*=  Cross section: Chakir et al. (2004)                                      =*
*=  Quantum yield: estimated same as i-C3H7CHO                               =*
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
      REAL x1(kdata), x2(kdata)
      REAL y1(kdata), y2(kdata)

* local

      REAL yg(kw), yg1(kw), dum
      REAL qy
      REAL sig
      INTEGER ierr, idum
      INTEGER iw

      INTEGER myld

* only Norish type I based on i-C3H7CHO
      j = j+1
      jlabel(j) = 'CH32C(OH)CHO + hv -> (CH3)2COH + CHO'

      IF(vers==1)THEN
        myld = 1 !From GECKO-A TUV version (Bernard Aumont group), not TUV5.2
       ELSEIF(vers==2)THEN
        myld = 4
       ELSEIF(vers==0) THEN
        myld = 4
       ELSE
        STOP "'vers' not set. Choose value between 0 and 2 in 'params'."
      ENDIF

      IF(vers==1 .OR. vers==2) THEN
        CONTiNUE
       ELSEIF(myld.EQ.1) THEN
        WRITE(kout,'(2A)')
     &       ' (CH3)2C(OH)CHO quantum yields from Desai et al. 1986',
     &       ' for i-C3H7CHO.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(2A)')
     &     ' (CH3)2C(OH)CHO quantum yields from Calvert book, opt. 1,',
     &     ' for i-C3H7CHO.'
       ELSEIF(myld.EQ.3) THEN
        WRITE(kout,'(2A)')
     &     ' (CH3)2C(OH)CHO quantum yields from Calvert book, opt. 2,',
     &     ' for i-C3H7CHO.'
       ELSEIF(myld.EQ.4) THEN
        WRITE(kout,'(2A)')
     &       ' (CH3)2C(OH)CHO quantum yields from IUPAC.',
     &       ' for i-C3H7CHO.'
       ELSE
        STOP "'myld' not defined for (CH3)2C(OH)CHO photolysis."
      ENDIF


* cross sections

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/bOHisobutyraldehyde.abs',
     $     STATUS='old')
      do i = 1, 4
         read(kin,*)
      enddo

      n = 12
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

      IF(myld==1) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/i_butyraldehyde_R.prn',
     $       STATUS='old')
        do i = 1, 3
           read(kin,*)
        enddo

        n = 101
        DO i = 1, n
           READ(kin,*) x1(i), dum, y1(i)
        ENDDO
        CLOSE(kin)

       ELSEIF(myld==2 .OR. myld==3) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/iC3H7CHO_calv.yld',
     $       STATUS='old')
        do i = 1, 6
           read(kin,*)
        enddo

        n = 73
        DO i = 1, n
           READ(kin,*) idum, dum, y1(i),y2(i)
           x1(i) = FLOAT(idum)
           x2(i) = x1(i)
        ENDDO
        CLOSE(kin)

       ELSEIF(myld==4) THEN

        OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/iC3H7CHO_iup.yld',
     $       STATUS='old')
        do i = 1, 7
           read(kin,*)
        enddo

        n = 11
        DO i = 1, n
           READ(kin,*) idum, y1(i)
           x1(i) = FLOAT(idum)
        ENDDO
        CLOSE(kin)

      ENDIF

      IF(myld==3)THEN
        CALL addpnt(x2,y2,kdata,n,x2(1)*(1.-deltax),0.)
        CALL addpnt(x2,y2,kdata,n,               0.,0.)
        CALL addpnt(x2,y2,kdata,n,x2(n)*(1.+deltax),0.)
        CALL addpnt(x2,y2,kdata,n,           1.e+38,0.)
        CALL inter2(nw,wl,yg1,n,x2,y2,ierr)
        IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
        ENDIF
       ELSE
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

*combine
      DO iw = 1, nw - 1
         sig = yg (iw)
         qy  = yg1(iw)
         DO i = 1, nz
            sq(j  ,i,iw) = sig * qy
         ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma19(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) !≥C8 n-aldehydes

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide product (cross section)x(quantum yield) for n-aldehyde photolysis=*
*=          n-aldehydes + hv -> products                                     =*
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
      PARAMETER(kdata=580)

      INTEGER i, n, n1
      REAL x1(kdata), x1oh(kdata), y1(kdata), y1oh(kdata)

* local

      REAL yg1(kw),yg2(kw),yg3(kw),yg4(kw),dum
      REAL yg1oh(kw),yg2oh(kw),yg3oh(kw),yg4oh(kw)
      REAL qy, qyoh
      REAL sig,sigoh
      INTEGER ierr, idum
      INTEGER iw

      INTEGER myld
* Labels
* unsubstituted:
      j = j+1
      jlabel(j) = 'nALD -> products'
      j = j+1
      jlabel(j) = 'nALDOHqy -> products'
      j = j+1
      jlabel(j) = 'nALDOHoh -> products'


* cross sections

*C4:
      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/nC3H7CHO_iup.abs',
     $     STATUS='old')
      do i = 1, 5
         read(kin,*)
      enddo

      n = 106
      DO i = 1, n
         READ(kin,*) idum, y1(i)
         x1(i) = FLOAT(idum)
         y1(i) = y1(i)*1.e-20
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg1,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg1oh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF

*C5:
      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/Tadic.abs',
     $     STATUS='old')

      do i = 1, 5
        read(kin,*)
      enddo

      n = 121
      DO i = 1, n
        READ(kin,*) x1(i), dum, y1(i)
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg2,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j-2)
        STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg2oh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF

*C6:
      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/hexanal_rad',
     $     STATUS='old')
      do i = 1, 2
        read(kin,*)
      enddo

      n = 89
      DO i = 1, n
         READ(kin,*) x1(i), y1(i), dum
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg3,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j)
          STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg3oh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF

*C7:
      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/nHeptanal.abs',
     $     STATUS='old')

      do i = 1, 5
        read(kin,*)
      enddo

      n = 11
      DO i = 1, n
        READ(kin,*) x1(i), y1(i)
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg4,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-1)
          STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg4oh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* quantum yields

* 1: Moortgat 99
* 2: IUPAC (Tadic et al. 01)

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
     &       ' n-C3H7CHO quantum yields from Moortgat 1999.'
       ELSEIF(myld.EQ.2) THEN
        WRITE(kout,'(A)')
     &       ' n-C3H7CHO quantum yields from IUPAC.'
       ELSE
        STOP "'myld' not defined for n-C3H7CHO photolysis."
      ENDIF



* OH quantum yield
      qy = 0.2466 ! from lin. regression: qy = 0.385 - 0.0173*CN(8)
      qyOH = 0.75


* combine:

      DO iw = 1, nw - 1
        ! Average, where all values exist, otherwise scale missing values
         IF(wc(iw)<230.) THEN
           sig = ((0.7567/1.342*yg1(iw))+yg1(iw))/2
          ELSEIF(wc(iw)>=230. .and. wc(iw)<=257.) THEN
           sig = ((0.7914/(1.9334+1.93)*(yg1(iw)+yg2(iw)))
     &           +yg1(iw)+yg2(iw))/3
          ELSEIF(wc(iw)>257. .and. wc(iw)<280.) THEN
           sig = ((2.7514/(5.175+5.2225+5.0857)*(yg1(iw)+yg2(iw)
     &           +yg3(iw)))+yg1(iw)+yg2(iw)+yg3(iw))/4
          ELSEIF(wc(iw)>330. .and. wc(iw)<347.) THEN
           sig = ((5.515/(8.7275+8.2313+9.0234)*(yg1(iw)+yg2(iw)
     &           +yg3(iw)))+yg1(iw)+yg2(iw)+yg3(iw))/4
          ELSEIF(wc(iw)>=347. .and. wc(iw)<=350.) THEN
           sig = ((4.3454/(3.1625+2.825)*(yg1(iw)+yg2(iw)))
     &           +yg1(iw)+yg2(iw))/3
          ELSEIF(wc(iw)>350.) THEN
           sig = ((7.7763/(1.525)*yg1(iw))+yg1(iw))/2
          ELSE
           sig   = (yg1(iw)+yg2(iw)+yg3(iw)+yg4(iw))/4
         ENDIF
         IF(wc(iw)<220.) THEN
           sig = ((0.7566/1.342*yg1(iw))+yg1(iw))/2
          ELSEIF(wc(iw)>=220. .and. wc(iw)<=247.) THEN
           sig = ((0.7913/(1.9334+1.93)*(yg1(iw)+yg2(iw)))
     &           +yg1(iw)+yg2(iw))/3
          ELSEIF(wc(iw)>247. .and. wc(iw)<270.) THEN
           sig = ((2.7511/(5.175+5.2225+5.0857)*(yg1(iw)+yg2(iw)
     &           +yg3(iw)))+yg1(iw)+yg2(iw)+yg3(iw))/4
          ELSEIF(wc(iw)>320. .and. wc(iw)<337.) THEN
           sig = ((5.5145/(8.7275+8.2313+9.0234)*(yg1(iw)+yg2(iw)
     &           +yg3(iw)))+yg1(iw)+yg2(iw)+yg3(iw))/4
          ELSEIF(wc(iw)>=337. .and. wc(iw)<=340.) THEN
           sig = ((4.3454/(3.1625+2.825)*(yg1(iw)+yg2(iw)))
     &           +yg1(iw)+yg2(iw))/3
          ELSEIF(wc(iw)>340.) THEN
           sig = ((7.7756/(1.525)*yg1(iw))+yg1(iw))/2
          ELSE
           sigoh = (yg1oh(iw)+yg2oh(iw)+yg3oh(iw)+yg4oh(iw))/4
         ENDIF
         DO i = 1, nz
             sq(j-2,i,iw) = sig * qy
             sq(j-1,i,iw) = sigOH * qy
             sq(j  ,i,iw) = sigOH * qyOH
         ENDDO
      ENDDO

      END

*=============================================================================*

      SUBROUTINE ma20(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! methyl substituted and cyclic aldehydes

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide product (cross section)x(quantum yield) for branched aldehyde    =*
*=  photolysis (aldehydes with methyl substitutions only):                   =*
*=          aldehydes + hv -> Norish I and II products                       =*
*=  Cross section:  average of C4 – C7 n-aldehydes                           =*
*=  Quantum yield:  0.385 - 0.0173 * CN                                      =*
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
      PARAMETER(kdata=580)

      INTEGER i, n, n1
      REAL x1(kdata), x1oh(kdata)
      REAL y1(kdata), y1oh(kdata)

* local

      REAL yg1(kw), yg2(kw), yg1oh(kw), yg2oh(kw)
      REAL qy1, qy2, qyc, qyoh
      REAL sig, sigoh
      INTEGER ierr, idum
      INTEGER iw


      j = j+1
      jlabel(j) = 'MeALD -> NI products'
      j = j+1
      jlabel(j) = 'MeALD -> NII products'

      j = j+1
      jlabel(j) = 'MeALDOHqy -> NI products'
      j = j+1
      jlabel(j) = 'MeALDOHqy -> NII products'

      j = j+1
      jlabel(j) = 'MeALDOHoh -> NI products'
      j = j+1
      jlabel(j) = 'MeALDOHoh -> NII products'

      j = j+1
      jlabel(j) = 'cALD -> NI products'
      j = j+1
      jlabel(j) = 'cALDOHqy -> NI products'
      j = j+1
      jlabel(j) = 'cALDOHoh -> NI products'


* cross sections:
* isobutyraldehyde:

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/iC3H7CHO_iup.abs',
     $     STATUS='old')
      do i = 1, 5
         read(kin,*)
      enddo

      n = 121
      DO i = 1, n
         READ(kin,*) idum, y1(i)
         x1(i) = FLOAT(idum)
         y1(i) = y1(i) * 1E-20
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg1,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg1oh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF

* isovaleraldehyde:
      OPEN(UNIT=kin,
     $     FILE='DATAJ1/MCMext/ALD/isovaleraldehyde_avrgext.abs',
     $     STATUS='old')
      do i = 1, 9
        read(kin,*)
      enddo

      n = 63
      DO i = 1, n
        READ(kin,*) idum, y1(i)
        x1(i) = FLOAT(idum)
        y1(i) = y1(i) * 1.E-20
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg2,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j-2)
        STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg2oh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


* quantum yields

      qy1 = 0.45
      qy2 = 0.13
      qyc = 0.14
      qyoh = 0.75

* combine:

      DO iw = 1, nw - 1
        ! Average, scale values, where only one value exists
        ! according to last common couple:
         IF(wc(iw)<280.) THEN
           sig   = (2.5051/5.1175*yg1(iw)+yg1(iw))/2
          ELSEIF(wc(iw)>=360.) THEN
           sig   = (2.5051/5.1175*yg1(iw)+yg1(iw))/2
          ELSE
           sig   = (yg1(iw)+yg2(iw))/2
         ENDIF
         IF(wc(iw)<270.) THEN
           sigoh = (2.5049/5.1175*yg1oh(iw)+yg1oh(iw))/2
          ELSEIF(wc(iw)>=350.) THEN
           sigoh = (0.0502/2.8452*yg2oh(iw)+yg2oh(iw))/2
          ELSE
           sigoh = (yg1oh(iw)+yg2oh(iw))/2
         ENDIF
         DO i = 1, nz
           sq(j-8,i,iw) = sig * qy1
           sq(j-7,i,iw) = sig * qy2
           sq(j-6,i,iw) = sigoh * qy1
           sq(j-5,i,iw) = sigoh * qy2
           IF(qy1+qy2 > 0.) THEN
             sq(j-4,i,iw) = sigoh * qyoh*qy1/(qy1+qy2)
             sq(j-3,i,iw) = sigoh * qyoh*qy2/(qy1+qy2)
            ELSE
             sq(j-4,i,iw) = 0.
             sq(j-3,i,iw) = 0.
           ENDIF
           sq(j-2,i,iw) = sig * qyc
           sq(j-1,i,iw) = sigoh * qyc
           sq(j  ,i,iw) = sigoh * qyoh
         ENDDO
      ENDDO

      END

* ============================================================================*

      SUBROUTINE ma21(nw,wl,wc,nz,tlev,airden,j,sq,jlabel) ! linear alpha,beta-unsaturated aldehydes

*-----------------------------------------------------------------------------*
*=  PURPOSE:                                                                 =*
*=  Provide product (cross section)x(quantum yield) for                      =*
*=  linear alpha,beta-unsaturated aldehyde photolysis:                       =*
*=          aldehydes + hv ->  products                                      =*
*=  Cross section:  average of crotonaldehyde and 2-hexenal                  =*
*=  Quantum yield:  10 * acrolein                                            =*
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
      PARAMETER(kdata=4500)

      INTEGER iw
      INTEGER i, n, n1
      REAL x1(kdata), x1oh(kdata)
      REAL y1(kdata), y1oh(kdata)

* local

      REAL yg1(kw), yg2(kw), yg3(kw), yg1oh(kw), yg2oh(kw), yg3oh(kw)
      real qy, qym1, qy1, qy2, qy3, qyoh
      REAL sig, sigoh
      INTEGER ierr, idum

**************** crotonaldehyde photodissociation

      j = j+1
      jlabel(j) = 'luALD -> NI products'
      j = j+1
      jlabel(j) = 'luALD -> alkene + CO'
      j = j+1
      jlabel(j) = 'luALD -> acyl + H'

      j = j+1
      jlabel(j) = 'luALDOHqy -> NI products'
      j = j+1
      jlabel(j) = 'luALDOHqy -> alkene + CO'
      j = j+1
      jlabel(j) = 'luALDOHqy -> acyl + H'

      j = j+1
      jlabel(j) = 'luALDOHoh -> NI products'
      j = j+1
      jlabel(j) = 'luALDOHoh -> alkene + CO'
      j = j+1
      jlabel(j) = 'luALDOHoh -> acyl + H'


* cross section from
* UV-C: Lee et al. 2007
* UV/VIS: unpublished high res data by Magneron et al. 1999
* quantum yields estimated 10x acrolein

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/crotonaldehyde_Lee07.abs',
     &     STATUS='OLD')
      DO i = 1, 6
        READ(kin,*)
      ENDDO
      n = 4368
      DO i = 1, n
        READ(kin,*) x1(i), y1(i)
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg1,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-1)
          STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg1oh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF


      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/crotonaldehyde_Mag99.abs',
     &     STATUS='OLD')
      DO i = 1, 6
        READ(kin,*)
      ENDDO
      n = 3202
      DO i = 1, n
        READ(kin,*) x1(i), y1(i)
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg2,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
          WRITE(*,*) ierr, jlabel(j-1)
          STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg2oh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF

      OPEN(UNIT=kin,FILE='DATAJ1/MCMext/ALD/hexenal_Jim07.abs',
     &     STATUS='OLD')
      DO i = 1, 6
        READ(kin,*)
      ENDDO

      n = 81
      DO i = 1, n
        READ(kin,*) idum, y1(i)
        x1(i) = FLOAT(idum)
      ENDDO
      CLOSE(kin)

      x1oh(:) = 0.
      x1oh(:) = x1(:) - 10.
      y1oh(:) = y1(:)
      n1 = n

      CALL addpnt(x1,y1,kdata,n,x1(1)*(1.-deltax),0.)
      CALL addpnt(x1,y1,kdata,n,               0.,0.)
      CALL addpnt(x1,y1,kdata,n,x1(n)*(1.+deltax),0.)
      CALL addpnt(x1,y1,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg3,n,x1,y1,ierr)
      IF (ierr .NE. 0) THEN
         WRITE(*,*) ierr, jlabel(j)
         STOP
      ENDIF

      n = n1
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(1)*(1.-deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,               0.,0.)
      CALL addpnt(x1oh,y1oh,kdata,n,x1oh(n)*(1.+deltax),0.)
      CALL addpnt(x1oh,y1oh,kdata,n,           1.e+38,0.)
      CALL inter2(nw,wl,yg3oh,n,x1oh,y1oh,ierr)
      IF (ierr .NE. 0) THEN
        WRITE(*,*) ierr, jlabel(j)
        STOP
      ENDIF

* combine xs with qy:

      qyoh = 0.75

      DO iw = 1, nw-1

* cross sections: combine UV-C and UV/VIS-data:
        IF(wc(iw)<=215.) THEN
          sig = (max(0.,yg1(iw))+yg3(iw))/2
          sigoh = (max(0.,yg1oh(iw))+yg3oh(iw))/2
         ELSEIF(wc(iw)<=225.) THEN
          sig = (max(0.,yg1(iw))+yg3(iw))/2
          sigoh = (max(0.,yg2oh(iw))+yg3oh(iw))/2
         ELSE
          sig = (max(0.,yg2(iw))+yg3(iw))/2
          sigoh = (max(0.,yg2oh(iw))+yg3oh(iw))/2
        ENDIF


        DO i = 1, nz

           if(airden(i) .gt. 2.6e19) then
             qy = 0.004
           elseif(airden(i) .gt. 8.e17 .and. airden(i) .lt. 2.6e19) then
             qym1 = 0.086 + 1.613e-17 * airden(i)
             qy = 0.004 + 1./qym1
           elseif(airden(i) .lt. 8.e17) then
             qym1 = 0.086 + 1.613e-17 * 8.e17
             qy = 0.004 + 1./qym1
           endif
* product distribution estimated from Calvert et al. 2011:
           qy  = MIN(10. * qy,1.) ! qy estimated 10 times higher than acrolein
           qy1 = qy*(-0.0173*(airden(i)/1.E19)**2
     &               +0.083*airden(i)/1.E19+0.0492)
           qy2 = qy*(0.0407*(airden(i)/1.E19)**2
     &               -0.1661*airden(i)/1.E19+0.8485)
           qy3 = qy*(-0.0217*(airden(i)/1.E19)**2
     &               +0.0788*airden(i)/1.E19+0.1029)
           sq(j-8,i,iw) = sig * qy1
           sq(j-7,i,iw) = sig * qy2
           sq(j-6,i,iw) = sig * qy3
           sq(j-5,i,iw) = sigoh * qy1
           sq(j-4,i,iw) = sigoh * qy2
           sq(j-3,i,iw) = sigoh * qy3
          IF(qy1+qy2+qy3 > 0.) THEN
            sq(j-2,i,iw) = sigoh * qyoh*qy1/(qy1+qy2+qy3)
            sq(j-1,i,iw) = sigoh * qyoh*qy2/(qy1+qy2+qy3)
            sq(j  ,i,iw) = sigoh * qyoh*qy3/(qy1+qy2+qy3)
           ELSE
            sq(j-2,i,iw) = 0.
            sq(j-1,i,iw) = 0.
            sq(j  ,i,iw) = 0.
          ENDIF
        ENDDO
      ENDDO

      END

*=============================================================================*