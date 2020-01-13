import pandas as pd 
import re
import numpy as np
df = pd.read_csv(str(__file__).replace('parsekpp/gen_class.py','datatables/smiles_mined.csv'))

df = df.set_index('name')

sm = pd.DataFrame( df.smiles.astype(str) )

ro2 = re.findall(r'ind_([\d\w]+)','''RO2 = & 
C(ind_CH3O2) + C(ind_C2H5O2) + C(ind_IC3H7O2) + C(ind_NC3H7O2) + & 
  C(ind_HOCH2CH2O2) + C(ind_HO1C3O2) + C(ind_HYPROPO2) + &  
  C(ind_IPROPOLO2) + C(ind_NBUTOLAO2) + C(ind_NBUTOLBO2) + &  
  C(ind_BUT2OLO2) + C(ind_IBUTOLBO2) + C(ind_IBUTOLCO2) + &  
  C(ind_TBUTOLO2) + C(ind_HO3C5O2) + C(ind_PE2ENEBO2) + C(ind_HM2C43O2) 
&  
  + C(ind_M2BUOL2O2) + C(ind_HM33C3O2) + C(ind_ME3BUOLO2) + &  
  C(ind_HO2M2C4O2) + C(ind_ME2BU2OLO2) + C(ind_PROL11MO2) + &  
  C(ind_H2M3C4O2) + C(ind_ME2BUOLO2) + C(ind_CYHEXOLAO2) + &  
  C(ind_MIBKAOHAO2) + C(ind_MIBKAOHBO2) + C(ind_MIBKHO4O2) + &  
  C(ind_CH3CO3) + C(ind_NMBOAO2) + C(ind_NMBOBO2) + C(ind_MBOAO2) + &  
  C(ind_MBOBO2) + C(ind_HCOCH2O2) + C(ind_C2H5CO3) + C(ind_C3H7CO3) + &  
  C(ind_BUTALO2) + C(ind_IPRCO3) + C(ind_IBUTALBO2) + C(ind_IBUTALCO2) 
+ &  
  C(ind_C4H9CO3) + C(ind_C4CHOBO2) + C(ind_NC4H9O2) + C(ind_ACO3) + &  
  C(ind_ACRO2) + C(ind_OCCOHCO2) + C(ind_CH3C2H2O2) + C(ind_MACO3) + &  
  C(ind_MACRO2) + C(ind_MACROHO2) + C(ind_C3DBCO3) + C(ind_C4CONO3O2) + 
&  
  C(ind_C4NO3COO2) + C(ind_C4OCCOHCO2) + C(ind_COCCOH2CO2) + &  
  C(ind_SC4H9O2) + C(ind_IC4H9O2) + C(ind_TC4H9O2) + C(ind_PEAO2) + &  
  C(ind_PEBO2) + C(ind_PECO2) + C(ind_IPEAO2) + C(ind_IPEBO2) + &  
  C(ind_IPECO2) + C(ind_NEOPO2) + C(ind_HEXAO2) + C(ind_HEXBO2) + &  
  C(ind_HEXCO2) + C(ind_M2PEAO2) + C(ind_M2PEBO2) + C(ind_M2PECO2) + &  
  C(ind_M2PEDO2) + C(ind_M3PEAO2) + C(ind_M3PEBO2) + C(ind_M3PECO2) + &  
  C(ind_M22C43O2) + C(ind_M22C4O2) + C(ind_M33C4O2) + C(ind_M23C43O2) + 
&  
  C(ind_M23C4O2) + C(ind_HEPTO2) + C(ind_M2HEXAO2) + C(ind_M2HEXBO2) + 
&  
  C(ind_M3HEXAO2) + C(ind_M3HEXBO2) + C(ind_OCTO2) + C(ind_NONO2) + &  
  C(ind_DECO2) + C(ind_UDECO2) + C(ind_DDECO2) + C(ind_CHEXO2) + &  
  C(ind_ETHENO3O2) + C(ind_PRONO3AO2) + C(ind_PRONO3BO2) + &  
  C(ind_BU1ENO3O2) + C(ind_C43NO34O2) + C(ind_HO3C4O2) + &  
  C(ind_C42NO33O2) + C(ind_MPRANO3O2) + C(ind_MPRBNO3O2) + &  
  C(ind_C51NO32O2) + C(ind_C52NO31O2) + C(ind_PE1ENEAO2) + &  
  C(ind_PE1ENEBO2) + C(ind_C52NO33O2) + C(ind_C53NO32O2) + &  
  C(ind_PE2ENEAO2) + C(ind_C4NO32M1O2) + C(ind_C4NO32M2O2) + &  
  C(ind_C4M3NO31O2) + C(ind_C4M3NO32O2) + C(ind_IPRCHOOA) + &  
  C(ind_ME3BU2OLO2) + C(ind_C4M2NO32O2) + C(ind_C4M2NO33O2) + &  
  C(ind_C65NO36O2) + C(ind_C66NO35O2) + C(ind_C6OH5O2) + C(ind_HO5C6O2) 
&  
  + C(ind_C62NO33O2) + C(ind_C63NO32O2) + C(ind_C64OH5O2) + &  
  C(ind_C65OH4O2) + C(ind_C4ME2NO3O2) + C(ind_C4ME2OHO2) + &  
  C(ind_BZBIPERO2) + C(ind_C6H5CH2O2) + C(ind_TLBIPERO2) + 
C(ind_OXYLO2) &  
  + C(ind_OXYBIPERO2) + C(ind_MXYLO2) + C(ind_MXYBIPERO2) + &  
  C(ind_PXYLO2) + C(ind_PXYBIPERO2) + C(ind_C6H5C2H4O2) + &  
  C(ind_EBZBIPERO2) + C(ind_PHC3O2) + C(ind_PBZBIPERO2) + 
C(ind_PHIC3O2) &  
  + C(ind_IPBZBIPRO2) + C(ind_TM123BO2) + C(ind_TM123BPRO2) + &  
  C(ind_TM124BO2) + C(ind_TM124BPRO2) + C(ind_TMBO2) + 
C(ind_TM135BPRO2) &  
  + C(ind_ETOLO2) + C(ind_OETLBIPRO2) + C(ind_METLBIPRO2) + &  
  C(ind_PETLBIPRO2) + C(ind_DM35EBO2) + C(ind_DMEBIPRO2) + &  
  C(ind_DE35TO2) + C(ind_DETLBIPRO2) + C(ind_NSTYRENO2) + &  
  C(ind_STYRENO2) + C(ind_C6H5CO3) + C(ind_C6H5O2) + C(ind_CH2CLO2) + &  
  C(ind_CHCL2O2) + C(ind_CCL3O2) + C(ind_CCL3CH2O2) + C(ind_TCEOHO2) + 
&  
  C(ind_C2CL3OHAO2) + C(ind_C2CL3OHBO2) + C(ind_C2CL2OHO2) + &  
  C(ind_DICLETO2) + C(ind_CH2OHCL2O2) + C(ind_CL2OHCH2O2) + &  
  C(ind_CL12PRAO2) + C(ind_CL12PRBO2) + C(ind_CL12PRCO2) + &  
  C(ind_CH3CCL2O2) + C(ind_CHCL2CH2O2) + C(ind_CH2CLCH2O2) + &  
  C(ind_CH3CHCLO2) + C(ind_CHCL2CL2O2) + C(ind_CH2CL3O2) + &  
  C(ind_CHCL3O2) + C(ind_CCLNO3O2) + C(ind_CNO3CLO2) + 
C(ind_CCLOHCH2O2) &  
  + C(ind_CH2OHCCLO2) + C(ind_NBUTDAO2) + C(ind_NBUTDBO2) + &  
  C(ind_BUTDAO2) + C(ind_BUTDBO2) + C(ind_BUTDCO2) + C(ind_NISOPO2) + &  
  C(ind_ISOP34O2) + C(ind_CHOOCH2O2) + C(ind_METHACETO2) + &  
  C(ind_MOCOCH2O2) + C(ind_ACETC2H4O2) + C(ind_EOCOCH2O2) + &  
  C(ind_ETHACETO2) + C(ind_NPROACEAO2) + C(ind_NPROACEBO2) + &  
  C(ind_NPROACECO2) + C(ind_IPRACBO2) + C(ind_IPROACETO2) + &  
  C(ind_NBUACETAO2) + C(ind_NBUACETBO2) + C(ind_NBUACETCO2) + &  
  C(ind_SBUACETAO2) + C(ind_SBUACETBO2) + C(ind_MCOOTBO2) + &  
  C(ind_TBOCOCH2O2) + C(ind_CH3OCH2O2) + C(ind_DIETETO2) + &  
  C(ind_ETOC2O2) + C(ind_MTBEAO2) + C(ind_MTBEBO2) + C(ind_DIIPRETO2) + 
&  
  C(ind_IPROMC2O2) + C(ind_ETBEAO2) + C(ind_ETBEBO2) + C(ind_ETBECO2) + 
&  
  C(ind_MO2EOLAO2) + C(ind_MO2EOLBO2) + C(ind_EOX2EOLAO2) + &  
  C(ind_EOX2EOLBO2) + C(ind_PR2OHMOXO2) + C(ind_H2C3OCO2) + &  
  C(ind_BOX2EOHAO2) + C(ind_BOX2EOHBO2) + C(ind_BOXPROLAO2) + &  
  C(ind_BOXPROLBO2) + C(ind_CH2BRO2) + C(ind_DIBRETO2) + &  
  C(ind_CH3COCH2O2) + C(ind_MEKAO2) + C(ind_MEKBO2) + C(ind_MEKCO2) + &  
  C(ind_CO2C54O2) + C(ind_MPRKAO2) + C(ind_DIEKAO2) + C(ind_DIEKBO2) + 
&  
  C(ind_MIPKAO2) + C(ind_MIPKBO2) + C(ind_HEX2ONAO2) + C(ind_HEX2ONBO2) 
&  
  + C(ind_HEX2ONCO2) + C(ind_HEX3ONAO2) + C(ind_HEX3ONBO2) + &  
  C(ind_HEX3ONCO2) + C(ind_HEX3ONDO2) + C(ind_MIBKAO2) + C(ind_MIBKBO2) 
&  
  + C(ind_MTBKO2) + C(ind_CYHXONAO2) + C(ind_NAPINAO2) + 
C(ind_NAPINBO2) &  
  + C(ind_APINAO2) + C(ind_APINBO2) + C(ind_APINCO2) + C(ind_NBPINAO2) 
+ &  
  C(ind_NBPINBO2) + C(ind_BPINAO2) + C(ind_BPINBO2) + C(ind_BPINCO2) + 
&  
  C(ind_NLIMO2) + C(ind_LIMAO2) + C(ind_LIMBO2) + C(ind_LIMCO2) + &  
  C(ind_NBCO2) + C(ind_BCAO2) + C(ind_BCBO2) + C(ind_BCCO2) + &  
  C(ind_DMMAO2) + C(ind_DMMBO2) + C(ind_DMCO2) + C(ind_CH3SCH2O2) + &  
  C(ind_HODMSO2) + C(ind_ETHOXO2) + C(ind_BUT2CO3) + C(ind_C3ME3CO3) + 
&  
  C(ind_C3ME3CHOO2) + C(ind_HOCH2CO3) + C(ind_CH3CHOHCO3) + &  
  C(ind_IPRHOCO3) + C(ind_IPRCHOO) + C(ind_BZEMUCCO3) + C(ind_BZEMUCO2) 
&  
  + C(ind_C5DIALO2) + C(ind_NPHENO2) + C(ind_PHENO2) + C(ind_CRESO2) + 
&  
  C(ind_NCRESO2) + C(ind_TLEMUCCO3) + C(ind_TLEMUCO2) + 
C(ind_C615CO2O2) &  
  + C(ind_OXYMUCCO3) + C(ind_OXYMUCO2) + C(ind_MC6CO2O2) + &  
  C(ind_NOXYOLO2) + C(ind_OXYOLO2) + C(ind_MXYMUCCO3) + C(ind_MXYMUCO2) 
&  
  + C(ind_C726CO5O2) + C(ind_MXYOLO2) + C(ind_NMXYOLO2) + &  
  C(ind_PXYMUCCO3) + C(ind_PXYMUCO2) + C(ind_C6M5CO2O2) + &  
  C(ind_NPXYOLO2) + C(ind_PXYOLO2) + C(ind_EBENZOLO2) + 
C(ind_NEBNZOLO2) &  
  + C(ind_EBZMUCCO3) + C(ind_EBZMUCO2) + C(ind_C715CO2O2) + &  
  C(ind_NPBNZOLO2) + C(ind_PBENZOLO2) + C(ind_PBZMUCCO3) + &  
  C(ind_PBZMUCO2) + C(ind_C815CO2O2) + C(ind_IPBENZOLO2) + &  
  C(ind_NIPBNZOLO2) + C(ind_IPBZMUCCO3) + C(ind_IPGLOOB) + &  
  C(ind_IPBZMUCO2) + C(ind_C7M15CO2O2) + C(ind_NTM123OLO2) + &  
  C(ind_TM123OLO2) + C(ind_TM123MUCO2) + C(ind_NTM124OLO2) + &  
  C(ind_TM124OLO2) + C(ind_TM124MUCO3) + C(ind_TM124MUCO2) + &  
  C(ind_C7CO2M5O2) + C(ind_NTM135OLO2) + C(ind_TM135OLO2) + &  
  C(ind_TM135MUCO3) + C(ind_TM135MUCO2) + C(ind_C7M2CO5O2) + &  
  C(ind_OETLMUCCO3) + C(ind_OETLMUCO2) + C(ind_MC7CO2O2) + &  
  C(ind_NOETOLO2) + C(ind_OETOLO2) + C(ind_METLMUCCO3) + &  
  C(ind_METLMUCO2) + C(ind_C826CO3O2) + C(ind_METOLO2) + 
C(ind_NMETOLO2) &  
  + C(ind_PETLMUCCO3) + C(ind_PETLMUCO2) + C(ind_C7M6CO2O2) + &  
  C(ind_NPETOLO2) + C(ind_PETOLO2) + C(ind_DMEBMUCO3) + 
C(ind_DMEBMUCO2) &  
  + C(ind_C8M2CO6O2) + C(ind_NDMEPHOLO2) + C(ind_DMEPHOLO2) + &  
  C(ind_NDEMPHOLO2) + C(ind_DEMPHOLO2) + C(ind_DETLMUCO3) + &  
  C(ind_DETLMUCO2) + C(ind_C9M2CO6O2) + C(ind_HMVKAO2) + C(ind_HMVKBO2) 
&  
  + C(ind_MVKO2) + C(ind_CISOPAO2) + C(ind_ISOPBO2) + C(ind_CISOPCO2) + 
&  
  C(ind_ISOPDO2) + C(ind_NC526O2) + C(ind_C530O2) + C(ind_M3BU3ECO3) + 
&  
  C(ind_C45O2) + C(ind_NC51O2) + C(ind_C51O2) + C(ind_CH2CHCH2O2) + &  
  C(ind_ISOPAO2) + C(ind_ISOPCO2) + C(ind_MEMOXYCO3) + C(ind_EOX2MECO3) 
&  
  + C(ind_ETOMEO2) + C(ind_PRONEMOXO2) + C(ind_BOXMCO3) + 
C(ind_BOX2MO2) &  
  + C(ind_BOXPRONAO2) + C(ind_BOXPRONBO2) + C(ind_C107O2) + &  
  C(ind_C109O2) + C(ind_C96O2) + C(ind_NOPINAO2) + C(ind_NOPINBO2) + &  
  C(ind_NOPINCO2) + C(ind_NOPINDO2) + C(ind_LIMALAO2) + C(ind_LIMALBO2) 
&  
  + C(ind_C923O2) + C(ind_BCALAO2) + C(ind_BCALBO2) + C(ind_C136O2) + &  
  C(ind_BCALCO2) + C(ind_C141O2) + C(ind_HOC2H4CO3) + C(ind_HOIPRCO3) + 
&  
  C(ind_HO13C5O2) + C(ind_HO3C4CO3) + C(ind_C54O2) + C(ind_H2M2C3CO3) + 
&  
  C(ind_PROL1MCO3) + C(ind_C56O2) + C(ind_HO2C43CO3) + 
C(ind_MIBKCOOHO2) &  
  + C(ind_NC4OHCO3) + C(ind_C4OH2CO3) + C(ind_CO2C3CO3) + &  
  C(ind_HO2C3CO3) + C(ind_IBUDIALCO3) + C(ind_PROPALO2) + &  
  C(ind_CO3C4CO3) + C(ind_HO1C4O2) + C(ind_A2PANOO) + C(ind_HCOCOHCO3) 
+ &  
  C(ind_HCOCO3) + C(ind_MACRNCO3) + C(ind_MACRNBCO3) + C(ind_CHOMOHCO3) 
&  
  + C(ind_CO2H3CO3) + C(ind_HO1C5O2) + C(ind_HO2C5O2) + C(ind_C52O2) + 
&  
  C(ind_TBUTCO3) + C(ind_HO1C6O2) + C(ind_C5H11CO3) + C(ind_HO2C6O2) + 
&  
  C(ind_HO3C6O2) + C(ind_HO1MC5O2) + C(ind_C54CO3) + C(ind_HO2MC5O2) + 
&  
  C(ind_EIPKAO2) + C(ind_EIPKBO2) + C(ind_HO2M2C5O2) + C(ind_H1MC5O2) + 
&  
  C(ind_M3C4CO3) + C(ind_H2MC5O2) + C(ind_M2BKAO2) + C(ind_M2BKBO2) + &  
  C(ind_HM33C4O2) + C(ind_M22C3CO3) + C(ind_HM22C4O2) + C(ind_M33C3CO3) 
&  
  + C(ind_HM23C4O2) + C(ind_M2C43CO3) + C(ind_HO3C76O2) + &  
  C(ind_CO3C75O2) + C(ind_H2M5C65O2) + C(ind_C75O2) + C(ind_H2M2C65O2) 
+ &  
  C(ind_H2M4C65O2) + C(ind_C710O2) + C(ind_H3M3C6O2) + C(ind_HO3C86O2) 
+ &  
  C(ind_CO3C85O2) + C(ind_HO3C96O2) + C(ind_C91O2) + C(ind_HO3C106O2) + 
&  
  C(ind_C101O2) + C(ind_HO3C116O2) + C(ind_C111O2) + C(ind_HO3C126O2) + 
&  
  C(ind_C121O2) + C(ind_CO1C6O2) + C(ind_NO3CH2CO3) + C(ind_PRNO3CO3) + 
&  
  C(ind_CO3C4NO3O2) + C(ind_HO3C3CO3) + C(ind_MPRBNO3CO3) + &  
  C(ind_C5NO3COAO2) + C(ind_C4NO3CO3) + C(ind_C5OH2CO4O2) + &  
  C(ind_C4OHCO3) + C(ind_C5NO3CO4O2) + C(ind_C5CONO34O2) + &  
  C(ind_C43NO3CO3) + C(ind_C4MCONO3O2) + C(ind_C3MNO3CO3) + &  
  C(ind_C3M3OH2CO3) + C(ind_MC4CONO3O2) + C(ind_C65NO36CO3) + &  
  C(ind_MNO3COC4O2) + C(ind_C4COMOH3O2) + C(ind_HO5C5CO3) + &  
  C(ind_C6NO3CO5O2) + C(ind_C6CONO34O2) + C(ind_MALDIALCO3) + &  
  C(ind_EPXDLCO3) + C(ind_C3DIALO2) + C(ind_MALDIALO2) + C(ind_OXYL1O2) 
&  
  + C(ind_C5CO14O2) + C(ind_OXYLCO3) + C(ind_EPXM2DLCO3) + &  
  C(ind_C4MCO2O2) + C(ind_DM123O2) + C(ind_MXYLCO3) + C(ind_MXYL1O2) + 
&  
  C(ind_C3MCODBCO3) + C(ind_EPXMDLCO3) + C(ind_C3MDIALO2) + &  
  C(ind_MXY1O2) + C(ind_PXYLCO3) + C(ind_PXYL1O2) + C(ind_PXY1O2) + &  
  C(ind_C6H5CH2CO3) + C(ind_EBENZO2) + C(ind_C6DCARBBO2) + &  
  C(ind_PHCOETO2) + C(ind_PBENZO2) + C(ind_C7DCCO3) + C(ind_IPBENZO2) + 
&  
  C(ind_IC7DCCO3) + C(ind_IPGLOO) + C(ind_TM123BCO3) + C(ind_TM123O2) + 
&  
  C(ind_EPXKTMCO3) + C(ind_C4CO2O2) + C(ind_TM124BCO3) + C(ind_DM124O2) 
&  
  + C(ind_TM124O2) + C(ind_TMBCO3) + C(ind_DMPHO2) + C(ind_C4MCODBCO3) 
+ &  
  C(ind_EPXMKTCO3) + C(ind_CO24C53O2) + C(ind_MPHCOMEO2) + &  
  C(ind_EPXMEDLCO3) + C(ind_C4ECO2O2) + C(ind_OET1O2) + C(ind_MET1O2) + 
&  
  C(ind_PET1O2) + C(ind_DMPHCOMO2) + C(ind_EMPHCOMO2) + C(ind_EMPHCO3) 
+ &  
  C(ind_C7CODBCO3) + C(ind_EPXEKTCO3) + C(ind_C3EDIALO2) + &  
  C(ind_CO24C63O2) + C(ind_CCL3CO3) + C(ind_CLETO3) + C(ind_CL2OHCO3) + 
&  
  C(ind_CL12CO3) + C(ind_CLCOCLMEO2) + C(ind_CHCL2CO3) + &  
  C(ind_CLCOCH2O2) + C(ind_CLCOCLO2) + C(ind_CCLOHCO3) + C(ind_HNMVKO2) 
&  
  + C(ind_NC3CO3) + C(ind_C42O2) + C(ind_HC3CO3) + C(ind_C41O2) + &  
  C(ind_MVKOHAO2) + C(ind_MVKOHBO2) + C(ind_HC3CCO3) + C(ind_INCO2) + &  
  C(ind_NC4CO3) + C(ind_C510O2) + C(ind_C536O2) + C(ind_C537O2) + &  
  C(ind_INAO2) + C(ind_C58O2) + C(ind_HC4CO3) + C(ind_CHOCOMOXO2) + &  
  C(ind_ACETMECO3) + C(ind_HOACETETO2) + C(ind_MECOACETO2) + &  
  C(ind_ACPRONEO2) + C(ind_ACCOETO2) + C(ind_ACETC2CO3) + &  
  C(ind_IPRACBCO3) + C(ind_ACBUONEAO2) + C(ind_ACBUONEBO2) + &  
  C(ind_ACCOC3H6O2) + C(ind_SBUACONEO2) + C(ind_TBUACCO3) + &  
  C(ind_MTBEACHOO2) + C(ind_MTBEBCO3) + C(ind_IPROC21O2) + &  
  C(ind_IPROMCCO3) + C(ind_EIPEO2) + C(ind_ETBEACO3) + C(ind_ETBECCO3) 
+ &  
  C(ind_BOXCOEOLO2) + C(ind_BRETO3) + C(ind_HO1CO3C4O2) + &  
  C(ind_BIACETO2) + C(ind_HO2CO4C5O2) + C(ind_CO23C54O2) + &  
  C(ind_HOCO3C54O2) + C(ind_C53O2) + C(ind_C41CO3) + C(ind_CO2HOC61O2) 
+ &  
  C(ind_CO24C6O2) + C(ind_CO25C6O2) + C(ind_HO2C4O2) + C(ind_C61O2) + &  
  C(ind_CO23C65O2) + C(ind_C6CO3OH5O2) + C(ind_C6CO34O2) + &  
  C(ind_C6HO1CO3O2) + C(ind_C3COCCO3) + C(ind_PEN2ONE1O2) + &  
  C(ind_MIBK3COO2) + C(ind_C612O2) + C(ind_CO2M33CO3) + 
C(ind_C6COCHOO2) &  
  + C(ind_CY6DIONO2) + C(ind_NC101O2) + C(ind_C96CO3) + C(ind_C720O2) + 
&  
  C(ind_NC91CO3) + C(ind_C8BCO2) + C(ind_C918CO3) + C(ind_C923CO3) + &  
  C(ind_C141CO3) + C(ind_NBCALO2) + C(ind_BCALO2) + C(ind_BCSOZO2) + &  
  C(ind_C151O2) + C(ind_C152O2) + C(ind_MMFO2) + C(ind_MMCFO2) + &  
  C(ind_DMSO2O2) + C(ind_CHOC4CO3) + C(ind_C6DIALO2) + C(ind_CHOC4O2) + 
&  
  C(ind_CYC6DIONO2) + C(ind_CONM2CO3) + C(ind_NBZFUO2) + C(ind_BZFUO2) 
+ &  
  C(ind_CATEC1O2) + C(ind_MCATEC1O2) + C(ind_MC3CODBCO3) + &  
  C(ind_C4M2ALOHO2) + C(ind_C5DICARBO2) + C(ind_NTLFUO2) + 
C(ind_TLFUO2) &  
  + C(ind_MC4CODBCO3) + C(ind_MC5CO2OHO2) + C(ind_NOXYFUO2) + &  
  C(ind_C6OTKETO2) + C(ind_OXYFUO2) + C(ind_OXCATEC1O2) + &  
  C(ind_C5MCO2OHO2) + C(ind_NMXYFUO2) + C(ind_C23O3MO2) + 
C(ind_MXYFUO2) &  
  + C(ind_NPXYFUO2) + C(ind_MCOCOMOXO2) + C(ind_PXYFUO2) + &  
  C(ind_MXCATEC1O2) + C(ind_DMKOHO2) + C(ind_PXCATEC1O2) + &  
  C(ind_ECATEC1O2) + C(ind_C6DICARBO2) + C(ind_NEBFUO2) + &  
  C(ind_BUTALAO2) + C(ind_EBFUO2) + C(ind_C7CO3OHO2) + C(ind_PCATEC1O2) 
&  
  + C(ind_C7DCO2) + C(ind_NPBFUO2) + C(ind_C4CHOAO2) + C(ind_PBFUO2) + 
&  
  C(ind_C8CO3OHO2) + C(ind_PHCOMEO2) + C(ind_IPCATEC1O2) + &  
  C(ind_IC7DCO2) + C(ind_NIPBFUO2) + C(ind_IC4CHOAO2) + C(ind_IPBFUO2) 
+ &  
  C(ind_C7MCO3OHO2) + C(ind_T123CAT1O2) + C(ind_C7ADCCO3) + &  
  C(ind_C7ADCO2) + C(ind_NTMB1FUO2) + C(ind_TMB1FUO2) + 
C(ind_NTMB2FUO2) &  
  + C(ind_MC6OTKETO2) + C(ind_TMB2FUO2) + C(ind_C7BDCO2) + &  
  C(ind_T124CAT1O2) + C(ind_OTCATEC1O2) + C(ind_MTCATEC1O2) + &  
  C(ind_C7EDCO2) + C(ind_PTCATEC1O2) + C(ind_C7DDCCO3) + C(ind_C7DDCO2) 
&  
  + C(ind_NMEBFUO2) + C(ind_C23O3EO2) + C(ind_MEBFUO2) + C(ind_EMPHO2) 
+ &  
  C(ind_CH3COCCLO2) + C(ind_CLCOCCL2O2) + C(ind_C527O2) + C(ind_C526O2) 
&  
  + C(ind_HC4ACO3) + C(ind_C58AO2) + C(ind_INB1O2) + C(ind_INB2O2) + &  
  C(ind_HPC52O2) + C(ind_HC4CCO3) + C(ind_C57AO2) + C(ind_C57O2) + &  
  C(ind_INDO2) + C(ind_C59O2) + C(ind_C524O2) + C(ind_ETHFORMO2) + &  
  C(ind_IPRMEETO2) + C(ind_CHOOMCO3) + C(ind_PRONFORMO2) + &  
  C(ind_PRCOOMCO3) + C(ind_PRCOOMO2) + C(ind_BOXCOCHOO2) + &  
  C(ind_BOXFORMO2) + C(ind_PRONOCOPO2) + C(ind_BOXCOCOMO2) + &  
  C(ind_PINALO2) + C(ind_C108O2) + C(ind_C89CO3) + C(ind_C920CO3) + &  
  C(ind_C920O2) + C(ind_C97O2) + C(ind_C85CO3) + C(ind_C85O2) + &  
  C(ind_C719O2) + C(ind_C918O2) + C(ind_C9DCO2) + C(ind_C915O2) + &  
  C(ind_C917O2) + C(ind_NLIMALO2) + C(ind_LIMALO2) + C(ind_C729CO3) + &  
  C(ind_C822CO3) + C(ind_C924O2) + C(ind_C816CO3) + C(ind_NORLIMO2) + &  
  C(ind_C816O2) + C(ind_NLMKAO2) + C(ind_LMKAO2) + C(ind_LMKBO2) + &  
  C(ind_C146O2) + C(ind_C131CO3) + C(ind_BCLKAO2) + C(ind_BCLKBO2) + &  
  C(ind_BCLKCO2) + C(ind_C131O2) + C(ind_C147O2) + C(ind_C126CO3) + &  
  C(ind_C136CO3) + C(ind_C148O2) + C(ind_C1311O2) + C(ind_NC1313O2) + &  
  C(ind_C1313O2) + C(ind_C126O2) + C(ind_C144O2) + C(ind_C142O2) + &  
  C(ind_NBCKO2) + C(ind_BCKAO2) + C(ind_BCKBO2) + C(ind_CH3SOO) + &  
  C(ind_H13C43CO3) + C(ind_C42CO3) + C(ind_HOC3H6CO3) + C(ind_C3DIOLO2) 
&  
  + C(ind_HO2C4CO3) + C(ind_HOIBUTCO3) + C(ind_C63O2) + C(ind_HO3C5CO3) 
&  
  + C(ind_C64O2) + C(ind_HO2C54O2) + C(ind_HO2C54CO3) + C(ind_C66O2) + 
&  
  C(ind_CO3C54CO3) + C(ind_H2M2C4CO3) + C(ind_C67O2) + C(ind_C610O2) + 
&  
  C(ind_H2M3C4CO3) + C(ind_C68O2) + C(ind_C69O2) + C(ind_C611O2) + &  
  C(ind_HM33C3CO3) + C(ind_HM22C3O2) + C(ind_HM22C3CO3) + &  
  C(ind_HM2C43CO3) + C(ind_C71O2) + C(ind_C76O2) + C(ind_C77O2) + &  
  C(ind_C78O2) + C(ind_C711O2) + C(ind_H3M3C5O2) + C(ind_H3M3C5CO3) + &  
  C(ind_C82O2) + C(ind_C81O2) + C(ind_C93O2) + C(ind_C92O2) + &  
  C(ind_HO6C7O2) + C(ind_C103O2) + C(ind_C102O2) + C(ind_HO7C8O2) + &  
  C(ind_C113O2) + C(ind_C112O2) + C(ind_HO8C9O2) + C(ind_C123O2) + &  
  C(ind_C122O2) + C(ind_CO1H63O2) + C(ind_C3NO3COO2) + C(ind_NPHEN1O2) 
+ &  
  C(ind_NNCATECO2) + C(ind_NCATECO2) + C(ind_NBZQO2) + C(ind_PBZQO2) + 
&  
  C(ind_NPTLQO2) + C(ind_PTLQO2) + C(ind_NCRES1O2) + C(ind_MNNCATECO2) 
+ &  
  C(ind_MNCATECO2) + C(ind_NOXYOL1O2) + C(ind_NOXYQO2) + C(ind_OXYQO2) 
+ &  
  C(ind_OXNNCATCO2) + C(ind_OXNCATECO2) + C(ind_C534O2) + &  
  C(ind_NMXYOL1O2) + C(ind_NMXYQO2) + C(ind_MXYQO2) + C(ind_MXNNCATCO2) 
&  
  + C(ind_MXNCATECO2) + C(ind_NPXYOL1O2) + C(ind_NPXYQO2) + &  
  C(ind_PXYQO2) + C(ind_PXNNCATCO2) + C(ind_PXNCATECO2) + &  
  C(ind_NEBNZ1O2) + C(ind_NPEBQO2) + C(ind_PEBQO2) + C(ind_ENNCATECO2) 
+ &  
  C(ind_ENCATECO2) + C(ind_CO3H4CO3) + C(ind_PHCOCOCO2) + &  
  C(ind_NPBNZ1O2) + C(ind_NPPRBQO2) + C(ind_PPRBQO2) + 
C(ind_PNNCATECO2) &  
  + C(ind_PNCATECO2) + C(ind_C5O45OHCO3) + C(ind_NIPBNZ1O2) + &  
  C(ind_NIPRBQO2) + C(ind_IPRBQO2) + C(ind_IPNNCATCO2) + &  
  C(ind_IPNCATECO2) + C(ind_C4MOHOCO3) + C(ind_NT123L1O2) + &  
  C(ind_T123NNCTO2) + C(ind_T123NCATO2) + C(ind_NT124L1O2) + &  
  C(ind_NTM124QO2) + C(ind_TM124QO2) + C(ind_T124NNCTO2) + &  
  C(ind_T124NCATO2) + C(ind_C5CO234O2) + C(ind_NOETOL1O2) + &  
  C(ind_NOETLQO2) + C(ind_OETLQO2) + C(ind_OTNNCATCO2) + &  
  C(ind_OTNCATECO2) + C(ind_NMETOL1O2) + C(ind_NMETLQO2) + &  
  C(ind_METLQO2) + C(ind_MTNNCATCO2) + C(ind_MTNCATECO2) + &  
  C(ind_NPETOL1O2) + C(ind_NPETLQO2) + C(ind_PETLQO2) + &  
  C(ind_PTNNCATCO2) + C(ind_PTNCATECO2) + C(ind_CO234C65O2) + &  
  C(ind_H13CO2CO3) + C(ind_CO2N3CO3) + C(ind_C535O2) + C(ind_C58NO3CO3) 
&  
  + C(ind_ACCOCOMEO2) + C(ind_ACEETOHO2) + C(ind_ACCOMCOMO2) + &  
  C(ind_ACCOCOETO2) + C(ind_MTBEAALCO3) + C(ind_C62O2) + 
C(ind_HO13C4O2) &  
  + C(ind_HM22CO3) + C(ind_C6COCHOCO3) + C(ind_C5COCHOO2) + &  
  C(ind_CHOC2H4O2) + C(ind_HCOCH2CO3) + C(ind_CY6TRIONO2) + &  
  C(ind_C6CYTONO2) + C(ind_NC102O2) + C(ind_C512CO3) + C(ind_C89O2) + &  
  C(ind_C926O2) + C(ind_C817CO3) + C(ind_C817O2) + C(ind_NC826O2) + &  
  C(ind_C826O2) + C(ind_C729O2) + C(ind_LMLKAO2) + C(ind_LMLKBO2) + &  
  C(ind_C116CO3) + C(ind_C116O2) + C(ind_C129O2) + C(ind_C1210O2) + &  
  C(ind_CH3SOO2) + C(ind_C1H4C5CO3) + C(ind_CHOC4OHO2) + &  
  C(ind_HOC4CHOO2) + C(ind_C6145COO2) + C(ind_COHM2CO3) + &  
  C(ind_CO2C4CO3) + C(ind_HOBUT2CO3) + C(ind_CO3C5CO3) + &  
  C(ind_CO2C54CO3) + C(ind_C65O2) + C(ind_CO2M3C4CO3) + C(ind_C72O2) + 
&  
  C(ind_CO25C73O2) + C(ind_CO25C74O2) + C(ind_C712O2) + C(ind_C713O2) + 
&  
  C(ind_C714O2) + C(ind_C84O2) + C(ind_C94O2) + C(ind_C104O2) + &  
  C(ind_C114O2) + C(ind_C6H13CO3) + C(ind_C124O2) + C(ind_MALANHYO2) + 
&  
  C(ind_NDNPHENO2) + C(ind_DNPHENO2) + C(ind_NDNCRESO2) + &  
  C(ind_DNCRESO2) + C(ind_C6O4KETO2) + C(ind_NDNOXYOLO2) + &  
  C(ind_DNOXYOLO2) + C(ind_MMALANHYO2) + C(ind_CH3COCO3) + &  
  C(ind_NDNMXYOLO2) + C(ind_DNMXYOLO2) + C(ind_TL4OHNO2O2) + &  
  C(ind_NDNPXYOLO2) + C(ind_DNPXYOLO2) + C(ind_NDNEBNZLO2) + &  
  C(ind_DNEBNZLO2) + C(ind_NDNPBNZLO2) + C(ind_DNPBNZLO2) + &  
  C(ind_C61CO3) + C(ind_NDNIPBZLO2) + C(ind_DNIPBNZLO2) + C(ind_C62CO3) 
&  
  + C(ind_NDNT123LO2) + C(ind_DNT123LO2) + C(ind_TM124NO2O2) + &  
  C(ind_NDNT124LO2) + C(ind_DNT124LO2) + C(ind_MXYOHNO2O2) + &  
  C(ind_NDNOETOLO2) + C(ind_DNOETOLO2) + C(ind_NDNMETOLO2) + &  
  C(ind_DNMETOLO2) + C(ind_NDNPETOLO2) + C(ind_DNPETOLO2) + &  
  C(ind_CO356OCO2) + C(ind_C531O2) + C(ind_INCNCO3) + C(ind_IEACO3) + &  
  C(ind_IECCO3) + C(ind_HPC52CO3) + C(ind_INDHCO3) + C(ind_C57NO3CO3) + 
&  
  C(ind_INAHPCO3) + C(ind_INANCO3) + C(ind_INAHCO3) + C(ind_NC524O2) + 
&  
  C(ind_C525O2) + C(ind_HMACO3) + C(ind_HMACRO2) + C(ind_ACCOMECO3) + &  
  C(ind_IPRFORMO2) + C(ind_PRCOFORMO2) + C(ind_PRONOCOMO2) + &  
  C(ind_CO23C4CO3) + C(ind_C5CO34CO3) + C(ind_C106O2) + C(ind_C717O2) + 
&  
  C(ind_C811CO3) + C(ind_C921O2) + C(ind_C98O2) + C(ind_C86O2) + &  
  C(ind_C919O2) + C(ind_C914O2) + C(ind_C916O2) + C(ind_C88CO3) + &  
  C(ind_C88O2) + C(ind_C512O2) + C(ind_C619O2) + C(ind_C626CO3) + &  
  C(ind_C626O2) + C(ind_C735O2) + C(ind_C822O2) + C(ind_C823CO3) + &  
  C(ind_C925O2) + C(ind_C622CO3) + C(ind_C1011CO3) + C(ind_C1210CO3) + 
&  
  C(ind_C132O2) + C(ind_C137CO3) + C(ind_C1013CO3) + C(ind_C1312O2) + &  
  C(ind_C127O2) + C(ind_C143O2) + C(ind_CH3SO2O2) + C(ind_HO24C5O2) + &  
  C(ind_C55O2) + C(ind_C67CO3) + C(ind_H3M2C4CO3) + C(ind_C79O2) + &  
  C(ind_H3M3C4CO3) + C(ind_H13M3C5O2) + C(ind_HO4C5CO3) + &  
  C(ind_HO5C6CO3) + C(ind_HO6C7CO3) + C(ind_HO7C8CO3) + C(ind_HO8C9CO3) 
&  
  + C(ind_C5CO2OHCO3) + C(ind_C6CO2OHCO3) + C(ind_C5M2OHOCO3) + &  
  C(ind_C4COMOHCO3) + C(ind_C23O3MCO3) + C(ind_C23O3CCO3) + &  
  C(ind_C7CO2OHCO3) + C(ind_C6MOHCOCO3) + C(ind_C7OHCO2CO3) + &  
  C(ind_ECO3CO3) + C(ind_C8OHCO2CO3) + C(ind_C8CO2OHCO3) + &  
  C(ind_NDMMALYO2) + C(ind_DMMALYO2) + C(ind_C7MOHCOCO3) + &  
  C(ind_C5MEJCO3) + C(ind_C6EO2OHCO3) + C(ind_C7MJPCO3) + &  
  C(ind_C23O3ECO3) + C(ind_EMPOHNO2O2) + C(ind_C47CO3) + &  
  C(ind_INB1HPCO3) + C(ind_INB1NACO3) + C(ind_INB1NBCO3) + &  
  C(ind_MMALNACO3) + C(ind_MMALNBCO3) + C(ind_INDHPCO3) + &  
  C(ind_INANCOCO3) + C(ind_HIEB1O2) + C(ind_HIEB2O2) + C(ind_HO13C3CO3) 
&  
  + C(ind_C5CO23O2) + C(ind_CHOC2CO3) + C(ind_CHOC3COCO3) + &  
  C(ind_C5124COCO3) + C(ind_CO235C6CO3) + C(ind_NC71O2) + C(ind_C811O2) 
&  
  + C(ind_CHOC3COO2) + C(ind_H3C25C6CO3) + C(ind_H3C25C6O2) + &  
  C(ind_C810O2) + C(ind_C818O2) + C(ind_C727CO3) + C(ind_NC728O2) + &  
  C(ind_C728O2) + C(ind_C622O2) + C(ind_C823O2) + C(ind_C819O2) + &  
  C(ind_C731CO3) + C(ind_C1011O2) + C(ind_C137O2) + C(ind_C1013O2) + &  
  C(ind_C1010O2) + C(ind_C117O2) + C(ind_C830CO3) + C(ind_C145O2) + &  
  C(ind_C927O2) + C(ind_C1214O2) + C(ind_CHOC4DOLO2) + 
C(ind_C6TRONOHO2) &  
  + C(ind_C23C54CO3) + C(ind_C73O2) + C(ind_C74O2) + C(ind_C715O2) + &  
  C(ind_C83O2) + C(ind_C95O2) + C(ind_C105O2) + C(ind_C115O2) + &  
  C(ind_C125O2) + C(ind_C4CO2DBCO3) + C(ind_C5CO2DBCO3) + &  
  C(ind_C4DBM2CO3) + C(ind_C5DBCO2CO3) + C(ind_C7CO2DBCO3) + &  
  C(ind_C8CO2DBCO3) + C(ind_C8DBCO2CO3) + C(ind_C4DBMECO3) + &  
  C(ind_C5DBECO3) + C(ind_C5EDBCO3) + C(ind_C31CO3) + C(ind_C533O2) + &  
  C(ind_MECOFORMO2) + C(ind_C5124COO2) + C(ind_CO235C6O2) + &  
  C(ind_C716O2) + C(ind_C922O2) + C(ind_C614O2) + C(ind_C511O2) + &  
  C(ind_C620O2) + C(ind_C87CO3) + C(ind_C616O2) + C(ind_C718CO3) + &  
  C(ind_C513O2) + C(ind_CO25C6CO3) + C(ind_C627O2) + C(ind_C727O2) + &  
  C(ind_C511CO3) + C(ind_C517CO3) + C(ind_C517O2) + C(ind_C628O2) + &  
  C(ind_C824O2) + C(ind_C1211CO3) + C(ind_C133O2) + C(ind_C830O2) + &  
  C(ind_C128O2) + C(ind_HO24C4CO3) + C(ind_C613O2) + C(ind_CO2OH3MCO3) 
+ &  
  C(ind_C812O2) + C(ind_C721CO3) + C(ind_C721O2) + C(ind_H3C2C4CO3) + &  
  C(ind_C87O2) + C(ind_C718O2) + C(ind_C514O2) + C(ind_C820O2) + &  
  C(ind_C518CO3) + C(ind_NC623O2) + C(ind_C623O2) + C(ind_C825O2) + &  
  C(ind_C731O2) + C(ind_C732CO3) + C(ind_C1012O2) + C(ind_C1211O2) + &  
  C(ind_C139O2) + C(ind_C1014O2) + C(ind_C736O2) + C(ind_C118O2) + &  
  C(ind_C928CO3) + C(ind_C630O2) + C(ind_C1215O2) + C(ind_EMALANHYO2) + 
&  
  C(ind_PMALANHYO2) + C(ind_IPMALNHYO2) + C(ind_C312COCO3) + &  
  C(ind_CHOCOCH2O2) + C(ind_NC72O2) + C(ind_C621O2) + C(ind_C515CO3) + 
&  
  C(ind_C515O2) + C(ind_C821O2) + C(ind_HMVKBCO3) + C(ind_C520O2) + &  
  C(ind_C624CO3) + C(ind_C732O2) + C(ind_C829O2) + C(ind_C134O2) + &  
  C(ind_C827CO3) + C(ind_C522CO3) + C(ind_C831O2) + C(ind_C928O2) + &  
  C(ind_C46CO3) + C(ind_C930O2) + C(ind_C813O2) + C(ind_C722O2) + &  
  C(ind_C615CO3) + C(ind_C617CO3) + C(ind_C618CO3) + C(ind_C617O2) + &  
  C(ind_C618O2) + C(ind_NC730O2) + C(ind_C730O2) + C(ind_C624O2) + &  
  C(ind_C733O2) + C(ind_C1212O2) + C(ind_C827O2) + C(ind_C1310O2) + &  
  C(ind_NC61CO3) + C(ind_C615O2) + C(ind_C519CO3) + C(ind_C629O2) + &  
  C(ind_C734O2) + C(ind_C521O2) + C(ind_C135O2) + C(ind_COO2C4CO3) + &  
  C(ind_COO2C4O2) + C(ind_C929O2) + C(ind_C516O2) + C(ind_C44O2) + &  
  C(ind_H1C23C4CO3) + C(ind_H1C23C4O2) + C(ind_CO1M22CO3) + &  
  C(ind_C519O2) + C(ind_C625O2) + C(ind_C1213O2) + C(ind_COO2C3CO3) + &  
  C(ind_C828CO3) + C(ind_C828O2 ) ''')
  
sm['PeroxyAlkyl(RO2)']= np.array([i in ro2 for i in df.index],dtype=int)

r = re.compile(r'C\(=O\)O\[O\]$|^\[O\]O\(=O\)C', re.IGNORECASE)
sm['PeroxyAcid(RCO3)'] = np.array([len(r.findall(i)) for i in sm.smiles],dtype=int)

r = re.compile(r'\(C\)\[O\.*\]|\[O\.*\]\(C\)|C{0,1}\(\[O\.*\]\)C{0,1}', re.IGNORECASE)
sm['Alcoxy(RO)'] = np.array([len(r.findall(i)) for i in sm.smiles],dtype=int)

r = re.compile(r'C$|\(C\)|^C', re.IGNORECASE)
sm['Alcohol(C-H)'] = np.array([len(r.findall(i)) for i in sm.smiles],dtype=int)

r = re.compile(r'.C=C.', re.IGNORECASE)
sm['Unsaturated(>C=C<)'] = np.array([len(r.findall(i)) for i in sm.smiles],dtype=int)

r = re.compile(r'^C\({0,1}=O\){0,1}|\(=O\)C$|O=C$', re.IGNORECASE)
sm['Aldehyde(-CHO)'] = np.array([len(r.findall(i)) for i in sm.smiles],dtype=int)

r = re.compile(r'C\({0,1}=O\){0,1}.|.\({0,1}=O\){0,1}C', re.IGNORECASE)
sm['Carbonyl(>C=O)'] = np.array([len(r.findall(i)) for i in sm.smiles],dtype=int)


r = re.compile(r'\({0,1}O(NO2\b|NOO\b|N\(=O\)=O\){0,1}|\[N\+\](?:\[O-\\]|\(=O\)){2})', re.IGNORECASE)
sm['Nitrate(-ONO2)'] = np.array([len(r.findall(i)) for i in sm.smiles],dtype=int)

r = re.compile(r'^OOC|COO$|C\(OO\)|C\([^\)]*\({0,1}[^\)]*\){0,1}\)OO[^\w\[]', re.IGNORECASE)
sm['HydroPeroxide(-OOH)'] = np.array([len(r.findall(i)) for i in sm.smiles],dtype=int)

r = re.compile(r'C\(=O\)OON\(=O\)=O$|^\[O-{0,1}\]\[N\+{0,1}\]\(=O\)OOC|!\&\verb! O=N\(=O\)OOC\(=O\)|C\(=O\)OO\[N\+{0,1}\]\(=O\)\[O-{0,1}\]', re.IGNORECASE)
sm['PAN(-C(O)OONO2)'] = np.array([len(r.findall(i)) for i in sm.smiles],dtype=int)

print(sm[sm[sm.columns[-1]]>0])


print('fi')