# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 14:23:04 2022

@author: IITM
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 15:39:58 2019

@author: IITM
DESCRIPTION:
[STEP ZERO.2]
*** this .py file creates a pandas dataframe of a .txt file
--- May consider running MergeCSV prior to this
--- processes single .txt file by first converting it to .csv
---import files as txt from all info visible data or import already created .txt file (may run MergeCSV prior to this)
---.txt is seperated by tab whereas .csv is seperated by comma
---first replace all tabs by comma
---change the header and get .csv file
---get a pickel file with required df; pkl file will be saved in root folder
---clear variable list before execution

--- ++++++Changes in code++++++
---clear variable list before execution
--- replace with req file name
--- Change sample_name, T_amb, T_cell
--- execution time 10-30 minutes
"""
import time
start_time = time.time()

import pandas as pd
import numpy as np
import os

#dfcolumns = pd.read_csv('D:\Academic\Python ML\Data files\t6.txt', nrows = 1)
#dfcolumns = pd.read_csv('D:\Academic\Python ML\Data files\t6.txt')
file_name="E:\\BRD\\Sample 3.1\\BRD_3.1_25Deg_AllCycles_modified_arranged.txt" # CHANGE AMBIENT TEMPERATURE AND CELL TEMPERATURE

with open(file_name) as fin, open('tempfile.csv', 'w') as fout:
    for line in fin:
        fout.write(line.replace('\t', ','))
        #fout.write(line.replace(':000.000', '.0'))
        

#data = pd.read_csv("D:\Academic\Python ML\Data files\myfinalcsvfile.txt", header=0, sep=',',error_bad_lines=False, index_col=False, dtype='unicode')
df = pd.read_csv("tempfile.csv", header=0, sep=',',error_bad_lines=False, index_col=False, dtype='unicode',low_memory=False)

# df[['Record_ID','Voltage','Capacity_2','Current','Energy_2','Capacity_3','Start_Voltage','Energy_3','End_Voltage','Chg_Mid_Vtg','DChg_Mid_Vtg']]=df[['Record_ID','Voltage','Capacity_2','Current','Energy_2','Capacity_3','Start_Voltage','Energy_3','End_Voltage','Chg_Mid_Vtg','DChg_Mid_Vtg']].astype(float)
df[['Cycle_No','Step_No','Voltage','Q_in_Step','Current','Q_in_and_out_Step','Start_Voltage','Energy_in_out','End_Voltage']]=df[['Cycle_No','Step_No','Voltage','Q_in_Step','Current','Q_in_and_out_Step','Start_Voltage','Energy_in_out','End_Voltage']].astype(float)       

df['T_amb'] = 25;
df['T_cell'] = 25;
df['OCV'] = 3.6;
df['IR'] = 0.01;
df['Sample_Name'] = "BRD_3.1";


print('1/4................') 
#%% extract step info
df2=df[pd.notnull(df['Cycle_No'])]
df2 = df2.drop(["Step_No","Step_Type","Time_Spent_in_Step","Q_in_Step","Q_in_and_out_Step","Start_Voltage","Energy_in_out","End_Voltage","Chg_Mid_Vtg","DCIR","RTC","a1","T_cell","OCV"] , axis=1) #,"y","a2","a3","a4","a5","Power"
df2['Q_in_out'] = pd.to_numeric(df2['Q_in_out'], errors='coerce')
df2 = df2.dropna(axis=1,how='all')
df2.rename(
    columns={
        "Cycle_No": "Cycle_No",
        "Record_ID": "Charge_in_cycle",
        "Time_Elapsed": "Charge_out_cycle",
        "Voltage": "Charge_Efficiency",
        "Current": "Energy_in_cycle",
        "Q_in_out": "Energy_out_cycle",
    },
    inplace=True
)
df2[['Energy_out_cycle','Energy_in_cycle']]=df2[['Energy_out_cycle','Energy_in_cycle']].astype(float)
df2['Energy_Efficiency']= ((df2.Energy_out_cycle) / (df2.Energy_in_cycle))* 100
df2['Energy_Efficiency'] = df2['Energy_Efficiency'].replace(np.inf,100)
cols = list(df2.columns)
# a, b = cols.index('DChg_Mid_Vtg'), cols.index('Energy_Efficiency')
# cols[b], cols[a] = cols[a], cols[b]
# df2 = df2[cols]
print('2/4................') 
#%% extract cycle info
df3 = df[pd.notnull(df['Step_No'])]
df3 = df3.drop(["Cycle_No","Record_ID","Time_Elapsed","Voltage","Current","Q_in_out","Energy_in_out","RTC","a1","OCV"], axis=1) #,"y","a2","a3","a4","a5","Power"

#%% remove nan and space and replace by uppper data
df.replace(' ',np.nan,inplace=True)
df=df.fillna(method='ffill')

#%% reset indices
df3 = df3.reset_index(drop=True)
df2 = df2.reset_index(drop=True)
print('3/4................')
#%% gives continuous cycle numbers to all
new_cyc_no_s = np.array(df.a1); new_cyc_no=np.asfarray(new_cyc_no_s,float)
new_cyc_no1_s = np.array(df2.Cycle_No); new_cyc_no1=np.asfarray(new_cyc_no1_s,float)
new_cyc_no2_s = np.array(df3.Step_No); new_cyc_no2=np.asfarray(new_cyc_no2_s,float)

cno=0;
for i in range(1, len(df.Cycle_No)-1):
    new_cyc_no[i] = cno
    k = int(df.Cycle_No[i+1])-int(df.Cycle_No[i])
    if k!=0:
        cno = cno+1;
df['New_Cycle_No'] = new_cyc_no    # gives continuous cycle numbers
print('3.5/4................') 
#%% 


new_cyc_no1_s = np.array(df2.Cycle_No); new_cyc_no1=np.asfarray(new_cyc_no1_s,float)
#%%
cno =0;
for i in range(1, len(df2.Cycle_No)-1):
    new_cyc_no1[i] = cno
    try:
        int(df2.Cycle_No[i+1])
        k = int(df2.Cycle_No[i+1])-int(df2.Cycle_No[i])
    except ValueError:
        continue
    if k!=0:
        cno = cno+1;
df2['New_Cycle_No'] = new_cyc_no1 # gives continuous cycle numbers
df2 = df2.loc[df2['New_Cycle_No'].shift(1) != df2['New_Cycle_No']]
print('4/4................') 
#%% clean df from unwanted points
df = df[pd.notnull(df['RTC'])] # to remove step start/end rows
df=df[(df.Voltage>0)] 
df=df[(df.Voltage<25)]# to remove step start/end rows
df=df.reset_index(drop=True)


#%%

df['RTC'] = df['RTC'].str.replace(':000.000', ".000")
df['Time_Elapsed'] = df['Time_Elapsed'].str.replace(':000.000', ".000")
#df['Time_Spent_in_Step'] = df['Time_Spent_in_Step'].str.replace(':000.000', ".000")

df['RTC'] = pd.to_datetime(df['RTC'], format = '%Y-%m-%d %H:%M:%S')
#df['Time_Elapsed'] = pd.to_datetime(df['Time_Elapsed'], format = '%H:%M:%S.%f')

#df['Time_Spent_in_Step'] = pd.to_datetime(df['Time_Spent_in_Step'], format = '%H:%M:%S.%f')

df = df.drop(["Start_Voltage","End_Voltage","Chg_Mid_Vtg","DCIR","RTC","a1","T_cell","OCV","y","Power"] , axis=1) #,"y","a2","a3","a4","a5","Power"
print(df.dtypes)

print('Raw Dataframe created') 

dff=df.head(10000)

#%%
# df2[['Charge_out_cycle']] = df2[['Charge_out_cycle']].astype(float)
Step_Info_df = df3.reset_index(drop=True)
Cycle_Info_df = df2.reset_index(drop=True)
All_Info_df = df.reset_index(drop=True)

#%%
fin_path=file_name.rsplit('\\',1)[0]+'\\Processed files'
if not os.path.exists(fin_path):
    os.makedirs(fin_path)
#%%
fin_name=file_name.rsplit('\\',1)[1].rsplit('.',1)[0]

# All_Info_df.to_pickle('LCH_19.1_25Deg_AllCycles_AllCycles_raw(1).pkl') # save the sorted txt file as a pickle file name as filename_raw
# Cycle_Info_df.to_pickle('LCH_19.1_25Deg_AllCycles_Cycles_Info_raw(1).pkl') # save the sorted txt file as a pickle file name as filename_raw
# Step_Info_df.to_pickle('LCH_19.1_25Deg_AllCycles_Steps_Info_raw(1).pkl') # save the sorted txt file as a pickle file name as filename_raw

All_Info_df.to_csv(fin_path+'\\'+fin_name+'_AllCycles_AllCycles_raw.csv') # save the sorted txt file as a pickle file name as filename_raw
# Cycle_Info_df.to_csv(fin_path+'\\'+fin_name+'_AllCycles_Cycles_Info_raw.csv') # save the sorted txt file as a pickle file name as filename_raw
# Step_Info_df.to_csv(fin_path+'\\'+fin_name+'_AllCycles_Steps_Info_raw.csv')

print("--- %s seconds ---" % (time.time() - start_time))
