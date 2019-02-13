import pandas as pd
df = pd.read_csv('centrality/collected.txt',header = None)

npts =144*3
<<<<<<< HEAD
maxlen   = 8
=======
maxlen   = 4
>>>>>>> master
df=df[df[0]>npts*.7]
minlen=1

lmp = [i.split('-') for i in df[1]]
for i in lmp:print len(i)


skip = set([ "CH3OH","C2H5OH","NPROPOL","IPROPOL","NBUTOL","BUT2OL","IBUTOL","TBUTOL","PECOH","IPEAOH	 ME3BUOL","IPECOH","IPEBOH","CYHEXOL","MIBKAOH","ETHGLY","PROPGLY","HCHO","CH3CHO","C2H5CHO	 C3H7CHO","IPRCHO","C4H9CHO","CH4","C2H6","C3H8","NC4H10","IC4H10","NC5H12","IC5H12","NEOP","NC6H14  M2PE","M3PE","M22C4","M23C4","NC7H16","M2HEX","M3HEX","NC8H18","NC9H20","NC10H22","NC11H24	 NC12H26","CHEX","C2H4","C3H6","BUT1ENE","CBUT2ENE","TBUT2ENE","MEPROPENE","PENT1ENE","CPENT2ENE	 TPENT2ENE","ME2BUT1ENE","ME3BUT1ENE","ME2BUT2ENE","HEX1ENE","CHEX2ENE","THEX2ENE","C2H2","BENZENE  TOLUENE","OXYL","MXYL","PXYL","EBENZ","PBENZ","IPBENZ","TM123B","TM124B","TM135B","OETHTOL	 METHTOL","PETHTOL","DIME35EB","DIET35TOL","STYRENE","BENZAL","C4H6","C5H8","CH3OCHO","METHACET	 ETHACET","NPROACET","IPROACET","NBUTACET","SBUTACET","TBUACET","CH3OCH3","DIETETHER","MTBE	 DIIPRETHER","ETBE","MO2EOL","EOX2EOL","PR2OHMOX","BUOX2ETOH","BOX2PROL","CH3COCH3","MEK","MPRK  DIEK","MIPK","HEX2ONE","HEX3ONE","MIBK","MTBK","CYHEXONE","APINENE","BPINENE","HCOOH","CH3CO2H  PROPACID","DMM","DMC",
"APINENE","BENZAL","BENZENE","BUT1ENE","BUT2CHO","C2H2","C2H4","C2H5OH","C2H6","C3H6","C3H7CHO","C3H8","C3ME3CHO","C4H6","C4H9CHO","C5H11CHO","C5H8","CH2CL2","CH3CHO","CH3COCH3","CH3O2","CH3OH","CH4","CO","CYHEXONE","EBENZ","ETHACET","HCHO","HEX2ONE","HNO3","HO2","HONO","IC4H10","IC5H12","IPRCHO","LIMONENE","MACR","MEK","MEPROPENE","METHTOL","MPRK","MVK","NC10H22","NC11H24","NC12H26","NC4H10","NC5H12","NC6H14","NC7H16","NC8H18","NC9H20","NO","NO2","NOY","NPROPOL","O3","OETHTOL","OH","OXYL","PAN","PBENZ","PETHTOL","PXYL+MXYL","STYRENE","TM123B","TM124B","TM135B","TOLUENE","TRICLETH"])


lumping=[]
for l in lmp:
    l=filter(lambda x: x not in skip,l)
    
    ll= len(l)
    
    if (ll>minlen) & (ll<maxlen):
        skip = skip.union(set(l))
        lumping.append(l)



with open('groupslimited.txt','w') as f:
        f.write('lumplist=\n')
        f.write(str(lumping).replace("'",'"'))

for i in lumping:
    print i
print 'dn' 