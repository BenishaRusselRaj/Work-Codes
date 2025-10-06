# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 12:17:02 2019

@author: IITM
"""
import time
t1=time.time()
import pandas as pd
import math
import numpy as np


df=pd.read_csv("D:\\Benisha\\Battery DCA\\Battery_data_for_analysis\\charging_data_mohali_INEXC0010202J2406009_new.tsv",header=0, sep='\t',index_col=False,error_bad_lines=False)
data=pd.read_csv("D:\\Benisha\\Battery DCA\\Battery_data_for_analysis\\charging_data_mohali_INEXC0010202J2406009_sessions.tsv",header=0, sep='\t',index_col=False,error_bad_lines=False)
df['C_Min']=df[['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12']].min(axis=1)


OCV =[3.305,3.487,3.528,3.571,3.617,3.670,3.740,3.796,3.832,3.858,3.881,3.904,3.932,3.976,4.016,4.042,4.057,4.081,4.121,4.200]
Gain_soc_frm_vtg = [8.263,27.513,120.77,116.66,109.99,93.249,71.963,88.183,140.25,190.91,215.61,219.59,180.64,114.13,125.06,189.75,325.1,214.87,123.27,63.187]
Offset_soc_frm_vtg = [-22.309, -85.933, -411.11, -396.59,-372.77,-312.23,-234.11,-294.77,-492.44, -686.57, -781.85, -797.29,-645.22, -383.73, -427.2, -686.97,-1234, -786.79, -413.03, -165.4]

for newcol in ['start_SOC','end_SOC','start_V_min','end_V_min','ocv_strt_init','ocv_end_init','soc_strt_init','soc_end_init','R_pred_start','R_pred_end','start_OCV','end_OCV']:
    data[newcol]=''
df1=pd.DataFrame()


#%%
grouped=df.groupby('session', sort=False)
result = [g[1] for g in list(grouped)]
k=0
start_SOC,soc1,R_pred_start,start_OCV,end_SOC,start_OCV,end_OCV,soc2,R_pred_end,end_OCV=np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan



#%%
for i in range (0,len(result)):
   
    result[i][['C_Min','current']]=result[i][['C_Min','current']].astype(float)
    result[i]['R']=result[i]['C_Min']/result[i]['current']
    ocv1=(result[i]['C_Min'].iloc[0])-(result[i]['current'].iloc[0]*0.003)
    
    data['ocv_strt_init'].iloc[k]=ocv1
    data['start_V_min'].iloc[k]=result[i]['C_Min'].iloc[0]
    data['end_V_min'].iloc[k]=result[i]['C_Min'].iloc[-1]
    
    for j in range(1,20):
        if((ocv1>=OCV[j-1]) and (ocv1<OCV[j])):
            soc1=Gain_soc_frm_vtg[j-1]*ocv1 + Offset_soc_frm_vtg[j-1]
            R_pred_start=((-0.538*math.log10(soc1))+11.586)/1000
            start_OCV=(result[i]['C_Min'].iloc[0])-(result[i]['current'].iloc[0]*R_pred_start)
            break
   
    data['soc_strt_init'].iloc[k]=soc1
    data['R_pred_start'].iloc[k]=R_pred_start
    data['start_OCV'].iloc[k]=start_OCV
    
    for j in range(1,20):
        if((start_OCV!=np.nan) and (start_OCV>=OCV[j]) and (start_OCV<OCV[j+1])):
            start_SOC=Gain_soc_frm_vtg[j-1]*start_OCV + Offset_soc_frm_vtg[j-1]  
    
    ocv2=(result[i]['C_Min'].iloc[-1])-(result[i]['current'].iloc[-1]*0.003)
    data['ocv_end_init'].iloc[k]=ocv2
   
    for j in range(1,20):
        if((ocv2>=OCV[j-1]) and (ocv2<OCV[j])):
            soc2=Gain_soc_frm_vtg[j-1]*ocv2 + Offset_soc_frm_vtg[j-1]
            R_pred_end=((-0.538*math.log10(soc2))+11.586)/1000
            end_OCV=(result[i]['C_Min'].iloc[-1])-(result[i]['current'].iloc[-1]*R_pred_end)
            break
   
    data['soc_end_init'].iloc[k]=soc2
    data['R_pred_end'].iloc[k]=R_pred_end
    data['end_OCV'].iloc[k]=end_OCV
    
    for j in range(1,20):
        if((end_OCV!=np.nan) and (end_OCV>=OCV[j-1]) and (end_OCV<OCV[j])):
            end_SOC=Gain_soc_frm_vtg[j-1]*end_OCV + Offset_soc_frm_vtg[j-1]      
    
    
    result[i]['start_SOC']=start_SOC
    result[i]['end_SOC']=end_SOC
    
    data['start_SOC'].iloc[k]=start_SOC
    data['end_SOC'].iloc[k]=end_SOC
    k=k+1
    
    start_SOC,soc1,R_pred_start,start_OCV,end_SOC,start_OCV,end_OCV,soc2,R_pred_end,end_OCV=np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan
    df1=pd.concat([df1,result[i]])
    
    
#%%

df1[['current','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12']]=df1[['current','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12']].astype(float)
df1.to_csv('charging_data_mohali_soc_calculated_6009.csv')
data.to_csv('charging_data_mohali_soc_calculated_6009_sessions_summary.csv')

print('---------%s seconds--------' % (time.time()-t1))