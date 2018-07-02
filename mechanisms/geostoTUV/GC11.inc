SELECT CASE(jl)
    !geos
    !tuv
    CASE(  1) !O2 -> O + O
       j(  1) =  seval(szabin,theta,tmp,tmp2,b,c,d)!O2 + hv = 2.000O 

    CASE(  3) !O3 -> O2 + O(3P)
       j(  2) =  seval(szabin,theta,tmp,tmp2,b,c,d)!O3 + hv = O + O2 

    CASE(  2) !O3 -> O2 + O(1D)
       j(  3) =  seval(szabin,theta,tmp,tmp2,b,c,d)!O3 + hv = O1D + O2 

    CASE(326) !NO -> N + O(3P)
       j(  6) =  seval(szabin,theta,tmp,tmp2,b,c,d)!NO + hv = O + N 

!CASE() !unknown
!j(  7) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH2O + hv = HO2 + H + CO 

    CASE( 23) !CH2O -> H2 + CO
       j(  8) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH2O + hv = H2 + CO 

    CASE(  5) !H2O2 -> 2 OH
       j(  9) =  seval(szabin,theta,tmp,tmp2,b,c,d)!H2O2 + hv = OH + OH 

!CASE() !unknown
!j( 10) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MP + hv = CH2O + HO2 + OH 

    CASE(  6) !NO2 -> NO + O(3P)
       j( 11) =  seval(szabin,theta,tmp,tmp2,b,c,d)!NO2 + hv = NO + O 

    CASE(  8) !NO3 -> NO2 + O(3P)
       j( 12) =  seval(szabin,theta,tmp,tmp2,b,c,d)!NO3 + hv = NO2 + O 

    CASE(  7) !NO3 -> NO + O2
       j( 13) =  seval(szabin,theta,tmp,tmp2,b,c,d)!NO3 + hv = NO + O2 

    CASE( 11) !N2O5 -> NO3 + NO2
       j( 14) =  seval(szabin,theta,tmp,tmp2,b,c,d)!N2O5 + hv = NO3 + NO2 

    CASE( 12) !HNO2 -> OH + NO
       j( 15) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HNO2 + hv = OH + NO 

    CASE( 13) !HNO3 -> OH + NO2
       j( 16) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HNO3 + hv = OH + NO2 

    CASE( 19) !HNO4 -> OH + NO3
       j( 17) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HNO4 + hv = OH + NO3 

    CASE( 18) !HNO4 -> HO2 + NO2
       j( 18) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HNO4 + hv = HO2 + NO2 

    CASE( 96) !ClONO2 -> Cl + NO3
       j( 19) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClNO3 + hv = Cl + NO3 

    CASE( 97) !ClONO2 -> ClO + NO2
       j( 20) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClNO3 + hv = ClO + NO2 

    CASE( 94) !ClNO2 -> Cl + NO2
       j( 21) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClNO2 + hv = Cl + NO2 

    CASE( 85) !Cl2 -> Cl + Cl
       j( 22) =  seval(szabin,theta,tmp,tmp2,b,c,d)!Cl2 + hv = 2.000Cl 

    CASE(117) !Br2 -> Br + Br
       j( 23) =  seval(szabin,theta,tmp,tmp2,b,c,d)!Br2 + hv = 2.000Br 

    CASE( 92) !HOCl -> OH + Cl
       j( 24) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HOCl + hv = Cl + OH 

    CASE( 89) !OClO -> Products
       j( 25) =  seval(szabin,theta,tmp,tmp2,b,c,d)!OClO + hv = ClO + O 

    CASE( 90) !ClOOCl -> Cl + ClOO
       j( 26) =  seval(szabin,theta,tmp,tmp2,b,c,d)!Cl2O2 + hv = Cl + ClOO 

    CASE( 87) !ClO -> Cl + O(3P)
       j( 27) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClO + hv = Cl + O 

    CASE(118) !BrO -> Br + O
       j( 28) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrO + hv = Br + O 

    CASE(125) !BrONO2 -> Br + NO3
       j( 29) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrNO3 + hv = Br + NO3 

    CASE(124) !BrONO2 -> BrO + NO2
       j( 30) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrNO3 + hv = BrO + NO2 

    CASE(123) !BrNO2 -> Br + NO2
       j( 31) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrNO2 + hv = Br + NO2 

    CASE(119) !HOBr -> OH + Br
       j( 32) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HOBr + hv = Br + OH 

    CASE(126) !BrCl -> Br + Cl
       j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrCl + hv = Br + Cl 

    CASE(327) !OCS -> CO + SO2
       j( 34) =  seval(szabin,theta,tmp,tmp2,b,c,d)!OCS + hv = SO2 + CO 

    CASE(  9) !N2O -> N2 + O(1D)
       j( 36) =  seval(szabin,theta,tmp,tmp2,b,c,d)!N2O + hv = N2 + O1D 

!CASE() !unknown
!j( 37) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CFC11 + hv = 3.000Cl 

!CASE() !unknown
!j( 38) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CFC12 + hv = 2.000Cl 

!CASE() !unknown
!j( 39) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CFC113 + hv = 3.000Cl 

!CASE() !unknown
!j( 40) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CFC114 + hv = 2.000Cl 

!CASE() !unknown
!j( 41) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CFC115 + hv = Cl 

    CASE( 98) !CCl4 -> Products
       j( 42) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CCl4 + hv = 4.000Cl 

    CASE(101) !CH3Cl -> Products
       j( 43) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3Cl + hv = MO2 + Cl 

    CASE(102) !CH3CCl3 -> Products
       j( 44) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3CCl3 + hv = 3.000Cl 

!CASE() !unknown
!j( 45) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH2Cl2 + hv = 2.000Cl 

!CASE() !unknown
!j( 46) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HCFC22 + hv = 2.000Cl 

!CASE() !unknown
!j( 47) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HCFC123 + hv = 2.000Cl 

!CASE() !unknown
!j( 48) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HCFC141b + hv = 2.000Cl 

!CASE() !unknown
!j( 49) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HCFC142b + hv = 2.000Cl 

    CASE(127) !CH3Br -> Products
       j( 50) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3Br + hv = MO2 + Br 

!CASE() !unknown
!j( 51) =  seval(szabin,theta,tmp,tmp2,b,c,d)!H1211 + hv = Cl + Br 

!CASE() !unknown
!j( 53) =  seval(szabin,theta,tmp,tmp2,b,c,d)!H1301 + hv = Br 

!CASE() !unknown
!j( 54) =  seval(szabin,theta,tmp,tmp2,b,c,d)!H2402 + hv = 2.000Br 

!CASE() !unknown
!j( 55) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH2Br2 + hv = 2.000Br 

    CASE(128) !CHBr3 -> Products
       j( 56) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CHBr3 + hv = 3.000Br 

    CASE( 25) !CH3CHO -> CH4 + CO
       j( 62) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ALD2 + hv = CH4 + CO 

!CASE() !unknown
!j( 63) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MVK + hv = PRPE + CO 

!CASE() !unknown
!j( 64) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MVK + hv = MCO3 + CH2O + CO + HO2 

!CASE() !unknown
!j( 65) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MVK + hv = MO2 + RCO3 

    CASE(329) !MACR -> products
       j( 66) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MACR + hv = CO + HO2 + CH2O + MCO3 

!CASE() !unknown
!j( 70) =  seval(szabin,theta,tmp,tmp2,b,c,d)!RCHO + hv = ETO2 + HO2 + CO 

!CASE() !unknown
!j( 71) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MGLY + hv = MCO3 + CO + HO2 

    CASE( 70) !CHOCHO -> 2 HO2 + 2 CO
       j( 72) =  seval(szabin,theta,tmp,tmp2,b,c,d)!GLYX + hv = 2.000HO2 + 2.000CO 

    CASE( 71) !CHOCHO -> H2 + 2 CO
       j( 73) =  seval(szabin,theta,tmp,tmp2,b,c,d)!GLYX + hv = H2 + 2.000CO 

    CASE( 72) !CHOCHO -> CH2O + CO
       j( 74) =  seval(szabin,theta,tmp,tmp2,b,c,d)!GLYX + hv = CH2O + CO 

!CASE() !unknown
!j( 75) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HAC + hv = MCO3 + CH2O + HO2 

!CASE() !unknown
!j( 76) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ACET + hv = MCO3 + MO2 

!CASE() !unknown
!j( 77) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ACET + hv = 2.000MO2 + CO 

!CASE() !unknown
!j( 78) =  seval(szabin,theta,tmp,tmp2,b,c,d)!INPN + hv = OH + HO2 + RCHO + NO2 

!CASE() !unknown
!j( 79) =  seval(szabin,theta,tmp,tmp2,b,c,d)!PRPN + hv = OH + HO2 + RCHO + NO2 

!CASE() !unknown
!j( 80) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ETP + hv = OH + HO2 + ALD2 

!CASE() !unknown
!j( 81) =  seval(szabin,theta,tmp,tmp2,b,c,d)!RA3P + hv = OH + HO2 + RCHO 

!CASE() !unknown
!j( 82) =  seval(szabin,theta,tmp,tmp2,b,c,d)!RB3P + hv = OH + HO2 + ACET 

!CASE() !unknown
!j( 83) =  seval(szabin,theta,tmp,tmp2,b,c,d)!R4P + hv = OH + HO2 + RCHO 

!CASE() !unknown
!j( 84) =  seval(szabin,theta,tmp,tmp2,b,c,d)!PP + hv = OH + HO2 + ALD2 + CH2O 

!CASE() !unknown
!j( 85) =  seval(szabin,theta,tmp,tmp2,b,c,d)!RP + hv = OH + HO2 + ALD2 

!CASE() !unknown
!j( 88) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ISNP + hv = OH + HO2 + RCHO + NO2 

!CASE() !unknown
!j( 91) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MAOP + hv = OH + CH2O + MCO3 

!CASE() !unknown
!j( 93) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MVKN + hv = GLYC + NO2 + MCO3 

!CASE() !unknown
!j( 94) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ISOPNB + hv = HC5 + NO2 + HO2 

!CASE() !unknown
!j( 95) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ISOPND + hv = HC5 + NO2 + HO2 

!CASE() !unknown
!j( 96) =  seval(szabin,theta,tmp,tmp2,b,c,d)!PROPNN + hv = CH2O + NO2 + CO + MO2 

!CASE() !unknown
!j( 97) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ATOOH + hv = OH + CH2O + MCO3 

!CASE() !unknown
!j( 99) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MAP + hv = OH + MO2 

!CASE() !unknown
!j(100) =  seval(szabin,theta,tmp,tmp2,b,c,d)!SO4 + hv = SO2 + 2.000OH 

    CASE( 88) !ClOO -> Products
       j(102) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClOO + hv = Cl + O2 

!CASE() !unknown
!j(104) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MPN + hv = CH2O + NO3 + HO2 

!CASE() !unknown
!j(105) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MPN + hv = MO2 + NO2 

!CASE() !unknown
!j(106) =  seval(szabin,theta,tmp,tmp2,b,c,d)!PIP + hv = RCHO + OH + HO2 

!CASE() !unknown
!j(108) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ETHLN + hv = NO2 + CH2O + CO + HO2 

!CASE() !unknown
!j(109) =  seval(szabin,theta,tmp,tmp2,b,c,d)!DHDC + hv = MGLY + GLYX + 2.000OH 

!CASE() !unknown
!j(112) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MONITS + hv = MEK + NO2 

!CASE() !unknown
!j(113) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MONITU + hv = RCHO + NO2 

!CASE() !unknown
!j(114) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HONIT + hv = HAC + NO2 

!CASE() !unknown
!j(115) =  seval(szabin,theta,tmp,tmp2,b,c,d)!I2 + hv = 2.000I 

!CASE() !unknown
!j(116) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HOI + hv = I + OH 

!CASE() !unknown
!j(117) =  seval(szabin,theta,tmp,tmp2,b,c,d)!IO + hv = I + O 

!CASE() !unknown
!j(118) =  seval(szabin,theta,tmp,tmp2,b,c,d)!OIO + hv = I + O2 

!CASE() !unknown
!j(119) =  seval(szabin,theta,tmp,tmp2,b,c,d)!INO + hv = I + NO 

!CASE() !unknown
!j(120) =  seval(szabin,theta,tmp,tmp2,b,c,d)!IONO + hv = I + NO2 

!CASE() !unknown
!j(121) =  seval(szabin,theta,tmp,tmp2,b,c,d)!IONO2 + hv = I + NO3 

!CASE() !unknown
!j(122) =  seval(szabin,theta,tmp,tmp2,b,c,d)!I2O2 + hv = I + OIO 

!CASE() !unknown
!j(123) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3I + hv = I 

!CASE() !unknown
!j(124) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH2I2 + hv = 2.000I 

!CASE() !unknown
!j(125) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH2ICl + hv = I + Cl 

!CASE() !unknown
!j(126) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH2IBr + hv = I + Br 

!CASE() !unknown
!j(127) =  seval(szabin,theta,tmp,tmp2,b,c,d)!I2O4 + hv = 2.000OIO 

!CASE() !unknown
!j(128) =  seval(szabin,theta,tmp,tmp2,b,c,d)!I2O3 + hv = OIO + IO 

!CASE() !unknown
!j(129) =  seval(szabin,theta,tmp,tmp2,b,c,d)!IBr + hv = I + Br 

!CASE() !unknown
!j(130) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ICl + hv = I + Cl 

END SELECT