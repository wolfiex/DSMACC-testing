''' 
Remove carrage returns and add dummy to new mechanisms
D.Ellis 2017
'''

import sys,re

filename = sys.argv[1]#'./mechanisms/mcm331complete.kpp'
data = tuple(open(filename))


regex = re.compile(r"^[\d\D]\s*=\s*IGNORE")
rx1   = re.compile(r"=\s*:")


overwrite = open(filename,'w')
[ overwrite.write(rx1.sub( '=DUMMY:', regex.sub( "DUMMY=IGNORE", line.strip('//r')) )) for line in data]
overwrite.close()

print filename, 'updated \n'

'''
add O = ignore 
remove multiple dummy declerations
kpp equation duplicates.

'''
