# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 12:14:56 2022

@author: IITM
"""


"""
This code calculates the time for which the cell stays in a particular voltage and temperature range

"""
import pandas as pd
import numpy as np
import os
import time
start=time.time()
import glob
#%% glob gets the mentioned files within a folder
# files=glob.glob("D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_22.2\\*.csv")
files=glob.glob("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_18.1\\*.csv")

#%% Storing the output files in a separate folder; creating that folder if it doesn't exist
fin_path=files[0].rsplit('\\',1)[0]+'\\LCH_Timestates_files'

if not os.path.exists(fin_path):
    os.makedirs(fin_path)

#
#%% Time spent in each step is divided into 8 states for voltage; 7 for temperature
for f in files:
    df=pd.read_csv(f)
    df=df.drop(columns=['Unnamed: 0', 'Record_ID', 'Chg_Mid_Vtg', 'Power','DChg_Mid_Vtg', 'a1', 'a2', 'a3', 'a4', 'a5', 'DCIR', 'y', 'OCV', 'IR','Sample_Name','Unnamed: 25', 'Unnamed: 26', 'Unnamed: 27', 'Unnamed: 28','Unnamed: 29','OCV', 'IR', 'Sample_Name']) #LCH Cell
    # df=df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'Power', 'Chg_Mid_Vtg', 'y', 'DCIR', 'a1', 'a2', 'a3', 'Unnamed: 22', 'Unnamed: 23']) #PHY Cell
    data=pd.DataFrame()
    
    df['RTC']=pd.to_datetime(df['RTC'], errors='coerce',format= "%Y-%m-%d %H:%M:%S" )  # arranges time in ascending order 
    df=df.sort_values(by='RTC',ascending=True)
    df=df[df['RTC'].dt.year>=2016]
    df=df.reset_index(drop=True)
    print('1/3................')
#%%     
    df['Vol_State_No']=pd.cut(x=df.Voltage,bins=[0,3,3.3,3.5,3.6,3.7,3.8,3.9,4,4.5],include_lowest=True,labels=[0,1,2,3,4,5,6,7,8]).astype(float) # the data in "Voltage" column is dicided into different bins and each bin is given the label as specified; in the column specified
    df['Temp_State_No']=pd.cut(x=df.T_cell,bins=[0,25,30,35,40,45,60,100],include_lowest=True,labels=[0,1,2,3,4,5,6]).astype(float)
#%% New columns are created
    stepval=['CCCV_Chg','CC_DChg','Rest']
    for name in stepval:      
        for j in range(0,9):
            df['Vol_s'+str(j)+'_'+name]=np.nan # Column name given based on state no and step type
    for name in stepval:
        for j in range(0,7):
            df['Temp_s'+str(j)+'_'+name]=np.nan
            
    grouped=df.groupby(['Cycle_No','Step_No'],sort=False)
    result=[f[1] for f in list(grouped)]
    print('2/3................')
#%% Time in each step is filled in the corresponding column, based on the voltage/temp state and the step_type
    for i in range(0,len(result)):
        Step_name=result[i]['Step_Type'].iloc[0]
        result[i]['Time_in_step_sec_s']=(result[i]['RTC'].shift(-1)-result[i]['RTC'])/np.timedelta64(1,'s')
        result[i]['Time_in_step_sec_s']=result[i]['Time_in_step_sec_s'].astype(float)
        for j in range(0,9):
            result[i]['Vol_s'+str(j)+'_'+Step_name]=np.where(result[i]['Vol_State_No']==j,result[i]['Time_in_step_sec_s'],result[i]['Vol_s'+str(j)+'_'+Step_name])
            result[i]['Vol_s'+str(j)+'_'+Step_name]=result[i]['Vol_s'+str(j)+'_'+Step_name].sum() 
        for j in range(0,7):
            result[i]['Temp_s'+str(j)+'_'+Step_name]=np.where(result[i]['Temp_State_No']==j,result[i]['Time_in_step_sec_s'],result[i]['Temp_s'+str(j)+'_'+Step_name])
            result[i]['Temp_s'+str(j)+'_'+Step_name]=result[i]['Temp_s'+str(j)+'_'+Step_name].sum()
    
        data=pd.concat([data,result[i]]) # in order to combine all step data into one file for one cell
    print('3/3................')
    data=data.reset_index(drop=True)
    data.to_csv(fin_path+'\\'+f.rsplit('.',1)[0].rsplit('\\',1)[1]+'_Timestates_added.csv')
    print('---------------Done---------------')

print('-------------------%s seconds-------------------' %(time.time()-start)) # to check the time for which the code runs