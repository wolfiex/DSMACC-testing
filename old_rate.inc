    ! ************************************************************************
    ! define generic reaction rates.
    ! ************************************************************************

    ! constants used in calculation of reaction rates
    !M  = 2.55E+19
    N2 = 0.79*M
    O2 = 0.2095*M

    ! kro2no : ro2      + no      = ro      + no2
    !        : ro2      + no      = rono2
    ! mcm 2009
    kro2no    = 2.54d-12*EXP(360.0/temp)

    ! kro2ho2: ro2      + ho2     = rooh    + o2
    ! mcm protocol [1997]
    kro2ho2   = 2.91d-13*EXP(1300.0/temp)

    ! kapho2 : rcoo2    + ho2     = products
    ! mcm protocol [1997]
    kapho2    = 4.30d-13*EXP(1040.0/temp)

    ! kapno  : rcoo2    + no      = products
    ! mej [1998]
    kapno = 8.10d-12*EXP(270.0/temp)

    ! kro2no3: ro2      + no3     = products
    ! mcm protocol [1997]
    kro2no3   = 2.50d-12

    ! kno3al : no3      + rcho    = rcoo2   + hno3
    ! mcm protocol [1997]
    kno3al    = 1.44d-12*EXP(-1862.0/temp)

    ! kdec   : ro                 = products
    ! mcm protocol [1997]
    kdec      = 1.00d+06
    krosec = 1.50e-14*EXP(-200.0/temp)

    kalkoxy=6.00d-14*EXP(-550.0/temp)*o2
    kalkpxy=1.50d-14*EXP(-200.0/temp)*o2

    ! kch3o2
    ! mcm protocol [v3.2]
    kch3o2    = 1.03d-13*EXP(365.0/temp)

    ! k298ch3o2
    ! mcm protocol [v3.2]
    k298ch3o2    = 3.5d-13


    ! -------------------------------------------------------------------
    ! complex reactions
    ! -------------------------------------------------------------------

    ! kfpan kbpan
    ! formation and decomposition of pan and ppn
    ! iupac 2001
    kc0     = 2.70d-28*m*(temp/300.0)**(-7.1)
    kci     = 1.21d-11*(temp/300.0)**(-0.9)
    krc     = kc0/kci
    fcc     = 0.30
    nc      = 0.75-1.27*(dlog10(fcc))
    fc      = 10**(dlog10(fcc)/(1+(dlog10(krc)/nc)**2))
    kfpan   = (kc0*kci)*fc/(kc0+kci)

    kd0     = 4.90d-03*m*EXP(-12100.0/temp)
    kdi     = 5.40d+16*EXP(-13830.0/temp)
    krd     = kd0/kdi
    fcd     = 0.30
    ncd     = 0.75-1.27*(dlog10(fcd))
    fd      = 10**(dlog10(fcd)/(1+(dlog10(krd)/ncd)**2))
    kbpan   = (kd0*kdi)*fd/(kd0+kdi)
    
    kppn0   = 1.70d-03*m*EXP(-11280.0/temp)
    kppni   = 8.30d+16*EXP(-13940.0/temp)
    krppn   = kppn0/kppni
    fcppn   = 0.36
    ncppn   = 0.75-1.27*(dlog10(fcppn))
    fppn    = 10**(dlog10(fcppn)/(1+(dlog10(krppn)/ncppn)**2))
    kbppn   = (kppn0*kppni)*fppn/(kppn0+kppni)

    ! kmt01  : o        + no      = no2
    ! iupac 1997, 2006 gives Fc=0.85, otherwise the same
    k10     = 1.00d-31*m*(temp/300.0)**(-1.6)

    k1i     = 3.00d-11*(temp/300.0)**(0.3)
    kr1     = k10/k1i
    fc1     = EXP(-temp/1850.0)
    f1      = 10**(dlog10(fc1)/(1+(dlog10(kr1))**2))
    kmt01   = (k10*k1i)*f1/(k10+k1i)

    ! kmt02  : o        + no2     = no3
    ! iupac 2006
    k20     = 1.30d-31*m*(temp/300.0)**(-1.5)
    k2i     = 2.30d-11*(temp/300.0)**(0.24)
    kr2     = k20/k2i
    fc2     = 0.6
    f2      = 10**(dlog10(fc2)/(1+(dlog10(kr2))**2))
    kmt02   = (k20*k2i)*f2/(k20+k2i)

    ! kmt03  : no2      + no3     = n2o5
    ! iupac 2006
    k30     = 3.60d-30*m*(temp/300.0)**(-4.1)
    k3i     = 1.90d-12*(temp/300.0)**(0.2)
    kr3     = k30/k3i
    fc3     = 0.35
    f3      = 10**(dlog10(fc3)/(1+(dlog10(kr3))**2))
    kmt03   = (k30*k3i)*f3/(k30+k3i)

    ! kmt04  : n2o5               = no2     + no3
    ! iupac 2006
    k40     = 1.30d-03*m*(temp/300.0)**(-3.5)*EXP(-11000.0/temp)
    k4i     = 9.70d+14*(temp/300.0)**(0.1)*EXP(-11080.0/temp)
    kr4     = k40/k4i
    fc4     = 0.35
    f4      = 10**(dlog10(fc4)/(1+(dlog10(kr4))**2))
    kmt04   = (k40*k4i)*f4/(k40+k4i)

    ! kmt05  : oh       + co(+o2) = ho2     + co2
    ! iupac 2006
    kmt05  = (1 + m/4.2d19)

    ! kmt06  : ho2      + ho2     = h2o2    + o2
    ! water enhancement factor
    ! iupac 1992

    kmt06  = 1 + (1.40d-21*EXP(2200.0/temp)*h2o)

    ! kmt06  = 1 + (2.00d-25*EXP(4670.0/temp)*h2o)
    ! S+R 2005 values

    ! kmt07  : oh       + no      = hono

    ! iupac 2006
    k70     = 7.40d-31*m*(temp/300.0)**(-2.4)
    k7i     = 3.30d-11*(temp/300.0)**(-0.3)
    kr7     = k70/k7i
    fc7     = 0.81
    f7      = 10**(dlog10(fc7)/(1+(dlog10(kr7))**2))
    kmt07   = (k70*k7i)*f7/(k70+k7i)

    ! kmt08  : oh       + no2     = hno3

    ! iupac 2006
    k80     = 3.30d-30*m*(temp/300.0)**(-3.0)
    k8i     = 4.10d-11
    kr8     = k80/k8i
    fc8     = 0.4
    f8      = 10**(dlog10(fc8)/(1+(dlog10(kr8))**2))
    kmt08   = (k80*k8i)*f8/(k80+k8i)

    ! kmt09  : ho2      + no2     = ho2no2
    ! iupac 1997

    k90     = 1.80d-31*m*(temp/300.0)**(-3.2)
    ! k90     = 2.0d-31*m*(temp/300.0)**(-3.4)
    k9i     = 4.70d-12
    ! k9i     = 2.90d-12*(temp/300.0)**(-1.1)
    kr9     = k90/k9i
    fc9     = 0.6
    f9      = 10**(dlog10(fc9)/(1+(dlog10(kr9))**2))
    kmt09   = (k90*k9i)*f9/(k90+k9i)

    ! kmt10  : ho2no2             = ho2     + no2
    ! iupac 1997

    k100     = 4.10d-05*m*EXP(-10650.0/temp)
    k10i     = 5.70d+15*EXP(-11170.0/temp)
    kr10     = k100/k10i
    fc10     = 0.5
    f10      = 10**(dlog10(fc10)/(1+(dlog10(kr10))**2))
    kmt10    = (k100*k10i)*f10/(k100+k10i)

    ! kmt10    = kmt09/(3.9d-27*EXP(10125/temp))

    ! kmt11  : oh       + hno3    = h2o     + no3
    ! iupac 2006

    k1     = 2.40d-14*EXP(460.0/temp)
    k3     = 6.50d-34*EXP(1335.0/temp)
    k4     = 2.70d-17*EXP(2199.0/temp)
    k2     = (k3*m)/(1+(k3*m/k4))
    kmt11  = k1 + k2

    ! kmt12 iupac 2006

    k0 = 4.50d-31*((temp/300.0)**(-3.9))*m
    ki = 1.30d-12*((temp/300.0)**(-0.7))
    fc = 0.525
    x = 1.0d+0
    ssign = dsign(x,(k0-ki))
    f=10**(dlog10(fc)/(1.0+(ssign*(ABS(dlog10(k0/ki)))**(2.0))))
    kmt12=(k0*ki*f)/(k0+ki)

    ! kmt13  : ch3o2    + no2     = ch3o2no2
    ! iupac 2006

    k130     = 2.50d-30*((temp/300.0)**(-5.5))*m
    k13i     = 1.80d-11
    kr13     = k130/k13i
    fc13     = 0.36
    f13      = 10**(dlog10(fc13)/(1+(dlog10(kr13))**2))
    kmt13    = (k130*k13i)*f13/(k130+k13i)

    ! kmt14  : ch3o2no2           = ch3o2   + no2
    ! iupac 2006

    k140     = 9.00d-05*EXP(-9690.0/temp)*m
    k14i     = 1.10d+16*EXP(-10560.0/temp)
    kr14     = k140/k14i
    fc14     = 0.6
    f14      = 10**(dlog10(fc14)/(1+(dlog10(kr14))**2))
    kmt14    = (k140*k14i)*f14/(k140+k14i)

    ! kmt15 iupac 2006

    k0=8.60d-29*((temp/300.0)**(-3.1))*m
    ki=9.00d-12*((temp/300.0)**(-0.85))
    fc=0.48
    x = 1.0d+0
    ssign = dsign(x,(k0-ki))
    f=10**(dlog10(fc)/(1.0+(ssign*(ABS(dlog10(k0/ki)))**(2.0))))
    kmt15=(k0*ki*f)/(k0+ki)

    ! kmt16  :  oh  +  c3h6
    ! iupac 2006

    k160     = 8.00d-27*((temp/300.0)**(-3.5))*m
    k16i     = 3.00d-11*((temp/300.0)**(-1.0))
    kr16     = k160/k16i
    fc16     = 0.5
    f16      = 10**(dlog10(fc16)/(1+(dlog10(kr16))**2))
    kmt16    = (k160*k16i)*f16/(k160+k16i)

    ! kmt17 iupac 2006

    k0 = 5.00d-30*((temp/300.0)**(-1.5))*m
    ki = 1.00d-12
    fc = 0.37
    x = 1.0d+0
    ssign = dsign(x,(k0-ki))
    f=10**(dlog10(fc)/(1.0+(ssign*(ABS(dlog10(k0/ki)))**(2.0))))
    kmt17=(k0*ki*f)/(k0+ki)

    !       mcm 2001

    kroprim  = 3.70d-14*EXP(-460.0/temp)
    krosec   = 1.80d-14*EXP(-260.0/temp)
