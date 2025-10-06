# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 13:27:34 2022

@author: IITM
"""

import time
start=time.time()
import pandas as pd
import glob
import os
import numpy as np

f="D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_5\\Pack_5_Complete_Cycle_data.csv"
df=pd.read_csv(f)

df['V_min']=df.loc[:,'C0':'C13'].min(axis=1)
df['V_max']=df.loc[:,'C0':'C13'].max(axis=1)
df['T_min']=df.loc[:,'T0':'T3'].min(axis=1)
df['T_max']=df.loc[:,'T0':'T3'].max(axis=1)
df['T_avg']=df.loc[:,'T0':'T3'].mean(axis=1)
df=df.rename(columns={'Inst_Mean_Voltage':'V_avg'})

#%% Storing the output files in a separate folder; creating that folder if it doesn't exist
# fin_path=f[0].rsplit('\\',1)[0]+'\\Timestates_files' ##uncomment
# fin_path=f.rsplit('\\',1)[0]+'\\Timestates_files' # Delete
# if not os.path.exists(fin_path):
#     os.makedirs(fin_path)

#%% Time spent in each step is divided into 8 states for voltage; 7 for temperature
df=df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0_x', 'Time_in_sec_s_x', 'Time_in_sec_x', 'Unnamed: 0_y', 'Time_in_sec_s_y', 'Time_in_sec_y', 'Unnamed: 0.1.1','Time_in_sec_s','Time_in_sec'])
data=pd.DataFrame()

df['DateTime']=pd.to_datetime(df['DateTime'], errors='coerce',format= "%Y-%m-%d %H:%M:%S" )  # arranges time in ascending order 
df=df.sort_values(by='DateTime',ascending=True)

print('1/4...............')

#%%
df['Vol_State_No']=pd.cut(x=df.V_max,bins=[0,3,3.3,3.5,3.6,3.7,3.8,3.9,4,4.5],include_lowest=True,labels=[0,1,2,3,4,5,6,7,8]).astype(float) # the data in "Voltage" column is dicided into different bins and each bin is given the label as specified; in the column specified
df['Temp_State_No']=pd.cut(x=df.T_max,bins=[0,25,30,35,40,45,60,100],include_lowest=True,labels=[0,1,2,3,4,5,6]).astype(float)


#%%
df=df.sort_values(by='DateTime')
df=df.reset_index(drop=True)
df['Chg_flag']=np.where(df['Session_Type']=='Charging', 3, 1)
df['Cycle_No']=(df['Chg_flag'].diff()>0).cumsum()

#%%
df['Time_diff']=(df['DateTime']-df['DateTime'].shift(1))/np.timedelta64(1,'m')
l1=df[df['Time_diff']>30].index.tolist()

df=df.reindex(list(range(len(df)+len(l1))))

#%%
for i in range(len(l1)):
    df.loc[l1[i]:,:]=df.loc[l1[i]:,:].shift(1)
    df.loc[l1[i],'Session_Type']='Rest'
    l1=[x+1 for x in l1]
    
df=df.fillna(method='ffill')
#%% New columns are createdm 
# stepval=['Charging','Discharging','Rest']
# for name in stepval:        
#     for j in range(0,9):
#         df['Vol_s'+str(j)+'_'+name]='' # Column name given based on state no and step type
# for name in stepval:
#     for j in range(0,7):
#         df['Temp_s'+str(j)+'_'+name]=''
        
grouped=df.groupby(['Cycle_No','Session_Type'],sort=False)
result=[f[1] for f in list(grouped)]
print('2/4...............')

#%%  Time in each step is filled in the corresponding column, based on the voltage/temp state and the step_type
for i in range(0,len(result)):
    Step_key=result[i]['Session_Type'].iloc[0]
    if Step_key=='Charging':
        Step_name='CCCV_Chg'
    elif Step_key=='Discharging':
        Step_name='CC_DChg'
    elif Step_key=='Rest':
        Step_name='Rest'
    result[i]['Time_in_mins_s']=(result[i]['DateTime'].shift(-1)-result[i]['DateTime'])/np.timedelta64(1,'m')
    result[i]['Time_in_mins_s']=result[i]['Time_in_mins_s'].astype(float)
    for j in range(0,9):
        result[i]['Vol_s'+str(j)+'_'+Step_name]=np.nan
        result[i]['Vol_s'+str(j)+'_'+Step_name]=np.where(result[i]['Vol_State_No']==j,result[i]['Time_in_mins_s'],result[i]['Vol_s'+str(j)+'_'+Step_name])
        result[i]['Vol_s'+str(j)+'_'+Step_name]=result[i]['Vol_s'+str(j)+'_'+Step_name].sum()
    for j in range(0,7):
        result[i]['Temp_s'+str(j)+'_'+Step_name]=np.nan
        result[i]['Temp_s'+str(j)+'_'+Step_name]=np.where(result[i]['Temp_State_No']==j,result[i]['Time_in_mins_s'],result[i]['Temp_s'+str(j)+'_'+Step_name])
        result[i]['Temp_s'+str(j)+'_'+Step_name]=result[i]['Temp_s'+str(j)+'_'+Step_name].sum()

    data=pd.concat([data,result[i]]) # in order to combine all step data into one file for one cell
data=data.reset_index(drop=True)

print('3/4...............')

#%%
# l2=data[data['Time_diff']>600].index.tolist()

# for i in range(len(l2)):
#     key=data['Time_diff'].iloc[l2[i]]
#     cycle_no=(key//60)//24 ##48
#     data.loc[l2[i]:,'Cycle_No']=data.loc[l2[i]:,'Cycle_No']+cycle_no

print('4/4...............')
#%%


data.to_csv(f.rsplit('\\',1)[0]+'\\'+f.rsplit('.',1)[0].rsplit('\\',1)[1]+'_Timestates_added.csv')

#%%
grouped=data.groupby(['Cycle_No','Session_Type'])
result=[g[1] for g in list (grouped)]

newcols=['Cycle_No','Session_Type','Start_Time','End_Time','Pack_Voltage','Pack_Current']+list(data.columns)
newcols=list(dict.fromkeys(newcols))
df_s=pd.DataFrame(columns=newcols,index=range(len(result)))

for i in range(len(result)):
    result[i]=result[i].reset_index(drop=True)
    df_s.loc[i,:]=result[i].iloc[-1]
    df_s.loc[i,'Start_Time']=result[i]['DateTime'].iloc[0]
    df_s.loc[i,'End_Time']=result[i]['DateTime'].iloc[-1]
    df_s.loc[i,'Capacity']=(abs(result[i]['Capacity'])).max()
    df_s.loc[i,'Start_V_max']=result[i]['V_max'].iloc[0]
    df_s.loc[i,'End_V_max']=result[i]['V_max'].iloc[-1]
    df_s.loc[i,'Start_V_min']=result[i]['V_min'].iloc[0]
    df_s.loc[i,'End_V_min']=result[i]['V_min'].iloc[-1]
    df_s.loc[i,'Start_V_Avg']=result[i]['V_avg'].iloc[0]
    df_s.loc[i,'End_V_Avg']=result[i]['V_avg'].iloc[-1]
    df_s.loc[i,'Start_T_max']=result[i]['T_max'].iloc[0]
    df_s.loc[i,'End_T_max']=result[i]['T_max'].iloc[-1]
    df_s.loc[i,'Start_T_min']=result[i]['T_min'].iloc[0]
    df_s.loc[i,'End_T_min']=result[i]['T_min'].iloc[-1]
    df_s.loc[i,'Start_T_Avg']=result[i]['T_avg'].iloc[0]
    df_s.loc[i,'End_T_Avg']=result[i]['T_avg'].iloc[-1]
    df_s.loc[i,'T_amb']=result[i]['T_max'].mean()
    if len(result[i])<=3:
        continue
    df_s.loc[i,'Start_SoC']=result[i]['SoC'].iloc[3]
    df_s.loc[i,'End_SoC']=result[i]['SoC'].iloc[-1]
    
#%%  
l3=df_s[df_s['Session_Type']=='Rest'].index.tolist()
for i in l3:
    df_s.loc[i,'Start_Time']=df_s.loc[i-1,'End_Time']
    df_s.loc[i,'Start_SoC']=df_s.loc[i-1,'End_SoC']
    try:
        df_s.loc[i,'End_Time']=df_s.loc[i+1,'Start_Time']
        df_s.loc[i,'End_SoC']=df_s.loc[i+1,'Start_SoC']
    except KeyError:
        continue
#%%

pack_no=f.split('\\',4)[3]

if ((pack_no=='Pack_1') | (pack_no=='Pack_3')):
    df_s['DoD']=85
    
elif ((pack_no=='Pack_2') | (pack_no=='Pack_4') | (pack_no=='Pack_5')):
    df_s['DoD']=90

elif (pack_no=='Pack_6'):
    df_s['DoD']=80

df_s['del_SoC']=abs(abs(df_s['End_SoC'])-abs(df_s['Start_SoC']))
df_s['del_SoC']=np.where(df_s['del_SoC']==0,abs(df_s['End_SoC']),df_s['del_SoC'])
#%%    
df_s=df_s.drop(columns=['DateTime','Chg_flag'])
df_s.to_csv(f.rsplit('\\',1)[0]+'\\'+f.rsplit('.',1)[0].rsplit('\\',1)[1]+'_Summary.csv')
    
print('-------------------%s seconds-------------------' %(time.time()-start))