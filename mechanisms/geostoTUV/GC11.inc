SELECT CASE(jl)
    !geos
    !tuv
    CASE(  1) !O2 + hv = 2.000O 
       j(  1) =  seval(szabin,theta,tmp,tmp2,b,c,d)!O2 -> O + O

    CASE(  2) !O3 + hv = O + O2 
       j(  3) =  seval(szabin,theta,tmp,tmp2,b,c,d)!O3 -> O2 + O(3P)

    CASE(  3) !O3 + hv = O1D + O2 
       j(  2) =  seval(szabin,theta,tmp,tmp2,b,c,d)!O3 -> O2 + O(1D)

    CASE(  6) !NO + hv = O + N 
       j(357) =  seval(szabin,theta,tmp,tmp2,b,c,d)!NO -> N + O(3P)

    CASE(  7) !CH2O + hv = HO2 + H + CO 
       j( 23) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH2O -> H2 + CO

    CASE(  8) !CH2O + hv = H2 + CO 
       j( 23) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH2O -> H2 + CO

    CASE(  9) !H2O2 + hv = OH + OH 
       j(  5) =  seval(szabin,theta,tmp,tmp2,b,c,d)!H2O2 -> 2 OH

    CASE( 10) !MP + hv = CH2O + HO2 + OH 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 11) !NO2 + hv = NO + O 
       j(  6) =  seval(szabin,theta,tmp,tmp2,b,c,d)!NO2 -> NO + O(3P)

    CASE( 12) !NO3 + hv = NO2 + O 
       j(  8) =  seval(szabin,theta,tmp,tmp2,b,c,d)!NO3 -> NO2 + O(3P)

    CASE( 13) !NO3 + hv = NO + O2 
       j(  7) =  seval(szabin,theta,tmp,tmp2,b,c,d)!NO3 -> NO + O2

    CASE( 14) !N2O5 + hv = NO3 + NO2 
       j( 11) =  seval(szabin,theta,tmp,tmp2,b,c,d)!N2O5 -> NO3 + NO2

    CASE( 15) !HNO2 + hv = OH + NO 
       j( 12) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HNO2 -> OH + NO

    CASE( 16) !HNO3 + hv = OH + NO2 
       j( 13) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HNO3 -> OH + NO2

    CASE( 17) !HNO4 + hv = OH + NO3 
       j( 19) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HNO4 -> OH + NO3

    CASE( 18) !HNO4 + hv = HO2 + NO2 
       j( 18) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HNO4 -> HO2 + NO2

    CASE( 19) !ClNO3 + hv = Cl + NO3 
       j( 97) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClONO2 -> Cl + NO3

    CASE( 20) !ClNO3 + hv = ClO + NO2 
       j( 98) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClONO2 -> ClO + NO2

    CASE( 21) !ClNO2 + hv = Cl + NO2 
       j( 95) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClNO2 -> Cl + NO2

    CASE( 22) !Cl2 + hv = 2.000Cl 
       j( 86) =  seval(szabin,theta,tmp,tmp2,b,c,d)!Cl2 -> Cl + Cl

    CASE( 23) !Br2 + hv = 2.000Br 
       j(118) =  seval(szabin,theta,tmp,tmp2,b,c,d)!Br2 -> Br + Br

    CASE( 24) !HOCl + hv = Cl + OH 
       j( 93) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HOCl -> OH + Cl

    CASE( 25) !OClO + hv = ClO + O 
       j( 90) =  seval(szabin,theta,tmp,tmp2,b,c,d)!OClO -> Products

    CASE( 26) !Cl2O2 + hv = Cl + ClOO 
       j( 91) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClOOCl -> Cl + ClOO

    CASE( 27) !ClO + hv = Cl + O 
       j( 88) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClO -> Cl + O(3P)

    CASE( 28) !BrO + hv = Br + O 
       j(119) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrO -> Br + O

    CASE( 29) !BrNO3 + hv = Br + NO3 
       j(126) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrONO2 -> Br + NO3

    CASE( 30) !BrNO3 + hv = BrO + NO2 
       j(125) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrONO2 -> BrO + NO2

    CASE( 31) !BrNO2 + hv = Br + NO2 
       j(124) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrNO2 -> Br + NO2

    CASE( 32) !HOBr + hv = Br + OH 
       j(120) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HOBr -> OH + Br

    CASE( 33) !BrCl + hv = Br + Cl 
       j(127) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrCl -> Br + Cl

    CASE( 34) !OCS + hv = SO2 + CO 
       j(358) =  seval(szabin,theta,tmp,tmp2,b,c,d)!OCS -> CO + SO2

    CASE( 36) !N2O + hv = N2 + O1D 
       j(  9) =  seval(szabin,theta,tmp,tmp2,b,c,d)!N2O -> N2 + O(1D)

    CASE( 37) !CFC11 + hv = 3.000Cl 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 38) !CFC12 + hv = 2.000Cl 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 39) !CFC113 + hv = 3.000Cl 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 40) !CFC114 + hv = 2.000Cl 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 41) !CFC115 + hv = Cl 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 42) !CCl4 + hv = 4.000Cl 
       j( 99) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CCl4 -> Products

    CASE( 43) !CH3Cl + hv = MO2 + Cl 
       j(102) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3Cl -> Products

    CASE( 44) !CH3CCl3 + hv = 3.000Cl 
       j(103) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3CCl3 -> Products

    CASE( 45) !CH2Cl2 + hv = 2.000Cl 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 46) !HCFC22 + hv = 2.000Cl 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 47) !HCFC123 + hv = 2.000Cl 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 48) !HCFC141b + hv = 2.000Cl 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 49) !HCFC142b + hv = 2.000Cl 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 50) !CH3Br + hv = MO2 + Br 
       j(128) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3Br -> Products

    CASE( 51) !H1211 + hv = Cl + Br 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 53) !H1301 + hv = Br 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 54) !H2402 + hv = 2.000Br 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 55) !CH2Br2 + hv = 2.000Br 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 56) !CHBr3 + hv = 3.000Br 
       j(129) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CHBr3 -> Products

    CASE( 62) !ALD2 + hv = CH4 + CO 
       j( 25) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3CHO -> CH4 + CO

    CASE( 63) !MVK + hv = PRPE + CO 
       j( 63) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3COCH=CH2 -> C3H6 + CO

    CASE( 64) !MVK + hv = MCO3 + CH2O + CO + HO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 65) !MVK + hv = MO2 + RCO3 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 66) !MACR + hv = CO + HO2 + CH2O + MCO3 
       j(360) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MACR -> products

    CASE( 70) !RCHO + hv = ETO2 + HO2 + CO 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 71) !MGLY + hv = MCO3 + CO + HO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 72) !GLYX + hv = 2.000HO2 + 2.000CO 
       j( 70) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CHOCHO -> 2 HO2 + 2 CO

    CASE( 73) !GLYX + hv = H2 + 2.000CO 
       j( 71) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CHOCHO -> H2 + 2 CO

    CASE( 74) !GLYX + hv = CH2O + CO 
       j( 72) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CHOCHO -> CH2O + CO

    CASE( 75) !HAC + hv = MCO3 + CH2O + HO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 76) !ACET + hv = MCO3 + MO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 77) !ACET + hv = 2.000MO2 + CO 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 78) !INPN + hv = OH + HO2 + RCHO + NO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 79) !PRPN + hv = OH + HO2 + RCHO + NO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 80) !ETP + hv = OH + HO2 + ALD2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 81) !RA3P + hv = OH + HO2 + RCHO 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 82) !RB3P + hv = OH + HO2 + ACET 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 83) !R4P + hv = OH + HO2 + RCHO 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 84) !PP + hv = OH + HO2 + ALD2 + CH2O 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 85) !RP + hv = OH + HO2 + ALD2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 88) !ISNP + hv = OH + HO2 + RCHO + NO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 91) !MAOP + hv = OH + CH2O + MCO3 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 93) !MVKN + hv = GLYC + NO2 + MCO3 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 94) !ISOPNB + hv = HC5 + NO2 + HO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 95) !ISOPND + hv = HC5 + NO2 + HO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 96) !PROPNN + hv = CH2O + NO2 + CO + MO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 97) !ATOOH + hv = OH + CH2O + MCO3 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE( 99) !MAP + hv = OH + MO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(100) !SO4 + hv = SO2 + 2.000OH 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(102) !ClOO + hv = Cl + O2 
       j( 89) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClOO -> Products

    CASE(104) !MPN + hv = CH2O + NO3 + HO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(105) !MPN + hv = MO2 + NO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(106) !PIP + hv = RCHO + OH + HO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(108) !ETHLN + hv = NO2 + CH2O + CO + HO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(109) !DHDC + hv = MGLY + GLYX + 2.000OH 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(112) !MONITS + hv = MEK + NO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(113) !MONITU + hv = RCHO + NO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(114) !HONIT + hv = HAC + NO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(115) !I2 + hv = 2.000I 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(116) !HOI + hv = I + OH 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(117) !IO + hv = I + O 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(118) !OIO + hv = I + O2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(119) !INO + hv = I + NO 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(120) !IONO + hv = I + NO2 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(121) !IONO2 + hv = I + NO3 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(122) !I2O2 + hv = I + OIO 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(123) !CH3I + hv = I 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(124) !CH2I2 + hv = 2.000I 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(125) !CH2ICl + hv = I + Cl 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(126) !CH2IBr + hv = I + Br 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(127) !I2O4 + hv = 2.000OIO 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(128) !I2O3 + hv = OIO + IO 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(129) !IBr + hv = I + Br 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

    CASE(130) !ICl + hv = I + Cl 
       0 
!j() =  seval(szabin,theta,tmp,tmp2,b,c,d)!unknown

