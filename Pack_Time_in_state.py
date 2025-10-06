# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 10:49:11 2019

@author: IITM
"""


import time
start=time.time()
import pandas as pd
import numpy as np

data = pd.read_csv("D:\\Benisha\\Code files\\charging_data_mohali_soc_calculated_6009.csv",header=0, sep=',',index_col=False,error_bad_lines=False)
df1=pd.read_csv("D:\\Benisha\\Code files\\charging_data_mohali_soc_calculated_6009_sessions_summary.csv",header=0, sep=',',index_col=False,error_bad_lines=False)
data['V_Min']=data[['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12']].min(axis=1)
data['V_Max']=data[['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12']].max(axis=1)
df=pd.DataFrame()
df1=df1.drop_duplicates('session')
print('1/4............')


#%%
data['time']=pd.to_datetime(data['time'],errors='coerce')
data['adj_soc_pred']=(data['SOC_pred']-5)/0.9
data['adj_soc_pred_s']=data['adj_soc_pred'].shift(1)
df1['Charging_Time_Min']=df1['chargingDuration']/60
for i in range(0,len(data['adj_soc_pred'])):
    if (data['adj_soc_pred'].iloc[i]>100):
        data['adj_soc_pred'].iloc[i]=100
#%%
print('2/4............')
data['adj_soc_pred'].iloc[i]=(0.8*data['adj_soc_pred'].iloc[i])+(0.2*data['adj_soc_pred_s'].iloc[i])
data = data.reset_index(drop=True)

for newcol in ['Vol_s0_mins','Vol_s1_mins','Vol_s2_mins','Vol_s3_mins','Vol_s4_mins','Vol_s5_mins','Vol_s6_mins','Vol_s7_mins','Vol_s8_mins']:
    df1[newcol]=np.nan

data['Vol_State_No']=pd.cut(x=data.V_Max,bins=[0,3,3.3,3.5,3.6,3.7,3.8,3.9,4,4.5],include_lowest=True,labels=[0,1,2,3,4,5,6,7,8]).astype(object)
k=0
print('3/4............')


#%%
grouped=data.groupby('session',sort=False)
result=[g[1]for g in list(grouped)]
for i in range(0,len(result)):
    result[i]['time_s']=result[i]['time'].shift(-1)    
    result[i]['Time_in_mins_s']=(result[i]['time_s']-result[i]['time'])/np.timedelta64(1,'m')
    result[i].loc[(result[i]['Vol_State_No']==0) , 'Vol_s0_mins'] = (result[i]['Time_in_mins_s'])
    result[i].loc[(result[i]['Vol_State_No']==1) , 'Vol_s1_mins'] = (result[i]['Time_in_mins_s'])
    result[i].loc[(result[i]['Vol_State_No']==2) , 'Vol_s2_mins'] = (result[i]['Time_in_mins_s'])
    result[i].loc[(result[i]['Vol_State_No']==3) , 'Vol_s3_mins'] = (result[i]['Time_in_mins_s'])
    result[i].loc[(result[i]['Vol_State_No']==4) , 'Vol_s4_mins'] = (result[i]['Time_in_mins_s'])
    result[i].loc[(result[i]['Vol_State_No']==5) , 'Vol_s5_mins'] = (result[i]['Time_in_mins_s'])
    result[i].loc[(result[i]['Vol_State_No']==6) , 'Vol_s6_mins'] = (result[i]['Time_in_mins_s'])
    result[i].loc[(result[i]['Vol_State_No']==7) , 'Vol_s7_mins'] = (result[i]['Time_in_mins_s'])
    result[i].loc[(result[i]['Vol_State_No']==8) , 'Vol_s8_mins'] = (result[i]['Time_in_mins_s'])
    result[i]['Vol_s0_mins'] = result[i]['Vol_s0_mins'].sum()
    result[i]['Vol_s1_mins'] = result[i]['Vol_s1_mins'].sum()
    result[i]['Vol_s2_mins'] = result[i]['Vol_s2_mins'].sum()
    result[i]['Vol_s3_mins'] = result[i]['Vol_s3_mins'].sum()
    result[i]['Vol_s4_mins'] = result[i]['Vol_s4_mins'].sum()
    result[i]['Vol_s5_mins'] = result[i]['Vol_s5_mins'].sum()
    result[i]['Vol_s6_mins'] = result[i]['Vol_s6_mins'].sum()
    result[i]['Vol_s7_mins'] = result[i]['Vol_s7_mins'].sum()
    result[i]['Vol_s8_mins'] = result[i]['Vol_s8_mins'].sum()
   
    if(df1['session'].iloc[k]==result[i]['session'].iloc[-1]):
        df1['Vol_s0_mins'].iloc[k]  = result[i]['Vol_s0_mins'].iloc[-1]
        df1['Vol_s1_mins'].iloc[k]  = result[i]['Vol_s1_mins'].iloc[-1]
        df1['Vol_s2_mins'].iloc[k]  = result[i]['Vol_s2_mins'].iloc[-1]
        df1['Vol_s3_mins'].iloc[k]  = result[i]['Vol_s3_mins'].iloc[-1]
        df1['Vol_s4_mins'].iloc[k]  = result[i]['Vol_s4_mins'].iloc[-1]
        df1['Vol_s5_mins'].iloc[k]  = result[i]['Vol_s5_mins'].iloc[-1]
        df1['Vol_s6_mins'].iloc[k]  = result[i]['Vol_s6_mins'].iloc[-1]
        df1['Vol_s7_mins'].iloc[k]  = result[i]['Vol_s7_mins'].iloc[-1]
        df1['Vol_s8_mins'].iloc[k]  = result[i]['Vol_s8_mins'].iloc[-1]    
        k=k+1
    
    df=pd.concat([df,result[i]])
    
print('4/4............')


#%%


df= df.drop(['time_s','Vol_State_No'], axis=1)
df.to_csv('Battery_pack_mohali_Charging_Data_timestates_6009.csv')
df1.to_csv('Battery_Pack_mohali_Charging_Date_timestates_6009_sessionSummary.csv')
print('----------%s seconds-----------' % (time.time()-start))
        
        