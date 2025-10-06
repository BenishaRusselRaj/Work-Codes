# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 15:13:05 2019

@author: IITM
"""

import time
t1=time.time()
import pandas as pd
import math
import numpy as np


df=pd.read_csv("D:\\Benisha\\Battery DCA\\Battery_data_for_analysis\\charging_data_mohali_INEXC0010202K2303809_new.tsv",header=0, sep='\t',index_col=False,error_bad_lines=False)
data=pd.read_csv("D:\\Benisha\\Battery DCA\\Battery_data_for_analysis\\charging_data_mohali_INEXC0010202K2303809_sessions.tsv",header=0, sep='\t',index_col=False,error_bad_lines=False)
df['V_Min']=df[['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12']].min(axis=1)


OCV =[3.305,3.487,3.528,3.571,3.617,3.670,3.740,3.796,3.832,3.858,3.881,3.904,3.932,3.976,4.016,4.042,4.057,4.081,4.121,4.200]
Gain_soc_frm_vtg = [8.263,27.513,120.77,116.66,109.99,93.249,71.963,88.183,140.25,190.91,215.61,219.59,180.64,114.13,125.06,189.75,325.1,214.87,123.27,63.187]
Offset_soc_frm_vtg = [-22.309, -85.933, -411.11, -396.59,-372.77,-312.23,-234.11,-294.77,-492.44, -686.57, -781.85, -797.29,-645.22, -383.73, -427.2, -686.97,-1234, -786.79, -413.03, -165.4]

for newcol in ['ocv_init','soc_init','R_pred_start','OCV','SOC_pred']:
    df[newcol]=np.nan
df1=pd.DataFrame()

for newcol in ['start_SOC_pred','end_SOC_pred','start_V_min','end_V_min']:
    data[newcol]=np.nan


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
    
    data['start_SOC_pred'].iloc[s]=result[i]['SOC_pred'].iloc[0]
    data['end_SOC_pred'].iloc[s]=result[i]['SOC_pred'].iloc[-1]
    data['start_V_min'].iloc[s]=result[i]['V_Min'].iloc[0]
    data['end_V_min'].iloc[s]=result[i]['V_Min'].iloc[-1]
    s=s+1
    df1=pd.concat([df1,result[i]])
    
    
#%%

df1[['current','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12']]=df1[['current','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12']].astype(float)
df1.to_csv('charging_data_mohali_soc_calculated_3809.csv')
data.to_csv('charging_data_mohali_soc_calculated_3809_sessions_summary.csv')

print('---------%s seconds--------' % (time.time()-t1))