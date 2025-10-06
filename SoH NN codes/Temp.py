# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:14:17 2022

@author: IITM
"""

import pandas as pd
import matplotlib.pyplot as plt
f1="D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_3\\IDC test\\Cycle 3- IDC.xlsx"
df=pd.read_excel(f1,sheet_name='Sheet1')
df['delV']=df.loc[:,'Cell 1':'Cell 14'].max(axis=1)-df.loc[:,'Cell 1':'Cell 14'].min(axis=1)

df['Max_Cell']=df.loc[:,'Cell 1':'Cell 14'].idxmax(axis=1) 
df['Min_Cell']=df.loc[:,'Cell 1':'Cell 14'].idxmin(axis=1)

df['V_max']=df.loc[:,'Cell 1':'Cell 14'].max(axis=1) 
df['V_min']=df.loc[:,'Cell 1':'Cell 14'].min(axis=1)

name=f1.rsplit('\\',1)[1].rsplit('.',1)[0]+'_After_Balancing'
#%%
plt.figure()
plt.plot(range(0,len(df)),df.loc[:,'Cell 1':'Cell 14'])
plt.ylabel('Voltage(V)')
plt.grid(linestyle='dotted')
plt.title(name+'_Cell Voltages')
plt.legend(['Cell 1','Cell 2','Cell 3','Cell 4','Cell 5','Cell 6','Cell 7','Cell 8','Cell 9','Cell 10','Cell 11','Cell 12','Cell 13','Cell 14'], prop={'size':10})

#%%
plt.figure()
plt.plot(range(len(df)),df.loc[:,'T0':'T5'])
plt.ylabel('Temperature ('+u'\N{DEGREE SIGN}'+')')
plt.grid(linestyle='dotted')
plt.title(name+'_Cell Temperatures')
plt.legend(['T0','T1','T2','T3','T4','T5'],prop={'size':10})
#%%
plt.figure()
plt.plot(range(len(df)),df['delV'])
plt.ylabel('Voltage(mV)')
plt.grid(linestyle='dotted')
plt.title(name+'_delV')

#%%
df2=pd.read_excel(f1,sheet_name='Sheet2')

plt.figure()
plt.plot(range(len(df2)),df2['Hall_Current'])
plt.ylabel('Current(A)')
plt.title(name+'_Current')
plt.grid(linestyle='dotted')
plt.title(name+'_Current')

#%%
# f=open(f1.rsplit('\\',1)[0]+'\\'+name+'_observations.txt','w')

# print('Avg Minimum Cell: %s' % (df['Min_Cell'].mode()[0]), file=f)
# print('End Minimum Cell: %s ; Voltage: %s' %(df['Min_Cell'].iloc[-1],df['V_min'].iloc[-1]),file=f)
# print('Avg Maximum Cell: %s' %(df['Max_Cell'].mode()[0]), file=f)
# print('End Maximum Cell: %s ;  Voltage: %s' %(df['Max_Cell'].iloc[-1],df['V_max'].iloc[-1]),file=f)
# print('End DelV: %s mV' %(df['delV'].iloc[-1]), file=f)
# print('================================================',file=f)
# print('Observations:',file=f)

# f.close()