import re

'''JVS(614) = Jac_FULL(96,99)'''


jacfile = ''.join( open('model_Jacobian.f90').readlines()  ).replace(' ','')
edges = re.findall('JVS\(\d+\)=Jac_FULL\((\d+),(\d+)\)\\n*JVS\(\d+\)',jacfile)

string = ','.join(['->'.join(i) for i in edges])


print len(edges)

with open('model_EdgeNames.inc','w') as f:
    f.write('write(jacsp_UNIT) "TIME,%s"'%(string))
    
