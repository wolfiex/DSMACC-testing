SELECT CASE (j)

 CASE(2)
        jval(1)=seval(n,theta,tmp, tmp2, b,c,d) ! O3->O1D

 CASE(3)
        jval(2)=seval(n,theta,tmp, tmp2, b,c,d) ! O3->O3P

 CASE(11)
        jval(3)=seval(n,theta,tmp, tmp2, b,c,d) ! H2O2->2*OH

 CASE(4)
        jval(4)=seval(n,theta,tmp, tmp2, b,c,d) ! NO2->NO+O3P

 CASE(5)
        jval(5)=seval(n,theta,tmp, tmp2, b,c,d) ! NO3->NO+O2

 CASE(6)
        jval(6)=seval(n,theta,tmp, tmp2, b,c,d) ! NO3->NO2+O3P

 CASE(12)
        jval(7)=seval(n,theta,tmp, tmp2, b,c,d) ! HNO2->OH+NO

 CASE(13)
        jval(8)=seval(n,theta,tmp, tmp2, b,c,d) ! HNO3->NO2+OH

 CASE(14)
        jval(1300)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(15)
        jval(11)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(16)
        jval(12)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(17)
        jval(13)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(20)
        jval(14)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(75)
        jval(15)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(76)
        jval(16)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(77)
        jval(17)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(62)
        jval(18)=seval(n,theta,tmp, tmp2, b,c,d)*0.5
        jval(19)=seval(n,theta,tmp, tmp2, b,c,d)*0.5

 CASE(25)
        jval(21)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(87)
        jval(22)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(61)
        jval(23)=seval(n,theta,tmp, tmp2, b,c,d)*0.5
        jval(24)=seval(n,theta,tmp, tmp2, b,c,d)*0.5

 CASE(21)
        jval(31)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(23)
        jval(32)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(22)
        jval(33)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(24)
        jval(34)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(60)
        jval(35)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(26)
        jval(41)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(27)
        jval(51)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(64)
        jval(52)=seval(n,theta,tmp, tmp2, b,c,d)
        jval(54)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(91)
        jval(53)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(94)
        jval(55)=seval(n,theta,tmp, tmp2, b,c,d)

 CASE(67)
        jval(56)=seval(n,theta,tmp, tmp2, b,c,d)*0.75
        jval(57)=seval(n,theta,tmp, tmp2, b,c,d)*0.25
!!!!!!!!!!Halogens !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

 CASE(72)
        jval(1001)=seval(n,theta,tmp, tmp2, b,c,d) ! HOBr

 CASE(73)
        jval(1002)=seval(n,theta,tmp, tmp2, b,c,d) ! BrO

 CASE(74)
        jval(1003)=seval(n,theta,tmp, tmp2, b,c,d) ! Br2

 CASE(50)
        jval(1004)=seval(n,theta,tmp, tmp2, b,c,d) ! BrNO3->Br+NO3

 CASE(51)
        jval(1005)=seval(n,theta,tmp, tmp2, b,c,d) ! BrNO3->BrO+NO2

 CASE(30)
        jval(1006)=seval(n,theta,tmp, tmp2, b,c,d) ! ClNO3->Cl+NO3

 CASE(31)
        jval(1007)=seval(n,theta,tmp, tmp2, b,c,d) ! ClNO3->ClO+NO2

 CASE(58)
        jval(1008)=seval(n,theta,tmp, tmp2, b,c,d) ! Cl2->2Cl

END SELECT

