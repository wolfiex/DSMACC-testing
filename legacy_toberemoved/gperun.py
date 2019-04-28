import pandas as pd
import gpflow
from matplotlib import pyplot as plt
import numpy as np

data = pd.read_csv('readres.csv')
groups = np.array(pd.read_csv('groups.csv'))[:,1:]


spec = 'O3'

for i in groups[:1000]:


    plt.plot(data.TIME.iloc[i],data.O3.iloc[i],alpha=0.2)
    
plt.show()
