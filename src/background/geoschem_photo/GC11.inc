
SELECT CASE(jl)

    CASE(  1) !O2 -> O + O
        j(  1) =  seval(szabin,theta,tmp,tmp2,b,c,d)!O2 -> O + O
        
    CASE(  2) !O3 -> O + O2
        j(  3) =  seval(szabin,theta,tmp,tmp2,b,c,d)!O3 -> O2 + O(3P)
        
    CASE(  3) !O3 -> O(1D) + O2
        j(  2) =  seval(szabin,theta,tmp,tmp2,b,c,d)!O3 -> O2 + O(1D)
        
    CASE(  5) !HO2 -> O + OH
        j(  4) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HO2 -> OH + O
        
    CASE(  6) !NO -> N + O
        j(358) =  seval(szabin,theta,tmp,tmp2,b,c,d)!NO -> N + O(3P)
        
    CASE(  7) !CH2O -> CO + H + HO2
        j( 22) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH2O -> H + HCO
        
    CASE(  8) !CH2O -> CO + H2
        j( 23) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH2O -> H2 + CO
        
    CASE(  9) !H2O2 -> OH + OH
        j(  5) =  seval(szabin,theta,tmp,tmp2,b,c,d)!H2O2 -> 2 OH
        
    CASE( 10) !MP -> CH2O + HO2 + OH
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE( 11) !NO2 -> NO + O
        j(  6) =  seval(szabin,theta,tmp,tmp2,b,c,d)!NO2 -> NO + O(3P)
        
    CASE( 12) !NO3 -> NO2 + O
        j(  8) =  seval(szabin,theta,tmp,tmp2,b,c,d)!NO3 -> NO2 + O(3P)
        
    CASE( 13) !NO3 -> NO + O2
        j(  7) =  seval(szabin,theta,tmp,tmp2,b,c,d)!NO3 -> NO + O2
        
    CASE( 14) !N2O5 -> NO2 + NO3
        j( 11) =  seval(szabin,theta,tmp,tmp2,b,c,d)!N2O5 -> NO3 + NO2
        
    CASE( 15) !HNO2 -> NO + OH
        j( 12) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HNO2 -> OH + NO
        
    CASE( 16) !HNO3 -> NO2 + OH
        j( 13) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HNO3 -> OH + NO2
        
    CASE( 17) !HNO4 -> NO3 + OH
        j( 19) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HNO4 -> OH + NO3
        
    CASE( 18) !HNO4 -> HO2 + NO2
        j( 18) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HNO4 -> HO2 + NO2
        
    CASE( 19) !ClNO3 -> Cl + NO3
        j(100) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClONO2 -> Cl + NO3
        
    CASE( 20) !ClNO3 -> ClO + NO2
        j(101) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClONO2 -> ClO + NO2
        
    CASE( 21) !ClNO2 -> Cl + NO2
        j( 98) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClNO2 -> Cl + NO2
        
    CASE( 22) !Cl2 -> Cl + Cl
        j( 89) =  seval(szabin,theta,tmp,tmp2,b,c,d)!Cl2 -> Cl + Cl
        
    CASE( 23) !Br2 -> Br + Br
        j(121) =  seval(szabin,theta,tmp,tmp2,b,c,d)!Br2 -> Br + Br
        
    CASE( 24) !HOCl -> Cl + OH
        j( 96) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HOCl -> OH + Cl
        
    CASE( 25) !OClO -> ClO + O
        j( 93) =  seval(szabin,theta,tmp,tmp2,b,c,d)!OClO -> Products
        
    CASE( 26) !Cl2O2 -> Cl + Cl + O2
        j( 94) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClOOCl -> Cl + ClOO
        
    CASE( 27) !ClO -> Cl + O
        j( 91) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClO -> Cl + O(3P)
        
    CASE( 28) !BrO -> Br + O
        j(122) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrO -> Br + O
        
    CASE( 29) !BrNO3 -> Br + NO3
        j(129) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrONO2 -> Br + NO3
        
    CASE( 30) !BrNO3 -> BrO + NO2
        j(128) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrONO2 -> BrO + NO2
        
    CASE( 31) !BrNO2 -> Br + NO2
        j(127) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrNO2 -> Br + NO2
        
    CASE( 32) !HOBr -> Br + OH
        j(123) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HOBr -> OH + Br
        
    CASE( 33) !BrCl -> Br + Cl
        j(130) =  seval(szabin,theta,tmp,tmp2,b,c,d)!BrCl -> Br + Cl
        
    CASE( 34) !OCS -> CO + SO2
        j(359) =  seval(szabin,theta,tmp,tmp2,b,c,d)!OCS -> CO + SO2
        
    CASE( 36) !N2O -> N2 + O
        j(  9) =  seval(szabin,theta,tmp,tmp2,b,c,d)!N2O -> N2 + O(1D)
        
    CASE( 37) !CFC11 -> Cl + PRODUCTS
        j(119) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CF3CF2CHCl2 (HCFC-225ca) -> Products
        
    CASE( 38) !CFC12 -> Cl + PRODUCTS
        j(110) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CCl2F2 (CFC-12) -> Products
        
    CASE( 39) !CFC113 -> Cl + PRODUCTS
        j(111) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CF2ClCFCl2 (CFC-113) -> Products
        
    CASE( 40) !CFC114 -> Cl + PRODUCTS
        j(112) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CF2ClCF2Cl (CFC-114) -> Products
        
    CASE( 41) !CFC115 -> Cl + PRODUCTS
        j(113) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CF3CF2Cl (CFC-115) -> Products
        
    CASE( 42) !CCl4 -> Cl + PRODUCTS
        j(102) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CCl4 -> Products
        
    CASE( 43) !CH3Cl -> Cl + PRODUCTS
        j(105) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3Cl -> Products
        
    CASE( 44) !CH3CCl3 -> Cl + PRODUCTS
        j(106) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3CCl3 -> Products
        
    CASE( 47) !HCFC123 -> Cl + PRODUCTS
        j(115) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CF3CHCl2 (HCFC-123) -> Products
        
    CASE( 48) !HCFC141b -> Cl + PRODUCTS
        j(117) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3CFCl2 (HCFC-141b) -> Products
        
    CASE( 49) !HCFC142b -> Cl + PRODUCTS
        j(118) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3CF2Cl (HCFC-142b) -> Products
        
    CASE( 50) !CH3Br -> Br + PRODUCTS
        j(131) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3Br -> Products
        
    CASE( 51) !H1211 -> Br + PRODUCTS
        j(132) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CHBr3 -> Products
        
    CASE( 53) !H1301 -> Br + PRODUCTS
        j(135) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CF3Br (Halon-1301) -> Products
        
    CASE( 54) !H2402 -> Br + PRODUCTS
        j(136) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CF2BrCF2Br (Halon-2402) -> Products
        
    CASE( 55) !CH2Br2 -> Br + PRODUCTS
        j(362) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH2Br2 -> CH2Br + Br
        
    CASE( 56) !CHBr3 -> Br + PRODUCTS
        j(132) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CHBr3 -> Products
        
    CASE( 59) !PAN -> CH3C(O)O2 + NO2
        j(333) =  seval(szabin,theta,tmp,tmp2,b,c,d)!PAN -> RCO(OO) + NO2
        
    CASE( 61) !ALD2 -> CH3 + HCO
        j( 24) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3CHO -> CH3 + HCO
        
    CASE( 62) !ALD2 -> CH4 + CO
        j( 24) = 0.01 *  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3CHO -> CH3 + HCO
        
    CASE( 63) !MVK -> CO + PRPE
        j( 63) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3COCH=CH2 -> C3H6 + CO
        
    CASE( 64) !MVK -> CH2O + CO + HO2 + MCO3
        j( 62) = 0.5 *  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3COCH=CH2 -> C2H3 + CH3CO
        
    CASE( 65) !MVK -> MO2 + RCO3
        j( 62) = 0.5 *  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3COCH=CH2 -> C2H3 + CH3CO
        
    CASE( 66) !MACR -> CH2O + CO + HO2 + MCO3
        j(361) =  seval(szabin,theta,tmp,tmp2,b,c,d)!MACR -> products
        
    CASE( 68) !GLYC -> CH2O + CO + HO2 + MOH + OH
        j( 64) =  seval(szabin,theta,tmp,tmp2,b,c,d)!HOCH2CHO -> CH2OH + HCO
        
    CASE( 69) !MEK -> EtO2 + MCO3 + MO2 + RCO3
        j( 70) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3COCH2CH3 -> CH3CO + CH2CH3
        
    CASE( 70) !RCHO -> CO + EtO2 + HO2
        j( 28) =  seval(szabin,theta,tmp,tmp2,b,c,d)!C2H5CHO -> C2H5 + HCO
        
    CASE( 71) !MGLY -> CO + HO2 + MCO3
        j( 76) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3COCHO -> CH3CO + HCO
        
    CASE( 72) !GLYX -> CO + CO + HO2 + HO2
        j( 73) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CHOCHO -> 2 HO2 + 2 CO
        
    CASE( 73) !GLYX -> CO + CO + H2
        j( 74) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CHOCHO -> H2 + 2 CO
        
    CASE( 74) !GLYX -> CH2O + CO
        j( 75) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CHOCHO -> CH2O + CO
        
    CASE( 75) !HAC -> HCHO + HO2 + MeCO3
        j( 70) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3COCH2CH3 -> CH3CO + CH2CH3
        
    CASE( 76) !ACET -> MCO3 + MO2
        j( 68) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3COCH3 -> CH3CO + CH3
        
    CASE( 77) !ACET -> CO + MO2 + MO2
        j( 69) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3COCH3 -> CO + 2 CH3
        
    CASE( 78) !INPN -> HO2 + NO2 + OH + RCHO
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE( 79) !PRPN -> HO2 + NO2 + OH + RCHO
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE( 80) !ETP -> ALD2 + HO2 + OH
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE( 81) !RA3P -> HO2 + OH + RCHO
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE( 82) !RB3P -> ACET + HO2 + OH
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE( 83) !R4P -> HO2 + OH + RCHO
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE( 84) !PP -> ALD2 + CH2O + HO2 + OH
        j( 41) =  seval(szabin,theta,tmp,tmp2,b,c,d)!1-C4H9ONO2 -> 1-C4H9O + NO2
        
    CASE( 85) !RP -> ALD2 + HO2 + OH
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE( 88) !ISNP -> HO2 + NO2 + OH + RCHO
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE( 89) !VRP -> CH2O + GLYC + HO2 + MCO3 + MGLY + OH
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE( 90) !MRP -> CH2O + CO + HAC + HO2 + OH
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE( 91) !MAOP -> CH2O + MCO3 + OH
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE( 93) !MVKN -> HO2 + OH + RCHO
        j( 40) =  seval(szabin,theta,tmp,tmp2,b,c,d)!n-C3H7ONO2 -> C3H7O + NO2
        
    CASE( 94) !ISOPNB -> HO2 + OH + RCHO
        j( 40) =  seval(szabin,theta,tmp,tmp2,b,c,d)!n-C3H7ONO2 -> C3H7O + NO2
        
    CASE( 96) !PROPNN -> HO2 + OH + RCHO
        j( 40) =  seval(szabin,theta,tmp,tmp2,b,c,d)!n-C3H7ONO2 -> C3H7O + NO2
        
    CASE( 97) !ATOOH -> HO2 + OH + RCHO
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE( 98) !R4N2 -> ACET + ALD2... + HO2 + MEK + MO2 + NO2
        j( 35) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3ONO2 -> CH3O + NO2
        
    CASE( 99) !MAP -> MO2 + OH
        j( 33) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3OOH -> CH3O + OH
        
    CASE(100) !SO4 -> OH + OH + SO2
        j(360) =  seval(szabin,theta,tmp,tmp2,b,c,d)!H2SO4 -> 2 OH + SO2
        
    CASE(101) !ClNO2 -> Cl + NO2
        j( 98) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClNO2 -> Cl + NO2
        
    CASE(102) !ClOO -> Cl + O2
        j( 92) =  seval(szabin,theta,tmp,tmp2,b,c,d)!ClOO -> Products
        
    CASE(103) !O3 -> O(1D) + O2
        j(  2) =  seval(szabin,theta,tmp,tmp2,b,c,d)!O3 -> O2 + O(1D)
        
    CASE(104) !MPN -> HCHO + HO2 + NO3
        j( 37) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3(OONO2) -> CH3(O) + NO3
        
    CASE(105) !MPN -> MO2 + NO2
        j( 36) =  seval(szabin,theta,tmp,tmp2,b,c,d)!CH3(OONO2) -> CH3(OO) + NO2
        
END SELECT