# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 15:24:03 2024

@author: IITM
"""

#%% Code Description

"""
1. This code is used to check the datalogger data obtained during the test
"""

#%% Import necessary libraries
import pandas as pd
import numpy as np
import math

#%% Path to the file to be processed
# BMS file is given as "file"
# Datalogger file is given as "dlog_f"
# Tester data is given as "t_file"
file = r"C:\Users\IITM\Downloads\10kwh pack 0.3C cyc test data 29.10.2024 1.xlsx"
dlog_f = r"D:\Benisha\LTVS\10kWh\Re_In_house_testing\New_Cycles\Farhan_Testing\06-09-2024\Dlog_LTVS_10kWh_pack_current_test_06-09-2024_datalogger.xlsx"
t_file = ""

# cols = ['Date','Hours','Minutes','Seconds','milliseconds','Pack_Hall_Sensor',
#         'External_Hall_Sensor','Temperature_on_External_Hall_Sensor','Ambient_Temperature'] Ambient Temperature

cols = ['ID', 'Date','Hours','Minutes','Seconds','milliseconds','SS-1',
        'External_Hall_Sensor','Temperature_on_External_Hall_Sensor','Ambient_Temperature_Dlogger', 'SS-2']


# The path to the file is split to get the path to the folder, to save the file
img_path=file.rsplit('\\',1)[0]
filename=file.rsplit('\\',1)[1].rsplit('.',1)[0]

#%% 
# Read the excel file
data=pd.read_excel(file,index_col=False, sheet_name='GPIO Data')

# Cleaning the data file by removing junk values
data = data[data['AFE_GPIO_instant_value']<=2.5]
data = data[data['AFE_GPIO_instant_value']>0]
tester_data = pd.read_excel(t_file, index_col = False, sheet_name = 'Tester data')

rt_data = pd.read_excel(file,index_col=False, sheet_name='Ambient Temperature')
shunt_data = pd.read_excel(file,index_col=False, sheet_name='Shunt Data')
dlog_data = pd.read_excel(dlog_f, names=cols, index_col = False)

#%% Data pre-processing
shunt_data['Shunt_instant_value'] = shunt_data['Shunt_instant_value'].replace('(NaN)',0)
shunt_data['Shunt_instant_value'] = (shunt_data['Shunt_instant_value'].astype(float))*0.001
dlog_data['Date'] = '2024-09-06'                         

dlog_data['DateTime']=np.nan
dlog_data['DateTime']=dlog_data['Date'].astype(str)+' '+dlog_data['Hours'].astype(str)+':'+dlog_data['Minutes'].astype(str)+':'+dlog_data['Seconds'].astype(str)

dlog_data['DateTime'] = pd.to_datetime(dlog_data['DateTime'],format='%Y-%m-%d %H:%M:%S',
                                errors='coerce')

dlog_data.drop_duplicates(subset = ['DateTime'], keep = 'first'
                                           , inplace = True)
dlog_data=dlog_data.drop(['Date','Hours','Minutes','Seconds','milliseconds'],axis=1)

tester_data.drop_duplicates(subset = ['Date'], keep = 'first', 
                            inplace=True)

#%%
# dlog_data['Pack_Hall_Sensor'] = dlog_data['Pack_Hall_Sensor']*0.001
# dlog_data['External_Hall_Sensor'] = dlog_data['External_Hall_Sensor']*0.001

#%% Merge dataframes based on the datetime column
c_data=pd.merge(left= data, right= dlog_data, on='DateTime') 
p=list(data.columns)
r=list(dlog_data.columns)
r.remove('DateTime')
p.extend(r)
c_data.columns = p

#%% Merge current data and the ambient temperature dataframes by the datetime column
d_data=pd.merge(left= c_data, right= rt_data, on='DateTime')
p=list(c_data.columns)
r=list(rt_data.columns)
r.remove('DateTime')
p.extend(r)
d_data.columns = p

#%%
e_data=pd.merge(left= d_data, right= shunt_data, on='DateTime')
p=list(d_data.columns)
r=list(shunt_data.columns)
r.remove('DateTime')
p.extend(r)
e_data.columns = p

#%% 
f_data=pd.merge(left= e_data, right= tester_data, left_on='DateTime', right_on='Date')
p=list(e_data.columns)
r=list(tester_data.columns)
# r.remove('Date')
p.extend(r)
f_data.columns = p

#%% 

# f_data['Approximated_Current'] = np.where((f_data['Current(A)']>=3) & (f_data['Current(A)']<=-3), (f_data['Current(A)']*10).apply(lambda x: (math.trunc(x))/10) , f_data['Current(A)'].apply(lambda x:round(x,0)))

#%%

# f_data['Approximated_Current'] = np.where(f_data['Current(A)']<=-3, f_data['Current(A)'].apply(lambda x:round(x,0)), (f_data['Current(A)']*10).apply(lambda x: (math.trunc(x))/10))

# f_data['Approximated_Current'] = np.where(f_data['Current(A)']>=3, f_data['Current(A)'].apply(lambda x:round(x,0)), f_data['Approximated_Current'])


#%%
f_data['Check_Current'] = np.where(f_data['Current(A)']<=-2.7, f_data['Current(A)'].apply(lambda x:round(x,0)), (f_data['Current(A)']*10).apply(lambda x: (math.trunc(x))/10))

f_data['Check_Current'] = np.where(f_data['Current(A)']>=2.7, f_data['Current(A)'].apply(lambda x:round(x,0)), f_data['Check_Current'])

#%%
f_data['Current_val'] = round(f_data['Current(A)'],3)

#%%
f_data['Approximated_Current'] = round(f_data.groupby(['Check_Current'])['Current_val'].transform('mean'),3)

#%% Save modified excel files
path = img_path+'\\'+filename+'_dlog_merged.xlsx'
writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
f_data.to_excel(writer, sheet_name = 'Hall Sensor data',index=False)
writer.close()

#%% Assign chg/dchg state in file
f_data['State'] = np.where(f_data['Current(A)']>=0, 'Chg', 'Dchg')

#%% Separate test data into 25 degC, 35 degC and 45 degC
deg_25 = f_data[f_data['Ambient_Temperature_Dlogger']<=30]
deg_35 = f_data[(f_data['Ambient_Temperature_Dlogger']>30) & (f_data['Ambient_Temperature_Dlogger']<=40)]
deg_45 = f_data[(f_data['Ambient_Temperature_Dlogger']>40) & (f_data['Ambient_Temperature_Dlogger']<=50)]

#%%
ss1 = []
ss2 = []
hl2 = []
afe_gpio=[]
shunt_inst = []

#%% A function that returns min/max/median depending on the chg/dchg state
def f(x, val):
    if x['State'].iloc[0] == 'Chg':
        # return x[val].min()
        return x[val].median()
    else:
        # return x[val].max()
        return x[val].median()
    
#%%  
for i in [deg_25,deg_35,deg_45]:
    ss1.append(i.groupby(['Check_Current'], as_index = False).apply(f, 'SS-1'))
    ss2.append(i.groupby(['Check_Current'], as_index = False).apply(f, 'SS-2'))
    hl2.append(i.groupby(['Check_Current'], as_index = False).apply(f, 'External_Hall_Sensor'))
    afe_gpio.append(i.groupby(['Check_Current'], as_index = False).apply(f, 'AFE_GPIO_instant_value'))
    shunt_inst.append(i.groupby(['Check_Current'], as_index = False).apply(f, 'Shunt_instant_value'))

#%% Drop duplicates to avoid redundancy
deg_25.drop_duplicates(subset = ['Check_Current'],
                     inplace = True, keep = 'first')

deg_35.drop_duplicates(subset = ['Check_Current'],
                     inplace = True, keep = 'first')

deg_45.drop_duplicates(subset = ['Check_Current'],
                     inplace = True, keep = 'first')

#%% Change column names
names = [ 'SS-1', 'SS-2', 'External_Hall_Sensor', 'AFE_GPIO_instant_value', 'Shunt_instant_value']

for i in range(len(ss1)):
    ss1[i].columns = ['Check_Current', names[0]]
    ss2[i].columns = ['Check_Current', names[1]]
    hl2[i].columns = ['Check_Current', names[2]]
    afe_gpio[i].columns = ['Check_Current', names[3]]
    shunt_inst[i].columns = ['Check_Current', names[4]]

#%% Merge different temperature data

for j in [ss1, ss2, hl2, afe_gpio, shunt_inst]:
    deg_25 = pd.merge(deg_25, j[0], on='Check_Current')
    deg_35 = pd.merge(deg_35, j[1], on='Check_Current')
    deg_45 = pd.merge(deg_45, j[2], on='Check_Current')

    
#%% Rename column names with duplicate names(which are named _x, _y, etc., by default)

deg_25 = deg_25.rename(columns = {'SS-1_y':'SS-1', 'SS-2_y':'SS-2', 
                                  'External_Hall_Sensor_y':'External_Hall_Sensor', 
                                  'AFE_GPIO_instant_value_y':'AFE_GPIO_instant_value',
                                  'Shunt_instant_value_y':'Shunt_instant_value'})
deg_35 = deg_35.rename(columns = {'SS-1_y':'SS-1', 'SS-2_y':'SS-2', 
                                  'External_Hall_Sensor_y':'External_Hall_Sensor', 
                                  'AFE_GPIO_instant_value_y':'AFE_GPIO_instant_value',
                                  'Shunt_instant_value_y':'Shunt_instant_value'})
deg_45 = deg_45.rename(columns = {'SS-1_y':'SS-1', 'SS-2_y':'SS-2', 
                                  'External_Hall_Sensor_y':'External_Hall_Sensor', 
                                  'AFE_GPIO_instant_value_y':'AFE_GPIO_instant_value',
                                  'Shunt_instant_value_y':'Shunt_instant_value'})

 
#%% Create a new excel file and write the dataframes into different sheets

path = img_path+'\\'+filename+'_Current_1.xlsx'
writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
deg_25.to_excel(writer, sheet_name = '25 deg data',index=False)
deg_35.to_excel(writer, sheet_name = '35 deg data',index=False)
deg_45.to_excel(writer, sheet_name = '45 deg data',index=False)
writer.close()