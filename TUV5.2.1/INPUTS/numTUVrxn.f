      PROGRAM numTUVrxn

      IMPLICIT NONE

      INTEGER        :: i
      CHARACTER(80)  :: line,ifile
      CHARACTER(1)   :: reset

      CALL getarg(1,ifile)
      IF (ifile == ' ') THEN
        WRITE(*,"('Name of input file: ',A)",advance='no')
        READ(*,*) ifile
      ENDIF
      ifile = TRIM(ADJUSTL(ifile))
      OPEN(11,file=ifile)
      OPEN(12,FILE='ofile.txt')

      CALL getarg(2,reset)
      IF(reset==' ') THEN
        WRITE(*,'(A)') "Choose options for reaction flags:"
        WRITE(*,'(A)') "T:       set all to true"
        WRITE(*,'(A)') "F:       set all to false"
        WRITE(*,'(A)') "<ENTER>: leave as it is"
        READ(*,"(A)") reset
      ENDIF

      OPEN(11,FILE=ifile)
      DO i = 1, 48
        READ(11,'(A)') line
        WRITE(12,'(A)') trim(line)
      ENDDO
      i = 0
      DO
        i = i + 1
        READ(11,'(A)') line
        IF(line(:3) == '===') THEN
          WRITE(12,'(A)') trim(line)
          EXIT
        ENDIF
        IF(reset=="T" .or. reset=="t") THEN
          WRITE(line(1:1),'(A1)') "T"
         ELSEIF(reset=="F" .or. reset=="f") THEN
          WRITE(line(1:1),'(A1)') "F"
        ENDIF
        WRITE(line(2:4),'(I3)') i
        WRITE(12,'(A)') trim(line)
      ENDDO

      CLOSE(11)
      CLOSE(12)

      CALL SYSTEM('mv ofile.txt '//trim(ifile))

      END PROGRAM numTUVrxn