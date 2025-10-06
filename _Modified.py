# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 15:58:31 2019

@author: IITM
"""
"""
**************************************READ THIS*****************************************************

1.Code to Match temperature base data of the thermistor data and the nda files
2.To get the pkl file from .nda file, run the "ReadSpecificLines.py" code on the .txt file extracted from .nda. cHANGE PATH AND NAME IN 1 PLACE ALONE
3.Now run "ProcessingRawData_2.py" on the resultant .txt file. CHANGE PATHS AND NAMES IN 4 PLACES
4.Out of the three .pkl files you get, use the Allcycles _raw.pkl(first one alone) file here
5. In this code, CHANGE PATHS AND NAMES IN 5 PLACES

Runtime: 20-30 mins

""" 

#%%
import time
start=time.time()
import pandas as pd
import numpy as np
from datetime import timedelta
import pickle as pkl

import glob


files = glob.glob("C:\\Users\\IITM\\Desktop\\AMBEDKAR\\Phy_13_5_therm\\Datalogger\\*.csv") # path to the Folder in which the data logger files are stored
cols=['Record_No','Realtime','T_Ch1','Alarm_Ch1','T_Ch2','Alarm_Ch2','T_Ch3','Alarm_Ch3','T_Ch4','Alarm_Ch4','T_Ch5','Alarm_Ch5','T_Ch6','Alarm_Ch6','T_Ch7','Alarm_Ch7','T_Ch8','Alarm_Ch8','T_Ch9','Alarm_Ch9','T_Ch10','Alarm_Ch10','T_Ch11','Alarm_Ch11','T_Ch12','Alarm_Ch12','T_Ch13','Alarm_Ch13','T_Ch14','Alarm_Ch14','T_Ch15','Alarm_Ch15','T_Ch16','Alarm_Ch16','T_Ch17','Alarm_Ch17'] # assigns Column names
#cols=['Record_No','Realtime','','T_Ch1','Alarm_Ch1','T_Ch2','Alarm_Ch2','T_Ch3','Alarm_Ch3','T_Ch4','Alarm_Ch4','T_Ch5','Alarm_Ch5','T_Ch6','Alarm_Ch6','T_Ch7','Alarm_Ch7','T_Ch8','Alarm_Ch8','T_Ch9','Alarm_Ch9','T_Ch10','Alarm_Ch10','T_Ch11','Alarm_Ch11','T_Ch12','Alarm_Ch12','T_Ch13','Alarm_Ch13','T_Ch14','Alarm_Ch14','T_Ch15','Alarm_Ch15','T_Ch16','Alarm_Ch16','T_Ch17','Alarm_Ch17'] # assigns Column names
df_s = [pd.read_csv(f, header=None, sep=',',index_col=False,error_bad_lines=False,names=cols,encoding = "utf-16-le",low_memory=False) for f in files]
df = pd.concat(df_s,ignore_index=True)
df['Realtime']=df['Realtime'].str.rsplit(':',n=1).str[0] #Realtime in data logger has the millisecond field, but nda does not have that so, we remove that field from data logger realtime

#%%

df['Realtime']=pd.to_datetime(df['Realtime'], errors= 'coerce')
df['Record_No']=pd.to_numeric(df['Record_No'],errors= 'coerce')
df = df.dropna(subset=['Realtime','Record_No'])
df.to_csv("C:\\Users\\IITM\\Desktop\\AMBEDKAR\\Phy_13_5_therm\\Datalogger\\dataloggermerged1.csv") #use any path and file name here
#%%

df=df.reset_index()
print('...........1/3')

#%%

x=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'] #Channel Names
with open("C:\\Users\\IITM\\Desktop\\AMBEDKAR\\Phy_13_5_therm\\first11.pkl",'rb') as f: # path to the .pkl file which has been processed from the .nda file
    data=pkl.load(f)
    #%%
    data['RTC']=pd.to_datetime(data['RTC'],errors='coerce')
    data=data.sort_values(by='RTC')
    #%%
    data['RTC']=data['RTC'] + timedelta(seconds=33)
    
    #%%
    data=data.drop_duplicates(subset=['RTC'],keep='first')
    data=data.reset_index(drop=True)
    y=pd.Series(data['RTC'])
    df['Flag']=df['Realtime'].isin(y)
    #%%
    df=df[df.Flag==True]
    #%%
    df=df.sort_values(by='Realtime')
    df=df.drop_duplicates(subset=['Realtime'],keep='first')
    df=df.reset_index(drop=True)
    data=pd.concat([data,df],axis=1)
    data['Timeflag']=data['RTC'].isin(data['Realtime']) # Checks if the timestamp in .nda file is present in the timestamp in datalogger file
#%%    
    data=data.reset_index(drop=True)
    print('...........2/3')

#%%  
    y=data[data.Timeflag==False].index.tolist()
    for a in range(0,17): # iterating channel names
        for c,i in enumerate (y):
            dfs=np.split(data['T_Ch'+x[a]],[i])
            data['T_Ch'+x[a]]=pd.concat([dfs[0],pd.DataFrame([None]),dfs[1]],ignore_index=True)

    print('...........2.5/3')
#%%    
    data=data.dropna(subset=['Cycle_No'])
    data=data.drop(['Realtime'],axis=1)
    data=data.dropna(subset=['RTC'])
    print('...........3/3')
    data.to_pickle("C:\\Users\\IITM\\Desktop\\AMBEDKAR\\Phy_13_5_therm\\finaldoc_TimebaseMatched7.pkl")
    data.to_csv("C:\\Users\\IITM\\Desktop\\AMBEDKAR\\Phy_13_5_therm\\finaldoc_TimebaseMatchedtest7.csv")
print('---------%s--------' % (time.time()-start))