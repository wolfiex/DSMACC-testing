PROGRAM driver
USE model_global
USE model_Parameters
USE model_Rates,       ONLY: Update_SUN, Update_RCONST
USE model_integrator,  ONLY: integrate
USE model_monitor,     ONLY: spc_names,Eqn_names
USE model_Util
USE constants


IMPLICIT NONE
REAL(dp) :: ENDSTATE(NVAR), total, RATIO, TNOX, TNOX_OLD
REAL(dp) :: STARTSTATE(NVAR), TIMESCALE, RH, RSTATE(20)
REAL(dp) :: DIURNAL_OLD(NVAR,3000), DIURNAL_NEW(NVAR,3000)
REAL(dp) :: DIURNAL_RATES(NREACT, 3000)
REAL(dp) :: FULL_CONCS(NSPEC,999999), concs(NSPEC)
! Photolysis calculation variables
 character(len=50), allocatable ::  s_names(:), r_names(:)


! DO NOT NEED ABOVE

REAL(dp) :: NOXRATIO,Alta,Fracdiff,SpeedRatio,oldfracdiff,FRACCOUNT, newtime
 character(50) :: counter, cw,filename
 character (10) :: ln
INTEGER  :: ERROR, IJ, PE ,runtimestep,ICNTRL_U(20)
Integer  :: CONSTNOXSPEC, JK, full_counter, line, nc_set, nc_counter
 character(200) :: dummychar
integer :: run_counter = 0


STEPMIN = 0.0_dp
STEPMAX = 0.0_dp
RTOL(:) = 1.0E-5_dp !-5
ATOL(:) = 1.0_dp    !-16?

!desired |true-computed| < RTOL*|TRUE| + ATOL
!want ATOL/calc_value < RTOL

!rtol - #sig fig

mechanism=''
LAST_POINT=.False.
CONSTRAIN_NOX=.False.
CONSTRAIN_RUN=.FALSE.
SAVE_LEGACY=.false.
time=tstart
!tuv defined globally


!spinup time 0 for false, number timesteps otherwise


!dt is the output timestep and the timestep between times
!rate constants and notably photolysis rates are calcualted " 600 = ten minutes
dt = 600.
nc_set=1!36 ! the grouping factor that decides how often to write to file (modulo daycounter/nc_set)
!use nc_set = 0 for a single memory dump at the end of simulation.


spinup=0 !allocate this within ics
allocate(spin_const(NVAR))

call getarg(1,counter)!name
call getarg(2,ln)!location in Init Cons
read(ln, *) line

call getarg(3,ln)
read(ln, *) obs



!set OUTPUT_UNIT to 6 in globals file.
open(UNIT=output_unit,FILE='Outputs/'//trim(counter)//'.sdout')


!all initialisation calculations:
INCLUDE './src/initialisations.inc'


!i'cs copied from python initiation program

!so T=0 of the output file gives the initial condition
!i'cs copied from python initiation program

WRITE (SPEC_UNIT) newtime,LAT, LON, PRESS, TEMP,H2O, CFACTOR, RO2, C(:NSPEC)
WRITE (RATE_UNIT) newtime,LAT, LON, PRESS, TEMP, M, RCONST(:NREACT)


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
TEND = TEND + spinup*dt !additional spinup time added if included


print*,  achar(27)//'[2J'
print*, 'Run Progress'
time_loop: DO WHILE (time < TEND)! This is the main loop for integrations
run_counter = run_counter+1


CALL Update_RCONST()! Update the rate constants

if (obs>0) then
        include 'include.obs'
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






newtime = Jday*86400 + DAYCOUNTER*dt

WRITE (SPEC_UNIT) newtime,LAT, LON, PRESS, TEMP,H2O, CFACTOR, RO2, C(:NSPEC)
WRITE (RATE_UNIT) newtime,LAT, LON, PRESS, TEMP, M, RCONST(:NREACT)


if (run_counter > nc_set) then !increased at start
    !print*, testcounter ,' write '

    DO i = 1,daycounter
    !write (SPEC_UNIT, 999) output_s(i,:) !(output_s(i,ij), ij=1,NSPEC)
    !write (RATE_UNIT, 999) output_r(i,:) !(output_r(i,ij), ij=1,NREACT)
    end do

    if (mod(run_counter/nc_set,20)==0) then
        print*, achar(27)//'[f', achar(27)//'['//trim(ln)//'B', achar(27)//'[94m |',repeat('#',floor(time/TEND*20)), repeat(' ',int(20-floor(time/TEND*20))),'| '//achar(27)//'[97m'//trim(counter)
    end if

else
    run_counter = 1
    output_s(:,:)=0.
    output_r(:,:)=0.
    !SaveOut(run_counter)


end if


! If we are doing a constrained run we need to store the diurnal profile of all the species
IF (CONSTRAIN_RUN .EQv. .TRUE.) THEN
    DIURNAL_NEW(1:NVAR,DAYCOUNTER)=C(1:NVAR)
    DIURNAL_RATES(1:NREACT,DAYCOUNTER)=RCONST(1:NREACT)
    FULL_CONCS(1:NVAR,full_counter+daycounter)=C(1:NVAR)
    full_counter=full_counter+daycounter+1.
    ! Are we at the end of a day?
    ! If so we need to 1) fiddle with the NOX to ensure it has the right concentrations see if we have reached a steady state
    IF (DAYCOUNTER*DT .GE. 24.*60.*60.) THEN
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

    print *, 'fractional difference aim 0 :', (fracdiff - 1e-3)
    IF (FRACDIFF .LE. 1e-3)  GOTO 1000    ! if system has converged end simulation


    DAYCOUNTER=0! reset the day counter to 0
    OLDFRACDIFF=FRACDIFF
    ENDIF

ENDIF


ENDDO time_loop
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

1000  print *, ' '//achar(27)//'[91m exit condition 1000 '//achar(27)//'[97m'
!if (CONSTRAIN_RUN .EQ. .true.) .AND. (OUTPUT_LAST .EQ. .false.)  print*, 'why not SaveOut(run_counter) work dammit'




    !NETCDF // WRITE TO FILE //
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    print*, 'special case if so, deallocate and allocate array'



    if(OUTPUT_LAST .eqv. .true.) then
        do I=1,DAYCOUNTER
        !not yet tested.
        output_s(I,1)= Jday*86400  + I*dt
        output_s(I,2)=Lat
        output_s(I,3)=Lon
        output_s(I,4)=Press
        output_s(I,5)=Temp
        output_s(I,6)=H2O
        output_s(I,7)=Cfactor

        output_s(I,8)=RO2
        output_s(I,9:)=(DIURNAL_NEW(1:NVAR,I))

        output_r(I,1)= Jday*86400  + I*dt
        output_r(I,2)=Lat
        output_r(I,3)=Lon
        output_r(I,4)=Press
        output_r(I,5)=Temp
        output_r(I,6)=H2O
        output_r(I,7)=Cfactor
        output_r(I,8:)=(DIURNAL_RATES(1:NREACT,I))
        enddo
    endif



    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !adjust for special cases


    CLOSE(10)
    CLOSE(12)



    close(output_unit)
    deallocate(output_s)
    deallocate(output_r)
    deallocate(s_names)
    deallocate(r_names)


    END PROGRAM driver
