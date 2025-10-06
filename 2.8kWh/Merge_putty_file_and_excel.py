# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 13:23:48 2022

@author: IITM
"""

import time
start=time.time()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
cols=['Time','PC','PE','CV0','CV1','CV2','CV3','CV4','CV5','CV6','CV7','CV8','CV9','CV10','CV11','CV12','CV13','CT0','CT1','CT2','CT3','CT4','CT5','SOC','SOH']
#%%
#df=pd.DataFrame()

df=pd.read_csv("D:\\Benisha\\2.8kWh_Charging Algorithm\\Tera Term Logs\\05_01_22\\Pack5balancing_8Kwh_Pack5_0401.csv",sep='|',low_memory=False,names=cols,index_col=False)
#df2=pd.read_csv("D:\\Benisha\\2.8kWh_Charging Algorithm\\Tera Term Logs\\3_01_22\\pack4balancing_30_12_21.csv",sep='|',low_memory=False,names=cols,index_col=False)
#df3=pd.read_csv("D:\\Benisha\\2.8kWh_Charging Algorithm\\Tera Term Logs\\3_01_22\\pack4balancing_31_12_21.csv",sep='|',low_memory=False,names=cols,index_col=False)
#
#df=pd.concat([df1,df2,df3])

#%%
df=df.dropna(subset=['CV0','CV1','CV2','CV3','CV4','CV5','CV6','CV7','CV8','CV9','CV10','CV11','CV12'])
df['CV0']=df['CV0'].str.rsplit(' ',1).str[1]
#df.loc[df['CV13'].str.contains('CT', na=False),'CV13']=np.NaN
df['CT0']=df['CT0'].str.rsplit(' ',1).str[1]
df['Time']=df['Time'].str.replace('[','')
df['Time']=df['Time'].str.replace(']','')

#%%

df[['CV0','CV1','CV2','CV3','CV4','CV5','CV6','CV7','CV8','CV9','CV10','CV11','CV12','CV13']]=df[['CV0','CV1','CV2','CV3','CV4','CV5','CV6','CV7','CV8','CV9','CV10','CV11','CV12','CV13']].astype(float)#,errors='ignore'
#df['CV13']=df['CV13'].astype(int)


#%%
df['Time']=df['Time'].str.rsplit(' ',2).str[0]
df['Time']=df['Time'].str.rsplit('.',1).str[0]

df['Time']=pd.to_datetime(df['Time'],errors='coerce',format='%Y-%m-%d %H:%M:%S')
df['Time_sec']=((df['Time']-df['Time'].shift())/np.timedelta64(1,'s')).cumsum()
df['Time_min']=((df['Time']-df['Time'].shift())/np.timedelta64(1,'m')).cumsum()
df['Time_hrs']=((df['Time']-df['Time'].shift())/np.timedelta64(1,'h')).cumsum()
df['del_V']=df.loc[:,'CV0':'CV13'].max(axis=1)-df.loc[:,'CV0':'CV13'].min(axis=1)

#%%
plt.figure()
plt.plot(df['Time_min'],df.loc[:,'CV0':'CV13'],'o-',markersize=2)
plt.xlabel('Time(min)',size=14)
plt.ylabel('Voltage(mV)',size=14)
plt.title('Cell Voltage',size=16,fontweight='bold')
plt.grid(linestyle='dotted')
plt.legend(['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13'],prop={'size':10})
#plt.savefig(path+'\\Cell Voltage.png',dpi=1200)

#%%
plt.figure()
plt.plot(df['Time_min'],df['del_V'],'o-',markersize=2)
plt.xlabel('Time(min)',size=14)
plt.ylabel('Voltage(mV)',size=14)
plt.title('Del V',size=16,fontweight='bold')
plt.grid(linestyle='dotted')
#plt.legend('',prop={'size':10})
#%%
#data=pd.read_excel("D:\\Benisha\\2.8kWh_Charging Algorithm\\Tera Term Logs\\3_01_22\\Pack 4-2.8kWh battery ideal case rest with balancing on.xlsx")
print("-----%s seconds-----" % (time.time() - start))