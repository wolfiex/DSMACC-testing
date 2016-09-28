import os,sys

content = tuple(open(sys.argv[1]))

strip = False

for line in xrange(len(content)):
    current = content[line]
    if 'RO2 =' in current: strip = True
    if strip = True:
        if 'CALL mcm' in current: 
            strip=False
        else:
            content[line]=current.replace('&','').replace('\n','')




