# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 13:56:12 2019

@author: IITM
"""
"""
Battery pack data soc estimation; general one; creates session summary from entire dataframe
"""
import time
t1=time.time()
import pandas as pd
import math
import numpy as np


df=pd.read_csv("D:\\Benisha\\Battery DCA\\Data_Files\\2019_M6_Jun_driving_temperature_voltage_sorted.csv",header=0, sep=',',index_col=False,error_bad_lines=False)

df['V_Min']=df[['CV1','CV2','CV3','CV4','CV5','CV6','CV7','CV8','CV9','CV10','CV11','CV12']].min(axis=1)
df['V_Max']=df[['CV1','CV2','CV3','CV4','CV5','CV6','CV7','CV8','CV9','CV10','CV11','CV12']].max(axis=1)
data=pd.DataFrame()
data['time']=df['time']

OCV =[3.305,3.487,3.528,3.571,3.617,3.670,3.740,3.796,3.832,3.858,3.881,3.904,3.932,3.976,4.016,4.042,4.057,4.081,4.121,4.200]
Gain_soc_frm_vtg = [8.263,27.513,120.77,116.66,109.99,93.249,71.963,88.183,140.25,190.91,215.61,219.59,180.64,114.13,125.06,189.75,325.1,214.87,123.27,63.187]
Offset_soc_frm_vtg = [-22.309, -85.933, -411.11, -396.59,-372.77,-312.23,-234.11,-294.77,-492.44, -686.57, -781.85, -797.29,-645.22, -383.73, -427.2, -686.97,-1234, -786.79, -413.03, -165.4]

for newcol in ['ocv_init','soc_init','R_pred_start','OCV','SOC_pred']:
    df[newcol]=np.nan
    
#for newcol in ['session','bin','vin','start_Time','end_Time','start_V_Min','end_V_Min','start_V_Max','end_V_Max','start_SOC_pred','end_SOC_pred']:
#    data[newcol]=np.nan
for newcol in ['session','bin','bmake','vin','vmake','regno','record','start_Time','end_Time','start_V_Min','end_V_Min','start_V_Max','end_V_Max','start_current','end_current','start_SOC_pred','end_SOC_pred']:
    data[newcol]=np.nan
df1=pd.DataFrame()


#%%
grouped=df.groupby('session', sort=False)
result = [g[1] for g in list(grouped)]
s=0                              


#%%
for i in range (0,len(result)):
   
    result[i][['V_Min','current']]=result[i][['V_Min','current']].astype(float)
    result[i]['R']=result[i]['V_Min']/result[i]['current']
    result[i]['ocv_init']=(result[i]['V_Min'])-(result[i]['current']*0.003)
    
    for k in range(0,len(result[i])):
        for j in range(1,20):
            if((result[i]['ocv_init'].iloc[k]>=OCV[j-1]) and (result[i]['ocv_init'].iloc[k]<OCV[j])):
                result[i]['soc_init'].iloc[k]=Gain_soc_frm_vtg[j-1]*result[i]['ocv_init'].iloc[k] + Offset_soc_frm_vtg[j-1]
                result[i]['R_pred_start'].iloc[k]=((-0.538*math.log10(result[i]['soc_init'].iloc[k]))+11.586)/1000
                result[i]['OCV'].iloc[k]=(result[i]['V_Min'].iloc[k])-(result[i]['current'].iloc[k]*(result[i]['R_pred_start'].iloc[k])/2)
                
    for k in range(0,len(result[i])):
        for j in range(1,20):
            if((result[i]['OCV'].iloc[k]!=np.nan) and (result[i]['OCV'].iloc[k]>=OCV[j-1]) and (result[i]['OCV'].iloc[k]<OCV[j])):
                result[i]['SOC_pred'].iloc[k]=Gain_soc_frm_vtg[j-1]*result[i]['OCV'].iloc[k] + Offset_soc_frm_vtg[j-1]  
    
    data['session'].iloc[s]=result[i]['session'].iloc[-1]
    data['bin'].iloc[s]=result[i]['bin'].iloc[-1]
    data['vin'].iloc[s]=result[i]['vin'].iloc[-1]
    data['bmake'].iloc[s]=result[i]['bmake'].iloc[-1]
    
    data['regno'].iloc[s]=result[i]['regno'].iloc[-1]
    data['record'].iloc[s]=result[i]['bin'].iloc[-1]
    data['start_current'].iloc[s]=result[i]['current'].iloc[0]
    data['end_current'].iloc[s]=result[i]['current'].iloc[-1]
    
    data['start_Time'].iloc[s]=result[i]['time'].iloc[0]
    data['end_Time'].iloc[s]=result[i]['time'].iloc[-1]
    
    data['start_SOC_pred'].iloc[s]=result[i]['SOC_pred'].iloc[0]
    data['end_SOC_pred'].iloc[s]=result[i]['SOC_pred'].iloc[-1]
    data['start_V_Min'].iloc[s]=result[i]['V_Min'].iloc[0]
    data['end_V_Min'].iloc[s]=result[i]['V_Min'].iloc[-1]
    data['start_V_Max'].iloc[s]=result[i]['V_Max'].iloc[0]
    data['end_V_Max'].iloc[s]=result[i]['V_Max'].iloc[-1]
    s=s+1
    df1=pd.concat([df1,result[i]])
    
    
#%%

df1[['current','CV1','CV2','CV3','CV4','CV5','CV6','CV7','CV8','CV9','CV10','CV11','CV12']]=df1[['current','CV1','CV2','CV3','CV4','CV5','CV6','CV7','CV8','CV9','CV10','CV11','CV12']].astype(float)
df1.to_csv('charging_data_mohali_soc_calculated_M6_Jun.csv')
data.to_csv('charging_data_mohali_soc_calculated_M6_Jun_sessions_summary.csv')

print('---------%s seconds--------' % (time.time()-t1))
        
        