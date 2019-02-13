import re

mc = ' '.join(tuple(open('formatted_GCGC_full.kpp')))
sp = re.findall(r'\b(\w+)\s*=\s*IGNORE' ,mc)

dp = tuple(open('depos_CAPRAM.kpp'))

def ftr(x):
	try:
		y = x.split(' ')[1]
		if (y not in sp):
			x='//'+x
	except:None
	return x

with open('formatted_CAPRAM.kpp','w') as f:
	for i in dp:
		f.write(ftr(i))


