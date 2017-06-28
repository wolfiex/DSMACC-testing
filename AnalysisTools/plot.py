#!/usr/local/anaconda/bin/python
# -*- coding: utf-8 -*-


def load(myfile,group,new):
    import pandas as pd
    import numpy as np
    import netCDF4
    from netCDF4 import Dataset
    import sys,os

    nc = Dataset(myfile,'r')
    print nc.date, '\n', nc.description

    specs = pd.DataFrame(nc.groups[group].variables['Spec'][:])
    specs.columns = nc.groups[group].variables['Spec'].head.split(',')

    rates = pd.DataFrame(nc.groups[group].variables['Rate'][:])
    rates.columns = nc.groups[group].variables['Rate'].head.split(',')[:]

    nc.close()

    print '\033[96mSpec and Rate files loaded from ', myfile, '\n\033[0m'

    # Format x-axis for plots
    time = specs['TIME']
    time[1:] = (specs['TIME'][1:]-specs['TIME'][1]+600.)/3600.
    xm = int(time.iloc[-1])+1

    # Added post-processing function from Fortran routine SPCgroup:
    specs['cc11'] = specs['MACROH']+specs['PRCOOMCHO']+specs['HOIBUTCHO']+specs['HO3C5CHO']+specs['C67OH'] \
        +specs['C4OCCOHCOH']+specs['IBUTALOH']+specs['M22C3CHO']+specs['C4OHCHO']+specs['HC4CHO'] \
        +specs['COHM2CO2H']+specs['MEMOXYCHO']+specs['HO24C4CHO']+specs['ACEC2CHO']+specs['HO13C3CHO'] \
        +specs['C6H13CHO']+specs['EOX2ETCHO']+specs['H2M2C4CHO']+specs['ACCOMECHO']+specs['ETBEACHO'] \
        +specs['HM22C3CHO']+specs['H13C43CHO']+specs['C4ALDB']+specs['HO3C3CHO']+specs['IEB1CHO'] \
        +specs['C3H7CHO']+specs['C68OH']+specs['M3C4CHO']+specs['HC4ACHO']+specs['C1H4C5CO2H'] \
        +specs['IPRCHO']+specs['HM2C43CHO']+specs['IECCHO']+specs['CH3CHOHCHO']+specs['IEB4CHO'] \
        +specs['HC4CCHO']+specs['C57OH']+specs['C3ME3CHO']+specs['CHOC2CO2H']+specs['HO2C43CHO'] \
        +specs['EOCOCHO']+specs['HMACR']+specs['MTBEACHO13']+specs['CHOC3DIOL']+specs['HOBUT2CHO'] \
        +specs['TBUACCO']+specs['C58OH']+specs['BUT2CHO']+specs['HO2C3CHO']+specs['C5H11CHO'] \
        +specs['HO3C4CHO']+specs['ME3BU3ECHO']+specs['TBUTCHO']+specs['IPROMCCHO']+specs['PRPAL2CO2H'] \
        +specs['HOC3H6CHO']+specs['MOXY2CHO']+specs['HO5C5CHO']+specs['HOIPRCHO']+specs['HC3CCHO'] \
        +specs['H2M2C3CHO']+specs['HC3CHO']+specs['HMACROH']+specs['HOC2H4CHO']+specs['BOX2ECHO'] \
        +specs['ACETETCHO']+specs['PROL1MCHO']+specs['HMAC']+specs['BOXCOCHO']+specs['CO1H63OH'] \
        +specs['C3M3OH2CHO']+specs['MTBEBCHO']+specs['IPRACBCHO']+specs['HCOCH2CO2H']+specs['HM33C3CHO'] \
        +specs['ACR']+specs['H3M3C4CHO']+specs['H2M3C4CHO']+specs['ETBECCHO']+specs['C41OH'] \
        +specs['C4H9CHO']+specs['H3M3C5CHO']+specs['CH3CHO']+specs['HO2C4CHO']+specs['C54CHO'] \
        +specs['M2C43CHO']+specs['HOCH2CHO']+specs['MOXYCOCHO']+specs['HM22CHO']+specs['HCOCO2H'] \
        +specs['HCHO']+specs['C2H5CHO']+specs['OCCOHCOH']+specs['M33C3CHO']+specs['CO1C6OH'] \
        +specs['MBOBCO']+specs['IEACHO']+specs['MC3ODBCO2H']+specs['HO2C54CHO']+specs['TBOCOCHO'] \
        +specs['MACR']+specs['C42CHO']
    specs['cc12'] = specs['C4COMOH3OH']+specs['BOXCOCOME']+specs['MPRK']+specs['BOXPRONOH']+specs['HO1CO4C6'] \
        +specs['HVMK']+specs['DEC3ONE']+specs['HO2CO4C5']+specs['MIPKAOH']+specs['SBUACCOH'] \
        +specs['HO14CO3C5']+specs['C51CO2H']+specs['CH3COCO2H']+specs['HO3CO6C7']+specs['HO3CO6C8'] \
        +specs['C77OH']+specs['ACPRONEOH']+specs['C41CO2H']+specs['MCOCOMOX']+specs['C78OH'] \
        +specs['ACCOCOC2H5']+specs['ME3CO2BUOL']+specs['MTBK']+specs['C51OH2CO']+specs['CO2C3CO2H'] \
        +specs['ACEBUTBONE']+specs['MTBKOH']+specs['HO6CO9C11']+specs['C6CO3HO25']+specs['C524CO'] \
        +specs['MIBK']+specs['C61OH']+specs['C63OH']+specs['CO2C54CO2H']+specs['C23O3CCO2H'] \
        +specs['C612OH']+specs['MEKCOH']+specs['HO5CO8C10']+specs['C93OH']+specs['H2M2CO5C6'] \
        +specs['CYHEXONE']+specs['C51OH']+specs['ACCOPRONE']+specs['C610OH']+specs['H13M3CO4C5'] \
        +specs['CO3C4CO2H']+specs['CO3C5CO2H']+specs['HO12CO3C4']+specs['C72OH']+specs['MIBKHO14'] \
        +specs['HO4CO7C9']+specs['MIBKBOH']+specs['C4COMEOH']+specs['M2CO5C6']+specs['BOXPRONE'] \
        +specs['C113OH']+specs['OCT3ONE']+specs['C6CO3HO14']+specs['C69OH']+specs['ACEBUTONE'] \
        +specs['ACECOCOCH3']+specs['M2BKAOH']+specs['MIPK']+specs['CO2M33CO2H']+specs['PRONFORM'] \
        +specs['C103OH']+specs['CH3COCH3']+specs['C64OH']+specs['MIPKBOH']+specs['DIEKAOH'] \
        +specs['SBUACEONE']+specs['HEX3ONDOH']+specs['C712OH']+specs['H2M3CO5C6']+specs['BUT2OLO'] \
        +specs['MVKOHAOH']+specs['M2BK']+specs['MEKAOH']+specs['C53OH']+specs['HEX3ONE'] \
        +specs['DDEC3ONE']+specs['UDEC3ONE']+specs['C23O3CHO']+specs['HO1CO3C5']+specs['EIPKAOH'] \
        +specs['HO14CO2C5']+specs['MIBKAOH']+specs['CO2HO3C6']+specs['HO13CO4C5']+specs['MIBKOH34'] \
        +specs['MVKOH']+specs['PRONEMOXOH']+specs['CYHXONAOH']+specs['NON3ONE']+specs['HEPT3ONE'] \
        +specs['MEK']+specs['ACBUONAOH']+specs['HEX2ONE']+specs['CO2C5OH']+specs['EIPKBOH'] \
        +specs['ACBUONBOH']+specs['MVK']+specs['M2BKBOH']+specs['C123OH']+specs['BOXPRONBOH'] \
        +specs['C66OH']+specs['HOCH2COCO2H']+specs['HEX3ONAOH']+specs['HEX3ONCOH']+specs['HCOC5'] \
        +specs['MPRKAOH']+specs['ACETOL']+specs['CO2M3C5OH']+specs['CO2MC5OH']+specs['C6CO3HO4'] \
        +specs['PRONEMOX']+specs['ACEPROPONE']+specs['PRCOOPRONE']+specs['CO2HO4C6']+specs['CYHXOLACO'] \
        +specs['MBOACO']+specs['HO14CO2C4']+specs['HO34CO6C8']+specs['M3CO5C6']+specs['HO7CO10C12'] \
        +specs['H2M4CO5C6']+specs['PE4E2CO']+specs['H13CO2C3']+specs['C532CO']+specs['HO2CO5C7'] \
        +specs['HO2CO5C6']+specs['DIEK']+specs['CO2C4CO2H']+specs['EIPK']
    specs['cc13'] = specs['HM22COCHO']+specs['C713OH']+specs['M3CO25C6']+specs['CO24M3C5']+specs['CO2C4CHO'] \
        +specs['C32OH13CO']+specs['C124OH']+specs['CO23C5']+specs['CO23C6']+specs['CO25C74OH'] \
        +specs['C77CO']+specs['C6COALCO2H']+specs['C123CO']+specs['CO356C9']+specs['C114OH'] \
        +specs['C65OH']+specs['MIBK3CO']+specs['MIBKAOH3CO']+specs['IPRGLYOX']+specs['CO24C6'] \
        +specs['CO24C5']+specs['C6CO134']+specs['C84OH']+specs['C4MDIAL']+specs['HO1CO24C6'] \
        +specs['EGLYOX']+specs['CO245C7']+specs['CO24M3C5OH']+specs['MBOCOCO']+specs['C6CODIAL'] \
        +specs['HO1CO24C5']+specs['CO346C8']+specs['HCOCH2CHO']+specs['CYC6DIONE']+specs['C67CHO'] \
        +specs['CO25C73OH']+specs['C6COHOCHO']+specs['CO3C5CHO']+specs['CO36C8']+specs['CO234C6'] \
        +specs['CO25C6OH']+specs['CY6DIONOH']+specs['C531CO']+specs['IBUTDIAL']+specs['C43OHCOCHO'] \
        +specs['CO35C5CHO']+specs['HO3CO46C8']+specs['C23O3CCHO']+specs['C6CO34HO1']+specs['C5CO234'] \
        +specs['HO1CO34C5']+specs['HO2CO35C7']+specs['C3MDIALOH']+specs['HO1CO3CHO']+specs['VGLYOX'] \
        +specs['HOCH2COCHO']+specs['H2M3CO4CHO']+specs['CO235C7']+specs['C6DIAL']+specs['CO2M3C4CHO'] \
        +specs['C5CO23CHO']+specs['C714OH']+specs['C4M2AL2OH']+specs['H14CO23C4']+specs['CO23C4CHO'] \
        +specs['CO2H3CHO']+specs['MGLYOX']+specs['H1CO23CHO']+specs['C611OH']+specs['C93CO'] \
        +specs['C3COCCHO']+specs['CO25C6']+specs['CO25C7']+specs['C113CO']+specs['CO13C4CHO'] \
        +specs['HO2CO4CHO']+specs['CO2C54CHO']+specs['C33CO']+specs['C6CO34']+specs['CO24C4CHO'] \
        +specs['CO3C54CHO']+specs['HOIPRGLYOX']+specs['CO235C6']+specs['C23C54CHO']+specs['CO2M33CHO'] \
        +specs['C94OH']+specs['MIBKHO4CHO']+specs['CO36C10']+specs['M3CO245C6']+specs['CY6TRION'] \
        +specs['BIACET']+specs['H13CO2CHO']+specs['GLYOX']+specs['C78CO']+specs['CO2C43CHO'] \
        +specs['CO13C4OH']+specs['CO36C11']+specs['CO36C12']+specs['CCOCOCOH']+specs['CO36C9'] \
        +specs['CO24M3CHO']+specs['BIACETOH']+specs['CO3C4CHO']+specs['PGLYOX']+specs['CYC613DION'] \
        +specs['C4CODIAL']+specs['CO356C10']+specs['CO356C11']+specs['CO356C12']+specs['C6CO23HO5'] \
        +specs['CO2C3CHO']+specs['C103CO']+specs['CO23C3CHO']+specs['C66CO']+specs['C6DIALOH'] \
        +specs['C104OH']+specs['C61CO']
    specs['cc21'] = specs['IBUTOLCNO3']+specs['M23C4NO3']+specs['C4ME2OHNO3']+specs['DECNO3']+specs['M3HEXBNO3'] \
        +specs['HO3C6NO3']+specs['ISOPCNO3']+specs['HM2C43NO3']+specs['ISOPANO3']+specs['MACRNCO2H'] \
        +specs['NBUACBNO3']+specs['HO1C4NO3']+specs['CHEXNO3']+specs['ETBEANO3']+specs['ETHFORMNO3'] \
        +specs['NC4CO2H']+specs['C54NO3']+specs['NONNO3']+specs['INB1OH']+specs['C56NO3'] \
        +specs['H3M3C5NO3']+specs['CH3NO3']+specs['ISOPBNO3']+specs['C65NO3CO2H']+specs['M33C4NO3'] \
        +specs['C2H5NO3']+specs['METACETNO3']+specs['MTBEAALNO3']+specs['M3BU2OLNO3']+specs['EOX2OLBNO3'] \
        +specs['HM33C3NO3']+specs['H1MC5NO3']+specs['HEXANO3']+specs['HO2C4NO3']+specs['M2PEDNO3'] \
        +specs['BOXPOLBNO3']+specs['M2HEXANO3']+specs['INAHCO2H']+specs['HEXCNO3']+specs['PECNO3'] \
        +specs['H3M3C6NO3']+specs['ETOC2NO3']+specs['HO3C106NO3']+specs['MBOBNO3']+specs['HO3C86NO3'] \
        +specs['HO2MC5NO3']+specs['BOXEOHBNO3']+specs['ACEC2H4NO3']+specs['HO3C126NO3']+specs['MTBEBNO3'] \
        +specs['C43NO3CO2H']+specs['HM22C3NO3']+specs['HO2M2C5NO3']+specs['PE2ENEANO3']+specs['C52NO3'] \
        +specs['PEANO3']+specs['ME3BUOLNO3']+specs['ISOPDNO3']+specs['MTBEANO3']+specs['BUTDANO3'] \
        +specs['IPROMC2NO3']+specs['HO13C4NO3']+specs['INDOH']+specs['HO3C96NO3']+specs['BUT2OLNO3'] \
        +specs['IPROC21NO3']+specs['HO3C4NO3']+specs['M23C43NO3']+specs['HO1MC5NO3']+specs['HO3C5NO3'] \
        +specs['MO2EOLBNO3']+specs['H13M3C5NO3']+specs['MO2EOLANO3']+specs['C6OH5NO3']+specs['M3HEXANO3'] \
        +specs['NPRACBNO3']+specs['C45NO3']+specs['MPRNO3CO2H']+specs['PE1ENEBNO3']+specs['MBOANO3'] \
        +specs['ETBEBNO3']+specs['IBUTOLBNO3']+specs['CH2CHCH2NO3']+specs['HEPTNO3']+specs['NC4H9NO3'] \
        +specs['CH3OCH2NO3']+specs['BOXPOLANO3']+specs['PROPOLNO3']+specs['HO1C6NO3']+specs['PRNO3CO2H'] \
        +specs['HM33C4NO3']+specs['HO2C5NO3']+specs['H2C3OCNO3']+specs['SC4H9NO3']+specs['DIIPRETNO3'] \
        +specs['NC524OH']+specs['PROL11MNO3']+specs['HEXBNO3']+specs['M2HEXBNO3']+specs['PEBNO3'] \
        +specs['NC3H7NO3']+specs['M2BU2OLNO3']+specs['HO2C54NO3']+specs['BOXEOHANO3']+specs['BUTDBNO3'] \
        +specs['C66NO35OH']+specs['TBUTOLNO3']+specs['IPRACNO3']+specs['H2M4C65NO3']+specs['C65OH4NO3'] \
        +specs['HO13C5NO3']+specs['DIETETNO3']+specs['HO1C5NO3']+specs['PR2OHMONO3']+specs['ETACETNO3'] \
        +specs['ETHOHNO3']+specs['TC4H9NO3']+specs['DDECNO3']+specs['C3MNO3CO2H']+specs['NBUTOLBNO3'] \
        +specs['M2BUOL2NO3']+specs['HM22C4NO3']+specs['NPRACCNO3']+specs['MCOOTBNO3']+specs['C524NO3'] \
        +specs['OCTNO3']+specs['M2PEANO3']+specs['M22C4NO3']+specs['SBUACANO3']+specs['NC3CO2H'] \
        +specs['HO2C6NO3']+specs['IPEBNO3']+specs['M2PECNO3']+specs['ETBECNO3']+specs['SBUACBNO3'] \
        +specs['M22C43NO3']+specs['NO3CH2CO2H']+specs['HO3C116NO3']+specs['IPRFORMNO3']+specs['HM23C4NO3'] \
        +specs['NBUTDAOH']+specs['IC4H9NO3']+specs['M3PEBNO3']+specs['NBUACCNO3']+specs['M3PECNO3'] \
        +specs['ISOP34NO3']+specs['C4NO3CO2H']+specs['NBUACANO3']+specs['INAOH']+specs['INCOH'] \
        +specs['M3PEANO3']+specs['H2M2C65NO3']+specs['CYHXOLANO3']+specs['PE2ENEBNO3']+specs['HO1C3NO3'] \
        +specs['NEOPNO3']+specs['HO3C76NO3']+specs['C58NO3CO2H']+specs['MACRNBCO3H']+specs['H2MC5NO3'] \
        +specs['IPEANO3']+specs['M2PEBNO3']+specs['NBUTOLANO3']+specs['C64OH5NO3']+specs['IPRACBNO3'] \
        +specs['ME2BUOLNO3']+specs['MACRNBCO2H']+specs['HO24C5NO3']+specs['C57NO3CO2H']+specs['EOX2OLANO3'] \
        +specs['H2M5C65NO3']+specs['NPRACANO3']+specs['H2M3C4NO3']+specs['IC3H7NO3']+specs['UDECNO3'] \
        +specs['PROLNO3']+specs['PE1ENEANO3']+specs['HO2M2C4NO3']+specs['CHOOCH2NO3']+specs['IPECNO3']
    specs['cc22'] = specs['INCNO3']+specs['INANO3']+specs['NBUTDBNO3']+specs['INANCO2H']+specs['NC524NO3'] \
        +specs['INB1NBCO2H']+specs['NISOPNO3']+specs['INB1NACO2H']+specs['INB1NO3']+specs['INCNCO2H']
    specs['cc23'] = specs['CH3O2NO2']
    specs['cc25'] = specs['PROL1MPAN']+specs['C6PAN23']+specs['C6PAN22']+specs['IPRACBPAN']+specs['C7PAN1'] \
        +specs['HC4PAN']+specs['A2PAN']+specs['C3PAN1']+specs['PAN']+specs['C6PAN21'] \
        +specs['C6PAN20']+specs['C3DBPAN']+specs['ACCOMEPAN']+specs['C7PAN2']+specs['PBN'] \
        +specs['PIPN']+specs['C3ME3PAN']+specs['C4PAN2']+specs['C4PAN4']+specs['C4PAN5'] \
        +specs['C4PAN7']+specs['C4PAN8']+specs['MTBEAALPAN']+specs['C10PAN1']+specs['PHPTN'] \
        +specs['C4PAN1']+specs['CHOOMPAN']+specs['IECPAN']+specs['IPROPOLPAN']+specs['PPEN'] \
        +specs['C5PAN10']+specs['C5PAN19']+specs['C5PAN11']+specs['C5PAN13']+specs['C5PAN12'] \
        +specs['C5PAN15']+specs['C5PAN17']+specs['C5PAN14']+specs['HO3C3PAN']+specs['C31PAN'] \
        +specs['C3M3OH2PAN']+specs['MTBEBPAN']+specs['C8PAN1']+specs['HMPAN']+specs['C4PAN3'] \
        +specs['ACRPAN']+specs['ACETC2PAN']+specs['IEAPAN']+specs['ETBEAPAN']+specs['ACETMEPAN'] \
        +specs['C4OHPAN']+specs['C6PAN3']+specs['PRCOOMPAN']+specs['ETOMEPAN']+specs['PHAN'] \
        +specs['C6PAN19']+specs['C6PAN14']+specs['M3BU3EPAN']+specs['PHXN']+specs['C6PAN1'] \
        +specs['C6PAN4']+specs['C6PAN8']+specs['IPROMCPAN']+specs['C5PAN8']+specs['C5PAN4'] \
        +specs['C5PAN6']+specs['C5PAN1']+specs['C5PAN3']+specs['ETBECPAN']+specs['C5PAN5'] \
        +specs['TBUACPAN']+specs['PPN']+specs['MEMOXYPAN']+specs['C9PAN1']+specs['C4OH2CPAN'] \
        +specs['C6PAN18']+specs['C6PAN10']+specs['C6PAN11']+specs['C6PAN13']+specs['C6PAN15'] \
        +specs['C6PAN17']+specs['BOXMPAN']
    specs['cc31'] = specs['HO1MC5OOH']+specs['PRCOFOROOH']+specs['CH3OCH2OOH']+specs['MBOAOOH']+specs['CH2CHCH2OOH'] \
        +specs['IPRACOOH']+specs['TBUTOLOOH']+specs['C51OH2OOH']+specs['BOX2OHBOOH']+specs['M2BU2OLOOH'] \
        +specs['HO13C5OOH']+specs['DIETETOOH']+specs['M2HEXBOOH']+specs['PEBOOH']+specs['ISOPAOOH'] \
        +specs['PR2OHMOOOH']+specs['IPROPOLO2H']+specs['BUTDBOOH']+specs['C52OH3OOH']+specs['HOACETEOOH'] \
        +specs['NBUTOLBOOH']+specs['M22C4OOH']+specs['PXYFUOOH']+specs['OCTOOH']+specs['C52OOH'] \
        +specs['SBUACAOOH']+specs['BUT2OLOOH']+specs['M2PEAOOH']+specs['MOCOCH2OOH']+specs['HO1C5OOH'] \
        +specs['M22C43OOH']+specs['SBUACBOOH']+specs['C65OH4OOH']+specs['IPEBOOH']+specs['HO2C6OOH'] \
        +specs['DDECOOH']+specs['HEPTOOH']+specs['TC4H9OOH']+specs['HM22C4OOH']+specs['BUFORMOOH'] \
        +specs['C524OOH']+specs['HO2M2C5OOH']+specs['C3DIOLOOH']+specs['ETHACETOOH']+specs['HO1C3OOH'] \
        +specs['HO3C116OOH']+specs['HO5C6OOH']+specs['HYPROPO2H']+specs['HM23C4OOH']+specs['HO3C76OOH'] \
        +specs['NBUACCOOH']+specs['H3M3C5OOH']+specs['IC4H9OOH']+specs['H2M4C65OOH']+specs['NBUACAOOH'] \
        +specs['ISOP34OOH']+specs['M3PEAOOH']+specs['M3PEBOOH']+specs['ACCOPROOH']+specs['NEOPOOH'] \
        +specs['M3PECOOH']+specs['PECOOH']+specs['IPRMETOOH']+specs['IPRACBOOH']+specs['C64OH5OOH'] \
        +specs['MMALNHYOOH']+specs['H13M3C5OOH']+specs['C52OH1OOH']+specs['HO24C5OOH']+specs['CYHXOLAOOH'] \
        +specs['H2M2C65OOH']+specs['HO2MC5OOH']+specs['ME2BUOLOOH']+specs['HYETHO2H']+specs['IBUTOLCO2H'] \
        +specs['ACCOETOOH']+specs['UDECOOH']+specs['H2M3C4OOH']+specs['H2MC5OOH']+specs['METACETO2H'] \
        +specs['M2PEBOOH']+specs['HO1C4OOH']+specs['IPECOOH']+specs['IPEAOOH']+specs['NBUTOLAOOH'] \
        +specs['DECOOH']+specs['M3HEXBOOH']+specs['HO3C6OOH']+specs['HM22C3OOH']+specs['NPRACAOOH'] \
        +specs['HM2C43OOH']+specs['HO6C7OOH']+specs['BOXCOOLOOH']+specs['MTBEBOOH']+specs['C53OH2OOH'] \
        +specs['IBUTOLBO2H']+specs['CHOOCH2OOH']+specs['HO1C6OOH']+specs['BOX2OHAOOH']+specs['HO2M2C4OOH'] \
        +specs['HO3C86OOH']+specs['C4ME2OHOOH']+specs['ME3BUOLOOH']+specs['M23C4OOH']+specs['NBUACBOOH'] \
        +specs['BOXMOOH']+specs['IPRFORMOOH']+specs['CHEXOOH']+specs['ETHOXOOH']+specs['BOCOCH2OOH'] \
        +specs['ETBEAOOH']+specs['MECOACEOOH']+specs['C56OOH']+specs['C54OOH']+specs['NONOOH'] \
        +specs['HO3C4OOH']+specs['IC3H7OOH']+specs['HM33C3OOH']+specs['M3BU2OLOOH']+specs['ISOPBOOH'] \
        +specs['MPAN']+specs['HO2M2C5O2']+specs['HEXCOOH']+specs['EIPEOOH']+specs['EOX2OLAOOH'] \
        +specs['HO3C106OOH']+specs['ETOC2OOH']+specs['ACEC2H4OOH']+specs['C2H5OOH']+specs['M33C4OOH'] \
        +specs['MTBEAALOOH']+specs['H2M5C65OOH']+specs['ISOPDOOH']+specs['EOX2OLBOOH']+specs['PEAOOH'] \
        +specs['H1MC5OOH']+specs['ISOPCOOH']+specs['HO2C4OOH']+specs['BUTDAOOH']+specs['MTBEAOOH'] \
        +specs['EOCOCH2OOH']+specs['HO2C5OOH']+specs['M2HEXAOOH']+specs['MBOBOOH']+specs['H3M3C6OOH'] \
        +specs['HO3C126OOH']+specs['BUTDCOOH']+specs['NC3H7OOH']+specs['HO8C9OOH']+specs['IPROC21OOH'] \
        +specs['HO3C96OOH']+specs['HO13C4OOH']+specs['M2BUOL2OOH']+specs['NC4H9OOH']+specs['NPRACBOOH'] \
        +specs['NPRACCOOH']+specs['C45OOH']+specs['ETOMEOOH']+specs['PRCOOMOOH']+specs['IPROMC2OOH'] \
        +specs['M2PECOOH']+specs['HO7C8OOH']+specs['CH3OOH']+specs['MECOFOROOH']+specs['ETHFORMOOH'] \
        +specs['M23C43OOH']+specs['ETBEBOOH']+specs['HO3C5OOH']+specs['MO2EOLAOOH']+specs['M2PEDOOH'] \
        +specs['HO2C54OOH']+specs['MCOOTBOOH']+specs['MO2EOLBOOH']+specs['BOXPOLAOOH']+specs['M3HEXAOOH'] \
        +specs['HEXAOOH']+specs['C6OH5OOH']+specs['ACEETOHOOH']+specs['HEXBOOH']+specs['PROL11MOOH'] \
        +specs['DIIPRETOOH']+specs['HM33C4OOH']+specs['SC4H9OOH']+specs['H2C3OCOOH']+specs['ETBECOOH']
    specs['cc33'] = specs['C42CO3H']+specs['PERPENACID']+specs['CH3CO3H']+specs['IPROPOLPER']+specs['IPRHOCO3H'] \
        +specs['IEACO3H']+specs['HC3CCO3H']+specs['C2OHOCOOH']+specs['HO13C3CO3H']+specs['MACO3H'] \
        +specs['ACETC2CO3H']+specs['C5H11CO3H']+specs['HOC3H6CO3H']+specs['M33C3CO3H']+specs['M2C43CO3H'] \
        +specs['HOCH2CO3H']+specs['H2M2C4CO3H']+specs['HO4C5CO3H']+specs['ETBECCO3H']+specs['HOC2H4CO3H'] \
        +specs['HC4CCO3H']+specs['C54CO3H']+specs['HC4ACO3H']+specs['TBUTCO3H']+specs['HOIPRCO3H'] \
        +specs['C31CO3H']+specs['HO24C4CO3H']+specs['HO3C5CO3H']+specs['H3M2C4CO3H']+specs['HM22C3CO3H'] \
        +specs['PERPROACID']+specs['C3DBCO3H']+specs['HO2C3CO3H']+specs['HO2C54CO3H']+specs['HM22CO3H'] \
        +specs['HOIBUTCO3H']+specs['PRCOOMCO3H']+specs['ETOMECO3H']+specs['HC3CO3H']+specs['C3ME3CO3H'] \
        +specs['ETBEACO3H']+specs['HO2C43CO3H']+specs['HMACO3H']+specs['M3C4CO3H']+specs['ACO3H'] \
        +specs['HO2C4CO3H']+specs['H3M3C5CO3H']+specs['HO8C9CO3H']+specs['TBUACCO3H']+specs['HO7C8CO3H'] \
        +specs['ACETMECO3H']+specs['H3M3C4CO3H']+specs['ACCOMECO3H']+specs['M3BU3ECO3H']+specs['H2M3C4CO3H'] \
        +specs['IPROMCCO3H']+specs['M22C3CO3H']+specs['MTBEALCO3H']+specs['HOBUT2CO3H']+specs['PROL1MCO3H'] \
        +specs['C6H13CO3H']+specs['MEMOXYCO3H']+specs['BOXMCO3H']+specs['H2M2C3CO3H']+specs['IECCO3H'] \
        +specs['IPRACBCO3H']+specs['C3M3OHCO3H']+specs['HO6C7CO3H']+specs['H13C43CO3H']+specs['HO5C6CO3H'] \
        +specs['HO5C5CO3H']+specs['PERIBUACID']+specs['HO3C3CO3H']+specs['HM2C43CO3H']+specs['C4OHCO3H'] \
        +specs['HC4CO3H']+specs['CHOOMCO3H']+specs['PERBUACID']+specs['MTBEBCO3H']+specs['C4OH2CO3H'] \
        +specs['BUT2CO3H']+specs['HM33C3CO3H']+specs['HO3C4CO3H']
    specs['cc4'] = specs['MACROO']+specs['C2H5CHOO']+specs['NC4H9CHOOA']+specs['MACROOA']+specs['IPRCHOO'] \
        +specs['NC4H9CHOO']+specs['CH3CCH3OOB']+specs['ACLOOA']+specs['C3H7CHOOB']+specs['C3H7CHOOA'] \
        +specs['CH3CCH3OOC']+specs['C2H5MECOO']+specs['IPRCHOOA']+specs['MBOOO']+specs['GAOO'] \
        +specs['CH2OO']+specs['CH3CCH3OOA']+specs['CH3CCH3OO']+specs['ACROOA']+specs['CH2OOB'] \
        +specs['C2H5CHOOB']+specs['C2H5CHOOA']+specs['ACLOO']+specs['M3FOOA']+specs['CH2OOG'] \
        +specs['CH2OOE']+specs['CH2OOD']+specs['CH2OOC']+specs['CH2OOA']+specs['GAOOB'] \
        +specs['GAOOA']+specs['C3H7CHOO']+specs['MVKOO']+specs['MBOOOA']+specs['C2H5MECOOA'] \
        +specs['CH3CHOOA']+specs['CH3CHOOC']+specs['CH3CHOOB']+specs['ACROO']+specs['CH3CHOO'] \
        +specs['MVKOOA']+specs['M3FOO']
    specs['cc5'] = specs['HEX3ONANO3']+specs['CHOPRNO3']+specs['ETHO2HNO3']+specs['MEKAOOH']+specs['CHOC3COPAN'] \
        +specs['MPRANO3OOH']+specs['NAOOA']+specs['C527OOH']+specs['C111OOH']+specs['C3COCCO3H'] \
        +specs['C611OOH']+specs['C61NO3']+specs['NOA']+specs['BIACETOOH']+specs['CO3C4NO3OH'] \
        +specs['MMALNAPAN']+specs['C42OH']+specs['MACROOH']+specs['C510OH']+specs['C63NO3'] \
        +specs['C47PAN']+specs['DHPMPAL']+specs['DHPMEK']+specs['INB1NACHO']+specs['C51NO324CO'] \
        +specs['C62NO335CO']+specs['MIBKBOOH']+specs['CHOC4CO3H']+specs['C5NO3OAOOH']+specs['MMALNBCO3H'] \
        +specs['C5NO3CO4OH']+specs['C51CO3H']+specs['C112OOH']+specs['CHOC4PAN']+specs['C4MALOHOOH'] \
        +specs['HMGLYOO']+specs['C6NO3CO4OH']+specs['HEX2ONBOOH']+specs['MIPKBNO3']+specs['C312COCO3H'] \
        +specs['CONM2CO2H']+specs['C6CONO3OOH']+specs['BU1ENO3OOH']+specs['C3NO3COOOH']+specs['C1H4C5CO3H'] \
        +specs['C81OOH']+specs['MACRNB']+specs['NC4OOA']+specs['DIEKBOOH']+specs['C3M3CHONO3'] \
        +specs['C52NO31CO']+specs['HMVKNGLYOX']+specs['MTBKNO3']+specs['HNC524CO']+specs['C5ONO34OOH'] \
        +specs['C64NO335CO']+specs['NC2OO']+specs['HOCHOCOOH']+specs['CHOC3COOOH']+specs['C57NO3'] \
        +specs['PACLOOA']+specs['C6CONO34OH']+specs['MMALNBCO2H']+specs['C51NO3']+specs['INDHPPAN'] \
        +specs['C6CYTONOOH']+specs['NMBOBCO']+specs['NC3CHO']+specs['C3PAN2']+specs['C58NO3'] \
        +specs['C82OOH']+specs['C75OOH']+specs['HMVKANO3']+specs['MPRKBOOH']+specs['C122OOH'] \
        +specs['C6COCHOPAN']+specs['CONM2CO3H']+specs['CO23C4NO3']+specs['C42OOH']+specs['BOXPROANO3'] \
        +specs['CO3C85OOH']+specs['CO1H63NO3']+specs['MACRNOOA']+specs['C123OOH']+specs['ALCOCH2OOH'] \
        +specs['BUTALO2H']+specs['C43NO3PAN']+specs['C42MNO3OOH']+specs['PGAOOB']+specs['NCO23CHO'] \
        +specs['CO2C3CO3H']+specs['CYHXONANO3']+specs['NC4CO3H']+specs['PR2O2HNO3']+specs['ACCOCOMOOH'] \
        +specs['SBUACCOOH']+specs['C526NO3']+specs['IBUDIALPAN']+specs['NC41OOA']+specs['INAHPCHO'] \
        +specs['INANCHO']+specs['C4CO2OOH']+specs['CH3COCO3H']+specs['PR1O2HNO3']+specs['GLYOOB'] \
        +specs['C312COPAN']+specs['C4CHOBOOH']+specs['HMVKBOOH']+specs['CO2N3CHO']+specs['C41CO3H'] \
        +specs['NC4OO']+specs['C536OOH']+specs['BUTAL2NO3']+specs['CHOC4OOH']+specs['NC3OOA'] \
        +specs['C613OOH']+specs['EIPKBNO3']+specs['C530OOH']+specs['C6DIALOOH']+specs['HMACROOH'] \
        +specs['MIBKOHAOOH']+specs['C531OOH']+specs['BOX2COMOOH']+specs['M2BKANO3']+specs['C537OOH'] \
        +specs['C64OOH']+specs['C4MCONO3OH']+specs['MVKOHBOOH']+specs['CHOMOHCO3H']+specs['C5124COPAN'] \
        +specs['C6CO134OOH']+specs['C23O3CCO3H']+specs['C67OOH']+specs['C4PAN6']+specs['C4PAN9'] \
        +specs['EIPKAOOH']+specs['PROPALOOH']+specs['C3MCODBPAN']+specs['HMGLOOA']+specs['C6TONOHOOH'] \
        +specs['HIEB2OOH']+specs['C525OOH']+specs['C65NO3CO3H']+specs['C534OOH']+specs['INDHPCO3H'] \
        +specs['C65OOH']+specs['C43NO3CO3H']+specs['C74OOH']+specs['CO2H3CO3H']+specs['C4MNO32OOH'] \
        +specs['NC524OOH']+specs['ACPRONEOOH']+specs['C3M3CHOOOH']+specs['INANCOCO2H']+specs['INB1OOH'] \
        +specs['C6CO134PAN']+specs['CHOC2CO3H']+specs['C4M3NO3ONE']+specs['NC4OHCPAN']+specs['C610NO3'] \
        +specs['INANCO3H']+specs['C71OOH']+specs['NAOO']+specs['INCNCHO']+specs['INB1HPCO2H'] \
        +specs['C6CO3OHOOH']+specs['CO3C5CO3H']+specs['C93NO3']+specs['C103NO3']+specs['C113OOH'] \
        +specs['C103OOH']+specs['NBUTDAOOH']+specs['C65NO36OOH']+specs['MC3CODBPAN']+specs['INB1NBCHO'] \
        +specs['C104OOH']+specs['C73OOH']+specs['C3COCPAN']+specs['CO2C54CO3H']+specs['C67NO3'] \
        +specs['NOAOOA']+specs['ALCOMOXOOH']+specs['CO234C6OOH']+specs['INDHPCHO']+specs['C105OOH'] \
        +specs['ACOMCOMOOH']+specs['NC41OO']+specs['INB1HPCO3H']+specs['INB1HPPAN']+specs['MMALNBPAN'] \
        +specs['C47CO3H']+specs['C4NO3PAN']+specs['C4M22CONO3']+specs['C53NO32CO']+specs['C710OOH'] \
        +specs['HCOCH2CO3H']+specs['COHM2PAN']+specs['C5PAN18']+specs['C5PAN16']+specs['PRPAL2CO3H'] \
        +specs['C82NO3']+specs['C5HPALD2']+specs['C5HPALD1']+specs['INB1NBCO3H']+specs['C84OOH'] \
        +specs['C66NO35CO']+specs['HEX2ONANO3']+specs['HPC52OOH']+specs['MEKCOOH']+specs['PPGAOOB'] \
        +specs['NPXYFUOOH']+specs['HPC52PAN']+specs['HCOCH2OOH']+specs['C4OCCOHOOH']+specs['C63NO32CO'] \
        +specs['BOXPROBOOH']+specs['C3MNO3PAN']+specs['C43NO34OOH']+specs['HEX2ONCOOH']+specs['INAHCO3H'] \
        +specs['C62NO33CO']+specs['C58NO3CO3H']+specs['INB1NAPAN']+specs['C78OOH']+specs['C4M2NO3OOH'] \
        +specs['CO3C75OOH']+specs['C413COOOH']+specs['CO1C6NO3']+specs['C5CONO3OOH']+specs['C6COALCO3H'] \
        +specs['C712NO3']+specs['MIBKAOHNO3']+specs['MEKANO3']+specs['NMVK']+specs['C59OOH'] \
        +specs['HNMVKOH']+specs['MIBKOHBOOH']+specs['PRONEMOOOH']+specs['MPRKAOOH']+specs['CHOC2H4OOH'] \
        +specs['C57NO3PAN']+specs['NMGLYOX']+specs['CO25C73OOH']+specs['INB1NBPAN']+specs['C527NO3'] \
        +specs['MVKOOH']+specs['HNMVKOOH']+specs['C41OOH']+specs['C4PAN10']+specs['CO23C54OOH'] \
        +specs['NO3CH2PAN']+specs['BUTONENO3']+specs['CO3C4CO3H']+specs['C58ANO3']+specs['MMALNACO2H'] \
        +specs['IEC2OOH']+specs['MPRBNO3CHO']+specs['HCOCOHPAN']+specs['C6COCHOOOH']+specs['C68NO3'] \
        +specs['C63NO32OOH']+specs['NC3OO']+specs['C4CONO3OOH']+specs['C535OOH']+specs['C4OCCOHNO3'] \
        +specs['CY6DIONOOH']+specs['CO23C65OOH']+specs['H3NCO2CHO']+specs['HYPERACET']+specs['INB1NACO3H'] \
        +specs['C72NO3']+specs['HEX2ONBNO3']+specs['MIPKBOOH']+specs['INCCO']+specs['C95OOH'] \
        +specs['C1H4C5PAN']+specs['C42NO33OOH']+specs['C4M2NO3ONE']+specs['INAOOH']+specs['C77OOH'] \
        +specs['HEX3ONCOOH']+specs['MIPKAOOH']+specs['MIBKAOOH']+specs['C6NO3CO5OH']+specs['CO2C3OO'] \
        +specs['HEX3ONBOOH']+specs['COHM2CO3H']+specs['PRNO3CO3H']+specs['C6NO3COOOH']+specs['MGLYOOA'] \
        +specs['PRNO3PAN']+specs['C4MCNO3OOH']+specs['MCOCOMOOOH']+specs['C67CO3H']+specs['PRNOCOMOOH'] \
        +specs['INB2OOH']+specs['HPC52CO3H']+specs['MTBKOOH']+specs['HEX3ONAOOH']+specs['NMBOBOOH'] \
        +specs['INB1HPCHO']+specs['CO2N3PAN']+specs['C76OOH']+specs['MMALNACO3H']+specs['CO2HOC6OOH'] \
        +specs['C58NO3PAN']+specs['MACRNO3']+specs['CO2M33CO3H']+specs['C92OOH']+specs['BOXPROOOH'] \
        +specs['C6NO324CO']+specs['C3MNO3CO3H']+specs['ACBUONBOOH']+specs['NMBOAOOH']+specs['CO24C6OOH'] \
        +specs['C5PAN9']+specs['CO23C4CO3H']+specs['C714OOH']+specs['C63OOH']+specs['MACRNOO'] \
        +specs['C4NO3CHO']+specs['ALC4DOLOOH']+specs['HMVKNO3']+specs['OCCOHCOOH']+specs['PE2ONE1OOH'] \
        +specs['MVKOHAOOH']+specs['MGLYOO']+specs['C121OOH']+specs['INANCOPAN']+specs['INDOOH'] \
        +specs['C94OOH']+specs['C23C54CO3H']+specs['DNC524CO']+specs['C4MNO31OOH']+specs['BUTALNO3'] \
        +specs['INB1CO']+specs['COC4NO3OOH']+specs['C124OOH']+specs['DIEKBNO3']+specs['C713OOH'] \
        +specs['HMGLYOOA']+specs['INANCOCO3H']+specs['C57AOOH']+specs['C711OOH']+specs['HIEB1OOH'] \
        +specs['CO2N3CO3H']+specs['MACROHOOH']+specs['C4CHOBNO3']+specs['C715OOH']+specs['C79OOH'] \
        +specs['C57OOH']+specs['MIBKHO4OOH']+specs['C55OOH']+specs['NISOPOOH']+specs['C114OOH'] \
        +specs['PRNFORMOOH']+specs['EIPKBOOH']+specs['C66NO35OOH']+specs['C53NO324CO']+specs['C83OOH'] \
        +specs['C115OOH']+specs['INCNPAN']+specs['C42AOH']+specs['C51OOH']+specs['HNBIACET'] \
        +specs['C5TRONCO3H']+specs['MEKBOOH']+specs['M2BKAOOH']+specs['NO3CH2CO3H']+specs['ACBUOAOOH'] \
        +specs['C23O3CPAN']+specs['C69OOH']+specs['MIBK3COOOH']+specs['C123NO3']+specs['MPRBNO3OOH'] \
        +specs['GLYOOC']+specs['GLYOOA']+specs['INAHPCO3H']+specs['C4NO3CO3H']+specs['C5CO234OOH'] \
        +specs['C6PAN5']+specs['NC51OOH']+specs['C5OHCO4OOH']+specs['CH3COPAN']+specs['CYHXONAOOH'] \
        +specs['BOXCOALOOH']+specs['C610OOH']+specs['C6PAN12']+specs['CO24C53OOH']+specs['CO3C54CO3H'] \
        +specs['HOC4CHOOOH']+specs['HEX3ONDNO3']+specs['C526OOH']+specs['COCCOHCOOH']+specs['C61OOH'] \
        +specs['C64NO3']+specs['INAHCHO']+specs['C58OOH']+specs['MACRNBPAN']+specs['NC3CO3H'] \
        +specs['INB1GLYOX']+specs['C530NO3']+specs['INCOOH']+specs['C66OOH']+specs['NOAOO'] \
        +specs['INANCOCHO']+specs['C6PAN2']+specs['C6PAN6']+specs['C6PAN7']+specs['C6PAN9'] \
        +specs['C5CO23OOH']+specs['MGLOOA']+specs['NC526OOH']+specs['HEX2ONAOOH']+specs['NBUTDBOOH'] \
        +specs['C91OOH']+specs['MGLYOOB']+specs['ACBUONANO3']+specs['C77NO3']+specs['C4NO32MOOH'] \
        +specs['C533OOH']+specs['C5PAN7']+specs['C5PAN2']+specs['DIEKAOOH']+specs['C4CONO3CO'] \
        +specs['C101OOH']+specs['CONM2CHO']+specs['C5PACALD2']+specs['C5PACALD1']+specs['C5COCHOOOH'] \
        +specs['NC4CHO']+specs['C57NO3CO3H']+specs['MGLOO']+specs['C62OOH']+specs['H13CO2CO3H'] \
        +specs['IBUTALO2H']+specs['INANPAN']+specs['INDHCO3H']+specs['C113NO3']+specs['MBKCOOHOOH'] \
        +specs['C4M2ALOHNO3']+specs['HMGLOO']+specs['INCGLYOX']+specs['IBUALANO3']+specs['PPACLOOA'] \
        +specs['C510OOH']+specs['ACCOCOEOOH']+specs['CONM2PAN']+specs['C3MDIALOOH']+specs['HPNC524CO'] \
        +specs['C93OOH']+specs['HCOCO3H']+specs['C5124COOOH']+specs['C51NO32CO']+specs['GLYOO'] \
        +specs['C53OOH']+specs['C6135COOOH']+specs['MPRBNO3PAN']+specs['MPRKNO3']+specs['C4NO3M2OOH'] \
        +specs['C4NO3M1OOH']+specs['C612OOH']+specs['COCCOHNO3']+specs['C712OOH']+specs['INANCO'] \
        +specs['C4NO3COOOH']+specs['C52NO31OOH']+specs['NO3CH2CHO']+specs['CO2C4CO3H']+specs['CONO3C6OOH'] \
        +specs['C65NO3PAN']+specs['INAHPPAN']+specs['CO1H63OOH']+specs['C58AOOH']+specs['C51NO32OOH'] \
        +specs['C65NO36CHO']+specs['MVKNO3']+specs['C41NO3']+specs['HEX3ONDOOH']+specs['CHOC2PAN'] \
        +specs['C52NO33CO']+specs['HCOCOHCO3H']+specs['C125OOH']+specs['INDHCHO']+specs['C3MNO3CHO'] \
        +specs['C52NO33OOH']+specs['INAHPAN']+specs['C68OOH']+specs['CHOC4OHOOH']+specs['CO2C3PAN'] \
        +specs['C6PAN16']+specs['HOCO3C5OOH']+specs['CO2C3OOA']+specs['CO2C3OOB']+specs['INAHPCO2H'] \
        +specs['CO25C6OOH']+specs['INCNCO3H']+specs['M2BKBOOH']+specs['C5NO3O4OOH']+specs['C6145COOOH'] \
        +specs['NC4OHCO3H']+specs['CHOMOHPAN']+specs['INDHPAN']+specs['HOCO3C4OOH']+specs['C102OOH'] \
        +specs['HOCO4C5OOH']+specs['C72OOH']+specs['CY6COCOOOH']+specs['C53NO32OOH']+specs['PRNOCOPOOH'] \
        +specs['MVKOHANO3']+specs['C62NO33OOH']+specs['C6CO34OOH']+specs['C6HOCOOOH']+specs['C47CHO'] \
        +specs['CO1C6OOH']+specs['MPRNO3CO3H']+specs['IBUTALBO2H']+specs['MIBKANO3']+specs['MACRNCO3H'] \
        +specs['C4COMOHOOH']+specs['NC2OOA']+specs['MACRNPAN']+specs['CO3C4NO3']+specs['CO25C74OOH']
    specs['cc0'] = specs['TBUACET']+specs['NBUTACET']+specs['IPROPOL']+specs['IPRHOCO2H']+specs['ETHGLY'] \
        +specs['HM33C4OH']+specs['NC9H20']+specs['BOX2COMOH']+specs['M23C4OH']+specs['MAE'] \
        +specs['EOX2ETB2OH']+specs['BUT2CO2H']+specs['IPRACBOH']+specs['PEBOH']+specs['HEPTOH'] \
        +specs['C56OH']+specs['IEPOXB']+specs['IEPOXA']+specs['MACO2H']+specs['ACETC2CO2H'] \
        +specs['ACETCOC3H7']+specs['HO2C4CO2H']+specs['ETHACETOH']+specs['MO2EOLA2OH']+specs['C5NO3COAO2'] \
        +specs['DIIPRETOH']+specs['ETBEAOH']+specs['HO2C5OH']+specs['HIEPOXB']+specs['PRCOFORM'] \
        +specs['ALLYLOH']+specs['PROH2MOX']+specs['NC8H18']+specs['PROPGLY']+specs['H14M4C6'] \
        +specs['HOCH2CO2H']+specs['SBUACAOH']+specs['C524OH']+specs['IPROACET']+specs['HEXBOH'] \
        +specs['M2PE']+specs['M3HEXAOH']+specs['CHEX']+specs['MTBEBOH']+specs['HOC2H4CO2H'] \
        +specs['HC4CCO2H']+specs['H2M2C4CO2H']+specs['MO2EOLB2OH']+specs['M2PEAOH']+specs['ME2BUT2ENE'] \
        +specs['C52OH']+specs['DIETETHER']+specs['CL']+specs['M3HEX']+specs['HC4ACO2H'] \
        +specs['PENT1ENE']+specs['NC12H26']+specs['DM23BU2ENE']+specs['BUOX2ETOH']+specs['C4ME22OH'] \
        +specs['MTBE']+specs['IEPOXC']+specs['PROL2FORM']+specs['NBUTOLAOH']+specs['M2HEXBOH'] \
        +specs['PXYFUONE']+specs['HOC3H6CO2H']+specs['DIIPRETHER']+specs['H3M3C5CO2H']+specs['M3F'] \
        +specs['M23C4']+specs['M2BUOL2OH']+specs['ETHACET']+specs['BOXMOH']+specs['M3PE'] \
        +specs['H25M2C6']+specs['HO2M2C4OH']+specs['BOX2PROL']+specs['OCTOH']+specs['HO3C5CO2H'] \
        +specs['M2C43CO2H']+specs['NBUTOL']+specs['HOC4H8OH']+specs['NC5H12']+specs['M2HEX'] \
        +specs['CYHXDIOLA']+specs['HO12C5']+specs['BOXOHETOH']+specs['EOX2COMEOH']+specs['IPROCHO'] \
        +specs['HO14M3C5']+specs['HO124C5']+specs['HO13C5']+specs['NEOP']+specs['MTBEACHOHO'] \
        +specs['CYHEXOL']+specs['ACO2H']+specs['M33C3CO2H']+specs['NPROACET']+specs['IC4H10'] \
        +specs['EOX2EOL']+specs['IPROC21OH']+specs['CHEX2ENE']+specs['HM33C3CO2H']+specs['HO36C11'] \
        +specs['ME3BUT1ENE']+specs['PENTACID']+specs['TBUTOL']+specs['ETBECOH']+specs['H134M3C5'] \
        +specs['NPRACBOH']+specs['PXYFUOH']+specs['HEX1ENE']+specs['NEOPOH']+specs['TBOCOCH2OH'] \
        +specs['CH3OCH2OH']+specs['M33C4OH']+specs['BOXCOEOL']+specs['ETOMECO2H']+specs['M23C43OH'] \
        +specs['NC4H10']+specs['IPEBOH']+specs['C523OH']+specs['M2PECOH']+specs['NBUACBOH'] \
        +specs['CHOOCH2OH']+specs['HO13M2C4']+specs['EOX2ETA2OH']+specs['IBUTACID']+specs['MTBEBCO2H'] \
        +specs['BUTDBOH']+specs['HC3CO2H']+specs['HM22C3CO2H']+specs['HO2C3CO2H']+specs['IC5H12'] \
        +specs['ETOMENO3']+specs['HM23C4OH']+specs['BUT2OLOH']+specs['IPROMC2OH']+specs['CH3OH'] \
        +specs['M22C4OH']+specs['NC10H22']+specs['HOIPRCO2H']+specs['MMALANHY']+specs['PEAOH'] \
        +specs['HM22C3OH']+specs['MEPROPENE']+specs['M3PEAOH']+specs['PECOH']+specs['METHACET'] \
        +specs['VINOH']+specs['MO2EOL']+specs['ETHOX']+specs['MBOAOH']+specs['PRCOOETOH'] \
        +specs['C645OH']+specs['C4ME3HO23']+specs['HO2C4OH']+specs['CH3OCH3']+specs['H13M3C5'] \
        +specs['CH3OCHO']+specs['EIPEOH']+specs['H25M3C6']+specs['HEXCOH']+specs['IPRACOH'] \
        +specs['ETACETOH']+specs['HEXAOH']+specs['C3ME3CO2H']+specs['HCOOH']+specs['C4ME3HO12'] \
        +specs['ME2BUT1ENE']+specs['MTBEACHO']+specs['BUTACID']+specs['NPRACAOH']+specs['HO2C43CO2H'] \
        +specs['HO14MC5']+specs['ME3BUOL']+specs['IPRFORMOH']+specs['SBUACBOH']+specs['CPENT2ENE'] \
        +specs['BOX2E2OH']+specs['SBUTACET']+specs['HMML']+specs['HO24C5']+specs['HOC3H6OH'] \
        +specs['DIETETOH']+specs['C2OHOCO2H']+specs['MTBEAOH']+specs['ISOPDOH']+specs['HOBUT2CO2H'] \
        +specs['BOXPR2OH']+specs['BOXPOLBOOH']+specs['TPENT2ENE']+specs['M2PEBOH']+specs['HO2M2C5OH'] \
        +specs['NC11H24']+specs['TBUACOH']+specs['DDECOH']+specs['MMALNHY2OH']+specs['HM22CO2H'] \
        +specs['ISOPBOH']+specs['HO25C7']+specs['HO25C6']+specs['C4H6']+specs['MOXCOCH2OH'] \
        +specs['BOXMCO2H']+specs['NC7H16']+specs['ISOPAOH']+specs['NPROPOL']+specs['M22C4'] \
        +specs['H2M3C4CO2H']+specs['PROPACID']+specs['METACETHO']+specs['ETBEBOH']+specs['MTBEALCO2H'] \
        +specs['BUT2OL']+specs['NONOH']+specs['ETHFORM']+specs['IBUTOLOHC']+specs['IBUTOLOHB'] \
        +specs['BUOHFORM']+specs['ETBE']+specs['BOXOHPROL']+specs['PRCOOPROL']+specs['C656OH'] \
        +specs['IPRMEETOH']+specs['M22C43OH']+specs['UDECOH']+specs['HO36C9']+specs['HO36C8'] \
        +specs['ETOMEOH']+specs['IBUTOL']+specs['METACETOH']+specs['C6H13CO2H']+specs['BOXCHO'] \
        +specs['METHCOACET']+specs['CHOOMCO2H']+specs['HO2C54CO2H']+specs['NBUACAOH']+specs['NBUACCOH'] \
        +specs['HMACO2H']+specs['ETOHOCHO']+specs['NC6H14']+specs['C5H8']+specs['HO13C4OH'] \
        +specs['MEMOXYCO2H']+specs['C3H5CO2H']+specs['DECOH']+specs['IPRACBCO2H']+specs['M3PECOH'] \
        +specs['C3H6']+specs['C3H8']+specs['NPRACCOH']+specs['C2H6']+specs['C2H4'] \
        +specs['M2HEXAOH']+specs['CBUT2ENE']+specs['H2C3OCOH']+specs['M3HEXBOH']+specs['C54OH'] \
        +specs['HO134C5']+specs['MBO']+specs['TBUT2ENE']+specs['M3PEBOH']+specs['BUT1ENE'] \
        +specs['IPECOH']+specs['IPEAOH']+specs['M2PEDOH']+specs['C2H5OH']+specs['ACETCOC2H5'] \
        +specs['ETHFORMOH']+specs['ETOHCO2M']+specs['CHOOCHO']+specs['HM2C43CO2H']+specs['CH3CO2H'] \
        +specs['HO14C6']+specs['PR2OHMOX']+specs['HO36C12']+specs['HO36C10']
    specs['cn1'] = specs['CH3NO3']+specs['CH3OH']+specs['CH3O2NO2']+specs['HCOOH']+specs['HCHO'] \
        +specs['CH3OOH']
    specs['cn2'] = specs['ETHGLY']+specs['ETHO2HNO3']+specs['CH3CO3H']+specs['HOCH2CO2H']+specs['PAN'] \
        +specs['HOCH2CO3H']+specs['C2H5NO3']+specs['HYETHO2H']+specs['HCOCH2OOH']+specs['NO3CH2PAN'] \
        +specs['VINOH']+specs['ETHOHNO3']+specs['NO3CH2CO3H']+specs['C2H5OOH']+specs['PHAN'] \
        +specs['NO3CH2CO2H']+specs['CH3CHO']+specs['HOCH2CHO']+specs['HCOCO2H']+specs['HCOCO3H'] \
        +specs['GLYOX']+specs['C2H6']+specs['C2H4']+specs['NO3CH2CHO']+specs['C2H5OH'] \
        +specs['CH3CO2H']
    specs['cn3'] = specs['CHOPRNO3']+specs['IPROPOL']+specs['CH3OCH2OOH']+specs['NOA']+specs['CH2CHCH2OOH'] \
        +specs['C32OH13CO']+specs['IPROPOLPER']+specs['C3NO3COOOH']+specs['ALLYLOH']+specs['A2PAN'] \
        +specs['IPROPOLO2H']+specs['PROPGLY']+specs['HOCHOCOOH']+specs['CH3COCO2H']+specs['C2OHOCOOH'] \
        +specs['C3PAN2']+specs['C3PAN1']+specs['HOC2H4CO2H']+specs['ALCOCH2OOH']+specs['PR2O2HNO3'] \
        +specs['CH3COCO3H']+specs['PR1O2HNO3']+specs['HOC2H4CO3H']+specs['PROPALOOH']+specs['C3DIOLOOH'] \
        +specs['HCOCH2CHO']+specs['HO1C3OOH']+specs['HYPROPO2H']+specs['ACO2H']+specs['PERPROACID'] \
        +specs['CH3CHOHCHO']+specs['CH3OCH2OH']+specs['IPROPOLPAN']+specs['HCOCH2CO3H']+specs['CHOOCH2OH'] \
        +specs['CHOC2H4OOH']+specs['NMGLYOX']+specs['CH2CHCH2NO3']+specs['CH3OCH2NO3']+specs['PROPOLNO3'] \
        +specs['HCOCOHPAN']+specs['PRNO3CO2H']+specs['ETHOX']+specs['HYPERACET']+specs['NC3H7NO3'] \
        +specs['CH3OCH3']+specs['HOCH2COCHO']+specs['CH3COCH3']+specs['CHOOCH2OOH']+specs['ACRPAN'] \
        +specs['CH3OCHO']+specs['PRNO3CO3H']+specs['PRNO3PAN']+specs['ACO3H']+specs['HOC2H4CHO'] \
        +specs['OCCOHCOOH']+specs['MGLYOX']+specs['ETHOXOOH']+specs['IC3H7OOH']+specs['C42AOH'] \
        +specs['HOC3H6OH']+specs['C2OHOCO2H']+specs['HCOCH2CO2H']+specs['CH3COPAN']+specs['ACR'] \
        +specs['C33CO']+specs['NPROPOL']+specs['PROPACID']+specs['NC3H7OOH']+specs['HOCH2COCO2H'] \
        +specs['HO1C3NO3']+specs['C2H5CHO']+specs['OCCOHCOH']+specs['ACETOL']+specs['C3H6'] \
        +specs['C3H8']+specs['PPN']+specs['HCOCOHCO3H']+specs['IC3H7NO3']+specs['H13CO2C3'] \
        +specs['PROLNO3']+specs['CHOOCHO']+specs['CHOOCH2NO3']
    specs['cn4'] = specs['IBUTOLCNO3']+specs['IPRHOCO2H']+specs['MACROH']+specs['MEKAOOH']+specs['MPRANO3OOH'] \
        +specs['BIACETOOH']+specs['CO3C4NO3OH']+specs['C42OH']+specs['MACROOH']+specs['TBUTOLOOH'] \
        +specs['MACO2H']+specs['DHPMPAL']+specs['DHPMEK']+specs['MACRNCO2H']+specs['C4OCCOHCOH'] \
        +specs['MO2EOLA2OH']+specs['HVMK']+specs['IBUTALOH']+specs['HO1C4NO3']+specs['C312COCO3H'] \
        +specs['CONM2CO2H']+specs['BU1ENO3OOH']+specs['MACRNB']+specs['IPRHOCO3H']+specs['ETHFORMNO3'] \
        +specs['HMVKNGLYOX']+specs['HC3CCO3H']+specs['BUTDBOOH']+specs['C56NO3']+specs['NC3CHO'] \
        +specs['NBUTOLBOOH']+specs['HO13C3CO3H']+specs['MACO3H']+specs['HMVKANO3']+specs['MO2EOLB2OH'] \
        +specs['CONM2CO3H']+specs['CO23C4NO3']+specs['C42OOH']+specs['COHM2CO2H']+specs['MEMOXYCHO'] \
        +specs['HOC3H6CO3H']+specs['C3DBPAN']+specs['BUTALO2H']+specs['BUT2OLOOH']+specs['MOCOCH2OOH'] \
        +specs['NCO23CHO']+specs['CO2C3CO3H']+specs['HO13C3CHO']+specs['IBUDIALPAN']+specs['NBUTOLAOH'] \
        +specs['C4CO2OOH']+specs['METACETNO3']+specs['TC4H9OOH']+specs['C312COPAN']+specs['HMVKBOOH'] \
        +specs['CO2N3CHO']+specs['HOC3H6CO2H']+specs['BUTAL2NO3']+specs['PBN']+specs['HMACROOH'] \
        +specs['HO2C4NO3']+specs['PIPN']+specs['EGLYOX']+specs['CO2C3CO2H']+specs['NBUTDBNO3'] \
        +specs['MVKOHBOOH']+specs['CHOMOHCO3H']+specs['HOIPRCO3H']+specs['C4PAN2']+specs['C4PAN4'] \
        +specs['C4PAN5']+specs['C4PAN6']+specs['C4PAN7']+specs['C4PAN8']+specs['C4PAN9'] \
        +specs['NBUTOL']+specs['HOC4H8OH']+specs['CO2H3CO3H']+specs['C4ALDB']+specs['HO3C3CHO'] \
        +specs['CHOC2CO3H']+specs['C3H7CHO']+specs['BUTDANO3']+specs['IC4H10']+specs['IC4H9OOH'] \
        +specs['MEKCOH']+specs['NBUTDAOOH']+specs['IPRCHO']+specs['C4PAN1']+specs['TBUTOL'] \
        +specs['HO13C4NO3']+specs['CHOOMPAN']+specs['ALCOMOXOOH']+specs['C3DBCO3H']+specs['BUT2OLNO3'] \
        +specs['HO3C4NO3']+specs['HO2C3CO3H']+specs['CHOC2CO2H']+specs['MO2EOLBNO3']+specs['IBUTOLCO2H'] \
        +specs['NC4H10']+specs['MO2EOLANO3']+specs['HMACR']+specs['CHOC3DIOL']+specs['COHM2PAN'] \
        +specs['IBUTDIAL']+specs['HO3C3PAN']+specs['HO12CO3C4']+specs['PRPAL2CO3H']+specs['IBUTACID'] \
        +specs['BUTDBOH']+specs['MEKCOOH']+specs['C45NO3']+specs['HC3CO2H']+specs['METACETO2H'] \
        +specs['HO2C3CO2H']+specs['C4OCCOHOOH']+specs['ETOMENO3']+specs['HO1C4OOH']+specs['HO2C3CHO'] \
        +specs['C43NO34OOH']+specs['BUT2OLOH']+specs['NBUTOLAOOH']+specs['C413COOOH']+specs['MPRNO3CO2H'] \
        +specs['HOIPRCO2H']+specs['IBUTOLBNO3']+specs['MEKANO3']+specs['NMVK']+specs['HNMVKOH'] \
        +specs['MEPROPENE']+specs['HC3CO3H']+specs['MVKOOH']+specs['PRPAL2CO2H']+specs['HNMVKOOH'] \
        +specs['C41OOH']+specs['C4PAN10']+specs['NC4H9NO3']+specs['BUTONENO3']+specs['HOC3H6CHO'] \
        +specs['MOXY2CHO']+specs['MPRBNO3CHO']+specs['HMPAN']+specs['C3MDIALOH']+specs['HO1CO3CHO'] \
        +specs['METHACET']+specs['MO2EOL']+specs['C4PAN3']+specs['SC4H9NO3']+specs['C4CONO3OOH'] \
        +specs['C4OCCOHNO3']+specs['HOIPRCHO']+specs['H3NCO2CHO']+specs['VGLYOX']+specs['IBUTOLBO2H'] \
        +specs['HO2C4OH']+specs['C42NO33OOH']+specs['HC3CCHO']+specs['HC3CHO']+specs['HMACROH'] \
        +specs['COHM2CO3H']+specs['BUTDBNO3']+specs['HMACO3H']+specs['CO2N3PAN']+specs['MACRNO3'] \
        +specs['TBUTOLNO3']+specs['H14CO23C4']+specs['BUT2OLO']+specs['HMVKNO3']+specs['MVKOHAOH'] \
        +specs['BUTACID']+specs['MVKOHAOOH']+specs['CO2H3CHO']+specs['MEKAOH']+specs['H1CO23CHO'] \
        +specs['BUTALNO3']+specs['COC4NO3OOH']+specs['HMAC']+specs['CO2N3CO3H']+specs['MACROHOOH'] \
        +specs['TC4H9NO3']+specs['HO3C4OOH']+specs['NBUTOLBNO3']+specs['HNBIACET']+specs['MEKBOOH'] \
        +specs['MPRBNO3OOH']+specs['MVKOH']+specs['NC3CO2H']+specs['MEK']+specs['C4H6'] \
        +specs['MOXCOCH2OH']+specs['COCCOHCOOH']+specs['NBUTDAOH']+specs['C41OH']+specs['IC4H9NO3'] \
        +specs['MACRNBPAN']+specs['NC3CO3H']+specs['HO2C4OOH']+specs['BUTDAOOH']+specs['METACETHO'] \
        +specs['MEMOXYCO3H']+specs['BUT2OL']+specs['MVK']+specs['ETHFORM']+specs['NBUTDBOOH'] \
        +specs['IBUTOLOHC']+specs['IBUTOLOHB']+specs['MOXYCOCHO']+specs['BUTDCOOH']+specs['C4CONO3CO'] \
        +specs['ETOMEOH']+specs['IBUTOL']+specs['METACETOH']+specs['CONM2CHO']+specs['HO13C4OOH'] \
        +specs['CHOOMCO2H']+specs['NC4H9OOH']+specs['H13CO2CO3H']+specs['IBUTALO2H']+specs['MACRNBCO3H'] \
        +specs['HMACO2H']+specs['ETOHOCHO']+specs['IBUALANO3']+specs['CONM2PAN']+specs['HO13C4OH'] \
        +specs['C3MDIALOOH']+specs['C45OOH']+specs['MEMOXYCO2H']+specs['C3H5CO2H']+specs['BIACET'] \
        +specs['ETOMEOOH']+specs['H13CO2CHO']+specs['MPRBNO3PAN']+specs['NBUTOLANO3']+specs['MECOFOROOH'] \
        +specs['CO13C4OH']+specs['ETHFORMOOH']+specs['COCCOHNO3']+specs['PERIBUACID']+specs['C4NO3COOOH'] \
        +specs['CBUT2ENE']+specs['MACRNBCO2H']+specs['HO3C3CO3H']+specs['HO14CO2C4']+specs['MO2EOLAOOH'] \
        +specs['MVKNO3']+specs['C41NO3']+specs['CCOCOCOH']+specs['TBUT2ENE']+specs['CHOOMCO3H'] \
        +specs['MEMOXYPAN']+specs['MO2EOLBOOH']+specs['CHOC2PAN']+specs['BUT1ENE']+specs['PERBUACID'] \
        +specs['BIACETOH']+specs['CO2C3PAN']+specs['ETHFORMOH']+specs['C4CODIAL']+specs['SC4H9OOH'] \
        +specs['CHOMOHPAN']+specs['HOCO3C4OOH']+specs['CO2C3CHO']+specs['CO23C3CHO']+specs['MVKOHANO3'] \
        +specs['MPRNO3CO3H']+specs['IBUTALBO2H']+specs['MACR']+specs['MACRNCO3H']+specs['MACRNPAN'] \
        +specs['CO3C4NO3']
    specs['cn5'] = specs['PROL1MPAN']+specs['MAE']+specs['EOX2ETB2OH']+specs['CHOC3COPAN']+specs['C42CO3H'] \
        +specs['BUT2CO2H']+specs['MBOAOOH']+specs['HOIBUTCHO']+specs['C527OOH']+specs['PEBOH'] \
        +specs['MPRK']+specs['MMALNAPAN']+specs['C56OH']+specs['C510OH']+specs['PERPENACID'] \
        +specs['HO2C4CO2H']+specs['C51OH2OOH']+specs['ISOPCNO3']+specs['C47PAN']+specs['HM2C43NO3'] \
        +specs['INB1NACHO']+specs['ETHACETOH']+specs['C51NO324CO']+specs['ISOPANO3']+specs['CO2C4CHO'] \
        +specs['C5NO3OAOOH']+specs['MMALNBCO3H']+specs['C5NO3CO4OH']+specs['INCNO3']+specs['INANO3'] \
        +specs['C4MALOHOOH']+specs['M2BU2OLOOH']+specs['HO13C5OOH']+specs['DIETETOOH']+specs['HC4PAN'] \
        +specs['HO2C5OH']+specs['PEBOOH']+specs['HO2CO4C5']+specs['MIPKBNO3']+specs['C4OHCHO'] \
        +specs['CO23C5']+specs['ISOPAOOH']+specs['PR2OHMOOOH']+specs['PROH2MOX']+specs['DIEKBOOH'] \
        +specs['C3M3CHONO3']+specs['NC4CO2H']+specs['C52NO31CO']+specs['C54NO3']+specs['MIPKAOH'] \
        +specs['HNC524CO']+specs['C524OH']+specs['C5ONO34OOH']+specs['INB1OH']+specs['HO14CO3C5'] \
        +specs['CHOC3COOOH']+specs['C57NO3']+specs['C52OH3OOH']+specs['HOACETEOOH']+specs['MMALNBCO2H'] \
        +specs['C51NO3']+specs['INDHPPAN']+specs['NMBOBCO']+specs['C58NO3']+specs['HC4CCO2H'] \
        +specs['MPRKBOOH']+specs['HC4CHO']+specs['HO24C4CHO']+specs['C41CO2H']+specs['ME2BUT2ENE'] \
        +specs['C52OOH']+specs['ISOPBNO3']+specs['C52OH']+specs['DIETETHER']+specs['C43NO3PAN'] \
        +specs['HC4ACO2H']+specs['PENT1ENE']+specs['HO1C5OOH']+specs['MCOCOMOX']+specs['IPEBOOH'] \
        +specs['NC4CO3H']+specs['ME3CO2BUOL']+specs['IPRGLYOX']+specs['CO24C5']+specs['C526NO3'] \
        +specs['EOX2ETCHO']+specs['INAHPCHO']+specs['INANCHO']+specs['PROL2FORM']+specs['C4MDIAL'] \
        +specs['C4CHOBOOH']+specs['M3BU2OLNO3']+specs['C41CO3H']+specs['C51OH2CO']+specs['C536OOH'] \
        +specs['CHOC4OOH']+specs['EOX2OLBNO3']+specs['HM33C3NO3']+specs['HC4CCO3H']+specs['C530OOH'] \
        +specs['M2BUOL2OH']+specs['ETHACET']+specs['HC4ACO3H']+specs['C537OOH']+specs['C4MCONO3OH'] \
        +specs['TBUTCO3H']+specs['INAHCO2H']+specs['INANCO2H']+specs['MBOCOCO']+specs['C3ME3PAN'] \
        +specs['C524OOH']+specs['C31CO3H']+specs['HO2M2C4OH']+specs['PECNO3']+specs['C524CO'] \
        +specs['ETOC2NO3']+specs['C3MCODBPAN']+specs['HO24C4CO3H']+specs['MBOBNO3']+specs['HIEB2OOH'] \
        +specs['C525OOH']+specs['C534OOH']+specs['HO1CO24C5']+specs['INDHPCO3H']+specs['C43NO3CO3H'] \
        +specs['NC5H12']+specs['C4MNO32OOH']+specs['NC524OOH']+specs['H13C43CHO']+specs['ACEC2H4NO3'] \
        +specs['C3M3CHOOOH']+specs['INANCOCO2H']+specs['C43NO3CO2H']+specs['ETHACETOOH']+specs['HM22C3NO3'] \
        +specs['HO12C5']+specs['INB1OOH']+specs['PE2ENEANO3']+specs['C4M3NO3ONE']+specs['C52NO3'] \
        +specs['EOX2COMEOH']+specs['IPROCHO']+specs['NC4OHCPAN']+specs['INANCO3H']+specs['HO124C5'] \
        +specs['HO13C5']+specs['PEANO3']+specs['NEOP']+specs['ME3BUOLNO3']+specs['INCNCHO'] \
        +specs['ISOPDNO3']+specs['INB1HPCO2H']+specs['HC4ACHO']+specs['EOX2EOL']+specs['NC524NO3'] \
        +specs['ME3BUT1ENE']+specs['ISOP34OOH']+specs['PENTACID']+specs['MC3CODBPAN']+specs['NEOPOOH'] \
        +specs['INB1NBCHO']+specs['PECOOH']+specs['IPRMETOOH']+specs['INDOH']+specs['HC4CCHO'] \
        +specs['NEOPOH']+specs['INDHPCHO']+specs['C52OH1OOH']+specs['HO24C5OOH']+specs['INB1HPCO3H'] \
        +specs['C51OH']+specs['INB1HPPAN']+specs['C57OH']+specs['MMALNBPAN']+specs['C3ME3CHO'] \
        +specs['C47CO3H']+specs['ME2BUOLOOH']+specs['HO3C5NO3']+specs['ETOMECO2H']+specs['C4NO3PAN'] \
        +specs['C4M22CONO3']+specs['HO2C43CHO']+specs['C53NO32CO']+specs['PPEN']+specs['EOCOCHO'] \
        +specs['IPEBOH']+specs['C523OH']+specs['HM22CO3H']+specs['CO3C4CO2H']+specs['C5PAN10'] \
        +specs['HOBUT2CHO']+specs['C5PAN19']+specs['C5PAN18']+specs['C5PAN11']+specs['C5PAN13'] \
        +specs['C5PAN12']+specs['C5PAN15']+specs['C5PAN17']+specs['C5PAN14']+specs['C5PAN16'] \
        +specs['C31PAN']+specs['HO13M2C4']+specs['EOX2ETA2OH']+specs['C5HPALD2']+specs['C5HPALD1'] \
        +specs['INB1NBCO3H']+specs['HPC52OOH']+specs['H2M3C4OOH']+specs['HPC52PAN']+specs['C58OH'] \
        +specs['IC5H12']+specs['BUT2CHO']+specs['C3MNO3PAN']+specs['INAHCO3H']+specs['C58NO3CO3H'] \
        +specs['IPECOOH']+specs['INB1NAPAN']+specs['C4M2NO3OOH']+specs['C5CO234']+specs['HOIBUTCO3H'] \
        +specs['HO3C4CHO']+specs['IPEAOOH']+specs['PE1ENEBNO3']+specs['C5CONO3OOH']+specs['MBOANO3'] \
        +specs['ME3BU3ECHO']+specs['C59OOH']+specs['PEAOH']+specs['PRONEMOOOH']+specs['MPRKAOOH'] \
        +specs['C57NO3PAN']+specs['ETOMECO3H']+specs['HO1CO34C5']+specs['HM22C3OOH']+specs['HM22C3OH'] \
        +specs['INB1NBPAN']+specs['C3M3OH2PAN']+specs['C527NO3']+specs['TBUTCHO']+specs['CO23C54OOH'] \
        +specs['PECOH']+specs['CO3C4CO3H']+specs['C58ANO3']+specs['MMALNACO2H']+specs['C3ME3CO3H'] \
        +specs['IEC2OOH']+specs['HM2C43OOH']+specs['HO2C5NO3']+specs['H2C3OCNO3']+specs['C535OOH'] \
        +specs['MBOAOH']+specs['NC524OH']+specs['C4ME3HO23']+specs['PROL11MNO3']+specs['MIPK'] \
        +specs['INB1NACO3H']+specs['MIPKBOOH']+specs['C53OH2OOH']+specs['INCCO']+specs['HO2C43CO3H'] \
        +specs['PEBNO3']+specs['PRONFORM']+specs['M2BU2OLNO3']+specs['C4M2NO3ONE']+specs['HO2C54NO3'] \
        +specs['INAOOH']+specs['H2M2C3CHO']+specs['MIPKAOOH']+specs['HO2M2C4OOH']+specs['INB1NBCO2H'] \
        +specs['MIPKBOH']+specs['C4MCNO3OOH']+specs['MCOCOMOOOH']+specs['ME3BUOLOOH']+specs['INB2OOH'] \
        +specs['HPC52CO3H']+specs['NMBOBOOH']+specs['INB1HPCHO']+specs['DIEKAOH']+specs['ETACETOH'] \
        +specs['MMALNACO3H']+specs['C3ME3CO2H']+specs['C58NO3PAN']+specs['HO2C4CO3H']+specs['C5CO23CHO'] \
        +specs['C4ME3HO12']+specs['C4M2AL2OH']+specs['C3MNO3CO3H']+specs['NMBOAOOH']+specs['C5PAN9'] \
        +specs['NISOPNO3']+specs['ME2BUT1ENE']+specs['CO23C4CO3H']+specs['C4NO3CHO']+specs['ALC4DOLOOH'] \
        +specs['CO23C4CHO']+specs['ACETETCHO']+specs['PE2ONE1OOH']+specs['ACETMECO3H']+specs['INB1NACO2H'] \
        +specs['INANCOPAN']+specs['IPRFORMOOH']+specs['INB1NO3']+specs['INDOOH']+specs['PROL1MCHO'] \
        +specs['HO2C43CO2H']+specs['C53OH']+specs['DNC524CO']+specs['C4MNO31OOH']+specs['HO13C5NO3'] \
        +specs['DIETETNO3']+specs['C23O3CHO']+specs['ME3BUOL']+specs['INB1CO']+specs['HO1C5NO3'] \
        +specs['ACETMEPAN']+specs['DIEKBNO3']+specs['HO1CO3C5']+specs['INANCOCO3H']+specs['PR2OHMONO3'] \
        +specs['C57AOOH']+specs['ETACETNO3']+specs['HIEB1OOH']+specs['C4CHOBNO3']+specs['MECOACEOOH'] \
        +specs['C57OOH']+specs['IPRFORMOH']+specs['C56OOH']+specs['CPENT2ENE']+specs['C55OOH'] \
        +specs['NISOPOOH']+specs['C54OOH']+specs['HO14CO2C5']+specs['C3MNO3CO2H']+specs['PRNFORMOOH'] \
        +specs['HM33C3OOH']+specs['C53NO324CO']+specs['HMML']+specs['INCNPAN']+specs['HO24C5'] \
        +specs['C51OOH']+specs['M3BU2OLOOH']+specs['M2BUOL2NO3']+specs['DIETETOH']+specs['HO13CO4C5'] \
        +specs['ISOPDOH']+specs['ISOPBOOH']+specs['M3BU3ECO3H']+specs['HOBUT2CO2H']+specs['C3M3OH2CHO'] \
        +specs['BOXPOLBOOH']+specs['TPENT2ENE']+specs['C524NO3']+specs['C4OHPAN']+specs['EOX2OLAOOH'] \
        +specs['INAHPCO3H']+specs['C4NO3CO3H']+specs['C5CO234OOH']+specs['ETOMEPAN']+specs['ETOC2OOH'] \
        +specs['NC51OOH']+specs['PRONEMOXOH']+specs['C5OHCO4OOH']+specs['ACEC2H4OOH']+specs['HM22CO2H'] \
        +specs['IPEBNO3']+specs['ISOPBOH']+specs['CO13C4CHO']+specs['HO2CO4CHO']+specs['HOBUT2CO3H'] \
        +specs['PROL1MCO3H']+specs['CO24C53OOH']+specs['M3BU3EPAN']+specs['HOC4CHOOOH']+specs['IPRFORMNO3'] \
        +specs['C526OOH']+specs['ISOPDOOH']+specs['EOX2OLBOOH']+specs['CO24C4CHO']+specs['PEAOOH'] \
        +specs['ISOPAOH']+specs['C4H9CHO']+specs['INAHCHO']+specs['ISOPCOOH']+specs['HOIPRGLYOX'] \
        +specs['C58OOH']+specs['INB1GLYOX']+specs['C530NO3']+specs['INCOOH']+specs['INANCOCHO'] \
        +specs['EOCOCH2OOH']+specs['CO2C5OH']+specs['C5CO23OOH']+specs['HO2C5OOH']+specs['HO2C4CHO'] \
        +specs['ISOP34NO3']+specs['C4NO3CO2H']+specs['NC526OOH']+specs['INAOH']+specs['MBOBOOH'] \
        +specs['INCOH']+specs['H2M2C3CO3H']+specs['IPRMEETOH']+specs['C4NO32MOOH']+specs['C5PAN8'] \
        +specs['C5PAN4']+specs['C5PAN7']+specs['C5PAN6']+specs['C5PAN1']+specs['C5PAN3'] \
        +specs['C5PAN2']+specs['HM22CHO']+specs['PE2ENEBNO3']+specs['DIEKAOOH']+specs['C3M3OHCO3H'] \
        +specs['METHCOACET']+specs['C5PACALD2']+specs['NEOPNO3']+specs['C5PACALD1']+specs['C5COCHOOOH'] \
        +specs['NC4CHO']+specs['C57NO3CO3H']+specs['M2BUOL2OOH']+specs['C58NO3CO2H']+specs['H13C43CO3H'] \
        +specs['INANPAN']+specs['HCOC5']+specs['INDHCO3H']+specs['C4M2ALOHNO3']+specs['INCGLYOX'] \
        +specs['IPEANO3']+specs['C510OOH']+specs['MPRKAOH']+specs['C5H8']+specs['HPNC524CO'] \
        +specs['PRONEMOX']+specs['C5124COOOH']+specs['C51NO32CO']+specs['INCNCO2H']+specs['C53OOH'] \
        +specs['MPRKNO3']+specs['C4NO3M2OOH']+specs['C4NO3M1OOH']+specs['CO2C43CHO']+specs['C5PAN5'] \
        +specs['ME2BUOLNO3']+specs['INANCO']+specs['C52NO31OOH']+specs['H2C3OCOH']+specs['CO2C4CO3H'] \
        +specs['INAHPPAN']+specs['C54OH']+specs['MBOACO']+specs['HO3C5OOH']+specs['HO24C5NO3'] \
        +specs['C58AOOH']+specs['HO134C5']+specs['C51NO32OOH']+specs['C4OHCO3H']+specs['HO2C54OOH'] \
        +specs['MBO']+specs['HC4CO3H']+specs['C57NO3CO2H']+specs['MBOBCO']+specs['EOX2OLANO3'] \
        +specs['C52NO33CO']+specs['IPECOH']+specs['IPEAOH']+specs['INDHCHO']+specs['C3MNO3CHO'] \
        +specs['C52NO33OOH']+specs['INAHPAN']+specs['CHOC4OHOOH']+specs['ACEETOHOOH']+specs['C4OH2CPAN'] \
        +specs['CO3C4CHO']+specs['PROL11MOOH']+specs['PE4E2CO']+specs['PGLYOX']+specs['HOCO3C5OOH'] \
        +specs['H2M3C4NO3']+specs['INAHPCO2H']+specs['INCNCO3H']+specs['C5NO3O4OOH']+specs['C4OH2CO3H'] \
        +specs['BUT2CO3H']+specs['NC4OHCO3H']+specs['H2C3OCOOH']+specs['ETOHCO2M']+specs['INDHPAN'] \
        +specs['PE1ENEANO3']+specs['MC3ODBCO2H']+specs['HOCO4C5OOH']+specs['PR2OHMOX']+specs['DIEK'] \
        +specs['C53NO32OOH']+specs['CO2C4CO2H']+specs['C47CHO']+specs['HO2M2C4NO3']+specs['C42CHO'] \
        +specs['IPECNO3']+specs['HO3C4CO3H']
    specs['cn6'] = specs['HEX3ONANO3']+specs['HM22COCHO']+specs['HM33C4OH']+specs['M23C4NO3']+specs['C4ME2OHNO3'] \
        +specs['HO1MC5OOH']+specs['M23C4OH']+specs['PRCOFOROOH']+specs['C4COMOH3OH']+specs['IPRACBOH'] \
        +specs['C6PAN23']+specs['C6PAN22']+specs['C3COCCO3H']+specs['C611OOH']+specs['C61NO3'] \
        +specs['IEPOXB']+specs['IEPOXA']+specs['IPRACOOH']+specs['HO3C6NO3']+specs['C63NO3'] \
        +specs['IPRACBPAN']+specs['ACETC2CO2H']+specs['HO3C5CHO']+specs['C67OH']+specs['C62NO335CO'] \
        +specs['CO24M3C5']+specs['MIBKBOOH']+specs['CHOC4CO3H']+specs['HO1CO4C6']+specs['C51CO3H'] \
        +specs['C5NO3COAO2']+specs['CHOC4PAN']+specs['M22C3CHO']+specs['C6NO3CO4OH']+specs['CHEXNO3'] \
        +specs['HEX2ONBOOH']+specs['HIEPOXB']+specs['C6CONO3OOH']+specs['CO23C6']+specs['PRCOFORM'] \
        +specs['C1H4C5CO3H']+specs['C6COALCO2H']+specs['MTBKNO3']+specs['IEACO3H']+specs['IPROACET'] \
        +specs['C64NO335CO']+specs['C6CONO34OH']+specs['HEXBOH']+specs['M2PE']+specs['C51CO2H'] \
        +specs['C6CYTONOOH']+specs['H3M3C5NO3']+specs['ACETC2CO3H']+specs['CHEX']+specs['MTBEBOH'] \
        +specs['C5H11CO3H']+specs['H2M2C4CO2H']+specs['ACPRONEOH']+specs['C6COCHOPAN']+specs['M22C4OOH'] \
        +specs['C6PAN21']+specs['C6PAN20']+specs['C65OH']+specs['M2PEAOH']+specs['PXYFUOOH'] \
        +specs['CO1H63NO3']+specs['MIBK3CO']+specs['ACEC2CHO']+specs['M33C3CO3H']+specs['M2PEAOOH'] \
        +specs['C42MNO3OOH']+specs['M2C43CO3H']+specs['M22C43OOH']+specs['ACCOMEPAN']+specs['C65NO3CO2H'] \
        +specs['M33C4NO3']+specs['C65OH4OOH']+specs['DM23BU2ENE']+specs['CYHXONANO3']+specs['HO2C6OOH'] \
        +specs['MIBKAOH3CO']+specs['ACCOCOMOOH']+specs['C4ME22OH']+specs['CO24C6']+specs['MTBE'] \
        +specs['C6CO134']+specs['IEPOXC']+specs['MTBK']+specs['H2M2C4CO3H']+specs['HO4C5CO3H'] \
        +specs['MTBEAALNO3']+specs['PXYFUONE']+specs['HO1CO24C6']+specs['M3F']+specs['H1MC5NO3'] \
        +specs['C613OOH']+specs['EIPKBNO3']+specs['M23C4']+specs['HEXANO3']+specs['C6DIALOOH'] \
        +specs['C54CO3H']+specs['MIBKOHAOOH']+specs['M2PEDNO3']+specs['C531OOH']+specs['BOXMOH'] \
        +specs['M2BKANO3']+specs['HM22C4OOH']+specs['BUFORMOOH']+specs['M3PE']+specs['MTBKOH'] \
        +specs['C64OOH']+specs['C5124COPAN']+specs['HEXCNO3']+specs['CO24M3C5OH']+specs['C6CO3HO25'] \
        +specs['H2M2C4CHO']+specs['C6CO134OOH']+specs['C23O3CCO3H']+specs['ACCOMECHO']+specs['C67OOH'] \
        +specs['HO2M2C5OOH']+specs['C6CODIAL']+specs['EIPKAOOH']+specs['C6TONOHOOH']+specs['HO3C5CO2H'] \
        +specs['M2C43CO2H']+specs['MIBK']+specs['MTBEAALPAN']+specs['C65NO3CO3H']+specs['C61OH'] \
        +specs['C65OOH']+specs['HO2MC5NO3']+specs['HM22C3CHO']+specs['C63OH']+specs['CYC6DIONE'] \
        +specs['ACPRONEOOH']+specs['CYHXDIOLA']+specs['MTBEBNO3']+specs['C67CHO']+specs['HO2M2C5NO3'] \
        +specs['C6CO134PAN']+specs['CO2C54CO2H']+specs['IEB1CHO']+specs['HO14M3C5']+specs['HO5C6OOH'] \
        +specs['C610NO3']+specs['C68OH']+specs['C23O3CCO2H']+specs['M3C4CHO']+specs['HM23C4OOH'] \
        +specs['C6COHOCHO']+specs['CO3C5CHO']+specs['MTBEACHOHO']+specs['C6CO3OHOOH']+specs['CYHEXOL'] \
        +specs['HO3C5CO3H']+specs['CO3C5CO3H']+specs['H3M2C4CO3H']+specs['MTBEANO3']+specs['M33C3CO2H'] \
        +specs['NPROACET']+specs['C1H4C5CO2H']+specs['IPROC21OH']+specs['H3M3C5OOH']+specs['CHEX2ENE'] \
        +specs['C612OH']+specs['HM33C3CO2H']+specs['HM2C43CHO']+specs['CO234C6']+specs['IECCHO'] \
        +specs['M3PEAOOH']+specs['HM22C3CO3H']+specs['M3PEBOOH']+specs['C65NO36OOH']+specs['M3PECOOH'] \
        +specs['C3COCPAN']+specs['CO2C54CO3H']+specs['H134M3C5']+specs['NPRACBOH']+specs['PXYFUOH'] \
        +specs['HEX1ENE']+specs['IPRACBOOH']+specs['C64OH5OOH']+specs['C67NO3']+specs['IEB4CHO'] \
        +specs['MMALNHYOOH']+specs['H13M3C5OOH']+specs['CO25C6OH']+specs['CO234C6OOH']+specs['CY6DIONOH'] \
        +specs['CYHXOLAOOH']+specs['IPROC21NO3']+specs['CYHEXONE']+specs['IECPAN']+specs['M23C43NO3'] \
        +specs['M33C4OH']+specs['HO2C54CO3H']+specs['HO2MC5OOH']+specs['HO1MC5NO3']+specs['H13M3C5NO3'] \
        +specs['C531CO']+specs['M23C43OH']+specs['ACCOETOOH']+specs['MTBEACHO13']+specs['C610OH'] \
        +specs['M2PECOH']+specs['H13M3CO4C5']+specs['C6OH5NO3']+specs['CO3C5CO2H']+specs['MTBEBCO2H'] \
        +specs['C66NO35CO']+specs['HEX2ONANO3']+specs['NPRACBNO3']+specs['C43OHCOCHO']+specs['H2MC5OOH'] \
        +specs['NPXYFUOOH']+specs['HM22C3CO2H']+specs['CO35C5CHO']+specs['MIBKHO14']+specs['C63NO32CO'] \
        +specs['M2PEBOOH']+specs['HM23C4OH']+specs['HEX2ONCOOH']+specs['C62NO33CO']+specs['C5H11CHO'] \
        +specs['M22C4OH']+specs['C23O3CCHO']+specs['C6CO34HO1']+specs['MIBKBOH']+specs['CO1C6NO3'] \
        +specs['C6COALCO3H']+specs['C4COMEOH']+specs['MIBKAOHNO3']+specs['MMALANHY']+specs['MIBKOHBOOH'] \
        +specs['HO3C6OOH']+specs['MTBEBPAN']+specs['M3PEAOH']+specs['NPRACAOOH']+specs['HO1C6NO3'] \
        +specs['HO5C5CHO']+specs['C6COCHOOOH']+specs['HM33C4NO3']+specs['C68NO3']+specs['C6CO3HO14'] \
        +specs['C63NO32OOH']+specs['C69OH']+specs['ACECOCOCH3']+specs['C645OH']+specs['CY6DIONOOH'] \
        +specs['HEXBNO3']+specs['MTBEBOOH']+specs['CO23C65OOH']+specs['M2BKAOH']+specs['CO2M33CO2H'] \
        +specs['HEX2ONBNO3']+specs['C1H4C5PAN']+specs['HEX3ONCOOH']+specs['H13M3C5']+specs['MIBKAOOH'] \
        +specs['C6NO3CO5OH']+specs['H2M3CO4CHO']+specs['HO1C6OOH']+specs['HEX3ONBOOH']+specs['C6DIAL'] \
        +specs['C6NO3COOOH']+specs['EIPEOH']+specs['C64OH']+specs['C4ME2OHOOH']+specs['ACETC2PAN'] \
        +specs['C67CO3H']+specs['PRNOCOMOOH']+specs['MTBKOOH']+specs['HEX3ONAOOH']+specs['M3C4CO3H'] \
        +specs['HEXCOH']+specs['IPRACOH']+specs['C66NO35OH']+specs['HEXAOH']+specs['M23C4OOH'] \
        +specs['CO2HOC6OOH']+specs['CO2M3C4CHO']+specs['CO2M33CO3H']+specs['C6NO324CO']+specs['HEX3ONDOH'] \
        +specs['CO24C6OOH']+specs['C63OOH']+specs['MTBEACHO']+specs['IPRACNO3']+specs['BOXMOOH'] \
        +specs['IEAPAN']+specs['NPRACAOH']+specs['M2BK']+specs['HEX3ONE']+specs['C611OH'] \
        +specs['C23C54CO3H']+specs['H3M3C4CO3H']+specs['CHEXOOH']+specs['C65OH4NO3']+specs['HO14MC5'] \
        +specs['C3COCCHO']+specs['CO1H63OH']+specs['CO25C6']+specs['MIBKHO4OOH']+specs['EIPKAOH'] \
        +specs['MIBKAOH']+specs['CO2HO3C6']+specs['EIPKBOOH']+specs['C66NO35OOH']+specs['C5TRONCO3H'] \
        +specs['HM22C4NO3']+specs['MTBEAOH']+specs['ACCOMECO3H']+specs['M2BKAOOH']+specs['C23O3CPAN'] \
        +specs['C69OOH']+specs['NPRACCNO3']+specs['H2M3C4CO3H']+specs['MIBK3COOOH']+specs['M2PEBOH'] \
        +specs['HEXCOOH']+specs['EIPEOOH']+specs['M2PEANO3']+specs['M22C3CO3H']+specs['M22C4NO3'] \
        +specs['MTBEBCHO']+specs['HO2M2C5OH']+specs['MIBKOH34']+specs['C6PAN3']+specs['IPRACBCHO'] \
        +specs['C6PAN5']+specs['CYHXONAOH']+specs['HM33C3CHO']+specs['MMALNHY2OH']+specs['HO2C6NO3'] \
        +specs['CYHXONAOOH']+specs['M33C4OOH']+specs['M2PECNO3']+specs['H3M3C4CHO']+specs['C6PAN19'] \
        +specs['HO25C6']+specs['MTBEALCO3H']+specs['M22C43NO3']+specs['MTBEAALOOH']+specs['C610OOH'] \
        +specs['C6PAN12']+specs['CO2C54CHO']+specs['C6PAN14']+specs['CO3C54CO3H']+specs['HEX3ONDNO3'] \
        +specs['H2M3C4CHO']+specs['HM23C4NO3']+specs['C6CO34']+specs['CO3C54CHO']+specs['C61OOH'] \
        +specs['C64NO3']+specs['HEX2ONE']+specs['H1MC5OOH']+specs['M22C4']+specs['H2M3C4CO2H'] \
        +specs['M3PEBNO3']+specs['MTBEAOOH']+specs['C66OOH']+specs['CO235C6']+specs['M3PECNO3'] \
        +specs['PHXN']+specs['C6PAN2']+specs['C6PAN1']+specs['C6PAN6']+specs['C6PAN7'] \
        +specs['C6PAN4']+specs['MTBEALCO2H']+specs['C6PAN8']+specs['C6PAN9']+specs['EIPKBOH'] \
        +specs['C54CHO']+specs['C23C54CHO']+specs['M2C43CHO']+specs['CO2M33CHO']+specs['HEX2ONAOOH'] \
        +specs['M2BKBOH']+specs['BUOHFORM']+specs['M3PEANO3']+specs['C656OH']+specs['C66OH'] \
        +specs['MIBKHO4CHO']+specs['C533OOH']+specs['IECCO3H']+specs['M22C43OH']+specs['IPROC21OOH'] \
        +specs['IPRACBCO3H']+specs['CYHXOLANO3']+specs['BOXCHO']+specs['HEX3ONAOH']+specs['CY6TRION'] \
        +specs['HEX3ONCOH']+specs['C62OOH']+specs['NPRACBOOH']+specs['HO2C54CO2H']+specs['MBKCOOHOOH'] \
        +specs['H2MC5NO3']+specs['NPRACCOOH']+specs['NC6H14']+specs['CO2M3C5OH']+specs['CO2MC5OH'] \
        +specs['C6CO3HO4']+specs['ACEPROPONE']+specs['IPRACBCO2H']+specs['PRCOOMOOH']+specs['M3PECOH'] \
        +specs['M2PEBNO3']+specs['M33C3CHO']+specs['M2PECOOH']+specs['C6135COOOH']+specs['NPRACCOH'] \
        +specs['CO2HO4C6']+specs['CYHXOLACO']+specs['C64OH5NO3']+specs['C612OOH']+specs['IPRACBNO3'] \
        +specs['HO5C5CO3H']+specs['M23C43OOH']+specs['CONO3C6OOH']+specs['C65NO3PAN']+specs['HM2C43CO3H'] \
        +specs['CO1H63OOH']+specs['C65NO36CHO']+specs['M2PEDOOH']+specs['HEX3ONDOOH']+specs['CO1C6OH'] \
        +specs['CO24M3CHO']+specs['M3PEBOH']+specs['M2PEDOH']+specs['C68OOH']+specs['HEXAOOH'] \
        +specs['C6OH5OOH']+specs['NPRACANO3']+specs['ACETCOC2H5']+specs['C6PAN18']+specs['HEXBOOH'] \
        +specs['C6PAN10']+specs['C6PAN11']+specs['C6PAN13']+specs['MTBEBCO3H']+specs['C6PAN15'] \
        +specs['C6PAN16']+specs['C6PAN17']+specs['CYC613DION']+specs['IEACHO']+specs['CO25C6OOH'] \
        +specs['M2BKBOOH']+specs['C6145COOOH']+specs['HM33C4OOH']+specs['C532CO']+specs['HO2CO5C6'] \
        +specs['C6CO23HO5']+specs['HM2C43CO2H']+specs['HO14C6']+specs['CY6COCOOOH']+specs['C66CO'] \
        +specs['C62NO33OOH']+specs['C6CO34OOH']+specs['C6HOCOOOH']+specs['HO2C54CHO']+specs['C6DIALOH'] \
        +specs['CO1C6OOH']+specs['EIPK']+specs['MIBKANO3']+specs['HM33C3CO3H']+specs['C4COMOHOOH'] \
        +specs['C61CO']
    specs['cn7'] = specs['TBUACET']+specs['NBUTACET']+specs['BOX2COMOH']+specs['M3HEXBNO3']+specs['PRCOOMCHO'] \
        +specs['HEPTOH']+specs['C713OH']+specs['ACETCOC3H7']+specs['M3CO25C6']+specs['NBUACBNO3'] \
        +specs['BOX2OHBOOH']+specs['C7PAN1']+specs['DIIPRETOH']+specs['ETBEAOH']+specs['M2HEXBOOH'] \
        +specs['CO25C74OH']+specs['ETBEANO3']+specs['C77CO']+specs['H14M4C6']+specs['SBUACCOH'] \
        +specs['SBUACAOH']+specs['M3HEXAOH']+specs['HO3CO6C7']+specs['C75OOH']+specs['C77OH'] \
        +specs['SBUACAOOH']+specs['M3HEX']+specs['SBUACBOOH']+specs['C7PAN2']+specs['C78OH'] \
        +specs['ACCOCOC2H5']+specs['BUOX2ETOH']+specs['C6H13CHO']+specs['SBUACCOOH']+specs['M2HEXBOH'] \
        +specs['HEPTOOH']+specs['ETBECCO3H']+specs['DIIPRETHER']+specs['H3M3C5CO2H']+specs['ACEBUTBONE'] \
        +specs['CO245C7']+specs['M2HEXANO3']+specs['H25M2C6']+specs['H3M3C6NO3']+specs['C74OOH'] \
        +specs['BOXEOHBNO3']+specs['M2HEX']+specs['ETBEACHO']+specs['PHPTN']+specs['BOXOHETOH'] \
        +specs['CO25C73OH']+specs['C71OOH']+specs['HO3C76OOH']+specs['NBUACCOOH']+specs['H2M4C65OOH'] \
        +specs['NBUACAOOH']+specs['ACCOPROOH']+specs['IPROMC2NO3']+specs['ETBECOH']+specs['C73OOH'] \
        +specs['ACOMCOMOOH']+specs['H2M2CO5C6']+specs['TBOCOCH2OH']+specs['H2M2C65OOH']+specs['C710OOH'] \
        +specs['ACCOPRONE']+specs['M3HEXANO3']+specs['NBUACBOH']+specs['C72OH']+specs['TBUACCO'] \
        +specs['IPROMC2OH']+specs['C78OOH']+specs['CO3C75OOH']+specs['C712NO3']+specs['ETBEBNO3'] \
        +specs['M2CO5C6']+specs['M3HEXBOOH']+specs['PRCOOMCO3H']+specs['CO25C73OOH']+specs['HO2CO35C7'] \
        +specs['IPROMCCHO']+specs['HEPTNO3']+specs['ETBEACO3H']+specs['HO6C7OOH']+specs['ACEBUTONE'] \
        +specs['DIIPRETNO3']+specs['PRCOOETOH']+specs['C72NO3']+specs['M2HEXBNO3']+specs['C77OOH'] \
        +specs['BOXEOHANO3']+specs['CO235C7']+specs['BOX2OHAOOH']+specs['H25M3C6']+specs['C76OOH'] \
        +specs['SBUACEONE']+specs['C714OH']+specs['H3M3C5CO3H']+specs['C712OH']+specs['H2M3CO5C6'] \
        +specs['ACBUONBOOH']+specs['TBUACCO3H']+specs['C714OOH']+specs['BOX2ECHO']+specs['NBUACBOOH'] \
        +specs['H2M4C65NO3']+specs['ETBEAPAN']+specs['BOCOCH2OOH']+specs['BOXCOCHO']+specs['C713OOH'] \
        +specs['ETBEAOOH']+specs['C711OOH']+specs['CO25C7']+specs['C715OOH']+specs['C79OOH'] \
        +specs['SBUACBOH']+specs['BOX2E2OH']+specs['SBUTACET']+specs['ACBUOAOOH']+specs['MCOOTBNO3'] \
        +specs['IPROMCCO3H']+specs['TBUACOH']+specs['PRCOOMPAN']+specs['SBUACANO3']+specs['HEPT3ONE'] \
        +specs['ETBECNO3']+specs['SBUACBNO3']+specs['BOXCOALOOH']+specs['HO25C7']+specs['ACBUONAOH'] \
        +specs['H2M5C65OOH']+specs['BOXMCO2H']+specs['C6H13CO3H']+specs['ETBECCHO']+specs['NC7H16'] \
        +specs['H3M3C5CHO']+specs['NBUACCNO3']+specs['ETBEBOH']+specs['ACBUONBOH']+specs['NBUACANO3'] \
        +specs['M2HEXAOOH']+specs['IPROMCPAN']+specs['ETBE']+specs['BOXMCO3H']+specs['ACBUONANO3'] \
        +specs['C77NO3']+specs['H3M3C6OOH']+specs['H2M2C65NO3']+specs['C6H13CO2H']+specs['M3CO245C6'] \
        +specs['HO3C76NO3']+specs['NBUACAOH']+specs['NBUACCOH']+specs['ACCOCOEOOH']+specs['ETBECPAN'] \
        +specs['IPROMC2OOH']+specs['HO5C6CO3H']+specs['C78CO']+specs['C712OOH']+specs['M2HEXAOH'] \
        +specs['M3HEXBOH']+specs['TBUACPAN']+specs['ETBEBOOH']+specs['MCOOTBOOH']+specs['H2M5C65NO3'] \
        +specs['M3HEXAOOH']+specs['M3CO5C6']+specs['H2M4CO5C6']+specs['DIIPRETOOH']+specs['HO2CO5C7'] \
        +specs['BOXMPAN']+specs['C72OOH']+specs['ETBECOOH']+specs['TBOCOCHO']+specs['CO25C74OOH']
    specs['cn8'] = specs['BOXCOCOME']+specs['BOXPRONOH']+specs['C81OOH']+specs['NC8H18']+specs['C82OOH'] \
        +specs['HO3CO6C8']+specs['BOXPROANO3']+specs['CO3C85OOH']+specs['OCTOOH']+specs['C84OH'] \
        +specs['BOX2COMOOH']+specs['BOXPOLBNO3']+specs['BOX2PROL']+specs['OCTOH']+specs['CO346C8'] \
        +specs['HO3C86NO3']+specs['CO36C8']+specs['BOXCOEOL']+specs['C82NO3']+specs['C84OOH'] \
        +specs['BOXPROBOOH']+specs['HO3CO46C8']+specs['BOXPRONE']+specs['BOXPOLANO3']+specs['OCT3ONE'] \
        +specs['C8PAN1']+specs['BOXCOOLOOH']+specs['HO3C86OOH']+specs['BOXPROOOH']+specs['C83OOH'] \
        +specs['MPAN']+specs['BOXPR2OH']+specs['HO2M2C5O2']+specs['OCTNO3']+specs['BOXOHPROL'] \
        +specs['PRCOOPROL']+specs['BOXPRONBOH']+specs['HO36C8']+specs['HO6C7CO3H']+specs['HO7C8OOH'] \
        +specs['PRCOOPRONE']+specs['BOXPOLAOOH']+specs['HO34CO6C8']+specs['PRNOCOPOOH']
    specs['cn9'] = specs['NC9H20']+specs['NONNO3']+specs['CO356C9']+specs['C93NO3']+specs['C93OH'] \
        +specs['HO3C96NO3']+specs['HO4CO7C9']+specs['C95OOH']+specs['C92OOH']+specs['HO7C8CO3H'] \
        +specs['C94OOH']+specs['C93CO']+specs['NONOOH']+specs['NON3ONE']+specs['NONOH'] \
        +specs['C91OOH']+specs['C94OH']+specs['HO8C9OOH']+specs['HO3C96OOH']+specs['HO36C9'] \
        +specs['C93OOH']+specs['CO36C9']+specs['C9PAN1']
    specs['cn0'] = specs['DECNO3']+specs['C111OOH']+specs['DEC3ONE']+specs['C112OOH']+specs['C124OH'] \
        +specs['C123CO']+specs['C114OH']+specs['C122OOH']+specs['C123OOH']+specs['CL'] \
        +specs['NC12H26']+specs['DDECOOH']+specs['HO6CO9C11']+specs['HO3C106NO3']+specs['C10PAN1'] \
        +specs['HO3C126NO3']+specs['HO3C116OOH']+specs['C103NO3']+specs['C113OOH']+specs['C103OOH'] \
        +specs['HO36C11']+specs['C104OOH']+specs['C105OOH']+specs['HO5CO8C10']+specs['UDECOOH'] \
        +specs['NC10H22']+specs['DECOOH']+specs['C113OH']+specs['C103OH']+specs['HO8C9CO3H'] \
        +specs['C121OOH']+specs['DDEC3ONE']+specs['UDEC3ONE']+specs['C124OOH']+specs['DDECNO3'] \
        +specs['C114OOH']+specs['C115OOH']+specs['C123NO3']+specs['NC11H24']+specs['HO3C106OOH'] \
        +specs['C113CO']+specs['DDECOH']+specs['HO3C116NO3']+specs['C123OH']+specs['HO3C126OOH'] \
        +specs['CO36C10']+specs['UDECOH']+specs['C101OOH']+specs['C113NO3']+specs['DECOH'] \
        +specs['CO36C11']+specs['CO36C12']+specs['C125OOH']+specs['HO7CO10C12']+specs['UDECNO3'] \
        +specs['CO356C10']+specs['CO356C11']+specs['CO356C12']+specs['C102OOH']+specs['C103CO'] \
        +specs['HO36C12']+specs['HO36C10']+specs['C104OH']
    specs['oc1'] = specs['TBUACET']+specs['NBUTACET']+specs['IPROPOL']+specs['HM33C4OH']+specs['NC9H20'] \
        +specs['DECNO3']+specs['M23C4OH']+specs['M3HEXBNO3']+specs['BUT2CO2H']+specs['BOXCOCOME'] \
        +specs['HOIBUTCHO']+specs['C111OOH']+specs['PEBOH']+specs['MPRK']+specs['HEPTOH'] \
        +specs['BOXPRONOH']+specs['C713OH']+specs['HO3C5CHO']+specs['M3CO25C6']+specs['CO24M3C5'] \
        +specs['CO2C4CHO']+specs['HO1CO4C6']+specs['DEC3ONE']+specs['C112OOH']+specs['C5NO3COAO2'] \
        +specs['DIIPRETOH']+specs['M22C3CHO']+specs['ETBEAOH']+specs['HO2C5OH']+specs['M2HEXBOOH'] \
        +specs['PEBOOH']+specs['HO2CO4C5']+specs['C4OHCHO']+specs['C124OH']+specs['CO23C5'] \
        +specs['CO23C6']+specs['CO25C74OH']+specs['ALLYLOH']+specs['C77CO']+specs['NC8H18'] \
        +specs['H14M4C6']+specs['MIPKAOH']+specs['NONNO3']+specs['IPROACET']+specs['C123CO'] \
        +specs['HEXBOH']+specs['M2PE']+specs['CO356C9']+specs['M3HEXAOH']+specs['HO3CO6C7'] \
        +specs['C75OOH']+specs['CHEX']+specs['HO3CO6C8']+specs['MTBEBOH']+specs['C77OH'] \
        +specs['C114OH']+specs['HC4CHO']+specs['C122OOH']+specs['M22C4OOH']+specs['CO3C85OOH'] \
        +specs['M2PEAOH']+specs['OCTOOH']+specs['C123OOH']+specs['ME2BUT2ENE']+specs['C52OH'] \
        +specs['MIBK3CO']+specs['DIETETHER']+specs['M2PEAOOH']+specs['M3HEX']+specs['PENT1ENE'] \
        +specs['M22C43OOH']+specs['NC12H26']+specs['DM23BU2ENE']+specs['IPEBOOH']+specs['C78OH'] \
        +specs['BUOX2ETOH']+specs['C6H13CHO']+specs['ME3CO2BUOL']+specs['C4ME22OH']+specs['IPRGLYOX'] \
        +specs['CO24C6']+specs['CO24C5']+specs['MTBE']+specs['MTBK']+specs['DDECOOH'] \
        +specs['M2HEXBOH']+specs['HEPTOOH']+specs['C84OH']+specs['C4MDIAL']+specs['PXYFUONE'] \
        +specs['C51OH2CO']+specs['DIIPRETHER']+specs['H3M3C5CO2H']+specs['M3F']+specs['M23C4'] \
        +specs['M2BUOL2OH']+specs['BOXMOH']+specs['CO245C7']+specs['M3PE']+specs['M2HEXANO3'] \
        +specs['MTBKOH']+specs['HO6CO9C11']+specs['H2M2C4CHO']+specs['H25M2C6']+specs['HO2M2C4OH'] \
        +specs['BOX2PROL']+specs['OCTOH']+specs['HO3C106NO3']+specs['M2C43CO2H']+specs['MIBK'] \
        +specs['NBUTOL']+specs['CO346C8']+specs['NC5H12']+specs['M2HEX']+specs['ETBEACHO'] \
        +specs['HM22C3CHO']+specs['CYC6DIONE']+specs['C4ALDB']+specs['HO3C126NO3']+specs['CYHXDIOLA'] \
        +specs['HO12C5']+specs['CO25C73OH']+specs['HO14M3C5']+specs['HO3C116OOH']+specs['C3H7CHO'] \
        +specs['HO13C5']+specs['M3C4CHO']+specs['NEOP']+specs['CO3C5CHO']+specs['HO3C76OOH'] \
        +specs['CYHEXOL']+specs['M33C3CO2H']+specs['NPROACET']+specs['HC4ACHO']+specs['IC4H10'] \
        +specs['CO36C8']+specs['IPROC21OH']+specs['C113OOH']+specs['CHEX2ENE']+specs['H2M4C65OOH'] \
        +specs['C103OOH']+specs['HO36C11']+specs['ME3BUT1ENE']+specs['IPRCHO']+specs['HM2C43CHO'] \
        +specs['PENTACID']+specs['M3PEAOOH']+specs['M3PEBOOH']+specs['TBUTOL']+specs['NEOPOOH'] \
        +specs['M3PECOOH']+specs['ETBECOH']+specs['C104OOH']+specs['PECOOH']+specs['HEX1ENE'] \
        +specs['HC4CCHO']+specs['NEOPOH']+specs['HO5CO8C10']+specs['C93OH']+specs['HO3C96NO3'] \
        +specs['H2M2CO5C6']+specs['CYHEXONE']+specs['H2M2C65OOH']+specs['M33C4OH']+specs['C3ME3CHO'] \
        +specs['BOXCOEOL']+specs['HO2C43CHO']+specs['M23C43OH']+specs['NC4H10']+specs['C710OOH'] \
        +specs['IPEBOH']+specs['C523OH']+specs['M2PECOH']+specs['HOBUT2CHO']+specs['M3HEXANO3'] \
        +specs['HO13M2C4']+specs['UDECOOH']+specs['C72OH']+specs['M2PEBOOH']+specs['IC5H12'] \
        +specs['BUT2CHO']+specs['HO4CO7C9']+specs['HM23C4OH']+specs['IPROMC2OH']+specs['IPECOOH'] \
        +specs['C5H11CHO']+specs['HO3CO46C8']+specs['M22C4OH']+specs['MIBKBOH']+specs['HO3C4CHO'] \
        +specs['IPEAOOH']+specs['CO3C75OOH']+specs['NC10H22']+specs['DECOOH']+specs['C4COMEOH'] \
        +specs['M2CO5C6']+specs['M3HEXBOOH']+specs['ME3BU3ECHO']+specs['PEAOH']+specs['BOXPRONE'] \
        +specs['HM22C3OH']+specs['HO2CO35C7']+specs['MEPROPENE']+specs['TBUTCHO']+specs['IPROMCCHO'] \
        +specs['HEPTNO3']+specs['M3PEAOH']+specs['C113OH']+specs['PECOH']+specs['HO5C5CHO'] \
        +specs['OCT3ONE']+specs['HO6C7OOH']+specs['C645OH']+specs['C4ME3HO23']+specs['M2BKAOH'] \
        +specs['MIPK']+specs['M2HEXBNO3']+specs['H2M2C3CHO']+specs['H13M3C5']+specs['C103OH'] \
        +specs['CH3COCH3']+specs['CO235C7']+specs['C6DIAL']+specs['EIPEOH']+specs['HO3C86OOH'] \
        +specs['MIPKBOH']+specs['H25M3C6']+specs['HEXCOH']+specs['DIEKAOH']+specs['HEXAOH'] \
        +specs['M23C4OOH']+specs['C3ME3CO2H']+specs['CO2M3C4CHO']+specs['C4ME3HO12']+specs['C92OOH'] \
        +specs['C714OH']+specs['HEX3ONDOH']+specs['C712OH']+specs['HO8C9CO3H']+specs['H2M3CO5C6'] \
        +specs['ME2BUT1ENE']+specs['BOX2ECHO']+specs['MTBEACHO']+specs['HO7C8CO3H']+specs['C121OOH'] \
        +specs['M2BK']+specs['PROL1MCHO']+specs['C94OOH']+specs['HEX3ONE']+specs['DDEC3ONE'] \
        +specs['CHEXOOH']+specs['UDEC3ONE']+specs['HO14MC5']+specs['ME3BUOL']+specs['C124OOH'] \
        +specs['HO1CO3C5']+specs['C93CO']+specs['C3COCCHO']+specs['CO25C6']+specs['CO25C7'] \
        +specs['DDECNO3']+specs['CPENT2ENE']+specs['EIPKAOH']+specs['NONOOH']+specs['MIBKAOH'] \
        +specs['CO2HO3C6']+specs['C114OOH']+specs['SBUTACET']+specs['C115OOH']+specs['HO24C5'] \
        +specs['MTBEAOH']+specs['ISOPDOH']+specs['MPAN']+specs['BOXPR2OH']+specs['C3M3OH2CHO'] \
        +specs['TPENT2ENE']+specs['C123NO3']+specs['OCTNO3']+specs['M2PEBOH']+specs['HEXCOOH'] \
        +specs['MTBEBCHO']+specs['HO2M2C5OH']+specs['NC11H24']+specs['HO3C106OOH']+specs['C113CO'] \
        +specs['DDECOH']+specs['CYHXONAOH']+specs['HM33C3CHO']+specs['ACR']+specs['NON3ONE'] \
        +specs['M33C4OOH']+specs['HEPT3ONE']+specs['ISOPBOH']+specs['H3M3C4CHO']+specs['HO25C7'] \
        +specs['HO25C6']+specs['MEK']+specs['HO3C116NO3']+specs['CO2C54CHO']+specs['C4H6'] \
        +specs['H2M5C65OOH']+specs['C6H13CO3H']+specs['H2M3C4CHO']+specs['ETBECCHO']+specs['NC7H16'] \
        +specs['C6CO34']+specs['CO3C54CHO']+specs['PEAOOH']+specs['ISOPAOH']+specs['C4H9CHO'] \
        +specs['HEX2ONE']+specs['NPROPOL']+specs['M22C4']+specs['H3M3C5CHO']+specs['ETBEBOH'] \
        +specs['CO2C5OH']+specs['EIPKBOH']+specs['BUT2OL']+specs['HO2C4CHO']+specs['NONOH'] \
        +specs['C54CHO']+specs['M2C43CHO']+specs['MVK']+specs['CO2M33CHO']+specs['M2HEXAOOH'] \
        +specs['M2BKBOH']+specs['C123OH']+specs['C91OOH']+specs['ETBE']+specs['BOXOHPROL'] \
        +specs['PRCOOPROL']+specs['BOXPRONBOH']+specs['C94OH']+specs['H3M3C6OOH']+specs['C656OH'] \
        +specs['HO3C126OOH']+specs['CO36C10']+specs['M22C43OH']+specs['HM22CHO']+specs['HO8C9OOH'] \
        +specs['UDECOH']+specs['HO3C96OOH']+specs['HO36C9']+specs['HO36C8']+specs['IBUTOL'] \
        +specs['C101OOH']+specs['C6H13CO2H']+specs['BOXCHO']+specs['M3CO245C6']+specs['HEX3ONAOH'] \
        +specs['HEX3ONCOH']+specs['HCOC5']+specs['C2H5CHO']+specs['C113NO3']+specs['MPRKAOH'] \
        +specs['NC6H14']+specs['C5H8']+specs['CO2M3C5OH']+specs['CO2MC5OH']+specs['C93OOH'] \
        +specs['C6CO3HO4']+specs['DECOH']+specs['M3PECOH']+specs['M33C3CHO']+specs['M2PECOOH'] \
        +specs['C3H6']+specs['HO7C8OOH']+specs['C3H8']+specs['PRCOOPRONE']+specs['CO2HO4C6'] \
        +specs['CYHXOLACO']+specs['C78CO']+specs['CO2C43CHO']+specs['C2H6']+specs['C2H4'] \
        +specs['M2HEXAOH']+specs['CBUT2ENE']+specs['M23C43OOH']+specs['M3HEXBOH']+specs['CO36C11'] \
        +specs['CO36C12']+specs['M2PEDOOH']+specs['MBO']+specs['TBUT2ENE']+specs['CO36C9'] \
        +specs['CO1C6OH']+specs['M3PEBOH']+specs['BUT1ENE']+specs['C125OOH']+specs['IPECOH'] \
        +specs['IPEAOH']+specs['M2PEDOH']+specs['HO34CO6C8']+specs['M3HEXAOOH']+specs['HEXAOOH'] \
        +specs['M3CO5C6']+specs['HO7CO10C12']+specs['CO3C4CHO']+specs['HEXBOOH']+specs['H2M4CO5C6'] \
        +specs['PE4E2CO']+specs['PGLYOX']+specs['CYC613DION']+specs['UDECNO3']+specs['HO2CO5C7'] \
        +specs['HO2CO5C6']+specs['CO356C10']+specs['CO356C11']+specs['CO356C12']+specs['HO14C6'] \
        +specs['C102OOH']+specs['DIEK']+specs['C103CO']+specs['HO36C12']+specs['HO36C10'] \
        +specs['HO2C54CHO']+specs['EIPK']+specs['C104OH']+specs['MACR']
    specs['oc2'] = specs['HEX3ONANO3']+specs['HM22COCHO']+specs['IPRHOCO2H']+specs['MACROH']+specs['M23C4NO3'] \
        +specs['C4ME2OHNO3']+specs['MEKAOOH']+specs['HO1MC5OOH']+specs['BOX2COMOH']+specs['MAE'] \
        +specs['EOX2ETB2OH']+specs['PRCOOMCHO']+specs['C4COMOH3OH']+specs['MBOAOOH']+specs['IPRACBOH'] \
        +specs['C3COCCO3H']+specs['C611OOH']+specs['C61NO3']+specs['CH2CHCH2OOH']+specs['C56OH'] \
        +specs['IEPOXB']+specs['IEPOXA']+specs['IPRACOOH']+specs['HO3C6NO3']+specs['C63NO3'] \
        +specs['TBUTOLOOH']+specs['MACO2H']+specs['ACETC2CO2H']+specs['PERPENACID']+specs['ACETCOC3H7'] \
        +specs['HO2C4CO2H']+specs['C51OH2OOH']+specs['ISOPCNO3']+specs['HM2C43NO3']+specs['C67OH'] \
        +specs['ETHACETOH']+specs['C62NO335CO']+specs['ISOPANO3']+specs['MIBKBOOH']+specs['C4OCCOHCOH'] \
        +specs['CHOC4CO3H']+specs['HVMK']+specs['C51CO3H']+specs['NBUACBNO3']+specs['IBUTALOH'] \
        +specs['BOX2OHBOOH']+specs['C7PAN1']+specs['M2BU2OLOOH']+specs['HO13C5OOH']+specs['DIETETOOH'] \
        +specs['C6NO3CO4OH']+specs['CHEXNO3']+specs['HEX2ONBOOH']+specs['MIPKBNO3']+specs['HIEPOXB'] \
        +specs['ISOPAOOH']+specs['PRCOFORM']+specs['C1H4C5CO3H']+specs['PROH2MOX']+specs['C81OOH'] \
        +specs['ETBEANO3']+specs['C6COALCO2H']+specs['DIEKBOOH']+specs['C3M3CHONO3']+specs['PROPGLY'] \
        +specs['C52NO31CO']+specs['MTBKNO3']+specs['SBUACCOH']+specs['SBUACAOH']+specs['C524OH'] \
        +specs['BUTDBOOH']+specs['C64NO335CO']+specs['HO14CO3C5']+specs['C52OH3OOH']+specs['C6CONO34OH'] \
        +specs['C51CO2H']+specs['C6CYTONOOH']+specs['H3M3C5NO3']+specs['NBUTOLBOOH']+specs['C82OOH'] \
        +specs['MACO3H']+specs['HC4CCO2H']+specs['C5H11CO3H']+specs['MPRKBOOH']+specs['H2M2C4CO2H'] \
        +specs['ACPRONEOH']+specs['BOXPROANO3']+specs['C65OH']+specs['MEMOXYCHO']+specs['HO24C4CHO'] \
        +specs['C41CO2H']+specs['CO1H63NO3']+specs['C52OOH']+specs['ISOPBNO3']+specs['SBUACAOOH'] \
        +specs['ACEC2CHO']+specs['BUTALO2H']+specs['BUT2OLOOH']+specs['M33C3CO3H']+specs['C42MNO3OOH'] \
        +specs['HC4ACO2H']+specs['HO1C5OOH']+specs['M2C43CO3H']+specs['SBUACBOOH']+specs['C7PAN2'] \
        +specs['C65NO3CO2H']+specs['MCOCOMOX']+specs['HO13C3CHO']+specs['M33C4NO3']+specs['C65OH4OOH'] \
        +specs['CYHXONANO3']+specs['HO2C6OOH']+specs['ACCOCOC2H5']+specs['MIBKAOH3CO']+specs['SBUACCOOH'] \
        +specs['C6CO134']+specs['IEPOXC']+specs['H2M2C4CO3H']+specs['EOX2ETCHO']+specs['PROL2FORM'] \
        +specs['NBUTOLAOH']+specs['HO4C5CO3H']+specs['TC4H9OOH']+specs['C4CHOBOOH']+specs['HOC3H6CO2H'] \
        +specs['M3BU2OLNO3']+specs['C41CO3H']+specs['ETBECCO3H']+specs['HO1CO24C6']+specs['CHOC4OOH'] \
        +specs['HM33C3NO3']+specs['HC4CCO3H']+specs['H1MC5NO3']+specs['C613OOH']+specs['EIPKBNO3'] \
        +specs['C530OOH']+specs['HEXANO3']+specs['ETHACET']+specs['C6DIALOOH']+specs['C54CO3H'] \
        +specs['HC4ACO3H']+specs['MIBKOHAOOH']+specs['M2PEDNO3']+specs['EGLYOX']+specs['CO2C3CO2H'] \
        +specs['BOX2COMOOH']+specs['M2BKANO3']+specs['ACEBUTBONE']+specs['HM22C4OOH']+specs['BOXPOLBNO3'] \
        +specs['BUFORMOOH']+specs['C64OOH']+specs['TBUTCO3H']+specs['HEXCNO3']+specs['CO24M3C5OH'] \
        +specs['MBOCOCO']+specs['C6CO3HO25']+specs['C524OOH']+specs['C6CO134OOH']+specs['ACCOMECHO'] \
        +specs['PECNO3']+specs['C67OOH']+specs['H3M3C6NO3']+specs['C524CO']+specs['HO2M2C5OOH'] \
        +specs['C6CODIAL']+specs['EIPKAOOH']+specs['HO3C5CO2H']+specs['HOC4H8OH']+specs['HO1CO24C5'] \
        +specs['HO3C86NO3']+specs['C61OH']+specs['C65OOH']+specs['HCOCH2CHO']+specs['HO2MC5NO3'] \
        +specs['C74OOH']+specs['BOXEOHBNO3']+specs['C10PAN1']+specs['H13C43CHO']+specs['C63OH'] \
        +specs['C3M3CHOOOH']+specs['PHPTN']+specs['MTBEBNO3']+specs['C67CHO']+specs['HM22C3NO3'] \
        +specs['HO2M2C5NO3']+specs['BOXOHETOH']+specs['HO3C3CHO']+specs['PE2ENEANO3']+specs['CO2C54CO2H'] \
        +specs['C4M3NO3ONE']+specs['IEB1CHO']+specs['C52NO3']+specs['EOX2COMEOH']+specs['IPROCHO'] \
        +specs['HO5C6OOH']+specs['C610NO3']+specs['C68OH']+specs['HO124C5']+specs['PEANO3'] \
        +specs['C71OOH']+specs['ME3BUOLNO3']+specs['HM23C4OOH']+specs['C6COHOCHO']+specs['ISOPDNO3'] \
        +specs['MTBEACHOHO']+specs['C6CO3OHOOH']+specs['HO3C5CO3H']+specs['CO3C5CO3H']+specs['H3M2C4CO3H'] \
        +specs['ACO2H']+specs['MTBEANO3']+specs['C93NO3']+specs['NBUACCOOH']+specs['EOX2EOL'] \
        +specs['C103NO3']+specs['C1H4C5CO2H']+specs['H3M3C5OOH']+specs['IC4H9OOH']+specs['C612OH'] \
        +specs['HM33C3CO2H']+specs['MEKCOH']+specs['NBUACAOOH']+specs['ISOP34OOH']+specs['CO234C6'] \
        +specs['IECCHO']+specs['HM22C3CO3H']+specs['ACCOPROOH']+specs['C65NO36OOH']+specs['IPROMC2NO3'] \
        +specs['C73OOH']+specs['CO2C54CO3H']+specs['IPRMETOOH']+specs['H134M3C5']+specs['CH3CHOHCHO'] \
        +specs['NPRACBOH']+specs['PXYFUOH']+specs['IPRACBOOH']+specs['C64OH5OOH']+specs['C67NO3'] \
        +specs['IEB4CHO']+specs['H13M3C5OOH']+specs['CO25C6OH']+specs['CO234C6OOH']+specs['C3DBCO3H'] \
        +specs['C105OOH']+specs['CY6DIONOH']+specs['C52OH1OOH']+specs['HO24C5OOH']+specs['CYHXOLAOOH'] \
        +specs['IPROC21NO3']+specs['TBOCOCH2OH']+specs['M23C43NO3']+specs['C51OH']+specs['C57OH'] \
        +specs['HO2C54CO3H']+specs['HO2MC5OOH']+specs['HO1MC5NO3']+specs['ME2BUOLOOH']+specs['HO3C5NO3'] \
        +specs['CHOC2CO2H']+specs['H13M3C5NO3']+specs['ETOMECO2H']+specs['C531CO']+specs['C53NO32CO'] \
        +specs['IBUTOLCO2H']+specs['EOCOCHO']+specs['HMACR']+specs['MTBEACHO13']+specs['ACCOPRONE'] \
        +specs['C610OH']+specs['CHOC3DIOL']+specs['H13M3CO4C5']+specs['HM22CO3H']+specs['C6OH5NO3'] \
        +specs['CO3C4CO2H']+specs['CO3C5CO2H']+specs['NBUACBOH']+specs['IBUTDIAL']+specs['HO12CO3C4'] \
        +specs['EOX2ETA2OH']+specs['C82NO3']+specs['C5HPALD2']+specs['C5HPALD1']+specs['IBUTACID'] \
        +specs['MTBEBCO2H']+specs['C84OOH']+specs['C66NO35CO']+specs['HEX2ONANO3']+specs['C43OHCOCHO'] \
        +specs['BUTDBOH']+specs['H2M3C4OOH']+specs['MEKCOOH']+specs['H2MC5OOH']+specs['C45NO3'] \
        +specs['HC3CO2H']+specs['HM22C3CO2H']+specs['CO35C5CHO']+specs['MIBKHO14']+specs['HO2C3CO2H'] \
        +specs['C63NO32CO']+specs['TBUACCO']+specs['C58OH']+specs['HO1C4OOH']+specs['HO2C3CHO'] \
        +specs['BOXPROBOOH']+specs['HEX2ONCOOH']+specs['BUT2OLOH']+specs['C62NO33CO']+specs['C23O3CCHO'] \
        +specs['C6CO34HO1']+specs['C78OOH']+specs['C5CO234']+specs['HOIBUTCO3H']+specs['NBUTOLAOOH'] \
        +specs['CO1C6NO3']+specs['PE1ENEBNO3']+specs['C6COALCO3H']+specs['C712NO3']+specs['HOIPRCO2H'] \
        +specs['MIBKAOHNO3']+specs['ETBEBNO3']+specs['MMALANHY']+specs['MIBKOHBOOH']+specs['MPRKAOOH'] \
        +specs['HO3C6OOH']+specs['PRCOOMCO3H']+specs['HO1CO34C5']+specs['HM22C3OOH']+specs['CO25C73OOH'] \
        +specs['MVKOOH']+specs['PRPAL2CO2H']+specs['CO23C54OOH']+specs['NC4H9NO3']+specs['CO3C4CO3H'] \
        +specs['HOC3H6CHO']+specs['BOXPOLANO3']+specs['C3ME3CO3H']+specs['NPRACAOOH']+specs['HM2C43OOH'] \
        +specs['HO1C6NO3']+specs['C8PAN1']+specs['C6COCHOOOH']+specs['HM33C4NO3']+specs['C68NO3'] \
        +specs['HO2C5NO3']+specs['ETBEACO3H']+specs['C6CO3HO14']+specs['C63NO32OOH']+specs['C3MDIALOH'] \
        +specs['HO1CO3CHO']+specs['METHACET']+specs['VINOH']+specs['MO2EOL']+specs['ETHOX'] \
        +specs['C69OH']+specs['SC4H9NO3']+specs['ACEBUTONE']+specs['ACECOCOCH3']+specs['DIIPRETNO3'] \
        +specs['MBOAOH']+specs['PRCOOETOH']+specs['BOXCOOLOOH']+specs['CY6DIONOOH']+specs['HOIPRCHO'] \
        +specs['PROL11MNO3']+specs['HEXBNO3']+specs['MTBEBOOH']+specs['CO23C65OOH']+specs['C72NO3'] \
        +specs['CO2M33CO2H']+specs['VGLYOX']+specs['HEX2ONBNO3']+specs['MIPKBOOH']+specs['C53OH2OOH'] \
        +specs['HO2C43CO3H']+specs['PEBNO3']+specs['C95OOH']+specs['IBUTOLBO2H']+specs['HO2C4OH'] \
        +specs['PRONFORM']+specs['HC3CCHO']+specs['M2BU2OLNO3']+specs['C4M2NO3ONE']+specs['HO2C54NO3'] \
        +specs['CH3OCH3']+specs['C77OOH']+specs['HEX3ONCOOH']+specs['MIPKAOOH']+specs['MIBKAOOH'] \
        +specs['HC3CHO']+specs['C6NO3CO5OH']+specs['H2M3CO4CHO']+specs['BOXEOHANO3']+specs['HO1C6OOH'] \
        +specs['BOX2OHAOOH']+specs['HEX3ONBOOH']+specs['HO2M2C4OOH']+specs['C64OH']+specs['C4ME2OHOOH'] \
        +specs['C67CO3H']+specs['ME3BUOLOOH']+specs['MTBKOOH']+specs['HEX3ONAOOH']+specs['M3C4CO3H'] \
        +specs['IPRACOH']+specs['C66NO35OH']+specs['C76OOH']+specs['HOC2H4CHO']+specs['ETACETOH'] \
        +specs['CO2HOC6OOH']+specs['HO2C4CO3H']+specs['C5CO23CHO']+specs['CO2M33CO3H']+specs['BOXPROOOH'] \
        +specs['C6NO324CO']+specs['SBUACEONE']+specs['H3M3C5CO3H']+specs['C4M2AL2OH']+specs['ACBUONBOOH'] \
        +specs['CO24C6OOH']+specs['TBUACCO3H']+specs['C714OOH']+specs['C63OOH']+specs['C4NO3CHO'] \
        +specs['BUT2OLO']+specs['CO23C4CHO']+specs['ACETETCHO']+specs['NBUACBOOH']+specs['BOXMOOH'] \
        +specs['BUTACID']+specs['PE2ONE1OOH']+specs['CO2H3CHO']+specs['NPRACAOH']+specs['MGLYOX'] \
        +specs['MEKAOH']+specs['H2M4C65NO3']+specs['HO2C43CO2H']+specs['C53OH']+specs['C611OH'] \
        +specs['C23C54CO3H']+specs['H3M3C4CO3H']+specs['C65OH4NO3']+specs['HO1C5NO3']+specs['HMAC'] \
        +specs['BOCOCH2OOH']+specs['BOXCOCHO']+specs['DIEKBNO3']+specs['C713OOH']+specs['ETBEAOOH'] \
        +specs['C711OOH']+specs['CO1H63OH']+specs['C4CHOBNO3']+specs['C715OOH']+specs['TC4H9NO3'] \
        +specs['C79OOH']+specs['IPRFORMOH']+specs['SBUACBOH']+specs['C56OOH']+specs['MIBKHO4OOH'] \
        +specs['C55OOH']+specs['C54OOH']+specs['HO14CO2C5']+specs['HO3C4OOH']+specs['EIPKBOOH'] \
        +specs['BOX2E2OH']+specs['C66NO35OOH']+specs['IC3H7OOH']+specs['HM33C3OOH']+specs['C83OOH'] \
        +specs['HMML']+specs['C51OOH']+specs['M3BU2OLOOH']+specs['M2BUOL2NO3']+specs['HOC3H6OH'] \
        +specs['DIETETOH']+specs['HO13CO4C5']+specs['HM22C4NO3']+specs['MEKBOOH']+specs['M2BKAOOH'] \
        +specs['ISOPBOOH']+specs['ACBUOAOOH']+specs['M3BU3ECO3H']+specs['HOBUT2CO2H']+specs['C69OOH'] \
        +specs['HO2M2C5O2']+specs['H2M3C4CO3H']+specs['MCOOTBNO3']+specs['MIBK3COOOH']+specs['IPROMCCO3H'] \
        +specs['EIPEOOH']+specs['M2PEANO3']+specs['M22C3CO3H']+specs['M22C4NO3']+specs['MIBKOH34'] \
        +specs['TBUACOH']+specs['C6PAN3']+specs['MVKOH']+specs['IPRACBCHO']+specs['SBUACANO3'] \
        +specs['ETOC2OOH']+specs['PRONEMOXOH']+specs['C5OHCO4OOH']+specs['HO2C6NO3']+specs['CYHXONAOOH'] \
        +specs['HM22CO2H']+specs['IPEBNO3']+specs['M2PECNO3']+specs['ETBECNO3']+specs['SBUACBNO3'] \
        +specs['BOXCOALOOH']+specs['M22C43NO3']+specs['CO13C4CHO']+specs['ACBUONAOH']+specs['MTBEAALOOH'] \
        +specs['HO2CO4CHO']+specs['C610OOH']+specs['HOBUT2CO3H']+specs['PROL1MCO3H']+specs['CO24C53OOH'] \
        +specs['CO3C54CO3H']+specs['HOC4CHOOOH']+specs['HEX3ONDNO3']+specs['BOXMCO2H']+specs['ISOPDOOH'] \
        +specs['HM23C4NO3']+specs['CO24C4CHO']+specs['C61OOH']+specs['C64NO3']+specs['H1MC5OOH'] \
        +specs['ISOPCOOH']+specs['HOIPRGLYOX']+specs['IC4H9NO3']+specs['H2M3C4CO2H']+specs['M3PEBNO3'] \
        +specs['NBUACCNO3']+specs['HO2C4OOH']+specs['PROPACID']+specs['CH3CHO']+specs['BUTDAOOH'] \
        +specs['MTBEAOOH']+specs['C66OOH']+specs['CO235C6']+specs['M3PECNO3']+specs['PHXN'] \
        +specs['MTBEALCO2H']+specs['C5CO23OOH']+specs['HO2C5OOH']+specs['C23C54CHO']+specs['ACBUONBOH'] \
        +specs['ISOP34NO3']+specs['NBUACANO3']+specs['ETHFORM']+specs['HEX2ONAOOH']+specs['MBOBOOH'] \
        +specs['IBUTOLOHC']+specs['IBUTOLOHB']+specs['BUOHFORM']+specs['M3PEANO3']+specs['BOXMCO3H'] \
        +specs['H2M2C3CO3H']+specs['C77NO3']+specs['C66OH']+specs['IPRMEETOH']+specs['MIBKHO4CHO'] \
        +specs['BUTDCOOH']+specs['H2M2C65NO3']+specs['NC3H7OOH']+specs['IPROC21OOH']+specs['CYHXOLANO3'] \
        +specs['PE2ENEBNO3']+specs['DIEKAOOH']+specs['C3M3OHCO3H']+specs['ETOMEOH']+specs['METHCOACET'] \
        +specs['C5PACALD2']+specs['NEOPNO3']+specs['C5PACALD1']+specs['CY6TRION']+specs['C5COCHOOOH'] \
        +specs['HO6C7CO3H']+specs['HO3C76NO3']+specs['NC4CHO']+specs['M2BUOL2OOH']+specs['C62OOH'] \
        +specs['NC4H9OOH']+specs['NPRACBOOH']+specs['HO2C54CO2H']+specs['NBUACAOH']+specs['NBUACCOH'] \
        +specs['IBUTALO2H']+specs['MBKCOOHOOH']+specs['HMACO2H']+specs['H2MC5NO3']+specs['IPEANO3'] \
        +specs['NPRACCOOH']+specs['ACETOL']+specs['HO13C4OH']+specs['C45OOH']+specs['C3H5CO2H'] \
        +specs['PRONEMOX']+specs['ACEPROPONE']+specs['IPRACBCO2H']+specs['BIACET']+specs['PRCOOMOOH'] \
        +specs['IPROMC2OOH']+specs['C51NO32CO']+specs['M2PEBNO3']+specs['HO5C6CO3H']+specs['C53OOH'] \
        +specs['C6135COOOH']+specs['NPRACCOH']+specs['MPRKNO3']+specs['C64OH5NO3']+specs['C612OOH'] \
        +specs['HO5C5CO3H']+specs['CO13C4OH']+specs['PERIBUACID']+specs['ME2BUOLNO3']+specs['C712OOH'] \
        +specs['H2C3OCOH']+specs['CO2C4CO3H']+specs['ETBEBOOH']+specs['C54OH']+specs['MBOACO'] \
        +specs['HM2C43CO3H']+specs['CO1H63OOH']+specs['HO3C5OOH']+specs['HO14CO2C4']+specs['HO134C5'] \
        +specs['C4OHCO3H']+specs['C65NO36CHO']+specs['HO2C54OOH']+specs['HEX3ONDOOH']+specs['HC4CO3H'] \
        +specs['CCOCOCOH']+specs['MCOOTBOOH']+specs['CO24M3CHO']+specs['MBOBCO']+specs['C52NO33CO'] \
        +specs['H2M5C65NO3']+specs['BOXPOLAOOH']+specs['C3MNO3CHO']+specs['C68OOH']+specs['PERBUACID'] \
        +specs['CHOC4OHOOH']+specs['C9PAN1']+specs['C6OH5OOH']+specs['BIACETOH']+specs['C2H5OH'] \
        +specs['ACETCOC2H5']+specs['C6PAN18']+specs['PROL11MOOH']+specs['C6PAN10']+specs['MTBEBCO3H'] \
        +specs['C6PAN15']+specs['C6PAN17']+specs['HOCO3C5OOH']+specs['IEACHO']+specs['H2M3C4NO3'] \
        +specs['C4CODIAL']+specs['CO25C6OOH']+specs['DIIPRETOOH']+specs['M2BKBOOH']+specs['C6145COOOH'] \
        +specs['BUT2CO3H']+specs['HM33C4OOH']+specs['C532CO']+specs['SC4H9OOH']+specs['ETOHCO2M'] \
        +specs['PE1ENEANO3']+specs['C6CO23HO5']+specs['HM2C43CO2H']+specs['MC3ODBCO2H']+specs['CO2C3CHO'] \
        +specs['HOCO4C5OOH']+specs['PR2OHMOX']+specs['C72OOH']+specs['ETBECOOH']+specs['CY6COCOOOH'] \
        +specs['CO23C3CHO']+specs['PRNOCOPOOH']+specs['C66CO']+specs['C62NO33OOH']+specs['C6CO34OOH'] \
        +specs['C6HOCOOOH']+specs['CO2C4CO2H']+specs['C6DIALOH']+specs['HO2M2C4NO3']+specs['CO1C6OOH'] \
        +specs['IBUTALBO2H']+specs['TBOCOCHO']+specs['C42CHO']+specs['MIBKANO3']+specs['HM33C3CO3H'] \
        +specs['C4COMOHOOH']+specs['IPECNO3']+specs['HO3C4CO3H']+specs['CO25C74OOH']+specs['C61CO']
    specs['oc3'] = specs['CHOPRNO3']+specs['PROL1MPAN']+specs['IBUTOLCNO3']+specs['ETHGLY']+specs['CHOC3COPAN'] \
        +specs['PRCOFOROOH']+specs['CH3OCH2OOH']+specs['C42CO3H']+specs['MPRANO3OOH']+specs['C527OOH'] \
        +specs['C6PAN23']+specs['C6PAN22']+specs['NOA']+specs['BIACETOOH']+specs['CO3C4NO3OH'] \
        +specs['C42OH']+specs['MACROOH']+specs['C510OH']+specs['IPRACBPAN']+specs['DHPMPAL'] \
        +specs['DHPMEK']+specs['INB1NACHO']+specs['C51NO324CO']+specs['MACRNCO2H']+specs['C5NO3OAOOH'] \
        +specs['MO2EOLA2OH']+specs['MMALNBCO3H']+specs['C5NO3CO4OH']+specs['INCNO3']+specs['CHOC4PAN'] \
        +specs['C32OH13CO']+specs['CH3CO3H']+specs['INANO3']+specs['C4MALOHOOH']+specs['HC4PAN'] \
        +specs['HO1C4NO3']+specs['C312COCO3H']+specs['CONM2CO2H']+specs['C6CONO3OOH']+specs['BU1ENO3OOH'] \
        +specs['IPROPOLPER']+specs['PR2OHMOOOH']+specs['IPROPOLO2H']+specs['MACRNB']+specs['IPRHOCO3H'] \
        +specs['ETHFORMNO3']+specs['NC4CO2H']+specs['HMVKNGLYOX']+specs['C54NO3']+specs['HOCH2CO2H'] \
        +specs['HNC524CO']+specs['IEACO3H']+specs['HC3CCO3H']+specs['C5ONO34OOH']+specs['HOCHOCOOH'] \
        +specs['INB1OH']+specs['CHOC3COOOH']+specs['C57NO3']+specs['HOACETEOOH']+specs['MMALNBCO2H'] \
        +specs['C51NO3']+specs['CH3COCO2H']+specs['NMBOBCO']+specs['C56NO3']+specs['C2OHOCOOH'] \
        +specs['NC3CHO']+specs['HO13C3CO3H']+specs['C58NO3']+specs['ACETC2CO3H']+specs['HMVKANO3'] \
        +specs['HOC2H4CO2H']+specs['MO2EOLB2OH']+specs['C6COCHOPAN']+specs['CONM2CO3H']+specs['CO23C4NO3'] \
        +specs['C6PAN21']+specs['C6PAN20']+specs['C42OOH']+specs['COHM2CO2H']+specs['PXYFUOOH'] \
        +specs['HOC3H6CO3H']+specs['C3DBPAN']+specs['ALCOCH2OOH']+specs['C43NO3PAN']+specs['MOCOCH2OOH'] \
        +specs['NCO23CHO']+specs['CO2C3CO3H']+specs['ACCOMEPAN']+specs['NC4CO3H']+specs['PR2O2HNO3'] \
        +specs['ACCOCOMOOH']+specs['C2H5NO3']+specs['C526NO3']+specs['IBUDIALPAN']+specs['INAHPCHO'] \
        +specs['INANCHO']+specs['C4CO2OOH']+specs['METACETNO3']+specs['CH3COCO3H']+specs['PR1O2HNO3'] \
        +specs['MTBEAALNO3']+specs['C312COPAN']+specs['HMVKBOOH']+specs['CO2N3CHO']+specs['C536OOH'] \
        +specs['BUTAL2NO3']+specs['EOX2OLBNO3']+specs['HOC2H4CO3H']+specs['PBN']+specs['HMACROOH'] \
        +specs['HO2C4NO3']+specs['PIPN']+specs['C531OOH']+specs['C537OOH']+specs['NBUTDBNO3'] \
        +specs['C4MCONO3OH']+specs['MVKOHBOOH']+specs['INAHCO2H']+specs['CHOMOHCO3H']+specs['C5124COPAN'] \
        +specs['HOIPRCO3H']+specs['INANCO2H']+specs['C3ME3PAN']+specs['C23O3CCO3H']+specs['C31CO3H'] \
        +specs['C4PAN2']+specs['C4PAN4']+specs['C4PAN5']+specs['C4PAN6']+specs['C4PAN7'] \
        +specs['C4PAN8']+specs['ETOC2NO3']+specs['PROPALOOH']+specs['C3MCODBPAN']+specs['HO24C4CO3H'] \
        +specs['C6TONOHOOH']+specs['MBOBNO3']+specs['HIEB2OOH']+specs['MTBEAALPAN']+specs['C525OOH'] \
        +specs['C65NO3CO3H']+specs['C534OOH']+specs['INDHPCO3H']+specs['C3DIOLOOH']+specs['C43NO3CO3H'] \
        +specs['CO2H3CO3H']+specs['C4MNO32OOH']+specs['NC524OOH']+specs['ACEC2H4NO3']+specs['ACPRONEOOH'] \
        +specs['INANCOCO2H']+specs['C43NO3CO2H']+specs['ETHACETOOH']+specs['INB1OOH']+specs['C6CO134PAN'] \
        +specs['CHOC2CO3H']+specs['HO1C3OOH']+specs['NC4OHCPAN']+specs['C23O3CCO2H']+specs['HYPROPO2H'] \
        +specs['INCNCHO']+specs['INB1HPCO2H']+specs['BUTDANO3']+specs['NC524NO3']+specs['NBUTDAOOH'] \
        +specs['C4PAN1']+specs['MC3CODBPAN']+specs['INB1NBCHO']+specs['C3COCPAN']+specs['PERPROACID'] \
        +specs['HO13C4NO3']+specs['INDOH']+specs['MMALNHYOOH']+specs['ALCOMOXOOH']+specs['INDHPCHO'] \
        +specs['ACOMCOMOOH']+specs['BUT2OLNO3']+specs['HO3C4NO3']+specs['IECPAN']+specs['INB1HPCO3H'] \
        +specs['CH3OCH2OH']+specs['HO2C3CO3H']+specs['C47CO3H']+specs['MO2EOLBNO3']+specs['C4NO3PAN'] \
        +specs['C4M22CONO3']+specs['HYETHO2H']+specs['PPEN']+specs['ACCOETOOH']+specs['MO2EOLANO3'] \
        +specs['HCOCH2CO3H']+specs['COHM2PAN']+specs['C5PAN10']+specs['C5PAN19']+specs['C5PAN18'] \
        +specs['C5PAN11']+specs['C5PAN13']+specs['C5PAN12']+specs['C5PAN15']+specs['C5PAN17'] \
        +specs['C5PAN14']+specs['C5PAN16']+specs['HO3C3PAN']+specs['CHOOCH2OH']+specs['C31PAN'] \
        +specs['PRPAL2CO3H']+specs['NPRACBNO3']+specs['HPC52OOH']+specs['NPXYFUOOH']+specs['METACETO2H'] \
        +specs['HCOCH2OOH']+specs['C4OCCOHOOH']+specs['ETOMENO3']+specs['C3MNO3PAN']+specs['C43NO34OOH'] \
        +specs['INAHCO3H']+specs['C58NO3CO3H']+specs['CH3OH']+specs['C4M2NO3OOH']+specs['C413COOOH'] \
        +specs['MPRNO3CO2H']+specs['C5CONO3OOH']+specs['MBOANO3']+specs['IBUTOLBNO3']+specs['MEKANO3'] \
        +specs['NMVK']+specs['C59OOH']+specs['HNMVKOH']+specs['PRONEMOOOH']+specs['CHOC2H4OOH'] \
        +specs['ETOMECO3H']+specs['NMGLYOX']+specs['CH2CHCH2NO3']+specs['C3M3OH2PAN']+specs['C527NO3'] \
        +specs['HC3CO3H']+specs['MTBEBPAN']+specs['HNMVKOOH']+specs['C41OOH']+specs['BUTONENO3'] \
        +specs['C58ANO3']+specs['MOXY2CHO']+specs['MMALNACO2H']+specs['PROPOLNO3']+specs['IEC2OOH'] \
        +specs['MPRBNO3CHO']+specs['PRNO3CO2H']+specs['HMPAN']+specs['H2C3OCNO3']+specs['C4PAN3'] \
        +specs['C4CONO3OOH']+specs['C535OOH']+specs['C4OCCOHNO3']+specs['NC524OH']+specs['H3NCO2CHO'] \
        +specs['HYPERACET']+specs['INCCO']+specs['C1H4C5PAN']+specs['C42NO33OOH']+specs['NC3H7NO3'] \
        +specs['INAOOH']+specs['HOCH2COCHO']+specs['ACRPAN']+specs['HMACROH']+specs['COHM2CO3H'] \
        +specs['CH3OCHO']+specs['INB1NBCO2H']+specs['C6NO3COOOH']+specs['ACETC2PAN']+specs['C4MCNO3OOH'] \
        +specs['MCOCOMOOOH']+specs['BUTDBNO3']+specs['PRNOCOMOOH']+specs['INB2OOH']+specs['HPC52CO3H'] \
        +specs['HMACO3H']+specs['NMBOBOOH']+specs['ACO3H']+specs['INB1HPCHO']+specs['MMALNACO3H'] \
        +specs['MACRNO3']+specs['C3MNO3CO3H']+specs['NMBOAOOH']+specs['TBUTOLNO3']+specs['C5PAN9'] \
        +specs['NISOPNO3']+specs['CO23C4CO3H']+specs['H14CO23C4']+specs['IPRACNO3']+specs['ALC4DOLOOH'] \
        +specs['HMVKNO3']+specs['MVKOHAOH']+specs['OCCOHCOOH']+specs['MVKOHAOOH']+specs['ACETMECO3H'] \
        +specs['INB1NACO2H']+specs['IEAPAN']+specs['IPRFORMOOH']+specs['INB1NO3']+specs['INDOOH'] \
        +specs['H1CO23CHO']+specs['DNC524CO']+specs['ETHOXOOH']+specs['C4MNO31OOH']+specs['HO13C5NO3'] \
        +specs['DIETETNO3']+specs['BUTALNO3']+specs['C23O3CHO']+specs['INB1CO']+specs['COC4NO3OOH'] \
        +specs['ETBEAPAN']+specs['ACETMEPAN']+specs['PR2OHMONO3']+specs['C57AOOH']+specs['ETACETNO3'] \
        +specs['HIEB1OOH']+specs['CO2N3CO3H']+specs['MACROHOOH']+specs['MECOACEOOH']+specs['C57OOH'] \
        +specs['NISOPOOH']+specs['C3MNO3CO2H']+specs['PRNFORMOOH']+specs['NBUTOLBNO3']+specs['C53NO324CO'] \
        +specs['C42AOH']+specs['HNBIACET']+specs['C5TRONCO3H']+specs['C2OHOCO2H']+specs['ACCOMECO3H'] \
        +specs['C23O3CPAN']+specs['NPRACCNO3']+specs['BOXPOLBOOH']+specs['C524NO3']+specs['C4OHPAN'] \
        +specs['MPRBNO3OOH']+specs['EOX2OLAOOH']+specs['INAHPCO3H']+specs['C4NO3CO3H']+specs['C5CO234OOH'] \
        +specs['PRCOOMPAN']+specs['ETOMEPAN']+specs['C6PAN5']+specs['NC51OOH']+specs['NC3CO2H'] \
        +specs['HCOCH2CO2H']+specs['ACEC2H4OOH']+specs['MMALNHY2OH']+specs['C2H5OOH']+specs['C6PAN19'] \
        +specs['MTBEALCO3H']+specs['C6PAN12']+specs['C6PAN14']+specs['M3BU3EPAN']+specs['MOXCOCH2OH'] \
        +specs['IPRFORMNO3']+specs['C526OOH']+specs['C33CO']+specs['COCCOHCOOH']+specs['EOX2OLBOOH'] \
        +specs['NBUTDAOH']+specs['C41OH']+specs['INAHCHO']+specs['C58OOH']+specs['NC3CO3H'] \
        +specs['INB1GLYOX']+specs['C530NO3']+specs['INCOOH']+specs['METACETHO']+specs['INANCOCHO'] \
        +specs['EOCOCH2OOH']+specs['C6PAN2']+specs['C6PAN1']+specs['C6PAN6']+specs['C6PAN7'] \
        +specs['C6PAN4']+specs['C6PAN8']+specs['C6PAN9']+specs['MEMOXYCO3H']+specs['C4NO3CO2H'] \
        +specs['NC526OOH']+specs['NBUTDBOOH']+specs['HOCH2CHO']+specs['INAOH']+specs['IPROMCPAN'] \
        +specs['INCOH']+specs['ACBUONANO3']+specs['C4NO32MOOH']+specs['C5PAN8']+specs['C533OOH'] \
        +specs['MOXYCOCHO']+specs['C5PAN4']+specs['C5PAN7']+specs['C5PAN6']+specs['C5PAN1'] \
        +specs['IECCO3H']+specs['C5PAN3']+specs['C5PAN2']+specs['HOCH2COCO2H']+specs['IPRACBCO3H'] \
        +specs['HCOCO2H']+specs['HCHO']+specs['C4CONO3CO']+specs['HO1C3NO3']+specs['METACETOH'] \
        +specs['CONM2CHO']+specs['HO13C4OOH']+specs['CHOOMCO2H']+specs['C57NO3CO3H']+specs['C58NO3CO2H'] \
        +specs['H13C43CO3H']+specs['H13CO2CO3H']+specs['MACRNBCO3H']+specs['INDHCO3H']+specs['ETOHOCHO'] \
        +specs['C4M2ALOHNO3']+specs['INCGLYOX']+specs['OCCOHCOH']+specs['IBUALANO3']+specs['C510OOH'] \
        +specs['ACCOCOEOOH']+specs['C3MDIALOOH']+specs['HPNC524CO']+specs['MEMOXYCO2H']+specs['ETOMEOOH'] \
        +specs['ETBECPAN']+specs['H13CO2CHO']+specs['C5124COOOH']+specs['GLYOX']+specs['INCNCO2H'] \
        +specs['C4NO3M2OOH']+specs['NBUTOLANO3']+specs['C4NO3M1OOH']+specs['MECOFOROOH']+specs['IPRACBNO3'] \
        +specs['ETHFORMOOH']+specs['COCCOHNO3']+specs['C5PAN5']+specs['INANCO']+specs['C4NO3COOOH'] \
        +specs['C52NO31OOH']+specs['MACRNBCO2H']+specs['CONO3C6OOH']+specs['C65NO3PAN']+specs['TBUACPAN'] \
        +specs['HO3C3CO3H']+specs['HO24C5NO3']+specs['C58AOOH']+specs['C51NO32OOH']+specs['MO2EOLAOOH'] \
        +specs['MVKNO3']+specs['C41NO3']+specs['PPN']+specs['CHOOMCO3H']+specs['C57NO3CO2H'] \
        +specs['MO2EOLBOOH']+specs['EOX2OLANO3']+specs['CHOC2PAN']+specs['HCOCOHCO3H']+specs['INDHCHO'] \
        +specs['C52NO33OOH']+specs['ACEETOHOOH']+specs['NPRACANO3']+specs['C4OH2CPAN']+specs['CO2C3PAN'] \
        +specs['ETHFORMOH']+specs['C6PAN11']+specs['C6PAN13']+specs['C6PAN16']+specs['INAHPCO2H'] \
        +specs['IC3H7NO3']+specs['H13CO2C3']+specs['C5NO3O4OOH']+specs['PROLNO3']+specs['C4OH2CO3H'] \
        +specs['NC4OHCO3H']+specs['H2C3OCOOH']+specs['BOXMPAN']+specs['CHOMOHPAN']+specs['CHOOCHO'] \
        +specs['HOCO3C4OOH']+specs['CH3CO2H']+specs['C53NO32OOH']+specs['MVKOHANO3']+specs['C47CHO'] \
        +specs['MPRNO3CO3H']+specs['MACRNCO3H']+specs['CO3C4NO3']
    specs['oc4'] = specs['ETHO2HNO3']+specs['MMALNAPAN']+specs['C47PAN']+specs['C3NO3COOOH']+specs['A2PAN'] \
        +specs['INDHPPAN']+specs['C3PAN2']+specs['C3PAN1']+specs['CH3NO3']+specs['PAN'] \
        +specs['HOCH2CO3H']+specs['C4PAN9']+specs['INANCO3H']+specs['CHOOMPAN']+specs['INB1HPPAN'] \
        +specs['MMALNBPAN']+specs['IPROPOLPAN']+specs['INB1NBCO3H']+specs['HPC52PAN']+specs['INB1NAPAN'] \
        +specs['C57NO3PAN']+specs['INB1NBPAN']+specs['C4PAN10']+specs['NO3CH2PAN']+specs['CH3OCH2NO3'] \
        +specs['HCOCOHPAN']+specs['INB1NACO3H']+specs['CHOOCH2OOH']+specs['PRNO3CO3H']+specs['PRNO3PAN'] \
        +specs['CH3O2NO2']+specs['CO2N3PAN']+specs['HCOOH']+specs['C58NO3PAN']+specs['INANCOPAN'] \
        +specs['INANCOCO3H']+specs['ETHOHNO3']+specs['INCNPAN']+specs['NO3CH2CO3H']+specs['CH3COPAN'] \
        +specs['PHAN']+specs['NO3CH2CO2H']+specs['MACRNBPAN']+specs['INANPAN']+specs['CONM2PAN'] \
        +specs['HCOCO3H']+specs['MPRBNO3PAN']+specs['CH3OOH']+specs['NO3CH2CHO']+specs['INAHPPAN'] \
        +specs['MEMOXYPAN']+specs['INAHPAN']+specs['INCNCO3H']+specs['INDHPAN']+specs['CHOOCH2NO3'] \
        +specs['MACRNPAN']

    if (new):
        specs['cc5'] += specs['NDNT124OOH']+specs['TM123OLO2']
        specs['cn5'] += specs['NDNT124OOH']
        specs['cn6'] += specs['TM123OLO2']
        specs['oc1'] += specs['newMLC1']
        specs['oc2'] += specs['newMLC2']+specs['TM123OLO2']
        specs['oc3'] += specs['newMLC3']+specs['NDNT124OOH']
        specs['oc4'] += specs['newMLC4']
    return time, xm, specs, rates

def order(val):
    """
    Function order
    ==============

    Purpose:
    Determine the order of magnitude of a given value (val).
    Return the order as number and a factor 10^(order).

    Variables:
    I/O:
    val:    input value (any number)
    ord:    order of magnitude
    (negative integers for values < 0, 0 for 0, positvie values for values > 0)
    mult:   factor 10^(order)

    Dependencies:
    uses:           numpy
    called from:    fitfcn.fitTUV, fitfcn.fitStat, pltfcn.scatdat
    """
    import numpy as np
    if (val != 0):
        ord  = np.floor(np.log10(np.abs(val)))
    else:
        ord = 0
    mult = 10**ord
    return ord, mult


### Plot function for new runs only

def plot_new(spc):

    print 'plotting',spc,'...'
    fig = plt.figure()
    fig.set_size_inches(6.,4.)
    axes = plt.gca()
    plt.rc('grid', linestyle=":", color='lightgrey')

    plt.xticks(np.arange(0,xm,12))
    plt.grid()
    plt.xlabel('model time / hours')

    ord, mult = order(max(spcM4[spc]))
    #s =pd.Series(spcM4[spc])
    #s.index=time
    #s.to_csv('test.dat',sep=' ')

    plt.ylabel('[%s] / 10$^{%i}\,$cm$^{-3}$' % (spc, ord)) #\n(F / cm$^{-3}$ s$^{-1}$)

    plt.plot(time,spcM4[spc]/mult,'b--')

    plt.legend(loc = 'upper center', prop={'size':12})
    plt.tight_layout()
    file = 'DUN15/new_'+spc+'.pdf'
    plt.savefig(file)
    plt.close(fig)


### Plot function for concentratrations in molecules/cm3

def plot_mlc(spc):

    print 'plotting',spc,'...'
    fig = plt.figure()
    fig.set_size_inches(6.,4.)
    axes = plt.gca()
    plt.rc('grid', linestyle=":", color='lightgrey')

    plt.xticks(np.arange(0,xm,12))
    plt.grid()
    plt.xlabel('model time / hours')

    ord, mult = order(max(spcM4[spc]))
    #s =pd.Series(spcM4[spc])
    #s.index=time
    #s.to_csv('test.dat',sep=' ')

    plt.ylabel('[%s] / 10$^{%i}\,$cm$^{-3}$' % (spc, ord)) #\n(F / cm$^{-3}$ s$^{-1}$)

    plt.plot(time,spcM3[spc]/mult,'g-',label=u'MCMv3.3.1')
    plt.plot(time,spcM4[spc]/mult,'b--',label=u'New Prot')

    plt.legend(loc = 'upper center', prop={'size':12})
    plt.tight_layout()
    file = 'DUN15/'+spc+'.pdf'
    plt.savefig(file)
    plt.close(fig)


### Plot function for mixing ratios

def plot_vmr(spc):

    print 'plotting',spc,'...'

    concM3 = spcM3[spc]/M
    concM4 = spcM4[spc]/M
    ord, mult = order(max(concM4))

    if (max(concM4) > 5.e-7):
        unit = 'ppm$_{\mathrm{v}}$'
        concM3 = concM3*1.e6
        concM4 = concM4*1.e6
    elif (max(concM4) > 5.e-10):
        unit = 'ppb$_{\mathrm{v}}$'
        concM3 = concM3*1.e9
        concM4 = concM4*1.e9
    else:
        unit = 'ppt$_{\mathrm{v}}$'
        concM3 = concM3*1.e12
        concM4 = concM4*1.e12

    fig = plt.figure()
    fig.set_size_inches(6.,4.)
    axes = plt.gca()
    plt.rc('grid', linestyle=":", color='lightgrey')

    plt.xticks(np.arange(0,xm,12))
    plt.grid()
    plt.xlabel('model time / hours')

    #s =pd.Series(spcM4[spc])
    #s.index=time
    #s.to_csv('test.dat',sep=' ')

    plt.ylabel('[%s] / %s' % (spc, unit)) #\n(F / cm$^{-3}$ s$^{-1}$)

    plt.plot(time,concM3,'g-',label=u'MCMv3.3.1')
    plt.plot(time,concM4,'b--',label=u'New Prot')

    # plt.legend(loc = 'upper center', prop={'size':12})
    plt.tight_layout()
    file = 'DUN15/'+spc+'.pdf'
    plt.savefig(file)
    plt.close(fig)


###############################################################################

import pandas as pd
import numpy as np
import netCDF4
from netCDF4 import Dataset
import glob,sys,os
import matplotlib.pyplot as plt

global spcM3, spcM4, rM3, rM4, xm, M
time, xm, spcM3, rM3 = load('../save/DUN15mcm3.nc', 'DUN15', False)
time, xm, spcM4, rM4 = load('../save/DUN15mcm4.nc', 'DUN15', True)
M = spcM4['M'].mean()
spcM3['NOx'] = spcM3['NO']+spcM3['NO2']
spcM4['NOx'] = spcM4['NO']+spcM4['NO2']

### plot for species in moelcules/cm3
spec = ['OH','HO2'] #,'newMLC1','newMLC2','newMLC3','newMLC4'] #,['OH','HO2']
for spc in spec:
    plot_mlc(spc)

### plot for species in mixing ratios
spec = ['O3','NO','NO2','NO3','NOx','HONO','HNO3','H2O2', \
    'cc11','cc12','cc13','cc21','cc22','cc23','cc25', \
    'cc31','cc33','cc4','cc5','cc0'] #, \
#    'newMLC1','newMLC2','newMLC3','newMLC4']
for spc in spec:
    plot_vmr(spc)

# spec = ['newMLC1','newMLC2','newMLC3','newMLC4']
# for spc in spec:
#     plot_new(spc)
# ### OH:HO2 ratio ###

ratM3 = spcM3['OH']/spcM3['HO2']
ratM4 = spcM4['OH']/spcM4['HO2']

fig = plt.figure()
fig.set_size_inches(6.,4.)
axes = plt.gca()
plt.rc('grid', linestyle=":", color='lightgrey')

plt.xticks(np.arange(0,xm,12))
plt.grid()
plt.xlabel('model time / hours')

plt.ylabel('[OH] / [HO$_2$]') #\n(F / cm$^{-3}$ s$^{-1}$)

plt.plot(time,ratM3,'g-',label=u'MCMv3.3.1')
plt.plot(time,ratM4,'b--',label=u'New Prot')

plt.legend(loc = 'upper center', prop={'size':12})
plt.tight_layout()
plt.savefig('DUN15/rat.pdf')
plt.close(fig)


# ### Mass by O:C ratio ###

# fig = plt.figure()
# fig.set_size_inches(6.,4.)
# axes = plt.gca()
# plt.rc('grid', linestyle=":", color='lightgrey')

# plt.xticks(np.arange(0,xm,12))
# plt.grid()
# plt.xlabel('model time / hours')
# ocM4 = spcM4['oc1']+spcM4['oc2']+spcM4['oc3']+spcM4['oc4']
# ord, mult = order(max(ocM4))
# plt.ylabel('[NMVOC] / 10$^{%i}\,$cm$^{-3}$' % ord) #\n(F / cm$^{-3}$ s$^{-1}$)

# plt.plot(time,spcM3['oc4']/mult,'g-',label=u'O:C ≥ 2 (MCMv3.3.1)')
# plt.plot(time,spcM4['oc4']/mult,'b--',label=u'O:C ≥ 2 (New Prot)')
# plt.plot(time,(spcM3['oc3']+spcM3['oc4'])/mult,'y-',label=u'1 ≤ O:C < 2 (MCMv3.3.1)')
# plt.plot(time,(spcM4['oc3']+spcM4['oc4'])/mult,'c--',label=u'1 ≤ O:C < 2 (New Prot)')
# plt.plot(time,(spcM3['oc2']+spcM3['oc3']+spcM3['oc4'])/mult,'r-',label=u'0.5 ≤ O:C < 1 (MCMv3.3.1)')
# plt.plot(time,(spcM4['oc2']+spcM4['oc3']+spcM4['oc4'])/mult,'k--',label=u'0.5 ≤ O:C < 1 (New Prot)')
# plt.plot(time,(spcM3['oc1']+spcM3['oc2']+spcM3['oc3']+spcM3['oc4'])/mult,'m-',label=u'O:C < 0.5 (MCMv3.3.1)')
# plt.plot(time,(spcM4['oc1']+spcM4['oc2']+spcM4['oc3']+spcM4['oc4'])/mult,color='skyblue',ls='--',label=u'O:C < 0.5 (New Prot)')

# plt.legend(loc = 'upper center', prop={'size':12})
# plt.tight_layout()
# plt.savefig('DUN15/oc.pdf')
# plt.close(fig)


# ### Mass by  O:C ratio as stacked area plot ###

# fig = plt.figure()
# fig.set_size_inches(6.,4.)
# plt.rc('grid', linestyle=":", color='lightgrey')
# axes = plt.gca()

# plt.xticks(np.arange(0,xm,12))
# plt.grid()
# plt.xlabel('model time / hours')
# plt.ylabel('c / cm$^{-3}$') #\n(F / cm$^{-3}$ s$^{-1}$)

# #plt.stackplot(time,spcM4['oc4'],spcM4['oc3'],spcM4['oc2'],spcM4['oc1'],colors=['b','c','k','skyblue'], \
# #    labels=[u'O:C ≥ 2 (New Prot)',u'1 ≤ O:C < 2 (New Prot)',u'0.5 ≤ O:C < 1 (New Prot)',u'O:C < 0.5 (New Prot)'])
# #plt.stackplot(time,spcM4['oc3'],label=u'1 ≤ O:C < 2 (New Prot)')
# #plt.stackplot(time,spcM4['oc2'],label=u'0.5 ≤ O:C < 1 (New Prot)')
# #plt.stackplot(time,spcM4['oc1'],label=u'O:C < 0.5 (New Prot)')

# plt.legend(loc = 'upper center', prop={'size':12})
# plt.tight_layout()
# plt.savefig('DUN15/oc_stack.pdf')
# plt.close(fig)


# ### Mass by chain length ###

# fig = plt.figure()
# fig.set_size_inches(6.,4.)
# axes = plt.gca()
# plt.rc('grid', linestyle=":", color='lightgrey')

# plt.xticks(np.arange(0,xm,12))
# plt.grid()
# plt.xlabel('model time / hours')
# cnM4 = spcM4['cn1']+spcM4['cn2']+spcM4['cn3']+spcM4['cn4']+spcM4['cn5'] \
#     +spcM4['cn6']+spcM4['cn7']+spcM4['cn8']+spcM4['cn9']+spcM4['cn0']
# ord, mult = order(max(cnM4))
# plt.ylabel('[NMVOC] / 10$^{%i}\,$cm$^{-3}$' % ord) #\n(F / cm$^{-3}$ s$^{-1}$)

# plt.plot(time,spcM3['cn0']/mult,'g-',label=u'CN ≥ 10')
# plt.plot(time,spcM4['cn0']/mult,'b--',label=u'CN ≥ 10')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9'])/mult,'y-',label=u'CN = 9')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9'])/mult,'c--',label=u'CN = 9')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8'])/mult,'r-',label=u'CN = 8')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8'])/mult,'k--',label=u'CN = 8')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7'])\
#     /mult,'m-',label=u'CN = 7')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7'])\
#     /mult,color='skyblue',ls='--',label=u'CN = 7')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7']\
#     +spcM3['cn6'])/mult,color='darkgreen',ls='-',label=u'CN = 6')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7']\
#     +spcM4['cn6'])/mult,color='orange',ls='--',label=u'CN = 6')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7']\
#     +spcM3['cn6']+spcM3['cn5'])/mult,color='blueviolet',ls='-',label=u'CN = 5')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7']\
#     +spcM4['cn6']+spcM4['cn5'])/mult,color='sandybrown',ls='--',label=u'CN = 5')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7']\
#     +spcM3['cn6']+spcM3['cn5']+spcM3['cn4'])/mult,color='olive',ls='-',label=u'CN = 4')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7']\
#     +spcM4['cn6']+spcM4['cn5']+spcM4['cn4'])/mult,color='m',ls='--',label=u'CN = 4')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7']\
#     +spcM3['cn6']+spcM3['cn5']+spcM3['cn4']+spcM3['cn3'])/mult,\
#     color='lightsteelblue',ls='-',label=u'CN = 3')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7']\
#     +spcM4['cn6']+spcM4['cn5']+spcM4['cn4']+spcM4['cn3'])/mult,\
#     color='indigo',ls='--',label=u'CN = 3')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7']\
#     +spcM3['cn6']+spcM3['cn5']+spcM3['cn4']+spcM3['cn3']+spcM3['cn2'])\
#     /mult,color='darkkhaki',ls='-',label=u'CN = 2')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7']\
#     +spcM4['cn6']+spcM4['cn5']+spcM4['cn4']+spcM4['cn3']+spcM4['cn2'])\
#     /mult,color='gold',ls='--',label=u'CN = 2')
# plt.plot(time,(spcM3['cn0']+spcM3['cn9']+spcM3['cn8']+spcM3['cn7']\
#     +spcM3['cn6']+spcM3['cn5']+spcM3['cn4']+spcM3['cn3']+spcM3['cn2']\
#     +spcM3['cn1'])/mult,color='palevioletred',ls='-',label=u'CN = 1')
# plt.plot(time,(spcM4['cn0']+spcM4['cn9']+spcM4['cn8']+spcM4['cn7']\
#     +spcM4['cn6']+spcM4['cn5']+spcM4['cn4']+spcM4['cn3']+spcM4['cn2']\
#     +spcM4['cn1'])/mult,color='wheat',ls='--',label=u'CN = 1')

# plt.legend(loc = 'upper center', prop={'size':12})
# plt.tight_layout()
# plt.savefig('DUN15/cn.pdf')
# plt.close(fig)


### new species

fig = plt.figure()
fig.set_size_inches(6.,4.)

df = spcM4[['newMLC1','newMLC2','newMLC3','newMLC4']]/M*1.0e12
df.index = time
df.plot(grid=True)

plt.savefig('DUN15/newMLC.pdf')
plt.close(fig)


### Mass by chain length (area plot) ###

fig = plt.figure(1)
fig.set_size_inches(6.,4.)

df = spcM3[['cn0','cn9','cn8','cn7','cn6','cn5','cn4','cn3','cn2','cn1']]/M*1.0e9
df.index = time
df.plot.area(color=['g','mediumseagreen','mediumturquoise','lawngreen','yellowgreen','olive','goldenrod','gold','palegoldenrod','peru'], \
    label=[u'CN ≥ 10 (MCMv3.3.1)',u'CN = 9 (MCMv3.3.1)',u'CN = 8 (MCMv3.3.1)',u'CN = 7 (MCMv3.3.1)',u'CN = 6 (MCMv3.3.1)', \
    u'CN = 5 (MCMv3.3.1)',u'CN = 4 (MCMv3.3.1)',u'CN = 3 (MCMv3.3.1)',u'CN = 2 (MCMv3.3.1)',u'CN = 1 (MCMv3.3.1)'],alpha=0.3, grid = True)


plt.savefig('DUN15/cnM3_stack.pdf')
plt.close(fig)


fig = plt.figure(2)
fig.set_size_inches(6.,4.)

df = spcM4[['cn0','cn9','cn8','cn7','cn6','cn5','cn4','cn3','cn2','cn1']]/M*1.0e9
df.index = time
df.plot.area(color=['blue','slateblue','darkviolet','m','fuchsia','violet','deeppink','red','orange','y'], \
    label=[u'CN ≥ 10 (New Prot)',u'CN = 9 (New Prot)',u'CN = 8 (New Prot)',u'CN = 7 (New Prot)',u'CN = 6 (New Prot)', \
    u'CN = 5 (New Prot)',u'CN = 4 (New Prot)',u'CN = 3 (New Prot)',u'CN = 2 (New Prot)',u'CN = 1 (New Prot)'], grid=True, alpha=0.3)

plt.savefig('DUN15/cnM4_stack.pdf')
plt.close(fig)


### Mass by O:C ratio (area plot) ###

fig = plt.figure(3)
fig.set_size_inches(6.,4.)

df = spcM3[['oc1','oc2','oc3','oc4']]/M*1.0e9
df.index = time
df.plot.area(color=['g','mediumseagreen','mediumturquoise','lawngreen'], \
    grid=True, alpha=0.3)

plt.savefig('DUN15/ocM3_stack.pdf')
plt.close(fig)


fig = plt.figure(4)
fig.set_size_inches(6.,4.)

df = spcM4[['oc1','oc2','oc3','oc4']]/M*1.0e9
df.index = time
df.plot.area(color=['blue','slateblue','darkviolet','m'], \
    alpha=0.3)

plt.savefig('DUN15/ocM4_stack.pdf')
plt.close(fig)

print 'Done.'
