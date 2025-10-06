# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:27:25 2022

@author: IITM
"""
import pandas as pd
import glob

#%%
path="D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_5"

#%% Charging
# state='Charging'
# f1=path+"\\*\\*\\*\\-charging_periodic_graph_data.xlsx_modified.xlsx"
# f2=path+"\\*\\*\\-charging_periodic_graph_data (1).xlsx_modified.xlsx"
# f3=path+"\\*\\*\\-charging_periodic_graph_data.xlsx_modified.xlsx"
# f4=path+"\\*\\*\\*\\-charging_periodic_graph_data (1).xlsx_modified.xlsx"


# f5=path+"\\*\\*\\-charging_periodic_graph_data(1).xlsx_modified.xlsx"
# f6=path+"\\*\\*\\*\\-charging_periodic_graph_data(1).xlsx_modified.xlsx"
#%% driving
state='driving'
f1=path+"\\*\\*\\*\\-battery_periodic_graph_data.xlsx_modified.xlsx"
f2=path+"\\*\\*\\-battery_periodic_graph_data (1).xlsx_modified.xlsx"
f3=path+"\\*\\*\\-battery_periodic_graph_data.xlsx_modified.xlsx"
f4=path+"\\*\\*\\*\\-battery_periodic_graph_data (1).xlsx_modified.xlsx"


# f5=path+"\\*\\*\\-battery_periodic_graph_data(1).xlsx_modified.xlsx"
# f6=path+"\\*\\*\\*\\-battery_periodic_graph_data(1).xlsx_modified.xlsx"
#%%
files=glob.glob(f1)
cols=['Start_DateTime','End_DateTime','Start_SoC_BMS','End_SoC_BMS','Start_SoC_calculated','End_SoC_calculated','Capacity_calculated']
data=pd.DataFrame(index=range(100),columns=cols)
k=0
#%%
for f in files:
    df=pd.read_excel(f)
    data.iloc[k]['Start_DateTime']=df['DateTime'].iloc[0]
    data.iloc[k]['End_DateTime']=df['DateTime'].iloc[-1]
    try:
        data.iloc[k]['Start_SoC_BMS']=df.loc[df['State Of Charge'].first_valid_index()]['State Of Charge']
        data.iloc[k]['End_SoC_BMS']=df.loc[df['State Of Charge'].last_valid_index()]['State Of Charge']
    except KeyError:
        pass
#%%
    data.iloc[k]['Start_SoC_calculated']=df['SoC'].iloc[3]
    data.iloc[k]['End_SoC_calculated']=df['SoC'].iloc[-1]
    data.iloc[k]['Capacity_calculated']=df['Capacity'].iloc[-1]
    k=k+1
    
pack_no=f1.split('\\',4)[3]

#%%

files2=glob.glob(f2)

for f in files2:
    df=pd.read_excel(f)
    data.iloc[k]['Start_DateTime']=df['DateTime'].iloc[0]
    data.iloc[k]['End_DateTime']=df['DateTime'].iloc[-1]
    try:
        data.iloc[k]['Start_SoC_BMS']=df.loc[df['State Of Charge'].first_valid_index()]['State Of Charge']
        data.iloc[k]['End_SoC_BMS']=df.loc[df['State Of Charge'].last_valid_index()]['State Of Charge']
    except KeyError:
        pass
    data.iloc[k]['Start_SoC_calculated']=df['SoC'].iloc[3]
    data.iloc[k]['End_SoC_calculated']=df['SoC'].iloc[-1]
    data.iloc[k]['Capacity_calculated']=df['Capacity'].iloc[-1]
    k=k+1
    
#%%

files3=glob.glob(f3)
for f in files3:
    df=pd.read_excel(f)
    data.iloc[k]['Start_DateTime']=df['DateTime'].iloc[0]
    data.iloc[k]['End_DateTime']=df['DateTime'].iloc[-1]
    try:
        data.iloc[k]['Start_SoC_BMS']=df.loc[df['State Of Charge'].first_valid_index()]['State Of Charge']
        data.iloc[k]['End_SoC_BMS']=df.loc[df['State Of Charge'].last_valid_index()]['State Of Charge']
    except KeyError:
        pass
    data.iloc[k]['Start_SoC_calculated']=df['SoC'].iloc[3]
    data.iloc[k]['End_SoC_calculated']=df['SoC'].iloc[-1]
    data.iloc[k]['Capacity_calculated']=df['Capacity'].iloc[-1]
    k=k+1
#%%

files4=glob.glob(f4)

for f in files4:
    df=pd.read_excel(f)
    data.iloc[k]['Start_DateTime']=df['DateTime'].iloc[0]
    data.iloc[k]['End_DateTime']=df['DateTime'].iloc[-1]
    try:
        data.iloc[k]['Start_SoC_BMS']=df.loc[df['State Of Charge'].first_valid_index()]['State Of Charge']
        data.iloc[k]['End_SoC_BMS']=df.loc[df['State Of Charge'].last_valid_index()]['State Of Charge']
    except KeyError:
        pass
    data.iloc[k]['Start_SoC_calculated']=df['SoC'].iloc[3]
    data.iloc[k]['End_SoC_calculated']=df['SoC'].iloc[-1]
    data.iloc[k]['Capacity_calculated']=df['Capacity'].iloc[-1]
    k=k+1   
#%%
# files5=glob.glob(f5)

# for f in files5:
#     df=pd.read_excel(f)
#     data.iloc[k]['DateTime']=df['DateTime'].iloc[0]
#     try:
#         data.iloc[k]['Start_SoC_BMS']=df['State Of Charge'].iloc[0]
#         data.iloc[k]['End_SoC_BMS']=df['State Of Charge'].iloc[-1]
#     except KeyError:
#         pass
#     data.iloc[k]['Start_SoC_calculated']=df['SoC'].iloc[3]
#     data.iloc[k]['End_SoC_calculated']=df['SoC'].iloc[-1]
#     data.iloc[k]['Capacity_calculated']=df['Capacity'].iloc[-1]
#     k=k+1   

# #%%
# files6=glob.glob(f6)

# for f in files6:
#     df=pd.read_excel(f)
#     data.iloc[k]['DateTime']=df['DateTime'].iloc[0]
#     try:
#         data.iloc[k]['Start_SoC_BMS']=df['State Of Charge'].iloc[0]
#         data.iloc[k]['End_SoC_BMS']=df['State Of Charge'].iloc[-1]
#     except KeyError:
#         pass
#     data.iloc[k]['Start_SoC_calculated']=df['SoC'].iloc[3]
#     data.iloc[k]['End_SoC_calculated']=df['SoC'].iloc[-1]
#     data.iloc[k]['Capacity_calculated']=df['Capacity'].iloc[-1]
#     k=k+1   

#%%
data=data.dropna(axis=0,how='all')
data=data.sort_values(by='Start_DateTime')

data.to_excel(path+"\\"+pack_no+"_"+state+"_SoC_BMS_and_Calculated.xlsx")