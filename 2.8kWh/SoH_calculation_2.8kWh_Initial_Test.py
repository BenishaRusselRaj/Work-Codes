# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 10:22:51 2022

@author: IITM
"""


import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

start=time.time()


#%%
chg_data_25=pd.read_csv("E:\\Davis-6A\\Phylion 14Ah\\25deg\\phy14_25_chg.csv")
chg_data_25['T_amb']=25
del_Cap_25=((chg_data_25['chg_Capacity'].iloc[-1]-chg_data_25['chg_Capacity'].iloc[0])*4)/1000

chg_data_35=pd.read_csv("E:\\Davis-6A\\Phylion 14Ah\\35deg\\phy14_35_chg.csv")
chg_data_35['T_amb']=35

chg_data_45=pd.read_csv("E:\\Davis-6A\\Phylion 14Ah\\45deg\\phy14_45_chg.csv")
chg_data_45['T_amb']=45

chg_data=pd.concat([chg_data_25,chg_data_35,chg_data_45])

chg_data=chg_data.reset_index(drop=True)
 
#%%
# cols1=['name','Shunt_Current','name1', 'Current'] # Pack 1 
cols1=['date','time','name','Shunt_Current','name1', 'Current']
# cols2=['Name','Pack_Voltage','Name1','Pack_Current','Name2','Pack_Energy','Name3','C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','Name4','t0','t1','t2','t3','t4','t5','Name5','SOC','Name6','SOH']
cols2=['Date','Time','Name','Pack_Voltage','Name1','Pack_Current','Name2','Pack_Energy','Name3','C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','Name4','t0','t1','t2','t3','t4','t5','Name5','SOC','Name6','SOH']
df_I_dchg=pd.read_excel("D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_5\\PACK_5_INITIAL TEST\\PACK_5_INITIAL TEST\\Cycle2\\15_09_2021_Step5_PN5_DisC3_Cycle2_raw.xlsx",names=cols1,sheet_name='Sheet1',header=None) #,index_col=0
df_V_dchg=pd.read_excel("D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_5\\PACK_5_INITIAL TEST\\PACK_5_INITIAL TEST\\Cycle2\\15_09_2021_Step5_PN5_DisC3_Cycle2_raw.xlsx",names=cols2,sheet_name='Sheet2',header=None) #,index_col=0
df_I_dchg['Index_assumed']=range(0,len(df_I_dchg))
df_V_dchg['Index_assumed']=range(0,len(df_V_dchg))

df_dchg=pd.merge(df_I_dchg,df_V_dchg,how='left')

df_dchg['V_min']=df_dchg.loc[:,'C0':'C13'].min(axis=1)
df_dchg['OCV']=np.nan

#%%
df_dchg=df_dchg.dropna(subset=['C0'])
df_dchg['Current']=df_dchg['Current'].fillna(0)
df_dchg['OCV']=np.where(((df_dchg['Current']>=-1.5) & (df_dchg['Current']<1)), df_dchg['V_min'],df_dchg['OCV']) #df_dchg['V_min'].iloc[-1]
# df_dchg['OCV']=np.where((df_dchg['Current']==0), df_dchg['V_min'],df_dchg['OCV']) 


#%%
df_dchg['OCV']=df_dchg['OCV'].fillna(method='bfill')
df_dchg['OCV']=df_dchg['OCV'].fillna(method='ffill')

if(df_dchg['OCV'].iloc[0]==df_dchg['OCV'].iloc[-1]):
    df_dchg['OCV'].iloc[-1]=df_dchg['V_min'].iloc[-1]        

if(df_dchg['OCV'].iloc[0]<df_dchg['OCV'].iloc[-1]):
    df_dchg['OCV'].iloc[0]=df_dchg['V_min'].iloc[0]  

del [[chg_data_25, chg_data_35, chg_data_45]]

#%%
df_V_chg=pd.read_excel("D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_5\PACK_5_INITIAL TEST\\PACK_5_INITIAL TEST\\Cycle2\\15_09_2021_Step4_PN5_ChrgC3_Cycle2_raw.xlsx",sheet_name='Sheet2',names=cols2,header=None)
df_V_chg['V_min']=df_V_chg.loc[:,'C0':'C13'].min(axis=1)
df_V_chg['OCV1']=np.nan
df_V_chg['OCV2']=np.nan

df_V_chg['OCV1']=np.where((np.isclose(df_V_chg['V_min'],df_dchg['OCV'].iloc[-1],rtol=0.02)),df_V_chg['V_min'],df_V_chg['OCV1']) #0.02 for Pack 5
df_V_chg['OCV2']=np.where((np.isclose(df_V_chg['V_min'],df_dchg['OCV'].iloc[0],rtol=0.001)),df_V_chg['V_min'],df_V_chg['OCV2'])
df_V_chg['OCV1']=df_V_chg['OCV1'].fillna(method='ffill')
df_V_chg['OCV2']=df_V_chg['OCV2'].fillna(method='bfill')

df_I_chg=pd.read_excel("D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_5\PACK_5_INITIAL TEST\\PACK_5_INITIAL TEST\\Cycle2\\15_09_2021_Step4_PN5_ChrgC3_Cycle2_raw.xlsx",sheet_name='Sheet1',names=cols1,header=None)

#%% For Pack 1 alone
# df_I_chg['Index_assumed']=range(0,len(df_I_chg))
# df_V_chg['Index_assumed']=range(0,len(df_V_chg))

# df_chg=pd.merge(df_I_chg,df_V_chg,how='left',on=['Index_assumed'])

#%% Change Datetime
df_V_chg['Time']=df_V_chg['Time'].str.split('.').str[0]
df_V_chg['Date']=df_V_chg['Date'].str.split('[').str[1]
df_V_chg['DateTime']=df_V_chg['Date']+' '+df_V_chg['Time']
df_V_chg['DateTime']=pd.to_datetime(df_V_chg['DateTime'],errors='coerce',format='%Y-%m-%d %H:%M:%S')

df_I_chg['time']=df_I_chg['time'].str.split('.').str[0]
df_I_chg['date']=df_I_chg['date'].str.split('[').str[1]
df_I_chg['DateTime']=df_I_chg['date']+' '+df_I_chg['time']
df_I_chg['DateTime']=pd.to_datetime(df_I_chg['DateTime'],errors='coerce',format='%Y-%m-%d %H:%M:%S')


#%%
df_chg=pd.merge(df_I_chg,df_V_chg,how='left',on=['DateTime'])
df_chg=df_chg.drop_duplicates(subset=['DateTime'],keep='first')
df_chg=df_chg.reset_index(drop=True)

#%%
df_chg['Time_in_sec']=(df_chg['DateTime']-df_chg['DateTime'].shift(1))/np.timedelta64(1,'s')
df_chg['Time_in_sec']=df_chg['Time_in_sec'].fillna(0)

df_chg=df_chg.dropna(subset=['Current'])
df_chg['Capacity']=(df_chg['Current']*df_chg['Time_in_sec']/3600).cumsum()
df_chg['T_avg']=df_chg.loc[:,'t0':'t3'].mean(axis=1)
df_chg['Temp_flag']=pd.cut(df_chg['T_avg'],bins=[0,35,45,100],labels=[25,35,45],include_lowest=True)
# df_chg['Capacity']=df_chg['Capacity'].fillna(0)
df_chg['SoC1']=np.nan
df_chg['SoC2']=np.nan

df_chg=df_chg.reset_index(drop=True)
#%%
a=df_chg['OCV1'].first_valid_index()
b=df_chg['OCV2'].last_valid_index()
df_chg['Computed_capacity']=df_chg['Capacity'].loc[b]-df_chg['Capacity'].loc[a]
df_chg['OCV1']=(df_chg['OCV1'].mean())/1000
df_chg['OCV2']=(df_chg['OCV2'].mean())/1000

#%%
for i in range(0,len(chg_data)):        
    df_chg['SoC1']=np.where((np.isclose(df_chg['OCV1'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==25) & (df_chg['Temp_flag']==25)),chg_data['chg_soc'][i],df_chg['SoC1'])
    df_chg['SoC1']=np.where((np.isclose(df_chg['OCV1'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==35) & (df_chg['Temp_flag']==35)),chg_data['chg_soc'][i],df_chg['SoC1'])
    df_chg['SoC1']=np.where((np.isclose(df_chg['OCV1'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==45) & (df_chg['Temp_flag']==45)),chg_data['chg_soc'][i],df_chg['SoC1'])

    df_chg['SoC2']=np.where((np.isclose(df_chg['OCV2'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==25) & (df_chg['Temp_flag']==25)),chg_data['chg_soc'][i],df_chg['SoC2'])
    df_chg['SoC2']=np.where((np.isclose(df_chg['OCV2'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==35) & (df_chg['Temp_flag']==35)),chg_data['chg_soc'][i],df_chg['SoC2'])
    df_chg['SoC2']=np.where((np.isclose(df_chg['OCV2'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==45) & (df_chg['Temp_flag']==45)),chg_data['chg_soc'][i],df_chg['SoC2'])
    
#%%
df_chg['del_SoC']=df_chg['SoC2']-df_chg['SoC1']
df_chg['del_SoC']=df_chg['del_SoC'].mean()
df_chg['SoH_Calculated']=(df_chg['Computed_capacity']/(del_Cap_25*df_chg['del_SoC']/100))*100 # *df_chg['del_SoC']/100

#%%
plt.figure()
plt.plot(df_chg['DateTime'],df_chg['SoH_Calculated'],label='SoH Calculated')
plt.title('SoH_calculated')
plt.ylabel('SoH')
plt.grid(linestyle='dotted')

#%%
print('----------------%s seconds----------------' %(time.time()-start))
