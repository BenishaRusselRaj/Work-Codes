# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 13:27:44 2022

@author: IITM
"""

import pandas as pd
import numpy as np
import glob
import time
import matplotlib.pyplot as plt

start=time.time()

#%%
files1=glob.glob("D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_1\\SoH_test\\*\\*\\Driving Data\\-battery_periodic_voltage*_modified.xlsx") #"D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_1\\SoH_test\\
files2=glob.glob("D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_1\\SoH_test\\*\\*\\Charging Data\\-charging_periodic_graph_data.xlsx_modified.xlsx")
files3=glob.glob("D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_1\\SoH_test\\*\\*\\Charging Data\\-charging_temperature_graph_data-.xlsx_modified.xlsx")
files4=glob.glob("D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_1\\SoH_test\\*\\*\\Charging Data\\-charging_voltage_graph_data.xlsx_modified.xlsx")

df_I=pd.DataFrame()   
df_T=pd.DataFrame()
df_V=pd.DataFrame()
df_V_dchg=pd.DataFrame()

data=pd.DataFrame()

#%%
chg_data_25=pd.read_csv("E:\\Davis-6A\\Phylion 14Ah\\25deg\\phy14_25_chg.csv")
chg_data_25['T_amb']=25
del_Cap_25=((chg_data_25['chg_Capacity'].iloc[-1]-chg_data_25['chg_Capacity'].iloc[0])*4)/1000
chg_data_35=pd.read_csv("E:\\Davis-6A\\Phylion 14Ah\\35deg\\phy14_35_chg.csv")
chg_data_35['T_amb']=35
# chg_data_35['del_Cap']=np.nan
chg_data_45=pd.read_csv("E:\\Davis-6A\\Phylion 14Ah\\45deg\\phy14_45_chg.csv")
chg_data_45['T_amb']=45
# chg_data_45['del_Cap']=np.nan

chg_data=pd.concat([chg_data_25,chg_data_35,chg_data_45])
# chg_data['del_Cap']=chg_data['del_Cap'].fillna(method='ffill')
chg_data=chg_data.reset_index(drop=True)
 
#%%
z=0
for f in files1:
    df=pd.read_excel(f)
    df['Flag']=z
    df['Time_in_sec']=df['Time_in_sec']/60
    df=df.rename(columns={'Time_in_sec':'Time_in_min'})
    
    df['V_min']=df.loc[:,'C0':'C13'].min(axis=1)

    df['OCV1']=df['V_min'].iloc[-2]
    df['OCV2']=np.nan
    df['OCV2']=np.where((np.isclose(df['Time_in_min'],30,rtol=0.01)),df['V_min'],df['OCV2'])
    df['OCV2']=df['OCV2'].fillna(method='ffill')
    df['OCV2']=df['OCV2'].fillna(method='bfill') 
    
    z=z+1
    df_V_dchg=pd.concat([df_V_dchg,df])
    del [[df]]

#%%
data['OCV1']=df_V_dchg['OCV1'] #.drop_duplicates(keep='first').values
data['OCV2']=df_V_dchg['OCV2'] #.drop_duplicates(keep='first').values
data['Flag']=df_V_dchg['Flag']

data=data.drop_duplicates(subset=['Flag'],keep='first')

del [[df_V_dchg, chg_data_25, chg_data_35, chg_data_45]]

#%%
x=0
for f in files2:
      df=pd.read_excel(f)
      df['Flag']=x
      x=x+1
      df_I=pd.concat([df_I,df])
      del [[df]]

#%%
x=0
for f in files3:
      df=pd.read_excel(f)
      df['Flag']=x
      x=x+1
      df_T=pd.concat([df_T,df])
      del [[df]]

#%%
x=0
for f in files4:
      df=pd.read_excel(f)
      df['Flag']=x
      df['V_min']=df.loc[:,'C0':'C13'].min(axis=1)
      df['OCV1']=np.nan
      df['OCV2']=np.nan

      df['OCV1']=np.where((np.isclose(df['V_min'],data['OCV1'].iloc[x],rtol=0.02)),df['V_min'],df['OCV1']) #0.02 for Pack 5
      df['OCV2']=np.where((np.isclose(df['V_min'],data['OCV2'].iloc[x],rtol=0.001)),df['V_min'],df['OCV2'])
      df['OCV1']=df['OCV1'].fillna(method='ffill')
      df['OCV2']=df['OCV2'].fillna(method='bfill')

      x=x+1
      df_V=pd.concat([df_V,df])
      del [[df]]

#%%
df_T=df_T.dropna(how='all',axis=1)

#%%
c=df_I['DateTime']

df_V=df_V[df_V['DateTime'].isin(c)]
df_T=df_T[df_T['DateTime'].isin(c)]

#%%
df=pd.DataFrame()

df=pd.merge(df_I,df_V,how='left',on='DateTime')
# df=df.dropna(subset=['C0'])

df=pd.merge(df,df_T,how='left', on='DateTime')
df['T_avg']=df.loc[:,'t0':'t3'].mean(axis=1)
df['Temp_flag']=pd.cut(df['T_avg'],bins=[0,35,45,100],labels=[25,35,45],include_lowest=True)
df['Capacity']=df['Capacity'].fillna(0)
df['SoC1']=np.nan
df['SoC2']=np.nan

df=df.reset_index(drop=True)
#%%
dff=pd.DataFrame()
grouped=df.groupby(['Flag'],sort=False)
result=[g[1] for g in grouped]
for i in range(0,len(result)):
    a=result[i]['OCV1'].first_valid_index()
    b=result[i]['OCV2'].last_valid_index()
    result[i]['Computed_capacity']=result[i]['Capacity'].loc[b]-result[i]['Capacity'].loc[a]
    result[i]['OCV1']=result[i]['OCV1'].mean()
    result[i]['OCV2']=result[i]['OCV2'].mean()
    
    dff=pd.concat([dff,result[i]])


#%%
for i in range(0,len(chg_data)):        
    dff['SoC1']=np.where((np.isclose(dff['OCV1'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==25) & (dff['Temp_flag']==25)),chg_data['chg_soc'][i],dff['SoC1'])
    dff['SoC1']=np.where((np.isclose(dff['OCV1'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==35) & (dff['Temp_flag']==35)),chg_data['chg_soc'][i],dff['SoC1'])
    dff['SoC1']=np.where((np.isclose(dff['OCV1'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==45) & (dff['Temp_flag']==45)),chg_data['chg_soc'][i],dff['SoC1'])

    dff['SoC2']=np.where((np.isclose(dff['OCV2'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==25) & (dff['Temp_flag']==25)),chg_data['chg_soc'][i],dff['SoC2'])
    dff['SoC2']=np.where((np.isclose(dff['OCV2'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==35) & (dff['Temp_flag']==35)),chg_data['chg_soc'][i],dff['SoC2'])
    dff['SoC2']=np.where((np.isclose(dff['OCV2'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==45) & (dff['Temp_flag']==45)),chg_data['chg_soc'][i],dff['SoC2'])
    
#%%
dff['del_SoC']=dff['SoC2']-dff['SoC1']
dff['SoH_Calculated']=(dff['Computed_capacity']/(del_Cap_25*dff['del_SoC']/100))*100 # *dff['del_SoC']/100
dff=dff.sort_values(by='DateTime',ascending=True)
#%%
plt.figure()
plt.plot(dff['DateTime'],dff['SoH_Calculated'],label='SoH Calculated')
plt.title('SoH_calculated')
plt.xlabel('Datetime')
plt.ylabel('SoH')
plt.grid(linestyle='dotted')


#%%
print('----------------%s seconds----------------' %(time.time()-start))
