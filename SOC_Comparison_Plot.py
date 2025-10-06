# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 16:23:33 2019

@author: IITM
"""
"""
Plots the soc predicted and soc received from bms; gives an idea about accuracy
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

df=pd.read_csv("D:\\Benisha\\Code files\\charging_data_mohali_soc_calculated_3809.csv",header=0,sep=',')

#%%
df['time']=pd.to_datetime(df['time'],errors='coerce')
df=df.dropna(subset=['SOC_pred'])
df['adj_soc_pred']=(df['SOC_pred']-5)/0.9
df['adj_soc_pred_s']=df['adj_soc_pred'].shift(1)
for i in range(0,len(df['adj_soc_pred'])):
    if (df['adj_soc_pred'].iloc[i]>100):
        df['adj_soc_pred'].iloc[i]=100
df['adj_soc_pred'].iloc[i]=(0.8*df['adj_soc_pred'].iloc[i])+(0.2*df['adj_soc_pred_s'].iloc[i])
#df['RMSE']=np.sqrt((df['adj_soc_pred']-df['soc'])**2/len(df['adj_soc_pred']))
#rmse=df['RMSE'].mean()
#mse=np.mean(np.sqrt(((df['adj_soc_pred']-df['soc'])**2)/len(df['adj_soc_pred'])))
#df['Time_Elapsed']=(df['time']-df['time'].iloc[0])/np.timedelta64(1,'m')
print(df.dtypes)
#%%
grouped=df.groupby('session',sort=False)
result=[g[1] for g in list(grouped)]
for i in range (0,len(result)):
        result[i]['Time_Elapsed']=(result[i]['time']-result[i]['time'].iloc[0])/np.timedelta64(1,'m')
#        x=[datetime.strptime(elem, '%Y-%m-%d %H:%M:%S') for elem in result[i]['time']]
#        plt.scatter(result[i]['Time_Elapsed'],result[i]['soc'],label='SOC - BMS estimation')
        plt.scatter(result[i]['Time_Elapsed'],result[i]['adj_soc_pred'],label='SOC - Server estimation')
        #plt.scatter(result[i]['Time_Elapsed'],result[i]['current'],s=25,label='current')
        plt.xlabel('Time (min)',size=14)
        plt.ylabel('SOC (%)',size=14)
#        plt.legend(loc=2, prop={'size':10})
        plt.title('SOC Estimation',fontweight='bold',size=14)
        plt.grid(linestyle='dotted')
        x=str(i)
        plt.savefig('SOC estim comparision.png', format='png', dpi=1200)
        plt.show()
        break
        