PROGRAM driver
USE model_global
USE model_Parameters
USE model_Rates,       ONLY: Update_SUN, Update_RCONST
USE model_integrator,  ONLY: integrate
USE model_monitor,     ONLY: spc_names,Eqn_names
!USE model_Function, ONLY: A,fun
USE model_Util
USE constants


IMPLICIT NONE
REAL(dp) :: ENDSTATE(NVAR), total, RATIO, TNOX, TNOX_OLD
REAL(dp) :: STARTSTATE(NVAR), TIMESCALE, RH, RSTATE(20)
REAL(dp) :: DIURNAL_OLD(NVAR,3000), DIURNAL_NEW(NVAR,3000)
REAL(dp) :: DIURNAL_RATES(NREACT, 3000)
REAL(dp) ::  concs(NSPEC)  !FULL_CONCS(NSPEC,999999),
! Photolysis calculation variables
 character(len=50), allocatable ::  s_names(:), r_names(:)


! DO NOT NEED ABOVE

REAL(dp) :: NOXRATIO,Alta,Fracdiff,SpeedRatio,oldfracdiff,FRACCOUNT, newtime,floorjday
 character(50) :: cw,filename
 character (10) :: ln
INTEGER  :: ERROR, IJ, PE ,runtimestep,ICNTRL_U(20)
Integer  :: CONSTNOXSPEC, JK, full_counter, line, nc_set, nc_counter,run_counter
INTEGER :: DAY = 24*60*60
 character(200) :: dummychar




STEPMIN = 0.0_dp
STEPMAX = 0.0_dp
RTOL(:) = 1.0E-5_dp !-5
ATOL(:) = 1.0_dp    !-16?
!desired |true-computed| < RTOL*|TRUE| + ATOL
!want ATOL/calc_value < RTOL
!rtol - #sig fig

LAST_POINT=.False.
CONSTRAIN_NOX=.False.
CONSTRAIN_RUN=.FALSE.
SAVE_LEGACY=.false.
time=tstart
!tuv defined globally



!dt is the output timestep and the timestep between times
!rate constants and notably photolysis rates are calcualted " 600 = ten minutes
dt = 600.
!spinup default
spinup = 9999.

call getarg(3,ln)!name
if (trim(ln) .eq. '--version') then
    write(06,*) trim(version)
    STOP
end if

call getarg(2,ln)
read(ln, *) obs

call getarg(1,ln)!location in Init Cons
read(ln, *) line



CALL system("echo $(date '+%A %W %Y %X') >> temp.txt")


!set OUTPUT_UNIT to 6 in globals file.
open(UNIT=output_unit,FILE='Outputs/'//trim(ln)//'.sdout')


!all initialisation calculations:
INCLUDE './src/initialisations.inc'

!so T=0 of the output file gives the initial condition
!i'cs copied from python initiation program

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!print*,  achar(27)//'[2J'
!print*, 'Run Progress'
time_loop: DO WHILE (time < TEND)! This is the main loop for integrations
run_counter = run_counter+1


CALL Update_RCONST()! Update the rate constants

!If we wish to spinup or constrain to observations
if (obs == 0) then
    continue

else if (obs > 0) then
    ! DFRACT - day fraction
    DFRACT = (Time-tstart)
    if (DFRACT < spinup) then
        DFRACT = mod(dfract,float(day))
        include 'include.obs'
    end if

end if


ICNTRL_U(:)=0
CALL INTEGRATE( TIN = time, TOUT = time+DT, RSTATUS_U = RSTATE, &! Integrate the model +1 timestep
ICNTRL_U = ICNTRL_U,IERR_U=ERROR)

! Traps for NaN
DO I=1,NVAR
IF (ISNAN(C(I)) .or. (ERROR .NE. 1)) then
    write (OUTPUT_UNIT,*) 'Integration error / NaN, Skipping Point'
    !print *, ''//achar(27)//'[95m', c,''//achar(27)//'[97m'
    !if (i .eqv. ind_DUMMY) then
    !    c(i)= 0.
    !    cycle
    !end if

    C(1:NVAR)=0.
    GOTO 1000
ENDIF
End Do

! Update the time to reflect the integration has taken place
time = RSTATE(1)
Daycounter=Daycounter+1

!print*, 'list of nox locations, no need to loop over all species again'
IF (CONSTRAIN_NOX) THEN
    write (OUTPUT_UNIT,*) 'Constraining NOx'
    TNOX=0.! Calcualte the total NOx in the box
    TNOX=TNOX+sum(C(1:NVAR)*NOX(1:NVAR))
    ! Update all NOx variables so that the total NOx in the box is the same as it was
    DO I=1,NVAR
      IF (NOX(I) .NE. 0)  C(I)=C(I)*TNOX_OLD/TNOX
    ENDDO
ENDIF


!!If constrain species concentrations if necessary
DO I=1,NVAR
    IF (CONSTRAIN(I) .GT. 0) C(I)=CONSTRAIN(I)
END DO






newtime = time

WRITE (SPEC_UNIT) newtime,LAT, LON, PRESS, TEMP,H2O,JO1D,JNO2, CFACTOR, RO2, J(1),SPINUP,C(:NSPEC)
WRITE (RATE_UNIT) newtime, RCONST(:NREACT)

    !if (mod(run_counter/nc_set,20)==0) then
    !    print*, achar(27)//'['//trim(ln)//';10 H ', achar(27)//'[94m |',repeat('#',floor(time/TEND*20)), repeat(' ',int(20-floor(time/TEND*20))),'| '//achar(27)//'[97m'//trim(counter)
    !end if



!!!!!!! STEADY STATE
! If we are doing a constrained run we need to store the diurnal profile of all the species

IF (CONSTRAIN_RUN .eqv. .TRUE.) THEN

    DIURNAL_NEW(1:NVAR,DAYCOUNTER)=C(1:NVAR)
    DIURNAL_RATES(1:NREACT,DAYCOUNTER)=RCONST(1:NREACT)

    ! Are we at the end of a day?
    ! If so we need to 1) fiddle with the NOX to ensure it has the right concentrations see if we have reached a steady state
    IF (DAYCOUNTER*DT .GE. DAY) THEN
        ! Sort out the NOx. Need to increase the NOx concentration so that the constrained species is right
        ! What is  the constrained NOx species? Put result into CONSTNOXSPEC
        ! Calculate the ratio between the value we the constrained NOx species and what we have
        ! Remember the constrained NOx species is given by the negative constrained value
        DO I=1,NVAR
            IF (CONSTRAIN(I) .LT. 0)     CONSTNOXSPEC=I
            IF (NOX(I) .NE. 0)        C(I)=C(I)*NOXRATIO
        ENDDO
        NOXRATIO=-CONSTRAIN(CONSTNOXSPEC)/C(CONSTNOXSPEC)
        ! Multiply all the NOx species by the ratio so
        ! Update the total amount of NOx in box
        TNOX_OLD=TNOX_OLD*NOXRATIO
        ! Lets see how much the diurnal ratios have changed since the last itteration
        ! Frac diff is our metric for how much it has changed
        FRACDIFF=0.
        FRACCOUNT=0.
        ! Add up for all species and for each time point in the day
        DO I=1,NVAR
            DO JK=1,DAYCOUNTER
            !If there is a concentration calculated
            IF (DIURNAL_NEW(I,JK) .GT. 1.e2 .AND. &
            TRIM(SPC_NAMES(I)) .NE. 'DUMMY') THEN
                !Calculate the absolute value of the fractional difference and add it on
                ! Increment the counter to calculate the average
                FRACDIFF=FRACDIFF+&
                ABS(DIURNAL_OLD(I,JK)-DIURNAL_NEW(I,JK))/&
                DIURNAL_NEW(I,JK)
                FRACCOUNT=FRACCOUNT+1
            ENDIF
            ENDDO
        ENDDO

    FRACDIFF=FRACDIFF/FRACCOUNT !average fractional difference
    write (OUTPUT_UNIT,*) 'Fraction difference in the diurnal profile:', FRACDIFF! Output diagnostic

    ! Store the new diurnal profile as the old one so we can compare with the next day
    DIURNAL_OLD(1:NVAR,1:Daycounter)=DIURNAL_NEW(1:NVAR,1:DAYCOUNTER)
    TEND = TEND + DAY
    print *, line, ' fractional difference aim 0 :', abs(fracdiff - 1e-3)
    IF (FRACDIFF .LE. 1e-3) THEN
            
            CONSTRAIN_RUN = .FALSE.
            obs = 0
            print *, 'Converged at ',spinup,'timesteps'
            call initVal(concs,.FALSE.)
            continue
            !If (FRACDIFF .le. 0) GOTO 1000    ! stop if system has converged end simulation

    END IF
    !Reset params and add a day to TEND
    
    SPINUP = SPINUP + DAY
    
    if (obs < 0) then
        call initVal(concs,.FALSE.)!re-initialise values
        print*, 'resetting concentrations @ ', spinup, 'seconds.'
    end if
    
    DAYCOUNTER=0! reset the day counter to 0
    OLDFRACDIFF=FRACDIFF
    ENDIF

ENDIF


ENDDO time_loop
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
print *, 'Finished Simulation Sucessfully!'


1000  print *, ' '//achar(27)//'[91m exit condition 1000 '//achar(27)//'[97m'
!if (CONSTRAIN_RUN .EQ. .true.) .AND. (OUTPUT_LAST .EQ. .false.)  print*, 'why not SaveOut(run_counter) work dammit'


    CLOSE(rate_unit)
    CLOSE(spec_unit)
    CLOSE(flux_unit)
    CLOSE(vdot_unit)
    CLOSE(jacsp_unit)
    close(output_unit)


    END PROGRAM driver
