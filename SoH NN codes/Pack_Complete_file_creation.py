# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 10:43:58 2022

@author: IITM
"""

import pandas as pd
import numpy as np
import glob
import time
start=time.time()

#%%
pack_no='Pack_5'
df_chg=pd.DataFrame()
df_dchg=pd.DataFrame()

files_chg=glob.glob("D:\\Benisha\\2.8kWh_Charging Algorithm\\"+pack_no+"\\*\\*\\*\\Charging_complete_graph_data.csv")
files_dchg=glob.glob("D:\\Benisha\\2.8kWh_Charging Algorithm\\"+pack_no+"\\*\\*\\*\\Driving_complete_graph_data.csv")

#%%
for f1 in files_chg:
    df=pd.read_csv(f1)
    df_chg=pd.concat([df_chg,df])
    
for f2 in files_dchg:
    df=pd.read_csv(f2)
    df_dchg=pd.concat([df_dchg,df])

#%%
files_chg=glob.glob("D:\\Benisha\\2.8kWh_Charging Algorithm\\"+pack_no+"\\*\\*\\Charging_complete_graph_data.csv")
files_dchg=glob.glob("D:\\Benisha\\2.8kWh_Charging Algorithm\\"+pack_no+"\\*\\*\\Driving_complete_graph_data.csv")

#%%
for f1 in files_chg:
    df=pd.read_csv(f1)
    df_chg=pd.concat([df_chg,df])
    
for f2 in files_dchg:
    df=pd.read_csv(f2)
    df_dchg=pd.concat([df_dchg,df])

#%%
df_chg=df_chg.rename(columns={'t0':'T0','t1':'T1','t2':'T2','t3':'T3','t4':'T4','t5':'T5','Charger Output Current':'Pack_Current','Battery Measured Voltage':'Pack_Voltage'})
df_dchg=df_dchg.rename(columns={'Battery inst Current':'Pack_Current','Battery inst Volt':'Pack_Voltage'})
df_dchg['Pack_Current']=abs(df_dchg['Pack_Current'])

#%%
df=pd.concat([df_chg,df_dchg])

df['DateTime']=pd.to_datetime(df['DateTime'],errors='coerce',format='%Y-%m-%d %H:%M:%S')
df=df.sort_values(by='DateTime',ascending=True)

#%%
# df['Time_diff']=(df['DateTime']-df['DateTime'].shift(1))/np.timedelta64(1,'s')
df=df.reset_index(drop=True)
# l1=df[df['Time_diff']>1800].index.tolist()

# df=df.reindex(list(range(len(df)+len(l1))))

# #%%
# for i in range(len(l1)):
#     df.loc[l1[i]:,:]=df.loc[l1[i]:,:].shift(1)
#     df.loc[l1[i],'Session_Type']='Rest'
#     l1=[x+1 for x in l1]

# df=df.fillna(method='ffill')

#%%
df.to_csv("D:\\Benisha\\2.8kWh_Charging Algorithm\\"+pack_no+"\\"+pack_no+"_Complete_Cycle_data.csv")

print('-----------------%s seconds-----------------' %(time.time()-start))