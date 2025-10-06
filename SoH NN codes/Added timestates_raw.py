 # -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 16:18:30 2022

@author: IITM
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 17:16:35 2021

@author: IITM
"""

"""
DESCRIPTION:
[STEP ONE]
This code calculates the time for which the cell stays in a particular voltage and temperature range
The input to this code is the processed_raw files(.csv) after running the "ProcessingRawData_2.py" code
The output(a csv file) of this code is saved automatically, with the same name and path as the input file, with a "_Timestates_added.csv" added at the end

'''''''''''''CHECK AMBIENT AND CELL TEMPERATURE, COLUMNS TO DROP'''''''''''''
"""
import pandas as pd
import numpy as np
import os
import time
start=time.time()
import glob
#%% glob gets the mentioned files within a folder
# files=glob.glob("D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_22.2\\*.csv") ##uncomment
f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\Raw files\\LCH_15.1_35Deg_AllCycles_AllCycles_raw(1).csv"## Delete
#%% Original data was in H:M:S format, so here we change it into seconds
def convert_time(x):
    h,m,s=map(int,x.split(':'))
    return(int(h)*3600+int(m)*60+s)

#%% Storing the output files in a separate folder; creating that folder if it doesn't exist
# fin_path=files[0].rsplit('\\',1)[0]+'\\Timestates_files' ##uncomment
fin_path=f.rsplit('\\',1)[0]+'\\Timestates_files' # Delete
if not os.path.exists(fin_path):
    os.makedirs(fin_path)

#%% Time spent in each step is divided into 8 states for voltage; 7 for temperature
# for f in files: ##uncomment
### block to indent
df=pd.read_csv(f)
# LCH 60Ah
# df=df.drop(columns=['Unnamed: 0', 'Record_ID', 'Chg_Mid_Vtg', 'Power','DChg_Mid_Vtg', 'DCIR', 'OCV', 'IR','Sample_Name','OCV', 'IR', 'Sample_Name','Q_End(mAh)','Capacitance_Chg(mAh)','Capacitance_DChg(mAh)','Q_Chg(mAh)','Engy_Chg(mWh)','Q_DChg(mAh)','Engy_DChg(mWh)','Engy_Chg(mWh).1','dQ/dV(mAh/V)','Engy_DChg(mWh).1','dQm/dV(mAh/V.g)','Q_Net_DChg(mAh)','Auxiliary_Channel_TU4 U(V)','Net Engy_DChg(mWh)','Auxiliary_Channel_TU4 T','Charge IR(O)','U4 Start(V)','Discharge IR(O)','U4 End(V)','End Temp','T4 StartTemp','Net Cap_DChg(mAh)','T1 EndTemp','Net Engy_DChg(mWh).1','Energy Efficiency','Unnamed: 56','Unnamed: 57','Unnamed: 58','Unnamed: 59','Unnamed: 60','Unnamed: 63','Unnamed: 64','Unnamed: 65']) #, 'a1', 'a2', 'a3', 'a4', 'a5', 'y','Unnamed: 25', 'Unnamed: 26', 'Unnamed: 27', 'Unnamed: 28','Unnamed: 29','Unnamed: 61,Unnamed: 62'
# LCH 
df=df.drop(columns=['Unnamed: 0','Start_Voltage','End_Voltage', 'Chg_Mid_Vtg', 'Power', 'DChg_Mid_Vtg', 'a1','a2', 'a3', 'a4', 'a5', 'DCIR', 'y', 'Unnamed: 25', 'Unnamed: 26','Unnamed: 27', 'Unnamed: 28', 'Unnamed: 29', 'OCV','IR', 'Sample_Name']) 
# PHY
# df=df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1','Start_Voltage','End_Voltage', 'Power', 'Chg_Mid_Vtg','y', 'DCIR', 'a1', 'a2', 'a3', 'Unnamed: 22', 'Unnamed: 23', 'OCV', 'IR', 'Sample_Name'])
#BRD
# df=df.drop(columns=['Unnamed: 0','Record_ID','Start_Voltage','End_Voltage','Q_in_and_out_Step', 'Q_in_out', 'Power','Energy_in_out', 'Chg_Mid_Vtg','y', 'DCIR', 'a1', 'a2', 'a3','Unnamed: 22', 'Unnamed: 23', 'Sample_Name','OCV', 'IR'])
data=pd.DataFrame()

df['RTC']=pd.to_datetime(df['RTC'], errors='coerce',format= "%Y-%m-%d %H:%M:%S" )  # arranges time in ascending order 
df=df[df['RTC'].dt.year>=2016]
df=df.sort_values(by='RTC',ascending=True)

# df['T_amb']=45
# df['T_cell']=45

# df=df[df['RTC'].dt.year>=2018]
# df=df.reset_index(drop=True)
print('1/4...............')

#%%
# df['Time_Spent_in_Step_sec']=df['Time_Spent_in_Step'].str.split('.').str[0] # to remove the millisecond data;it was only .000 so it was removed
# df['Time_Spent_in_Step_sec']=df['Time_Spent_in_Step_sec'].apply(convert_time)

df['Vol_State_No']=pd.cut(x=df.Voltage,bins=[0,3,3.3,3.5,3.6,3.7,3.8,3.9,4,4.5],include_lowest=True,labels=[0,1,2,3,4,5,6,7,8]).astype(float) # the data in "Voltage" column is dicided into different bins and each bin is given the label as specified; in the column specified
df['Temp_State_No']=pd.cut(x=df.T_amb,bins=[0,25,30,35,40,45,60,100],include_lowest=True,labels=[0,1,2,3,4,5,6]).astype(float)
print('2/4...............')
#%% New columns are created
stepval=['CCCV_Chg','CC_DChg','Rest']
for name in stepval:        
    for j in range(0,9):
        df['Vol_s'+str(j)+'_'+name]='' # Column name given based on state no and step type

for name in stepval:
    for j in range(0,7):
        df['Temp_s'+str(j)+'_'+name]=''
        
grouped=df.groupby(['New_Cycle_No','Step_No'],sort=False)
result=[f[1] for f in list(grouped)]
print('3/4...............')
#%%  Time in each step is filled in the corresponding column, based on the voltage/temp state and the step_type
for i in range(0,len(result)):
    Step_name=result[i]['Step_Type'].iloc[0]
    result[i]['Time_in_mins_s']=(result[i]['RTC'].shift(-1)-result[i]['RTC'])/np.timedelta64(1,'m')
    result[i]['Time_in_mins_s']=result[i]['Time_in_mins_s'].astype(float)
    result[i]['Time_in_Step_DateTime']=result[i]['RTC'].iloc[-1]-result[i]['RTC'].iloc[0]
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
print('4/4...............')

data.to_csv(fin_path+'\\'+f.rsplit('.',1)[0].rsplit('\\',1)[1]+'_Timestates_added.csv')

# del data
del df
print('-------------------%s seconds-------------------' %(time.time()-start))
### end of block
print('-------------------%s seconds-------------------' %(time.time()-start)) # to check the time for which the code runs