import glob

__ics__ = './InitCons'
__csvpath__ = './src/examples/constrain_obs/camp_avg_day'
__hour__ = 12

dur = 5*24*60*60

csvs = glob.glob(__csvpath__+'/*.csv')

text = '''Description: Optional,Do not write time more than once. ,,
,,,
Index,Species,Constrain,methane
ii,TIME,-0,%s
ii,TEMP,0,298
ii,LAT,0,52.1
ii,LON,0,0
ii,JDAY,0,173.5
ii,H2O,0,0.02
ii,ALBEDO,0,0
ii,PRESS,0,1013
ii,NOx,1,1
ii,DEPOS,1,0
ii,FEMISS,1,0
ii,H2,0,0.0000005
1,NO,0,0.00000001
2,NO2,0,0
3,O3,0,0.00000004
4,CH4,0,0.00000002
5,OH,0,1e-6
6,SPINUP,0,%s
'''%(dur,dur)
counter = 6
for i in csvs:
    counter+=1
    for j in tuple(open(i)):
        if '%s,'%__hour__ in j:
            text+='%d,%s,0,%s'%(counter,i.split('/')[-1].split('_')[0],j.split(',')[-1])


with open(__ics__+'/observationdiurnal.csv','w') as f :
    f.write(text)
print tuple(open(__ics__+'/observationdiurnal.csv'))
