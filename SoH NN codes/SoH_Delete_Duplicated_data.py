# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 13:18:41 2021

@author: IITM
"""

"""
To filter duplicate sessions by comparing timestamps; for discharge alone

Run this SECOND on both chg and dchg summary data

"""
#%%
def timecheck(x,path,key):
    import time
    start=time.time()
    import pandas as pd
    import numpy as np
    dff=x
#    dff=pd.read_csv(x) # this is only the summary data  #Replace x with this format, in case you need to run this code alone;  "D:\\Benisha\\Code files\\Battery_Pack_mohali_Charging_Data_M4_Apr_timestates_sessionSummary.csv"
    dff1=pd.DataFrame()
    dff['start_Time']=pd.to_datetime(dff['start_Time'],errors='coerce')
    dff['end_Time']=pd.to_datetime(dff['end_Time'],errors='coerce')
    grouped=dff.groupby(['bin'],sort=False)
    result=[g[1] for g in list(grouped)]
#    
    #%% 
    for i in range (0,len(result)):
        result[i]=result[i].sort_values(by=['start_Time'])
        result[i]['start_Time_check']=(abs((result[i]['start_Time'].shift(1)-result[i]['start_Time'])/np.timedelta64(1,'m'))).astype(float)  
        result[i]['end_Time_check']=(abs((result[i]['end_Time'].shift(1)-result[i]['end_Time'])/np.timedelta64(1,'m'))).astype(float)
        result[i]['Flag']=(result[i]['start_Time_check']==0) & (result[i]['end_Time_check']==0) # difference in time(in minutes)
        result[i]['Flag_del_diff']=(result[i]['start_Time_check']<=5) & (result[i]['end_Time_check']<=10) 
        result[i]['Flag_overlap']=((result[i]['end_Time'].shift(1)-result[i]['start_Time'])/np.timedelta64(1,'m'))>5
        dff1=pd.concat([dff1,result[i]])
    
    #%%
    dff1=dff1[dff1.Flag==False] # false if time difference is more ie, a different session
    dff1.loc[dff1['Flag_del_diff']==True, 'Remark']='--Delete--'  #dff['Remark'] +
    dff1.loc[(dff1['Flag_overlap']==True) & (dff1['Flag_del_diff']==False), 'Remark']='--Overlap--'#dff['Remark'] +
    dff1=dff1.sort_values(by=['start_Time'])
    dff1=dff1.drop(['start_Time_check','end_Time_check','Flag','Flag_del_diff','Flag_overlap'],axis=1)
    dff1=dff1.reset_index(drop=True)
    
#    x=x.split('.')
    dff1.to_csv(path+'\\'+key+'_summary_Time_filtered.csv')
    return (path+'\\'+key+'_summary_Time_filtered.csv')
    print('-----------%s seconds---------' % (time.time()-start))