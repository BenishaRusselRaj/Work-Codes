# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 16:40:56 2022

@author: IITM
"""

import pandas as pd
import os


#%% Reads the necessary files
d1=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\Input\\INCBE0010102E3000809_Combined_cyclesData_filtered_test.csv") 
d2=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\Input\\INCBE0010102E3001409_Combined_cyclesData_filtered_test.csv")
d3=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\Input\\INCBE0010223H3005009_Combined_cyclesData_filtered_test.csv")
d4=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\Input\\INCBE0010230H3002309_Combined_cyclesData_filtered_test.csv")
d5=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\Input\\INCBE0010230H3002609_Combined_cyclesData_filtered_test.csv")
d6=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\Input\\INCBE0010230H3002709_Combined_cyclesData_filtered_test.csv")
d7=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\Input\\INCBE0010102E3001709_Combined_cyclesData_filtered_test.csv")
d8=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\Input\\INEXC0010102E3002009_Combined_cyclesData_filtered_test.csv")
d9=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\Input\\INEXC0010230H3002809_Combined_cyclesData_filtered_test.csv")

#%% Creates a file path for the output file to be stored
file_path="C:\\Users\\IITM\\Downloads\\Average_temperatures_\\Temperature_Added_files" # could be any path

if not os.path.exists(file_path):
    os.makedirs(file_path)
#%%
d1=d1[d1['T_pack_Min']>=10] # because d1 has temperature values less than 1
l=[d1,d2,d3,d4,d5,d6,d7,d8,d9]
l1=['Bin','Session_Type','Bin_Max_Temp','Bin_Min_Temp','Bin_Avg_Temp']
l2=['Bin_Max_Temp','Bin_Min_Temp','Bin_Avg_Temp']
df_binwise=pd.DataFrame(index=range(0,len(d1)),columns=l1)
x=0
    
#%%
for f in l:
    grouped=f.groupby(['Session_Type'],sort=False) # to compute the values for each session type separately
    result=[g[1] for g in grouped]
    for i in range(0,len(result)):
        result[i]=result[i].reset_index(drop=True)
        df_binwise['Bin'].loc[x]=result[i]['bin'].iloc[0]
        df_binwise['Session_Type'].loc[x]=result[i]['Session_Type'].iloc[0]
        df_binwise['Bin_Max_Temp'].loc[x]=result[i]['T_pack_Max'].mean()   # mean because .max() gave really large values
        df_binwise['Bin_Min_Temp'].loc[x]=result[i]['T_pack_Min'].min()
        df_binwise['Bin_Avg_Temp'].loc[x]=result[i]['T_pack_Avg'].mean()
        for j in l2:
            if df_binwise[j].iloc[x]>45:  # special requirements; to change any temperature value >45 to a constant: 35 deg C
                df_binwise[j].iloc[x]=35
            if df_binwise[j].iloc[x]>35: # special requirements; to change any temperature value >35 to a constant: 30 deg C
                df_binwise[j].iloc[x]=30
        x=x+1
#%%
df_binwise=df_binwise.dropna(subset=['Bin']) # Drops unnecessary rows with no values 
df_binwise.to_csv(file_path+'\\Temperature_Added_File_filtered_T_max.csv') # saves the file in csv format