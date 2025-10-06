# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 09:45:36 2019

@author: IITM
"""

import time
start=time.time()
import pickle
import pandas as pd
import numpy as np
with open("D:\\New folder (2)\\PHY\\PHY_21.1_25Deg_AllCycles_AllCycles_raw.pkl",'rb') as f:
    data = pickle.load(f)
    data['New_Cycle_No']=data['New_Cycle_No'].astype(object)
    data=data[data.New_Cycle_No<=897]
    print('1/4............')
    
    
#%%
    data=data.sort_values('RTC',ascending=True)
    data['Year']=data.RTC.map(lambda x: x.year)
    data=data.loc[(data.Year>=2017) & (data.Year<=2019)]
    data['RTC_s']=data['RTC'].shift(-1)
    
    
    data['Time_in_Sec_s']=data['RTC_s']-data['RTC']
    data['Time_in_Sec_s']=data['Time_in_Sec_s']/np.timedelta64(1,'s')
    data = data.reset_index(drop=True)
    print('1.5/4............')
    
    
#%%
    data['Time_in_Sec']=data.RTC-data.RTC.loc[data.index[0]]
    data['Time_in_Sec']=data['Time_in_Sec']/np.timedelta64(1,'s')
    data['Vol_State_No']=pd.cut(x=data.Voltage,bins=[0,3,3.3,3.5,3.6,3.7,3.8,3.9,4,5],include_lowest=True,labels=[0,1,2,3,4,5,6,7,8]).astype(object)
    data['Temp_State_No']=pd.cut(x=data.T_amb,bins=[25,30,35,40,45,60],include_lowest=True,labels=[1,2,3,4,5]).astype(object)
    print('2/4............')
    
    
#%%
    data.loc[(data['Vol_State_No']==0) & (data['Current']>0), 'Vol_s0_Chg'] = (data['Time_in_Sec_s']);data['Vol_s0_Chg'] = data['Vol_s0_Chg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==1) & (data['Current']>0), 'Vol_s1_Chg'] = (data['Time_in_Sec_s']);data['Vol_s1_Chg'] = data['Vol_s1_Chg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==2) & (data['Current']>0), 'Vol_s2_Chg'] = (data['Time_in_Sec_s']);data['Vol_s2_Chg'] = data['Vol_s2_Chg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==3) & (data['Current']>0), 'Vol_s3_Chg'] = (data['Time_in_Sec_s']);data['Vol_s3_Chg'] = data['Vol_s3_Chg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==4) & (data['Current']>0), 'Vol_s4_Chg'] = (data['Time_in_Sec_s']);data['Vol_s4_Chg'] = data['Vol_s4_Chg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==5) & (data['Current']>0), 'Vol_s5_Chg'] = (data['Time_in_Sec_s']);data['Vol_s5_Chg'] = data['Vol_s5_Chg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==6) & (data['Current']>0), 'Vol_s6_Chg'] = (data['Time_in_Sec_s']);data['Vol_s6_Chg'] = data['Vol_s6_Chg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==7) & (data['Current']>0), 'Vol_s7_Chg'] = (data['Time_in_Sec_s']);data['Vol_s7_Chg'] = data['Vol_s7_Chg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==8) & (data['Current']>0), 'Vol_s8_Chg'] = (data['Time_in_Sec_s']);data['Vol_s8_Chg'] = data['Vol_s8_Chg'].replace(np.NaN,0)
    
    
    data.loc[(data['Temp_State_No']==1) & (data['Current']>0), 'Temp_s1_Chg'] = (data['Time_in_Sec_s']);data['Temp_s1_Chg'] = data['Temp_s1_Chg'].replace(np.NaN,0)
    data.loc[(data['Temp_State_No']==2) & (data['Current']>0), 'Temp_s2_Chg'] = (data['Time_in_Sec_s']);data['Temp_s2_Chg'] = data['Temp_s2_Chg'].replace(np.NaN,0)
    data.loc[(data['Temp_State_No']==3) & (data['Current']>0), 'Temp_s3_Chg'] = (data['Time_in_Sec_s']);data['Temp_s3_Chg'] = data['Temp_s3_Chg'].replace(np.NaN,0)
    data.loc[(data['Temp_State_No']==4) & (data['Current']>0), 'Temp_s4_Chg'] = (data['Time_in_Sec_s']);data['Temp_s4_Chg'] = data['Temp_s4_Chg'].replace(np.NaN,0)
    data.loc[(data['Temp_State_No']==5) & (data['Current']>0), 'Temp_s5_Chg'] = (data['Time_in_Sec_s']);data['Temp_s5_Chg'] = data['Temp_s5_Chg'].replace(np.NaN,0)
    print('3/4............')
    
    
#%%
    data.loc[(data['Vol_State_No']==0) & (data['Current']==0), 'Vol_s0_Rst'] = (data['Time_in_Sec_s']);data['Vol_s0_Rst'] = data['Vol_s0_Rst'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==1) & (data['Current']==0), 'Vol_s1_Rst'] = (data['Time_in_Sec_s']);data['Vol_s1_Rst'] = data['Vol_s1_Rst'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==2) & (data['Current']==0), 'Vol_s2_Rst'] = (data['Time_in_Sec_s']);data['Vol_s2_Rst'] = data['Vol_s2_Rst'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==3) & (data['Current']==0), 'Vol_s3_Rst'] = (data['Time_in_Sec_s']);data['Vol_s3_Rst'] = data['Vol_s3_Rst'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==4) & (data['Current']==0), 'Vol_s4_Rst'] = (data['Time_in_Sec_s']);data['Vol_s4_Rst'] = data['Vol_s4_Rst'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==5) & (data['Current']==0), 'Vol_s5_Rst'] = (data['Time_in_Sec_s']);data['Vol_s5_Rst'] = data['Vol_s5_Rst'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==6) & (data['Current']==0), 'Vol_s6_Rst'] = (data['Time_in_Sec_s']);data['Vol_s6_Rst'] = data['Vol_s6_Rst'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==7) & (data['Current']==0), 'Vol_s7_Rst'] = (data['Time_in_Sec_s']);data['Vol_s7_Rst'] = data['Vol_s7_Rst'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==8) & (data['Current']==0), 'Vol_s8_Rst'] = (data['Time_in_Sec_s']);data['Vol_s8_Rst'] = data['Vol_s8_Rst'].replace(np.NaN,0)
   
    
    data.loc[(data['Temp_State_No']==1) & (data['Current']==0), 'Temp_s1_Rst'] = (data['Time_in_Sec_s']);data['Temp_s1_Rst'] = data['Temp_s1_Rst'].replace(np.NaN,0)
    data.loc[(data['Temp_State_No']==2) & (data['Current']==0), 'Temp_s2_Rst'] = (data['Time_in_Sec_s']);data['Temp_s2_Rst'] = data['Temp_s2_Rst'].replace(np.NaN,0)
    data.loc[(data['Temp_State_No']==3) & (data['Current']==0), 'Temp_s3_Rst'] = (data['Time_in_Sec_s']);data['Temp_s3_Rst'] = data['Temp_s3_Rst'].replace(np.NaN,0)
    data.loc[(data['Temp_State_No']==4) & (data['Current']==0), 'Temp_s4_Rst'] = (data['Time_in_Sec_s']);data['Temp_s4_Rst'] = data['Temp_s4_Rst'].replace(np.NaN,0)
    data.loc[(data['Temp_State_No']==5) & (data['Current']==0), 'Temp_s5_Rst'] = (data['Time_in_Sec_s']);data['Temp_s5_Rst'] = data['Temp_s5_Rst'].replace(np.NaN,0)
    print('3.5/4............')
    
    
#%%
    data.loc[(data['Vol_State_No']==0) & (data['Current']<0), 'Vol_s0_DChg'] = (data['Time_in_Sec_s']);data['Vol_s0_DChg'] = data['Vol_s0_DChg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==1) & (data['Current']<0), 'Vol_s1_DChg'] = (data['Time_in_Sec_s']);data['Vol_s1_DChg'] = data['Vol_s1_DChg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==2) & (data['Current']<0), 'Vol_s2_DChg'] = (data['Time_in_Sec_s']);data['Vol_s2_DChg'] = data['Vol_s2_DChg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==3) & (data['Current']<0), 'Vol_s3_DChg'] = (data['Time_in_Sec_s']);data['Vol_s3_DChg'] = data['Vol_s3_DChg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==4) & (data['Current']<0), 'Vol_s4_DChg'] = (data['Time_in_Sec_s']);data['Vol_s4_DChg'] = data['Vol_s4_DChg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==5) & (data['Current']<0), 'Vol_s5_DChg'] = (data['Time_in_Sec_s']);data['Vol_s5_DChg'] = data['Vol_s5_DChg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==6) & (data['Current']<0), 'Vol_s6_DChg'] = (data['Time_in_Sec_s']);data['Vol_s6_DChg'] = data['Vol_s6_DChg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==7) & (data['Current']<0), 'Vol_s7_DChg'] = (data['Time_in_Sec_s']);data['Vol_s7_DChg'] = data['Vol_s7_DChg'].replace(np.NaN,0)
    data.loc[(data['Vol_State_No']==8) & (data['Current']<0), 'Vol_s8_DChg'] = (data['Time_in_Sec_s']);data['Vol_s8_DChg'] = data['Vol_s8_DChg'].replace(np.NaN,0)
    
    
    data.loc[(data['Temp_State_No']==1) & (data['Current']<0), 'Temp_s1_DChg'] = (data['Time_in_Sec_s']);data['Temp_s1_DChg'] = data['Temp_s1_DChg'].replace(np.NaN,0)
    data.loc[(data['Temp_State_No']==2) & (data['Current']<0), 'Temp_s2_DChg'] = (data['Time_in_Sec_s']);data['Temp_s2_DChg'] = data['Temp_s2_DChg'].replace(np.NaN,0)
    data.loc[(data['Temp_State_No']==3) & (data['Current']<0), 'Temp_s3_DChg'] = (data['Time_in_Sec_s']);data['Temp_s3_DChg'] = data['Temp_s3_DChg'].replace(np.NaN,0)
    data.loc[(data['Temp_State_No']==4) & (data['Current']<0), 'Temp_s4_DChg'] = (data['Time_in_Sec_s']);data['Temp_s4_DChg'] = data['Temp_s4_DChg'].replace(np.NaN,0)
    data.loc[(data['Temp_State_No']==5) & (data['Current']<0), 'Temp_s5_DChg'] = (data['Time_in_Sec_s']);data['Temp_s5_DChg'] = data['Temp_s5_DChg'].replace(np.NaN,0)
    print('4/4............')
    
    
#%%
    
    
    data= data.drop(['RTC_s','Time_in_Sec_s','Year'], axis=1)
    data.to_pickle('PHY_21.1_25Deg_AllCycles_1092Cycles_processed.pkl')
    end=time.time()
    print(end-start)
            
            
            
            
