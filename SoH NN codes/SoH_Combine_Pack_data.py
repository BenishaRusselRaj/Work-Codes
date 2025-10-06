# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 14:56:58 2021

@author: IITM
"""

"""
to combine the chg and dchg summary data into one; battery pack data

Run this THIRD

"""
def combinedata(x,y,path):
    import time
    start=time.time()
    import pandas as pd
    import numpy as np
    from statistics import mode
    
    #"D:\\Benisha\\Battery DCA\\Mohali Monthly data\\2018_M8_Aug_charging_temperature_voltage_sortedTimestates_sessionSummary_Time_filtered_test.csv"
    #"D:\\Benisha\\Battery DCA\\Mohali Monthly data\\2018_M8_Aug_Driving_Data_Combined_sortedTimestates_sessionSummary_Time_filtered_test.csv"
    
    df11=pd.read_csv(x, sep=',',header=0,low_memory=False) # Charging sessions summary alone  # "D:\\Benisha\\Code files\\Battery_Pack_mohali_Charging_Data_M4_Apr_timestates_sessionSummary_Time_filtered.csv"
    df12=pd.read_csv(y,sep=',',header=0,low_memory=False) # discharging sessions summary alone   # "D:\\Benisha\\Code files\\Battery_Pack_mohali_Driving_Data_M4_Apr_timestates_sessionSummary_Time_filtered.csv"
    #df11['Remark']='' # if this column is absent, enable this
    df11['Session_Type']='Chg'
    df12['Session_Type']='DChg'
    
    try:
        df12= df12.drop(labels=['Unnamed: 0'], axis=1) # remove unwanted columns, if present #,'Unnamed: 0.1'
        df11= df11.drop(labels=['Unnamed: 0'], axis=1)
    except KeyError:
        pass
   
    #%%
    df13=pd.DataFrame(columns=df11.columns)
    data=pd.DataFrame()
    df13=pd.concat([df13,df11,df12])
    df13=df13.reset_index(drop=True)
    
    #%%
    df13['start_Time']=pd.to_datetime(df13['start_Time'],errors='coerce')
    df13['end_Time']=pd.to_datetime(df13['end_Time'],errors='coerce')
    df13=df13[df13['end_Time'].dt.month >= mode(df13['end_Time'].dt.month)]
    df13=df13[df13['start_Time'].dt.month >= (mode(df13['start_Time'].dt.month))-1]  #
    
    df13=df13.reset_index(drop=True)
    r=df13.groupby(['bin'], sort=False)
    df1f=[g[1] for g in list(r)]
    #%%
    for i in range(0, len(df1f)):
        df1f[i]=df1f[i].sort_values(by='start_Time')
        df1f[i]=df1f[i].reset_index(drop=True)
        df1f[i]['Chg_flag']=np.where(df1f[i]['Session_Type']=='Chg', 3, 1)
        df1f[i]['Cycle_No']=(df1f[i]['Chg_flag'].diff()>0).cumsum()
        df1f[i]['Flag_Time_diff']=((df1f[i]['start_Time']-df1f[i]['end_Time'].shift(1))/np.timedelta64(1,'m'))>20
        y1=df1f[i][(df1f[i].Flag_Time_diff==True) & df1f[i].Remark.isnull()].index.tolist()
        
        df1f[i]=df1f[i].reindex(df1f[i].index.tolist()+list(range(len(df1f[i]), 2*len(df1f[i]))))
        
        #%%
        for j in range(0,len(y1)):
            df1f[i].loc[y1[j]:,:]=df1f[i].loc[y1[j]:,:].shift(1)
            df1f[i].loc[y1[j],'Session_Type']='Rest'
            df1f[i].loc[y1[j],'Remark']='Rest_included'
            df1f[i].loc[y1[j],'start_Time']= df1f[i].loc[y1[j]-1,'end_Time']
            df1f[i].loc[y1[j],'end_Time']=df1f[i].loc[y1[j]+1,'start_Time']
            df1f[i].loc[y1[j],'start_V_Min']=df1f[i].loc[y1[j]-1,'end_V_Min']
            df1f[i].loc[y1[j],'end_V_Min']=df1f[i].loc[y1[j]+1, 'start_V_Min']
            df1f[i].loc[y1[j],'start_V_Max']=df1f[i].loc[y1[j]-1,'end_V_Max']
            df1f[i].loc[y1[j],'end_V_Max']=df1f[i].loc[y1[j]+1, 'start_V_Max'] 
            df1f[i].loc[y1[j],'start_Temp_Min']=df1f[i].loc[y1[j]-1,'end_Temp_Min']
            df1f[i].loc[y1[j],'end_Temp_Min']=df1f[i].loc[y1[j]+1, 'start_Temp_Min']
            df1f[i].loc[y1[j],'start_Temp_Max']=df1f[i].loc[y1[j]-1,'end_Temp_Max']
            df1f[i].loc[y1[j],'end_Temp_Max']=df1f[i].loc[y1[j]+1, 'start_Temp_Max']
            df1f[i].loc[y1[j],'start_Avg_Vtg']=df1f[i].loc[y1[j]-1,'end_Avg_Vtg']
            df1f[i].loc[y1[j],'end_Avg_Vtg']=df1f[i].loc[y1[j]+1, 'start_Avg_Vtg']
            df1f[i].loc[y1[j],'start_Avg_Temp']=df1f[i].loc[y1[j]-1,'end_Temp_Min']
            df1f[i].loc[y1[j],'end_Avg_Temp']=df1f[i].loc[y1[j]+1, 'start_Temp_Min']
            df1f[i].loc[y1[j],'Vol_s0_mins':'Temp_s6_mins']='N/A'
            df1f[i].loc[y1[j],'Time_Estimate']= (df1f[i].loc[y1[j],'end_Time'] - df1f[i].loc[y1[j],'start_Time'])/np.timedelta64(1,'m')
            df1f[i].loc[y1[j],'Time_in_session_mins']= (df1f[i].loc[y1[j],'end_Time'] - df1f[i].loc[y1[j],'start_Time'])/np.timedelta64(1,'m')
            y1=[x1+1 for x1 in y1]
        data=pd.concat([data,df1f[i]])
    
    #%%
    data['Remark']=data['Remark'].fillna('---')
    data=data.dropna(subset=['Session_Type'])
    data=data.fillna(method='ffill')
    data=data.sort_values(by='start_Time',ascending=True)
    data=data.drop(['Chg_flag','Flag_Time_diff'],axis=1) #'Unnamed: 0.1',
    
    p=x.rsplit('\\',1)[1]
    data.to_csv(path+'\\'+p.rsplit('.',1)[0]+'_Combined_cyclesData_filtered_test.csv')
    
    print('-----------%s seconds------------' %((time.time())-start))