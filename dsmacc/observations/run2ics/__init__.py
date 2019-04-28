'''
Take a selected timestep from a model run and use it to create the initial conditions for a new run.

Usage: 
    python -m dsmacc.observations.run2ics <filename>.h5 <timestep number> -r 


file created args : contiune_h5name_groupname_timestep_datenow


If using the lumped function it reads groups from a mechanism file.
Must use format from lumper.jl for this to work.

'''
import pandas as pd
import numpy as np
import datetime
import zhdf
import re


def lumpfn(df,mech):
    kpp = ' '.join(open(mech).readlines())
    gs = re.findall(r'(LMP\d),\s*String(["\'\w\d/ ,]+)\n+?',re.sub(r'\n */+','',kpp))
    print df
    for g in gs:
        cols = list(eval(g[1].replace(' ','')))
        new = df[cols].sum(axis=1)
        new.Species = g[0]
        new.Index = '_'.join(cols)
        df = df.drop(cols,axis=1)
        df[g[0]] = new
    return df





def newics(
h5file,
lump = False,
filename = False,
write = False,
group = 0,
rmspinup = False,
timestep=144,
constrain = ['NOX'],
ignore = ['R','RO2','M','NO','NO2','HO2','CH3O2','OH','TRICLETH','HONO','BUT2CHO', 'C3ME3CHO', 'C5H11CHO', 'CH2CL2', 'LIMONENE', 'MACR', 'MVK'],
df = pd.DataFrame(
    [
           ['ii', 'TIME', '0',str(24*60*60*5)],
           ['ii', 'TEMP', '0', '298'],
           ['ii', 'LAT', '0', '36.9'],
           ['ii', 'LON', '0', '116.31'],
           ['ii', 'JDAY', '0', '173.5'],
           ['ii', 'H2O', '0', '0.02'],
           ['ii', 'ALBEDO', '0', '0'],
           ['ii', 'PRESS', '0', '1013'],
           ['ii', 'NOx', '0', '0'],
           ['ii', 'DEPOS', '1', '0'],
           ['ii', 'FEMISS', '1', '0'],
           ['s', 'SPINUP', '0', '1e99']

           ]
    ),
    ):


    ''' 
    make new InitCons

    Args required:
     - h5file
     
     Many optional arguments
     
     '''
        

    df.columns =  ['Index', 'Species', 'Constrain', 'base']

    a = zhdf.new(h5file,group)
    if rmspinup: a.rm_spinup()
    
    cols = filter(lambda x: x not in ignore,a.spec.columns)
    try:
        specs = a.spec.loc[a.timesteps[timestep],cols].compute()
    except:
        specs = a.spec.loc[timestep,cols].compute()
    df.index = df.Species
    df = df.T

    for s in specs.columns:
        M = 1
        if s in ['LAT','LON','TEMP']: M = a.M.compute()
        df[s] = ['continue',s,int(s in constrain),specs[s][0]*M]

    if lump:
        df = lumpfn(df,lump)

    df = df.astype(str)




    if write:
        if not filename:
                filename = 'contiunue_%s_%s_%s_%s'%(h5file.split('.h5')[0],group,timestep,datetime.date.today().strftime("%d%m%y"))

        df = df.astype(str).T
        with open('InitCons/'+filename+'.csv','w') as f:
            f.write('A continuation ics file'+','*(df.shape[1]-1))
            f.write('\n')
            f.write(','*(df.shape[1]-1))
            f.write('\n')
            f.write(','.join(df.columns))
            f.write('\n')
            f.write('\n'.join([','.join(i) for i in df.values]))
        print filename, 'written'

    return df
'''
df = newics('test.h5', filename = 'normalcri', write =True,lump = False)

df = newics('test.h5', filename = 'lumpedcri', write =True,lump = './mechanisms/lumped_formatted_CRI_FULL_2.2.kpp')


'''
