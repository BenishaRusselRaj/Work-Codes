# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 12:51:08 2022

@author: IITM
"""

# -*- coding: utf-8 -*-
"""
Created on Sat May 21 12:39:11 2022

@author: IITM
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
start=time.time()

f="D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_6.1\\SoH_Calculated_summary_files\\PHY_6.1_AllCycles_Timestates_added_soh_summary.csv"
dff=pd.read_csv(f)

#%%

plt.figure()
plt.plot(range(0,len(dff)),dff['SoH_calculated'])
plt.title('SoH_calculated')

#%%

plt.figure()
plt.plot(range(0,len(dff)),dff['mean_SoC'])
plt.title('SoC_calculated')

#%%

df_c=pd.DataFrame()

df_c=dff[(dff.SoH_calculated>65)&(dff.SoH_calculated<111)] # Change according to cell 38,101
# df_c['mean_SoC']=np.where((df_c['mean_SoC']>55)&(df_c['mean_SoC']<60),df_c['mean_SoC'],np.nan)
df_c['SoH_diff']=df_c['SoH_calculated'].shift(1)-df_c['SoH_calculated']
# df_c['SoC_diff']=df_c['mean_SoC'].shift(1)-df_c['mean_SoC']

#%%
plt.figure()
plt.plot(range(0,len(df_c)),df_c['SoH_calculated'])
plt.title('SoH_calculated_limit')
#%%
while (df_c['SoH_diff'].abs()>0.5).any(): # change numbers as per need
    l1=df_c.index[df_c['SoH_diff'].abs()>0.5].tolist()
    for n,i in enumerate(l1):
        df_c.loc[i:,'SoH_calculated']=df_c.loc[i:,'SoH_calculated']+df_c.loc[i]['SoH_diff']
    df_c['SoH_diff']=df_c['SoH_calculated'].shift(1)-df_c['SoH_calculated']

#%%
# while (df_c['SoC_diff'].abs()>0.1).any(): # change numbers as per needed
#     l2=df_c.index[df_c['SoC_diff'].abs()>0.1].tolist()
#     for n,i in enumerate(l2):
#         df_c.loc[i:,'mean_SoC']=df_c.loc[i:,'mean_SoC']+df_c.loc[i]['SoC_diff']
#     df_c['SoC_diff']=df_c['mean_SoC'].shift(1)-df_c['mean_SoC']
    
#%% for 14.1 and 15.1
    
# x0=dff['SoH_calculated'].iloc[10]-dff['SoH_calculated'].iloc[-10]
# df_c['SoH_calculated']=df_c['SoH_calculated']-x0
df_c['SoH_calculated']=df_c['SoH_calculated'].rolling(20).mean()
df_c['SoH_calculated']=df_c['SoH_calculated'].fillna(method='bfill')

# df_c['mean_SoC']=df_c['mean_SoC'].rolling(20).mean()
# df_c['mean_SoC']=df_c['mean_SoC'].fillna(method='bfill')
#%%
plt.figure()
plt.plot(range(0,len(df_c)),df_c['SoH_calculated'])
plt.title('SoH_smooth')

# #%%
# plt.figure()
# plt.plot(range(0,len(df_c)),df_c['mean_SoC'])

#%%
# df_c.to_csv(f.rsplit('\\',1)[0]+'\\'+f.rsplit('\\',1)[1].rsplit('.',1)[0]+'_soh_smooth.csv')
df_c.to_csv(f.rsplit('.',1)[0]+'_soh_smooth.csv')

print('-----------------------%s seconds-----------------------' %(time.time()-start))