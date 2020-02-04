from ..helperscripts import picker
import pandas as pd

def keep(x):
    try:
        x = float(x)
        return x != 0
    except:
        return True



icloc='InitCons/'

split = picker.Picker(icloc+'[!split]*.csv',remove=[''],title = 'Select File').getSelected()[0]

print(split)


df = pd.read_csv(split)
for i in df.columns[3:]:
    i = df[i]
    dummy = df[df.columns[:3]].copy()
    name = i.loc[1]
    dummy[name] = list(i)
    dummy = dummy.loc[dummy.index[list(map(keep,i))],:]
    #print(dummy)

    dummy.to_csv(icloc+'split_'+name+'.csv',index=False,header=True)

    print('Written',icloc+'split_'+name+'.csv',len(df),len(dummy))
