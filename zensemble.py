import pandas as pd
import numpy as np

spinup = 3 # in whole number days
nruns = 2

df = pd.DataFrame(
[
       ['ii', 'TIME', '0', str(24*60*60*12)],
       ['ii', 'TEMP', '0', '298'],
       ['ii', 'LAT', '0', '51.5'],
       ['ii', 'LON', '0', '0.1'],
       ['ii', 'JDAY', '0', '173.5'],
       ['ii', 'H2O', '0', '0.02'],
       ['ii', 'ALBEDO', '0', '0'],
       ['ii', 'PRESS', '0', '1013'],
       ['ii', 'NOx', '0', '0'],
       ['ii', 'DEPOS', '1', '0'],
       ['ii', 'FEMISS', '1', '0'],
       ['ii', 'H2', '0', '0.0000005'],
       ['ii', 'NO', '0', '0.00000001'],
       ['ii', 'NO2', '0', '0'],
       ['ii', 'O3', '0', '0.00000004'],
       ['ii', 'CH4', '0', '0.00000002'],
       ['ii', 'OH', '0', '1e-6'],
       ['s', 'SPINUP', '0', '1e99']

       ]
)

df.columns =  ['Index', 'Species', 'Constrain', 'base']

col = list(df['base'])

for i,s in enumerate(np.linspace(spinup, spinup+1, nruns)):
    col[-1]=str(s)
    df['spin_'+str(i+1)] = col


with open('InitCons/ensemble.csv','w') as f:
    f.write(','*(df.shape[1]-1))
    f.write('\n')
    f.write(','*(df.shape[1]-1))
    f.write('\n')
    f.write(','.join(df.columns))
    f.write('\n')
    f.write('\n'.join([','.join(i) for i in df.values]))
