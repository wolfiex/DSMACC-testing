import re,os,sys

filedata = ''.join(tuple(open('./model.kpp')))
mech = re.findall(r'[^/\h]#INCLUDE(\s*.+)' ,filedata,re.IGNORECASE)


for i in mech:
    i = re.sub(r'//.+$','',i)
    os.system('cp %s ./save/exec/%s/' %(i,sys.argv[1]))

os.system('cp ./model.kpp ./save/exec/%s/' %(sys.argv[1]))
os.system('cp ./model ./save/exec/%s/' %(sys.argv[1]))

print sys.argv[1] + ' saved'
