# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 09:30:26 2019

@author: IITM
"""
"""
after the session summary was created; dchg data did not have volt values at top and bottom, so took the first and last valid data respectively
"""

import time
start=time.time()
import pandas as pd
import numpy as np
df=pd.read_csv("D:\\Benisha\\Code files\\Battery_Pack_mohali_Driving_Data_M6_Jun_timestates_sessionSummary.csv",header=0,sep=',',low_memory=False)
df1=pd.read_csv("D:\\Benisha\\Code files\\Battery_pack_mohali_Driving_Data_M6_Jun_timestates.csv",header=0,sep=',',low_memory=False)
grouped=df1.groupby('session',sort=False)
k=0
df['Remark']=None
print('1/3.............')
result=[g[1] for g in list(grouped)]
for i in range (0,len(result)):
    try:
        df['session'].iloc[k]=result[i]['session'].iloc[-1]
        df['bin'].iloc[k]=result[i]['bin'].iloc[-1]
        df['vin'].iloc[k]=result[i]['vin'].iloc[-1]
        df['bmake'].iloc[k]=result[i]['bmake'].iloc[-1]
        
        df['regno'].iloc[k]=result[i]['regno'].iloc[-1]
        df['record'].iloc[k]=result[i]['bin'].iloc[-1]
        try:
            df['start_V_Min'].iloc[k]=pd.to_numeric(result[i]['V_Min'].loc[0])
            df['end_V_Min'].iloc[k]=pd.to_numeric(result[i]['V_Min'].loc[-1])
            df['start_V_Max'].iloc[k]=pd.to_numeric(result[i]['V_Max'].loc[0])
            df['end_V_Max'].iloc[k]=pd.to_numeric(result[i]['V_Max'].loc[-1])
            df['start_SOC_pred'].iloc[k]=pd.to_numeric(result[i]['SOC_pred'].loc[0])
            df['end_SOC_pred'].iloc[k]=pd.to_numeric(result[i]['SOC_pred'].loc[-1])
        except KeyError:
            df['Remark'].iloc[k]='First and last values were NAN;Taken the first valid data for summary'
            df['start_V_Min'].iloc[k]=result[i]['V_Min'].loc[result[i]['V_Min'].first_valid_index()]
            df['end_V_Min'].iloc[k]=result[i]['V_Min'].loc[result[i]['V_Min'].last_valid_index()]
            df['start_V_Max'].iloc[k]=result[i]['V_Max'].loc[result[i]['V_Max'].first_valid_index()]
            df['end_V_Max'].iloc[k]=result[i]['V_Max'].loc[result[i]['V_Max'].last_valid_index()]
            df['start_SOC_pred'].iloc[k]=result[i]['SOC_pred'].loc[result[i]['SOC_pred'].first_valid_index()]
            df['end_SOC_pred'].iloc[k]=result[i]['SOC_pred'].loc[result[i]['SOC_pred'].last_valid_index()]
    except KeyError:
        df['session'].iloc[k]=result[i]['session'].iloc[-1]
        df['bin'].iloc[k]=result[i]['bin'].iloc[-1]
        df['vin'].iloc[k]=result[i]['vin'].iloc[-1]
        df['bmake'].iloc[k]=result[i]['bmake'].iloc[-1]
        
        df['regno'].iloc[k]=result[i]['regno'].iloc[-1]
        df['record'].iloc[k]=result[i]['bin'].iloc[-1]
        
        df['start_V_Min'].iloc[k]=np.nan
        df['end_V_Min'].iloc[k]=np.nan
        df['start_V_Max'].iloc[k]=np.nan
        df['end_V_Max'].iloc[k]=np.nan
        df['start_SOC_pred'].iloc[k]=np.nan
        df['end_SOC_pred'].iloc[k]=np.nan
    k=k+1
print('2/3.............')
df.reset_index(drop=True)
df=df.drop(labels=['Unnamed: 0.1','start_current','end_current'],axis=1)
df.to_csv('Battery_Pack_mohali_Driving_Data_M6_Jun_timestates_sessionSummary_Modified_Vs.csv')
print('3/3.............')
print('---------%s seconds-----------' % (start-time.time()))