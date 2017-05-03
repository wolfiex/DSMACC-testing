         OPEN(UNIT=kin,FILE='DATAJ1/CH2O/HCHO_IUPAC.yld',STATUS='old')
         DO i = 1, 9
            READ(kin,*)
         ENDDO
         n = 74
         n1 = n
         n2 = n
         DO i = 1, n
            READ(kin,*) idum, qr(i), qm(i), dum
            x1(i) = FLOAT(idum)
            x2(i) = x1(i)
            print*, x1(i),qr(i),qm(i)
         ENDDO
         CLOSE(kin)

           CALL addpnt(x1,qr,kdata,n1,x1(1)*(1.-deltax),qr(1))
           CALL addpnt(x1,qr,kdata,n1,               0.,qr(1))
           CALL addpnt(x1,qr,kdata,n1,x1(n1)*(1.+deltax),0.)
           CALL addpnt(x1,qr,kdata,n1,            1.e+38,0.)
           CALL inter2(nw,wl,yg3,n1,x1,qr,ierr)
           IF (ierr .NE. 0) THEN
              WRITE(*,*) ierr, jlabel(j-1)
              STOP
           ENDIF

           CALL addpnt(x2,qm,kdata,n2,x2(1)*(1.-deltax),qm(1))
           CALL addpnt(x2,qm,kdata,n2,               0.,qm(1))
           CALL addpnt(x2,qm,kdata,n2,x2(n2)*(1.+deltax),0.)
           CALL addpnt(x2,qm,kdata,n2,            1.e+38,0.)
           CALL inter2(nw,wl,yg4,n2,x2,qm,ierr)
           IF (ierr .NE. 0) THEN
              WRITE(*,*) ierr, jlabel(j)
              STOP
           ENDIF