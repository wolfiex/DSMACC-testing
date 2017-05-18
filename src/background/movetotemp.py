import re,os,sys

filedata = ''.join(tuple(open('./src/model.kpp')))
mech = re.findall(r'[^/\h]#INCLUDE\s(\./mechanisms/.+)' ,filedata,re.IGNORECASE)

for i in mech:
    os.system('cp %s ./save/exec/%s/' %(i,sys.argv[1]))
    
os.system('cp ./src/model.kpp ./save/exec/%s/' %(sys.argv[1]))
os.system('cp ./model ./save/exec/%s/' %(sys.argv[1]))

print sys.argv[1] + ' saved'
