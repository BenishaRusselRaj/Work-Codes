# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 14:13:15 2023

@author: IITM
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%%
data=pd.read_excel("D:\\Benisha\\10p15s\\LFP_OCV_Mean.xlsx")

#%%
v_array=np.array(data['Chg_Voltage(V)'])
v_array=np.append(v_array,data['DChg_Voltage(V)'])
s_array=np.array(data['Chg_SoC(%)'])
s_array=np.append(s_array,data['DChg_SoC(%)'])

#%%
# v_array=data['Chg_Voltage(V)']
# v_array.append(data['DChg_Voltage(V)'])
# s_array=data['Chg_SoC(%)']
# s_array.append(data['DChg_SoC(%)'])
#%%
cols=['OCV','SoC']
df=pd.DataFrame(columns=cols)

df['OCV']=v_array
df['SoC']=s_array

df=df.sort_values(by='SoC')

df['OCV']=df['OCV'].rolling(50).mean()
df['SoC']=df['SoC'].rolling(50).mean()

#%%
plt.figure()
plt.plot(data['Chg_SoC(%)'],data['Chg_Voltage(V)'],label='Charging')
plt.plot(data['DChg_SoC(%)'],data['DChg_Voltage(V)'],label='Discharging')
plt.plot(df['SoC'],df['OCV'],label='Mean')
plt.legend()
plt.xlabel('SoC (%)',fontweight='bold')
plt.ylabel('Voltage (V)',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('SoC Vs OCV',fontweight='bold')
plt.show()