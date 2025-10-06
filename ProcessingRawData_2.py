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
import glob

# path="D:\\Benisha\\SoH_NN\\Data\\Variable Temperature\\Extracted files_PHY13\\Modified_Files\\Combined_Files\\PHY13_CYC_33.1_100%_AllCycles__modified_arranged.txt"
# files=glob.glob(path)

# name="D:\\Benisha\\SoH_NN\\Data\\LCH_60Ah\\LCH60Ah_1.2_CYC_25deg_100cycles_modified_arranged.txt"
name="D:\\Benisha\\SoH_NN\\Data\\LCH_60Ah\\LCH60_CYC_1.3_45deg_100cycles_modified_arranged.txt"
# for name in files:
#dfcolumns = pd.read_csv('D:\Academic\Python ML\Data files\t6.txt', nrows = 1)
#dfcolumns = pd.read_csv('D:\Academic\Python ML\Data files\t6.txt')
# SAMPLE: file_name="E:\\BRD\\Sample 3.1\\BRD_3.1_25Deg_0050 Cycles_modified_arranged.txt" # CHANGE AMBIENT TEMPERATURE AND CELL TEMPERATURE
    # file_name="D:\\Benisha\\SoH_NN\\Data\\Variable Temperature\\Extracted files_PHY15\\Modified_Files\\PHY15_CYC_37.1_100%_ 22.5 deg_ 20Cycles_modified_arranged.txt"
    # file_name=file_name.replace('\\','\\\\')
file_name=name

# Uncomment block
with open(file_name) as fin, open(name.rsplit("\\",1)[0]+"\\tempfile.csv", 'w') as fout:
    for line in fin:
        fout.write(line.replace('\t', ',').replace(':000.000', '.0'))
        # fout.write(line.replace(':000.000', '.0'))
## End of block        

# cols=['Cycle_No','Step_No', 'Record_ID','Step_Type', 'Time_Elapsed', 'Time_Spent_in_Step', 'Voltage', 'Q_in_Step', 'Current',
#       'Q_in_and_out_Step', 'Temperature', 'Energy_in_Step', 'Capacity(Ah)', 'Energy_in_and_out_Step', 'Q_in_and_out_Step(1)',
#       'Capacitance', 'Energy(mWh)','Energy_in_out(mWh/g)', 'RTC', 'Start_Temperature','','End_Temperature'
#       '','Q_End(mAh)',]
#data = pd.read_csv("D:\Academic\Python ML\Data files\myfinalcsvfile.txt", header=0, sep=',',error_bad_lines=False, index_col=False, dtype='unicode')
df = pd.read_csv(name.rsplit("\\",1)[0]+"\\tempfile.csv", header=0, sep=',',error_bad_lines=False, index_col=False, dtype='unicode',low_memory=False)
# df = pd.read_csv(name, header=0, sep=',',error_bad_lines=False, index_col=False, dtype='unicode',low_memory=False)
# df = pd.read_csv(name, header=0,error_bad_lines=False, index_col=False, dtype='unicode',low_memory=False)

# df[['Record_ID','Voltage','Capacity_2','Current','Energy_2','Capacity_3','Start_Voltage','Energy_3','End_Voltage','Chg_Mid_Vtg','DChg_Mid_Vtg']]=df[['Record_ID','Voltage','Capacity_2','Current','Energy_2','Capacity_3','Start_Voltage','Energy_3','End_Voltage','Chg_Mid_Vtg','DChg_Mid_Vtg']].astype(float)
df[['Cycle_No','Step_No','Voltage','Q_in_Step','Current','Q_in_and_out_Step','Start_Voltage','Energy_in_out','End_Voltage']]=df[['Cycle_No','Step_No','Voltage','Q_in_Step','Current','Q_in_and_out_Step','Start_Voltage','Energy_in_out','End_Voltage']].astype(float)       

# df['T_amb'] = 25;
df['T_amb'] = ''
df['T_cell'] = 45;
df['OCV'] = 3.6;
df['IR'] = 0.01;
df['Sample_Name'] =  "LCH60_"+name.rsplit('\\',1)[1].split('_',3)[2]   #"LCH_60Ah_1.2" 

# df['Cycle_No'].iloc[0]=1
df['RTC'] = df['RTC'].str.replace(':000.000', ".000")
df['Time_Elapsed'] = df['Time_Elapsed'].str.replace(':000.000', ".000")
df['Time_Spent_in_Step'] = df['Time_Spent_in_Step'].str.replace(':000.000', ".000")

#%%
# df['RTC'] = pd.to_datetime(df['RTC'], format = '%Y-%m-%d %H:%M:%S',errors='coerce')
df['RTC'] = pd.to_datetime(df['RTC'], format = '%m/%d/%Y %H:%M:%S',errors='coerce')

#%%
# df['RTC'] = df['RTC'].str.replace(':000.000', ".000")
# df['Time_Elapsed'] = df['Time_Elapsed'].str.replace(':000.000', ".000")

# df['Cycle_No']=df['Cycle_No'].fillna(method='ffill')
# df['Step_Type']=df['Step_Type'].fillna(method='ffill')
# df['Cycle_No']=df['Cycle_No'].fillna(method='bfill')

#%%
# df['RTC']=pd.to_datetime(df['RTC'], errors='coerce',format= "%Y-%m-%d %H:%M:%S" )  # arranges time in ascending order 


# df['Cycle_No']=df['Cycle_No'].fillna(method='bfill')

print('1/4................') 
#%% extract step info
df2=df[(df.Voltage>25)]
df2 = df2.drop(["Step_No","Step_Type","Time_Spent_in_Step","Q_in_Step","Q_in_and_out_Step","Start_Voltage","Energy_in_out","End_Voltage","Chg_Mid_Vtg","DCIR","RTC","a1","T_cell","OCV"] , axis=1) #,"y","a2","a3","a4","a5","Power"
df2['Q_in_out'] = pd.to_numeric(df2['Q_in_out'], errors='coerce')
df2 = df2.dropna(subset=['Q_in_out'])
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
df2['Energy_Efficiency']= ((df2.Energy_out_cycle) / (df2.Energy_in_cycle))* 100
df2['Energy_Efficiency'] = df2['Energy_Efficiency'].replace(np.inf,100)
cols = list(df2.columns)
a, b = cols.index('DChg_Mid_Vtg'), cols.index('Energy_Efficiency')
cols[b], cols[a] = cols[a], cols[b]
df2 = df2[cols]
print('2/4................') 
#%% extract cycle info
df3 = df[pd.notnull(df['Step_No'])]
df3 = df3.drop(["Cycle_No","Record_ID","Time_Elapsed","Voltage","Current","Q_in_out","Energy_in_out","RTC","a1","OCV"], axis=1) #,"y","a2","a3","a4","a5","Power"

#%% remove nan and space and replace by uppper data
df.replace(' ',np.nan,inplace=True)
df=df.fillna(method='ffill')

#%%
df=df[df['RTC'].dt.year>=2016]
df=df.sort_values(by='RTC',ascending=True)

df=df.reset_index(drop=True)

#%% reset indices
df3 = df3.reset_index(drop=True)
df2 = df2.reset_index(drop=True)
print('3/4................')
#%% gives continuous cycle numbers to all
new_cyc_no_s = np.array(df.a1); new_cyc_no=np.asfarray(new_cyc_no_s,float)
new_cyc_no1_s = np.array(df2.Cycle_No); new_cyc_no1=np.asfarray(new_cyc_no1_s,float)
new_cyc_no2_s = np.array(df3.Step_No); new_cyc_no2=np.asfarray(new_cyc_no2_s,float)

#%%
cno=0; 
for i in range(1, len(df.Cycle_No)-1):
    new_cyc_no[i] = cno
    k = int(df.Cycle_No[i+1])-int(df.Cycle_No[i])
    # l = int(df.Step_No[i+1])-int(df.Step_No[i])
    try:
        l = int(df.Step_No[i+3])-int(df.Step_No[i+1])
    except KeyError: 
        l=1
    if k!=0:
        if k==1 and l==0:
            cno = cno+1
            
        else:
            continue

#%%        
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


#df['Time_Spent_in_Step'] = df['Time_Spent_in_Step'].str.replace(':000.000', ".000")

# df['RTC'] = pd.to_datetime(df['RTC'], format = '%Y-%m-%d %H:%M:%S')
# df['RTC'] = pd.to_datetime(df['RTC'], format = '%m/%d/%Y %H:%M:%S')
## df['Time_Elapsed'] = pd.to_datetime(df['Time_Elapsed'], format = '%H:%M:%S.%f')

# df['Time_Spent_in_Step'] = pd.to_datetime(df['Time_Spent_in_Step'], format = '%H:%M:%S.%f') # commented for PHY variable temp data
df['Time_Spent_in_Step'] = pd.to_datetime(df['Time_Spent_in_Step'], format = '%H:%M:%S',errors='coerce')

df = df.drop(["Start_Voltage","End_Voltage","Chg_Mid_Vtg","DCIR","T_cell","IR","OCV","Power", 'Unnamed: 56', 'Unnamed: 57', 'Unnamed: 58',
       'Unnamed: 59', 'Unnamed: 60', 'Unnamed: 61', 'Unnamed: 62',
       'Unnamed: 63', 'Unnamed: 64', 'Unnamed: 65'] , axis=1) #,"a1","y","a2","a3","a4","a5","Power" ,'Net Engy_DChg(mWh).1', 'Energy Efficiency', 'Unnamed: 56', 'Unnamed: 57', 'Unnamed: 58', 'Unnamed: 59', 'Unnamed: 60','Unnamed: 61', 'Unnamed: 62', 'Unnamed: 63', 'Unnamed: 64','Unnamed: 65',
# df = df.drop(['ShowAuxVolt','ShowAuxTemp',"Chg_Mid_Vtg","DCIR","T_cell","OCV","y","Power",
#        'Capacitance_DChg(F)', 'DChgCap(mAh)', 'rd(mO)', 'ChgEng(mWh)',
#        'Mid_value Voltage(V)', 'DChgEng(mWh)', 'Discharge Fading Ratio(%)','NetDChgCap(mAh)', 'Charge Time', 'NetDChgEng(mWh)', 'Discharge Time',
#        'OriStepID', 'Charge IR(mO)', 'Discharge IR(mO)', 'End Temp()',
#        'Unnamed: 51', 'Net_Cap_DChg(mAh)', 'Unnamed: 53', 'Net_Engy_DChg(mWh)'] , axis=1) # Variable Temp PHY

print(df.dtypes)

print('Raw Dataframe created') 
#%%    
cycles_key=[5,5,20,12,8,10,9,11,1,3,16,12,30,8,15,7,8,2,1]
temp_key=[16.5,19.5,22.5,25.5,28.5,37.5,40.5,43.5,49.5,46.5,37.5,37.5,34.5,31.5,31.5,28.5,22.5,16.5,19.5]
count=0

while (count<=df['New_Cycle_No'].max()):
    for i in range(len(cycles_key)):
        df.loc[(df['New_Cycle_No']>=count) & (df['New_Cycle_No']<count+cycles_key[i]),'T_amb']=temp_key[i]
        count=count+cycles_key[i]
    
 
dff=df.head(30000)
dfl=df.tail(30000)

#%%
df2[['Charge_out_cycle']] = df2[['Charge_out_cycle']].astype(float)
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

#%%
All_Info_df.to_csv(fin_path+'\\'+fin_name+'_AllCycles_AllCycles_raw_test.csv') # save the sorted txt file as a pickle file name as filename_raw
# Cycle_Info_df.to_csv(fin_path+'\\'+fin_name+'_AllCycles_Cycles_Info_raw.csv') # save the sorted txt file as a pickle file name as filename_raw
# Step_Info_df.to_csv(fin_path+'\\'+fin_name+'_AllCycles_Steps_Info_raw.csv')
# del df,df2,df3,All_Info_df,Cycle_Info_df,Step_Info_df
# os.remove(name.rsplit("\\",1)[0]+"\\tempfile.csv")

print("--- %s seconds ---" % (time.time() - start_time))
