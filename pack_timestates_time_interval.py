# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 13:24:30 2019

@author: IITM
"""
"""
from pack_timestates_test.py; to modify the timestamp column
"""

import time
start=time.time()
import pandas as pd
import numpy as np

data = pd.read_csv("D:\\Benisha\\Battery DCA\\Data_Files\\2019_M6_Jun_MOH_charging_temperature_voltage_sorted.csv",header=0, sep=',',index_col=False,error_bad_lines=False)
data['V_Min']=data[['CV1','CV2','CV3','CV4','CV5','CV6','CV7','CV8','CV9','CV10','CV11','CV12']].min(axis=1)
data['V_Max']=data[['CV1','CV2','CV3','CV4','CV5','CV6','CV7','CV8','CV9','CV10','CV11','CV12']].max(axis=1)
df1=pd.DataFrame()
df=pd.DataFrame()

print('1/4............')


#%%

data['time']=pd.to_datetime(data['time'],format= "%d/%m/%Y %H:%M:%S")
data=data.sort_values(by='time',ascending=True)
df1['time']=data['time']
#data['adj_soc_pred']=(data['SOC_pred']-5)/0.9
#data['adj_soc_pred_s']=data['adj_soc_pred'].shift(1)
#
#for i in range(0,len(data['adj_soc_pred'])):
#    if (data['adj_soc_pred'].iloc[i]>100):
#        data['adj_soc_pred'].iloc[i]=100
data=data.reset_index(drop=True)
print('2/4............')
#%%
#data=data.sort_values(data['time'],ascending=True)
#data['adj_soc_pred'].iloc[i]=(0.8*data['adj_soc_pred'].iloc[i])+(0.2*data['adj_soc_pred_s'].iloc[i])
data = data.reset_index(drop=True)
for newcol1 in ['session','bin','bmake','vin','vmake','regno','record','start_Time','end_Time','start_V_Min','end_V_Min','start_V_Max','end_V_Max','start_SOC_pred','end_SOC_pred']:
    df1[newcol1]=np.nan
for newcol in ['Vol_s0_mins','Vol_s1_mins','Vol_s2_mins','Vol_s3_mins','Vol_s4_mins','Vol_s5_mins','Vol_s6_mins','Vol_s7_mins','Vol_s8_mins']:
    data[newcol]=np.nan
    df1[newcol]=np.nan
data['time_s']=data['time'].shift(-1)    
data['Time_in_mins_s']=(data['time_s']-data['time'])/np.timedelta64(1,'m')
data['Vol_State_No']=pd.cut(x=data.V_Max,bins=[0,3,3.3,3.5,3.6,3.7,3.8,3.9,4,4.5],include_lowest=True,labels=[0,1,2,3,4,5,6,7,8]).astype(object) #Chg-V_Max; DChg-V_Min
data['Vol_State_No']=data['Vol_State_No'].astype(float)
data['Time_in_mins_s']=data['Time_in_mins_s'].astype(float)
k=0
print('3/4............')


#%%
#data['session_s']=data['session'].shift()
#data['Num_check']=(data['session']!=data['session_s']).cumsum()
#print(data['Num_check'])

data.loc[(data['Vol_State_No']==0) , 'Vol_s0_mins'] = (data['Time_in_mins_s'])
data.loc[(data['Vol_State_No']==1) , 'Vol_s1_mins'] = (data['Time_in_mins_s'])
data.loc[(data['Vol_State_No']==2) , 'Vol_s2_mins'] = (data['Time_in_mins_s'])
data.loc[(data['Vol_State_No']==3) , 'Vol_s3_mins'] = (data['Time_in_mins_s'])
data.loc[(data['Vol_State_No']==4) , 'Vol_s4_mins'] = (data['Time_in_mins_s'])
data.loc[(data['Vol_State_No']==5) , 'Vol_s5_mins'] = (data['Time_in_mins_s'])
data.loc[(data['Vol_State_No']==6) , 'Vol_s6_mins'] = (data['Time_in_mins_s'])
data.loc[(data['Vol_State_No']==7) , 'Vol_s7_mins'] = (data['Time_in_mins_s'])
data.loc[(data['Vol_State_No']==8) , 'Vol_s8_mins'] = (data['Time_in_mins_s'])

data.loc[(data['Vol_s0_mins']>10) , 'Vol_s0_mins'] = 0
data.loc[(data['Vol_s1_mins']>10) , 'Vol_s1_mins'] = 0
data.loc[(data['Vol_s2_mins']>10) , 'Vol_s2_mins'] = 0
data.loc[(data['Vol_s3_mins']>10) , 'Vol_s3_mins'] = 0
data.loc[(data['Vol_s4_mins']>10) , 'Vol_s4_mins'] = 0
data.loc[(data['Vol_s5_mins']>10) , 'Vol_s5_mins'] = 0
data.loc[(data['Vol_s6_mins']>10) , 'Vol_s6_mins'] = 0
data.loc[(data['Vol_s7_mins']>10) , 'Vol_s7_mins'] = 0
data.loc[(data['Vol_s8_mins']>10) , 'Vol_s8_mins'] = 0


print('3.5/4............')


grouped=data.groupby('session',sort=False)
result=[g[1]for g in list(grouped)]
for i in range(0,len(result)):


    result[i]['Vol_s0_mins'] = result[i]['Vol_s0_mins'].sum()
    result[i]['Vol_s1_mins'] = result[i]['Vol_s1_mins'].sum()
    result[i]['Vol_s2_mins'] = result[i]['Vol_s2_mins'].sum()
    result[i]['Vol_s3_mins'] = result[i]['Vol_s3_mins'].sum()
    result[i]['Vol_s4_mins'] = result[i]['Vol_s4_mins'].sum()
    result[i]['Vol_s5_mins'] = result[i]['Vol_s5_mins'].sum()
    result[i]['Vol_s6_mins'] = result[i]['Vol_s6_mins'].sum()
    result[i]['Vol_s7_mins'] = result[i]['Vol_s7_mins'].sum()
    result[i]['Vol_s8_mins'] = result[i]['Vol_s8_mins'].sum()
   

    df1['Vol_s0_mins'].iloc[k]  = result[i]['Vol_s0_mins'].iloc[-1]
    df1['Vol_s1_mins'].iloc[k]  = result[i]['Vol_s1_mins'].iloc[-1]
    df1['Vol_s2_mins'].iloc[k]  = result[i]['Vol_s2_mins'].iloc[-1]
    df1['Vol_s3_mins'].iloc[k]  = result[i]['Vol_s3_mins'].iloc[-1]
    df1['Vol_s4_mins'].iloc[k]  = result[i]['Vol_s4_mins'].iloc[-1]
    df1['Vol_s5_mins'].iloc[k]  = result[i]['Vol_s5_mins'].iloc[-1]
    df1['Vol_s6_mins'].iloc[k]  = result[i]['Vol_s6_mins'].iloc[-1]
    df1['Vol_s7_mins'].iloc[k]  = result[i]['Vol_s7_mins'].iloc[-1]
    df1['Vol_s8_mins'].iloc[k]  = result[i]['Vol_s8_mins'].iloc[-1] 
    
    df1['session'].iloc[k]=result[i]['session'].iloc[-1]
    df1['bin'].iloc[k]=result[i]['bin'].iloc[-1]
    df1['vin'].iloc[k]=result[i]['vin'].iloc[-1]
    df1['bmake'].iloc[k]=result[i]['bmake'].iloc[-1]
    
    df1['regno'].iloc[k]=result[i]['regno'].iloc[-1]
    df1['record'].iloc[k]=result[i]['bin'].iloc[-1]
    
    df1['start_Time'].iloc[k]=result[i]['time'].iloc[0]
    df1['end_Time'].iloc[k]=result[i]['time'].iloc[-1]
    
    df1['start_V_Min'].iloc[k]=result[i]['V_Min'].iloc[0]
    df1['end_V_Min'].iloc[k]=result[i]['V_Min'].iloc[-1]
    df1['start_V_Max'].iloc[k]=result[i]['V_Max'].iloc[0]
    df1['end_V_Max'].iloc[k]=result[i]['V_Max'].iloc[-1]

    
    k=k+1
    
    df=pd.concat([df,result[i]])
    
print('4/4............')


#%%
df=df.reset_index(drop=True)
df1=df1.reset_index(drop=True)
df1=df1.drop(['time'],axis=1)
df1=df1.dropna(subset=['session'])
df= df.drop(['time_s'], axis=1)
df.to_csv('Battery_pack_mohali_Charging_Data_M6_Jun_timestates.csv')
df1.to_csv('Battery_Pack_mohali_Charging_Data_M6_Jun_timestates_sessionSummary.csv')
print('----------%s seconds-----------' % (time.time()-start))
        
        