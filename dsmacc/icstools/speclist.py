from ..helperscripts import picker
import pandas as pd

icloc='InitCons/'

split = picker.Picker(icloc+'*.csv',remove=[''],title = 'Select File').getSelected()[0]

print(split)


df = pd.read_csv(split)
s = df[df.columns[1]].values
print('\n')
ignore ='nan Species TIME TEMP LAT LON JDAY H2O PRESS SPINUP O3 NO NO2 CO O3 HO OH HONO CL NOX '.split()

s = list(filter(lambda x:x not in ignore,s.astype(str)))


print(' '.join(s))
