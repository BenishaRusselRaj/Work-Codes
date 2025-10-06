# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 11:24:23 2021

@author: IITM
"""

#%% Import necessary libraries
import pandas as pd
import numpy as np
import time

start=time.time()
#x="D:\\Benisha\\Battery Pack Data\\IITM data\\iitm_driving_charging_data\\iitm\\INEXD0010102E3001009\\charging_session_data_iitm_INEXD0010102E3001009_00001.2019092515065400.001.tsv"
#data1 = pd.read_csv(x,header=0, sep='\t',index_col=False,error_bad_lines=False)   # Replace x with this format, in case you need to run this code alone; "D:\\Benisha\\Battery DCA\\Mohali_data1\\Original_data1_files\\2019_M4_Apr_driving_temperature_voltage_sorted.csv"

#%% Separating the voltage values into different voltage bins and times spent on these voltage levels
def timestates(data1,file_path,summary_path,key):
    for j in ['T0','T1','T2','T3','T4','T5','T6','T7','T8','T9','T10','T11','T12','T13','T14','T15','T16']:
        data1[j]=data1[j].where(data1[j]!=119,0)
    try:
        data1[['voltage','current']]=data1[['voltage','current']].shift(-1)
    except KeyError:        
        pass
    data1=data1.dropna(subset=['C0'])
    data1=data1.reset_index(drop=True)
    
    #%% Calculate max, min and average for voltage and temperature 
    data1['V_Min']=data1.loc[:,'C0':'C12'].min(axis=1)
    data1['V_Max']=data1.loc[:,'C0':'C12'].max(axis=1)
    data1['T_Max']=data1.loc[:,'T0':'T16'].max(axis=1)
    data1['T_Min']=data1.loc[:,'T0':'T16'].min(axis=1)
    data1['Avg_Temp']=data1.loc[:,'T0':'T16'].mean(axis=1)
    data1['Avg_Vtg']=data1.loc[:,'C0':'C12'].mean(axis=1)
    
    #%% Filter junk values
    data1=data1[data1.V_Max<4.5]
    data1=data1[(data1.T_Max<100)]
    data=pd.DataFrame()
    
    #%% Get the cell with maximum voltage and temperature
    data1['Maximum_Temp_Cell']=data1.loc[:,'T0':'T16'].idxmax(axis=1)
    data1['Maximum_Voltage_cell']=data1.loc[:,'C0':'C12'].idxmax(axis=1)
    df1=pd.DataFrame(columns=data1.columns,index=data1.index)
    df=pd.DataFrame()
    print('1/4............')
    
    #%% Time column is set to datetime format and the dataframe is sorted accordingly
    data1['time']=pd.to_datetime(data1['time'], errors='coerce',format= "%Y-%m-%d %H:%M:%S") 
    data1=data1.sort_values(by='time',ascending=True)
    data1=data1[data1['time'].dt.year>=2018]
    data1=data1.reset_index(drop=True)
    print('2/4............')
    
    #%%  Adds empty columns iteratively; we do this beforehand as we use .loc and .iloc later
    for newcol in ['start_Time','end_Time','start_V_Min','end_V_Min','start_V_Max','end_V_Max',
                   'start_Temp_Min','end_Temp_Min','start_Temp_Max','end_Temp_Max','start_current',
                   'end_current','start_Avg_Vtg','end_Avg_Vtg','start_Avg_Temp','end_Avg_Temp',
                   'Vol_s0_mins','Vol_s1_mins','Vol_s2_mins','Vol_s3_mins','Vol_s4_mins','Vol_s5_mins',
                   'Vol_s6_mins','Vol_s7_mins','Vol_s8_mins','Temp_s0_mins','Temp_s1_mins','Temp_s2_mins',
                   'Temp_s3_mins','Temp_s4_mins','Temp_s5_mins','Temp_s6_mins','Remark']:
        df1[newcol]=np.nan
    
    #%% Voltage and temperature values are separated into bins and labels are assigned as "State Numbers"
    data1['Vol_State_No']=pd.cut(x = data1.V_Max,bins=[0,3,3.3,3.5,3.6,3.7,3.8,3.9,4,4.5],
                                 include_lowest=True,labels=[0,1,2,3,4,5,6,7,8]).astype(float) 
    data1['Temp_State_No']=pd.cut(x = data1.T_Max,bins=[0,25,30,35,40,45,60,100], 
                                  include_lowest=True,labels=[0,1,2,3,4,5,6]).astype(float)
    k=0
    print('3/4............')
    
    #%%
    g1=data1.groupby('session',sort=False)
    dff=[f[1] for f in list(g1)]
    for i in range (0,len(dff)):
        dff[i]['Flag']=(abs(dff[i]['V_Max']-dff[i]['V_Max'].shift())>0.15).cumsum()
        data=pd.concat([data,dff[i]])
    data=data.sort_values(by='time',ascending=True)
    print('3.5/4............')
    
    #%%
    grouped=data.groupby(['session','Flag'])
    result=[g[1]for g in list(grouped)]
    
    #%%
    for i in range(0,len(result)):
        result[i]=result[i].reset_index(drop=True)
        result[i]['Time_in_mins_s']=(result[i]['time'].shift(-1)-result[i]['time'])/np.timedelta64(1,'m')
        result[i]['Time_in_mins_s']=(result[i]['Time_in_mins_s']).astype(float) #  Time between two successive data1 points(in minutes)
        result[i]['Time_in_mins_s']=np.round(result[i]['Time_in_mins_s'],3)
        
        result[i].loc[(result[i]['Vol_State_No']==0) , 'Vol_s0_mins'] = (result[i]['Time_in_mins_s']) # when condition is met, assign value to the specified column name
        result[i].loc[(result[i]['Vol_State_No']==1) , 'Vol_s1_mins'] = (result[i]['Time_in_mins_s'])
        result[i].loc[(result[i]['Vol_State_No']==2) , 'Vol_s2_mins'] = (result[i]['Time_in_mins_s'])
        result[i].loc[(result[i]['Vol_State_No']==3) , 'Vol_s3_mins'] = (result[i]['Time_in_mins_s'])
        result[i].loc[(result[i]['Vol_State_No']==4) , 'Vol_s4_mins'] = (result[i]['Time_in_mins_s']) 
        result[i].loc[(result[i]['Vol_State_No']==5) , 'Vol_s5_mins'] = (result[i]['Time_in_mins_s'])
        result[i].loc[(result[i]['Vol_State_No']==6) , 'Vol_s6_mins'] = (result[i]['Time_in_mins_s'])
        result[i].loc[(result[i]['Vol_State_No']==7) , 'Vol_s7_mins'] = (result[i]['Time_in_mins_s'])
        result[i].loc[(result[i]['Vol_State_No']==8) , 'Vol_s8_mins'] = (result[i]['Time_in_mins_s'])
        
        result[i].loc[(result[i]['Temp_State_No']==0) , 'Temp_s0_mins'] = (result[i]['Time_in_mins_s'])
        result[i].loc[(result[i]['Temp_State_No']==1) , 'Temp_s1_mins'] = (result[i]['Time_in_mins_s'])
        result[i].loc[(result[i]['Temp_State_No']==2) , 'Temp_s2_mins'] = (result[i]['Time_in_mins_s'])
        result[i].loc[(result[i]['Temp_State_No']==3) , 'Temp_s3_mins'] = (result[i]['Time_in_mins_s'])
        result[i].loc[(result[i]['Temp_State_No']==4) , 'Temp_s4_mins'] = (result[i]['Time_in_mins_s'])
        result[i].loc[(result[i]['Temp_State_No']==5) , 'Temp_s5_mins'] = (result[i]['Time_in_mins_s'])
        result[i].loc[(result[i]['Temp_State_No']==6) , 'Temp_s6_mins'] = (result[i]['Time_in_mins_s'])
            
        result[i]['Vol_s0_mins'] = result[i]['Vol_s0_mins'].sum() # sum of time spent in this voltage state in this particular session alone
        result[i]['Vol_s1_mins'] = result[i]['Vol_s1_mins'].sum()
        result[i]['Vol_s2_mins'] = result[i]['Vol_s2_mins'].sum()
        result[i]['Vol_s3_mins'] = result[i]['Vol_s3_mins'].sum()
        result[i]['Vol_s4_mins'] = result[i]['Vol_s4_mins'].sum()
        result[i]['Vol_s5_mins'] = result[i]['Vol_s5_mins'].sum()
        result[i]['Vol_s6_mins'] = result[i]['Vol_s6_mins'].sum()
        result[i]['Vol_s7_mins'] = result[i]['Vol_s7_mins'].sum()
        result[i]['Vol_s8_mins'] = result[i]['Vol_s8_mins'].sum()
        
        result[i]['Temp_s0_mins'] = result[i]['Temp_s0_mins'].sum()
        result[i]['Temp_s1_mins'] = result[i]['Temp_s1_mins'].sum()
        result[i]['Temp_s2_mins'] = result[i]['Temp_s2_mins'].sum()
        result[i]['Temp_s3_mins'] = result[i]['Temp_s3_mins'].sum()
        result[i]['Temp_s4_mins'] = result[i]['Temp_s4_mins'].sum()
        result[i]['Temp_s5_mins'] = result[i]['Temp_s5_mins'].sum()
        result[i]['Temp_s6_mins'] = result[i]['Temp_s6_mins'].sum()
        
        try:
            df1['session'].iloc[k]=result[i]['session'].iloc[-1] # if data1 is normal and continuous, this block gets executed
            df1['bin'].iloc[k]=result[i]['bin'].iloc[-1]
            df1['start_Time'].iloc[k]=result[i]['time'].iloc[0]
            df1['end_Time'].iloc[k]=result[i]['time'].iloc[-1]
            
            try:
                df1['start_Avg_Temp'].iloc[k]=pd.to_numeric(result[i]['Avg_Temp'].iloc[0]) 
                df1['start_Avg_Vtg'].iloc[k]=pd.to_numeric(result[i]['Avg_Vtg'].iloc[0])
                df1['end_Avg_Temp'].iloc[k]=pd.to_numeric(result[i]['Avg_Temp'].iloc[-1]) 
                df1['end_Avg_Vtg'].iloc[k]=pd.to_numeric(result[i]['Avg_Vtg'].iloc[-1])
                df1['start_Temp_Min'].iloc[k]=pd.to_numeric(result[i]['T_Min'].iloc[0])
                df1['end_Temp_Min'].iloc[k]=pd.to_numeric(result[i]['T_Min'].iloc[-1])
                df1['start_Temp_Max'].iloc[k]=pd.to_numeric(result[i]['T_Max'].iloc[0])
                df1['end_Temp_Max'].iloc[k]=pd.to_numeric(result[i]['T_Max'].iloc[-1])
                df1['start_V_Min'].iloc[k]=pd.to_numeric(result[i]['V_Min'].iloc[0])
                df1['end_V_Min'].iloc[k]=pd.to_numeric(result[i]['V_Min'].iloc[-1])
                df1['start_V_Max'].iloc[k]=pd.to_numeric(result[i]['V_Max'].iloc[0])
                df1['end_V_Max'].iloc[k]=pd.to_numeric(result[i]['V_Max'].iloc[-1])
    
            except KeyError:
                df1['Remark'].iloc[k]='First and last values were NAN;Taken the first valid data1 for summary'  # when some data1 is present in the session but starting and ending were nan, this block gets executed
                df1['start_Avg_Temp'].iloc[k]=result[i]['Avg_Temp'].loc[result[i]['Avg_Temp'].first_valid_index()]
                df1['start_Avg_Vtg'].iloc[k]=result[i]['Avg_Vtg'].loc[result[i]['Avg_Vtg'].first_valid_index()]
                df1['end_Avg_Temp'].iloc[k]=result[i]['Avg_Temp'].loc[result[i]['Avg_Temp'].last_valid_index()]
                df1['end_Avg_Vtg'].iloc[k]=result[i]['Avg_Vtg'].loc[result[i]['Avg_Vtg'].last_valid_index()]
                df1['start_Temp_Min'].iloc[k]=result[i]['T_Min'].loc[result[i]['T_Min'].first_valid_index()]
                df1['end_Temp_Min'].iloc[k]=result[i]['T_Min'].loc[result[i]['T_Min'].last_valid_index()] 
                df1['start_Temp_Max'].iloc[k]=result[i]['T_Max'].loc[result[i]['T_Max'].first_valid_index()]
                df1['end_Temp_Max'].iloc[k]=result[i]['T_Max'].loc[result[i]['T_Max'].last_valid_index()]
                df1['start_V_Min'].iloc[k]=result[i]['V_Min'].loc[result[i]['V_Min'].first_valid_index()]
                df1['end_V_Min'].iloc[k]=result[i]['V_Min'].loc[result[i]['V_Min'].last_valid_index()] 
                df1['start_V_Max'].iloc[k]=result[i]['V_Max'].loc[result[i]['V_Max'].first_valid_index()]
                df1['end_V_Max'].iloc[k]=result[i]['V_Max'].loc[result[i]['V_Max'].last_valid_index()]
    
        except KeyError:
            df1['session'].iloc[k]=result[i]['session'].iloc[-1] # if entire session is nan, this block gets executed
            df1['bin'].iloc[k]=result[i]['bin'].iloc[-1]
            df1['start_Time'].iloc[k]=result[i]['time'].iloc[0]
            df1['end_Time'].iloc[k]=result[i]['time'].iloc[-1]
            
            df1['start_Avg_Temp'].iloc[k]=np.nan
            df1['start_Avg_Vtg'].iloc[k]=np.nan
            df1['end_Avg_Temp'].iloc[k]=np.nan
            df1['end_Avg_Vtg'].iloc[k]=np.nan
            df1['start_Temp_Min'].iloc[k]=np.nan
            df1['end_Temp_Min'].iloc[k]=np.nan
            df1['start_Temp_Max'].iloc[k]=np.nan
            df1['end_Temp_Max'].iloc[k]=np.nan
            df1['start_V_Min'].iloc[k]=np.nan
            df1['end_V_Min'].iloc[k]=np.nan
            df1['start_V_Max'].iloc[k]=np.nan
            df1['end_V_Max'].iloc[k]=np.nan
            df1['start_SOC_pred'].iloc[k]=np.nan
            df1['end_SOC_pred'].iloc[k]=np.nan
    
        df1['Vol_s0_mins'].iloc[k]  = result[i]['Vol_s0_mins'].iloc[-1] # iloc[0] and iloc[-1] are used to get first and last data1 from that session
        df1['Vol_s1_mins'].iloc[k]  = result[i]['Vol_s1_mins'].iloc[-1]
        df1['Vol_s2_mins'].iloc[k]  = result[i]['Vol_s2_mins'].iloc[-1]
        df1['Vol_s3_mins'].iloc[k]  = result[i]['Vol_s3_mins'].iloc[-1]
        df1['Vol_s4_mins'].iloc[k]  = result[i]['Vol_s4_mins'].iloc[-1]
        df1['Vol_s5_mins'].iloc[k]  = result[i]['Vol_s5_mins'].iloc[-1]
        df1['Vol_s6_mins'].iloc[k]  = result[i]['Vol_s6_mins'].iloc[-1]
        df1['Vol_s7_mins'].iloc[k]  = result[i]['Vol_s7_mins'].iloc[-1]
        df1['Vol_s8_mins'].iloc[k]  = result[i]['Vol_s8_mins'].iloc[-1]
        
        df1['Temp_s0_mins'].iloc[k]  = result[i]['Temp_s0_mins'].iloc[-1]
        df1['Temp_s1_mins'].iloc[k]  = result[i]['Temp_s1_mins'].iloc[-1]
        df1['Temp_s2_mins'].iloc[k]  = result[i]['Temp_s2_mins'].iloc[-1]
        df1['Temp_s3_mins'].iloc[k]  = result[i]['Temp_s3_mins'].iloc[-1]
        df1['Temp_s4_mins'].iloc[k]  = result[i]['Temp_s4_mins'].iloc[-1]
        df1['Temp_s5_mins'].iloc[k]  = result[i]['Temp_s5_mins'].iloc[-1]
        df1['Temp_s6_mins'].iloc[k]  = result[i]['Temp_s6_mins'].iloc[-1]
        
        k=k+1
        df=pd.concat([df,result[i]])
        
    print('4/4............')
    
    
    #%%
    df1=df1.dropna(axis=1, how='all')
    df=df.reset_index(drop=True)
    df1['Time_Cumulative_Estimate']=df1[['Vol_s0_mins','Vol_s1_mins','Vol_s2_mins','Vol_s3_mins',
                                         'Vol_s4_mins','Vol_s5_mins','Vol_s6_mins','Vol_s7_mins',
                                         'Vol_s8_mins']].sum(axis=1)
    df1['Time_in_session_mins']=(df1['end_Time']-df1['start_Time'])/np.timedelta64(1,'m')
    df1=df1.reset_index(drop=True)
    df1=df1.dropna(subset=['session'])
    df= df.drop(['Time_in_mins_s'], axis=1)
    
    df.to_csv(file_path+'\\'+key+'_Combined_timestates.csv')         
    df1.to_csv(summary_path+'\\'+key+'_Timestates_sessionSummary.csv')  
    return (summary_path+'\\'+key+'_Timestates_sessionSummary.csv') 
    
    print('----------%s seconds-----------' % (time.time()-start))