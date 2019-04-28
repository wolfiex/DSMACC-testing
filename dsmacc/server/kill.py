import os

server = os.popen("lsof -i :8000 | grep 'python'").read().replace('  ',' ').split(' ')


os.system('kill -9 '+server[1])







 




 
