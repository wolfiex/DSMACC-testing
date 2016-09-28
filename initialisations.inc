!!!!!Input arguments!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!open the init cons file. 
open(UNIT=21,FILE='Init_cons.dat')
READ(21,'(i10)') IntTime
! check if a special run has been selected.
if (INTTIME .LE. 0)  then
    CONSTRAIN_RUN=.TRUE.
    print*, 'reverting to legacy output.' 
    SAVE_LEGACY= .TRUE.
            
    WRITE (OUTPUT_UNIT,*) 'Integration to convergence'
    
    if (INTTIME .EQ. -1) then 
        INTTIME=int(4380*24.*60.*60.)
        OUTPUT_LAST=.FALSE.

        
    else if (INTTIME .EQ. -2) then      
        INTTIME=int(50*24.*60.*60.)
        OUTPUT_LAST=.TRUE.

    
    else;
        WRITE (OUTPUT_UNIT,*) 'Negative Integration Time \n &
        But not a special case'
        STOP
    endif
else
    
endif

runtimestep=int(Inttime / dt) !used for netcdf


!read species and concentrations
!number of read == 10000


READ(21,'(*(a15,x))') spec_name
READ(21,'(*(i15,x))') const_method 


if (line.gt.1) then !skip lines 
    do 133 i = 1,(line-1)
    133 read(21,*)
end if

!get required concentrations
READ (21,'(10000(e15.4,x))') concs
 close(21)


if (save_legacy) nc_set = 144 ! 1day 
if (nc_set .eq. 0)  nc_set = runtimestep

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!Variable Initialisation !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
allocate(output_s(1:nc_set, Nspec+10))
allocate(output_r(1:nc_set, Nreact+6))
allocate(s_names(Nspec+10))
allocate(r_names(Nreact+6))
output_s(:,:) = 0. 
output_r(:,:) = 0.
call initVal(concs)!initialise val;ues
M   = CFACTOR
O2 = 0.21 * CFACTOR
N2 = 0.78 * CFACTOR
tstart = (mod(jday,1.))*24.*60.*60. ! time start
tstart = tstart+LON/360.*24.*60.*60.!conv 2 localtime
tend = tstart + IntTime  !end time  
nc_counter=0                      


write (OUTPUT_UNIT,*) 'Initializing model ', counter
write (OUTPUT_UNIT,*) 'Starting Jday:',jday
write (OUTPUT_UNIT,*) 'Starting time:',tstart
write (OUTPUT_UNIT,*) 'Ending time:', tend
write (OUTPUT_UNIT,*) 'Time step:', dt
write (OUTPUT_UNIT,*) 'hvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhv'
write (OUTPUT_UNIT,*) 'Using TUV to calculate photolysis rates as a function of SZA'
alta=(1-(press/1013.25)**0.190263)*288.15/0.00198122*0.304800/1000.
write (OUTPUT_UNIT,*) 'Aerosol surface area', SAREA
write (OUTPUT_UNIT,*) 'Aerosol particle radius 1', RP1
write (OUTPUT_UNIT,*) 'Altitude =', alta
write (OUTPUT_UNIT,*) 'Pressure =', Press
write (OUTPUT_UNIT,*) 'Temperature =', Temp
write (OUTPUT_UNIT,*) 'Latitude =', Lat
write (OUTPUT_UNIT,*) 'Lon =', Lon
write (OUTPUT_UNIT,*) 'Local Time =', Tstart/(60.*60.)
write (OUTPUT_UNIT,*) 'SZA =',ZENANG(int(jday),Tstart/(60.*60.),lat)*180./(4*ATAN(1.))

if (o3col .eq. 0) then 
    o3col=260.
    write (OUTPUT_UNIT,*) 'Ozone column not specified using 260 Dobsons'
else
    write (OUTPUT_UNIT,*) 'Ozone column =', o3col
endif

if (albedo .eq. 0) then 
    albedo=0.1
    write (OUTPUT_UNIT,*) 'Albedo not specified using 0.1'
else
    write (OUTPUT_UNIT,*) 'Albedo =', albedo
endif       
!    Calculate the photolysis rates for the run
call set_up_photol(O3col,Albedo,alta,temp,bs,cs,ds,szas,svj_tj)
write (OUTPUT_UNIT,*) 'Photolysis rates calculated'
write (OUTPUT_UNIT,*) 'hvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhvhv'
time = tstart
OLDFRACDIFF=0.

! If NOx is being constrained calculate the total NOx in the model 
IF (CONSTRAIN_NOX) THEN 
    TNOX_OLD=0.
    TNOX_OLD=TNOX_OLD+sum(C(1:NVAR)*NOX(1:NVAR))
ENDIF

! Define the initial state of the model 
STARTSTATE(1:NVAR)=C(1:NVAR)
DIURNAL_OLD(:,:)=0.
! Calculate clear sky photolysis rates
JFACTNO2=1.
JFACTO1D=1.

! Update the rate constants
CALL Update_RCONST()
! Calcualte correction factors for the model photolysis rates
if (JO1D .NE. 0.) then
    if (J(1) .GT. 0.) JFACTO1D=JO1D/J(1)
    if (JNO2 .NE. 0.) JFACTO1D=JFACTNO2
endif

if (JNO2 .NE. 0.) then
    if (J(4) .GT. 0.) JFACTNO2=JNO2/J(4)
    if (JO1D .NE. 0.) JFACTNO2=JFACTO1D    
endif

write (OUTPUT_UNIT,*) 'JO1D Calc=', J(1)
write (OUTPUT_UNIT,*) 'JO1D Measre =', JO1D
write (OUTPUT_UNIT,*) 'Correction JO1D and JNO2 by', JFACTO1D,JFACTNO2

! Set up a counter to count the number time that the model has been run for 
Daycounter=0
full_counter=0


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!NETCDF INITIALISATIONS
print *, 'ncstart', nspec, nreact ,nvar

if (SAVE_LEGACY .eq. .false.) then
        ! netcdf 64bit does not work apparently so cannot handle large runs.
        ! for this the legacy format shall be used for constrained runs 

        !write
        call check(nf90_create( trim(counter)//'.nc', NF90_64BIT_OFFSET, ncid) )
        !def dims
        call check(nf90_def_dim(ncid, 'nspec', Nspec+10 , spec_id) )
        call check(nf90_def_dim(ncid, 'nrate', Nreact+6 , reac_id) )
        call check(nf90_def_dim(ncid, 'time', runtimestep+1 , dayid) ) !
        call check(nf90_def_dim(ncid, 'Char', 50 , char_id) )

        !def vars
        s_dimids =  (/dayid,spec_id/) !!! NETCDF USES C ORDER :. reverse
        r_dimids =  (/dayid,reac_id/) !!! NETCDF USES C ORDER :. reverse
        sh_dims =  (/char_id,spec_id/)
        rh_dims =  (/char_id,reac_id/)

        !rate ones
        call check(nf90_def_var(ncid, "Spec", NF90_DOUBLE, s_dimids, s_id) )
        call check(nf90_def_var(ncid, "Rate", NF90_DOUBLE, r_dimids, r_id) )
        call check(nf90_def_var(ncid, "reactions", NF90_char, rh_dims, rh_id) )
        call check(nf90_def_var(ncid, "species", NF90_char, sh_dims, sh_id) )

        print*,'check2'
        
        !end def
        call check(nf90_enddef(ncid))  

        print*, 'check3'
        
        !headers 
        s_names(:10) = (/'TIME','LAT','LON','PRESS','TEMP','H2O','M', 'JNO2FACT','JO1DFACT','RO2' /)
        s_names(11:) = SPC_NAMES(:)
        print*,'spc',size(s_names)
        r_names(1:6) = (/'TIME','LAT','LON','PRESS','TEMP','M'/)
        r_names(7:)= EQN_NAMES(:)
        print*,'rte',size(r_names)
        call check(nf90_put_var(ncid, sh_id, s_names(:) ))
        call check(nf90_put_var(ncid, rh_id, r_names(:) ))
        
        print*, 'check4'

end if 
print *, 'scmade'


    !previous dsmacc format
    if (SAVE_LEGACY) then 
        filename=trim(counter)//'_'//trim(mechanism)//'.spec'
        open(SPEC_UNIT, file=filename)
        filename=trim(counter)//'_'//trim(mechanism)//'.rate'
        open(RATE_UNIT, file=filename) 
        
        write (SPEC_UNIT,'(100000(a25,"!"))') 'TIME','LAT','LON','PRESS','TEMP','H2O'&
        ,'M', 'JNO2FACT','JO1DFACT','RO2', SPC_NAMES
        write (RATE_UNIT,'(100000(a50,"!"))') 'TIME','LAT','LON','PRESS','TEMP','M'&
        ,EQN_NAMES

         999 FORMAT(*(E24.16,"!"))
    end if 





