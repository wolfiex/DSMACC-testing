#!/usr/local/anaconda/bin/python
import re,os,sys,glob

# Find all KPP input files
filedata = ''.join(tuple(open('./model.kpp')))
mech = re.findall(r'[^/\h]#INCLUDE(\s*.+)' ,filedata,re.IGNORECASE)

# Move KPP input files to save folder
for i in mech:
    i = re.sub(r'//.+$','',i)
    os.system('cp %s ./save/exec/%s/' %(i,sys.argv[1]))

# Move model.kpp and executable
os.system('cp ./model.kpp ./save/exec/%s/' %(sys.argv[1]))
os.system('cp ./model ./save/exec/%s/' %(sys.argv[1]))

# List all nc files
nc = glob.glob('*.nc')
print "Choose nc file to save:\n"
print "0  -  Save no nc files"
for i,f in enumerate(nc): print i+1 , ' - ', f.replace('.nc','')
selected_nc = raw_input("\nEnter number (only 1 choice possible): ")
i = int(selected_nc) - 1

# Move selected nc file to save folder
if i >=0: os.system('cp '+nc[i]+' ./save/ncfiles/%s.nc'%(sys.argv[1],sys.argv[1]))
print sys.argv[1] + ' saved\n'
