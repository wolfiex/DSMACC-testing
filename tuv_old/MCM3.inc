SELECT CASE (jl)

 CASE(2)
        j(1)=seval(szabin,theta,tmp, tmp2, b,c,d) ! O3->O1D

 CASE(3)
        j(2)=seval(szabin,theta,tmp, tmp2, b,c,d) ! O3->O3P

 CASE(11)
        j(3)=seval(szabin,theta,tmp, tmp2, b,c,d) ! H2O2->2*OH

 CASE(4)
        j(4)=seval(szabin,theta,tmp, tmp2, b,c,d) ! NO2->NO+O3P

 CASE(5)
        j(5)=seval(szabin,theta,tmp, tmp2, b,c,d) ! NO3->NO+O2

 CASE(6)
        j(6)=seval(szabin,theta,tmp, tmp2, b,c,d) ! NO3->NO2+O3P

 CASE(12)
        j(7)=seval(szabin,theta,tmp, tmp2, b,c,d) ! HNO2->OH+NO

 CASE(13)
        j(8)=seval(szabin,theta,tmp, tmp2, b,c,d) ! HNO3->NO2+OH

 CASE(14)
        j(1300)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(15)
        j(11)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(16)
        j(12)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(17)
        j(13)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(20)
        j(14)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(75)
        j(15)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(76)
        j(16)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(77)
        j(17)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(62)
        j(18)=seval(szabin,theta,tmp, tmp2, b,c,d)*0.5
        j(19)=seval(szabin,theta,tmp, tmp2, b,c,d)*0.5

 CASE(25)
        j(21)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(87)
        j(22)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(61)
        j(23)=seval(szabin,theta,tmp, tmp2, b,c,d)*0.5
        j(24)=seval(szabin,theta,tmp, tmp2, b,c,d)*0.5

 CASE(21)
        j(31)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(23)
        j(32)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(22)
        j(33)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(24)
        j(34)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(60)
        j(35)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(26)
        j(41)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(27)
        j(51)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(64)
        j(52)=seval(szabin,theta,tmp, tmp2, b,c,d)
        j(54)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(91)
        j(53)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(94)
        j(55)=seval(szabin,theta,tmp, tmp2, b,c,d)

 CASE(67)
        j(56)=seval(szabin,theta,tmp, tmp2, b,c,d)*0.75
        j(57)=seval(szabin,theta,tmp, tmp2, b,c,d)*0.25
!!!!!!!!!!Halogens !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

 CASE(72)
        j(1001)=seval(szabin,theta,tmp, tmp2, b,c,d) ! HOBr

 CASE(73)
        j(1002)=seval(szabin,theta,tmp, tmp2, b,c,d) ! BrO

 CASE(74)
        j(1003)=seval(szabin,theta,tmp, tmp2, b,c,d) ! Br2

 CASE(50)
        j(1004)=seval(szabin,theta,tmp, tmp2, b,c,d) ! BrNO3->Br+NO3

 CASE(51)
        j(1005)=seval(szabin,theta,tmp, tmp2, b,c,d) ! BrNO3->BrO+NO2

 CASE(30)
        j(1006)=seval(szabin,theta,tmp, tmp2, b,c,d) ! ClNO3->Cl+NO3

 CASE(31)
        j(1007)=seval(szabin,theta,tmp, tmp2, b,c,d) ! ClNO3->ClO+NO2

 CASE(58)
        j(1008)=seval(szabin,theta,tmp, tmp2, b,c,d) ! Cl2->2Cl

END SELECT

