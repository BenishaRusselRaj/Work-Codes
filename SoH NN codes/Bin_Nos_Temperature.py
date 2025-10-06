# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 16:12:45 2022

@author: IITM
"""


import pandas as pd
import numpy as np
import glob

files=glob.glob("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\*.csv")

l=[]
for i in range(0,len(files)):
    l.append('d'+str(i))

for i,f1 in enumerate(files):
    l[i]=pd.read_csv(f1)

#%%
# d1=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\INCBE0010102E3000809_Combined_cyclesData_filtered_test.csv") 
# d2=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\INCBE0010102E3001409_Combined_cyclesData_filtered_test.csv")
# d3=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\INCBE0010223H3005009_Combined_cyclesData_filtered_test.csv")
# d4=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\INCBE0010230H3002309_Combined_cyclesData_filtered_test.csv")
# d5=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\INCBE0010230H3002609_Combined_cyclesData_filtered_test.csv")
# d6=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\INCBE0010230H3002709_Combined_cyclesData_filtered_test.csv")
# d7=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\INCBE0010102E3001709_Combined_cyclesData_filtered_test.csv")
# d8=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\INEXC0010102E3002009_Combined_cyclesData_filtered_test.csv")
# d9=pd.read_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\INEXC0010230H3002809_Combined_cyclesData_filtered_test.csv")

    
#%%
l[0]=l[0][l[0]['T_pack_Min']>=10]
# l=[d1,d2,d3,d4,d5,d6,d7,d8,d9]
cols=['Bin','Session_Type','Bin_Max_Temp','Bin_Min_Temp','Bin_Avg_Temp']
l1=['Bin_Max_Temp','Bin_Min_Temp','Bin_Avg_Temp']
df_binwise=pd.DataFrame(index=range(0,len(l[0])),columns=cols)
x=0
    
#%%
for f in l:
    grouped=f.groupby(['Session_Type'],sort=False)
    result=[g[1] for g in grouped]
    for i in range(0,len(result)):
        result[i]=result[i].reset_index(drop=True)
        df_binwise['Bin'].loc[x]=result[i]['bin'].iloc[0]
        df_binwise['Session_Type'].loc[x]=result[i]['Session_Type'].iloc[0]
        df_binwise['Bin_Max_Temp'].loc[x]=result[i]['T_pack_Max'].max()
        df_binwise['Bin_Min_Temp'].loc[x]=result[i]['T_pack_Min'].min()
        df_binwise['Bin_Avg_Temp'].loc[x]=result[i]['T_pack_Avg'].mean()
        for j in l1:
            if df_binwise[j].iloc[x]>45:
                df_binwise[j].iloc[x]=35
            if df_binwise[j].iloc[x]>35:
                df_binwise[j].iloc[x]=30
        x=x+1
#%%
df_binwise=df_binwise.dropna(subset=['Bin'])
df_binwise.to_csv("C:\\Users\\IITM\\Downloads\\Average_temperatures_\\Temperature_Added_File_filtered.csv")