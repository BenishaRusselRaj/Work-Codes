# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 12:48:01 2023

@author: IITM
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta


#%%
# file="D:\\Benisha\\10p15s_LFP\\23_10_10\\Static Test\\pack_static_test 10-10-2023.xlsx"
file="D:\\Benisha\\10p15s_LFP\\Current Calibration test\\Dchg\\Dot3mOhm_CM_calibration_60A_DHG.xlsx"
file_tester="D:\\Benisha\\10p15s_LFP\\Current Calibration test\\Dchg\\Dot3mOhm_CM0_4_60A_DHG_tester_data_31-10-2023.xlsx"
# file="D:\\Benisha\\10p15s_LFP\\Capacity Test\\23_10_06\\c_3_1cycle.xlsx"
cols=['Date','Time','CV_tag','val1','val2','val_3','val_4','val_5','val_6_PV','val_7','val_8','val_9','val_10','val_11','val_12','val_13','val_14','val_15','junk','junk','junk','Die Temperature']
cols=['Date','Time','junk','ADC','junk','junk','ADC_filtered','junk','Pack Current','junk','A1','junk','A2']


data=pd.read_excel(file,names=cols,index_col=False) #,sheet_name='chg and dchg 20-09-2023 (2)'
tester_data=pd.read_excel(file_tester,sheet_name='record')
tester_data['Date']=pd.to_datetime(tester_data['Date'],format='%Y-%m-%d %H:%M:%S',errors='coerce')
#%%
data['Date']=data['Date'].str.replace('[','',regex=True)
data['Time']=data['Time'].str.replace(']','',regex=True)

data['Time']=data['Time'].astype(str)
data[['Time_format','string']]=data['Time'].str.split('.',expand=True)

data['DateTime']=data['Date'].astype(str)+' '+data['Time_format']
#%%
data['DateTime']=pd.to_datetime(data['DateTime'],format='%Y-%m-%d %H:%M:%S',errors='coerce')

data=data[['DateTime'] + [col for col in data.columns if col!='DateTime']]
data=data.drop(['Time_format','string'],axis=1)
data['DateTime']=data['DateTime']+timedelta(minutes=7,seconds=19)
#%%
temperature_data=data[data['CV_tag']=='AUX'].dropna(how='all',axis=1).reset_index(drop=True)
max_min_data=data[data['CV_tag']=='OV/UV'].reset_index(drop=True).dropna(how='all',axis=1)
pack_details=data[data['CV_tag']=='LTime'].dropna(how='all',axis=1).reset_index(drop=True)

#%% columns names
v_names=[f'V_{x}' for x in range(1,16)]
t_names=['DateTime','Date','Time','junk','junk','Aux_V1','Aux_V2','Aux_V3','Aux_V4','Aux_V5','Aux_V6','Aux_V7','Aux_V8','Aux_V9','junk','T1','T2','T3','T4','T5','junk','junk','Die_Temperature'] # junk *9
# Final detail_names:
# detail_names=['DateTime','Date','Time','junk','LTime(ms)','junk','junk','junk','junk','junk','junk','Pack Voltage','junk','Pack Current','junk','Pack State','junk','Capacity(Ah)','junk','Cycle No','junk','junk']

detail_names=['DateTime','Date','Time','junk','LTime(ms)','junk','junk','junk','junk','Pack Voltage','junk','Pack Current','junk','Pack State','junk','junk','junk','junk','junk','junk','junk','Capacity(Ah)','junk']

max_min_names=['DateTime','Date','Time','junk','junk','junk','junk','junk','junk','junk','junk','OV/UV Flag','junk','Cell_Max_V_BMS','junk','Cell_Min_V_BMS','junk','delmlV_BMS'] #14 junk

status=['DateTime','Date','Time','junk','junk','Pack Status','junk','Shutdown','Normal','junk','junk','Precharge Relay','junk','junk','Main Relay']

pack_details.columns=detail_names
max_min_data.columns=max_min_names
temperature_data.columns=t_names

pack_details=pack_details.drop([col for col in pack_details.columns if "junk" in col], axis=1)
max_min_data=max_min_data.drop([col for col in max_min_data.columns if "junk" in col], axis=1)

pack_details['LTime(ms)']=pack_details['LTime(ms)'].str.extract(r'(\d{1,})') ## can comment
#%%
voltage_data=data[data['CV_tag']=='CV:'].dropna(how='all',axis=1).reset_index(drop=True)

voltage_data=voltage_data.drop([col for col in voltage_data.columns if "junk" in col], axis=1)
voltage_data=voltage_data.drop([col for col in voltage_data.columns if "tag" in col], axis=1)

#%%
for i,n in enumerate(['DateTime','Date','Time']):
    v_names.insert(i,n)

#%%
voltage_data.columns=v_names


for i in range(1,16):
    voltage_data['V_'+str(i)]=voltage_data['V_'+str(i)].astype(str).str.extract(r'(\d{5,})').fillna(method='ffill').astype(int)
    

#%%
voltage_data['Mean_V']=voltage_data.loc[:,'V_1':'V_15'].mean(axis=1)
voltage_data['Min_V']=voltage_data.loc[:,'V_1':'V_15'].min(axis=1)
voltage_data['Max_V']=voltage_data.loc[:,'V_1':'V_15'].max(axis=1)

voltage_data['Min_V']=voltage_data['Min_V'].astype(str).str.extract(r'(\d{5,})').fillna(method='ffill').astype(int)
voltage_data['Max_V']=voltage_data['Max_V'].astype(str).str.extract(r'(\d{5,})').fillna(method='ffill').astype(int)
max_min_data['Cell_Max_V_BMS']=max_min_data['Cell_Max_V_BMS'].astype(str).str.extract(r'(\d{5,})').fillna(method='ffill').astype(int)
#%% Calculating Capacity_calculated and energy

pack_details['Time_in_sec_s']=(pack_details['DateTime']-pack_details['DateTime'].shift(1))/np.timedelta64(1,'s')# time difference b/w every datapt
pack_details['Time_in_sec']=(pack_details['DateTime']-pack_details['DateTime'].iloc[0])/np.timedelta64(1,'s')

pack_details['Pack Current']=pack_details['Pack Current'].astype(float)
# pack_details['Capacity']=np.where(pack_details['Capacity']>80,np.nan,pack_details['Capacity'])

#%%
pack_details['State']=np.nan
pack_details['Time_in_sec_s_cap']=np.where((pack_details['Time_in_sec_s']>300),np.nan,pack_details['Time_in_sec_s'])
pack_details['State']=np.where(pack_details['Pack Current']>1,0,pack_details['State'])
pack_details['State']=np.where(pack_details['Pack Current']<-2,1,pack_details['State'])
pack_details['State']=pack_details['State'].fillna(2)

#%% the Capacity 100 issue solution

# index=pack_details[pack_details['Capacity(Ah)']==100].index[0]
# diff=pack_details.loc[index,'Capacity(Ah)']-pack_details.loc[index-1,'Capacity(Ah)']
# pack_details.loc[index:,'Capacity(Ah)']=pack_details.loc[index:,'Capacity(Ah)']-diff
#%%
pack_details['Cap_inst_dt']=pack_details['Time_in_sec_s_cap']*abs(pack_details['Pack Current'])/3600
pack_details['Capacity_calculated_dt']=pack_details['Cap_inst_dt'].groupby(pack_details['State']).cumsum()
pack_details['Capacity_calculated_chg_dt']=(pack_details[pack_details['State']==0]['Cap_inst_dt']).cumsum()
pack_details['Capacity_calculated_dchg_dt']=(pack_details[pack_details['State']==1]['Cap_inst_dt']).cumsum()

pack_details['Capacity_calculated_chg_dt']=pack_details['Capacity_calculated_chg_dt'].fillna(method='bfill')
pack_details['Capacity_calculated_dchg_dt']=pack_details['Capacity_calculated_dchg_dt'].fillna(method='bfill')

pack_details['Energy_calculated_dt']=pack_details['Capacity_calculated_dt']*pack_details['Pack Voltage']
pack_details['Energy_calculated_chg_dt']=pack_details['Capacity_calculated_chg_dt']*pack_details['Pack Voltage']
pack_details['Energy_calculated_dchg_dt']=pack_details['Capacity_calculated_dchg_dt']*pack_details['Pack Voltage']


#%%
pack_details['LTime(ms)']=pack_details['LTime(ms)'].astype(float)
pack_details['Cap_inst']=pack_details['LTime(ms)']*abs(pack_details['Pack Current'])/3600
pack_details['Capacity_calculated']=pack_details['Cap_inst'].groupby(pack_details['State']).cumsum()
pack_details['Capacity_calculated_chg']=(pack_details[pack_details['State']==0]['Cap_inst']).cumsum()
pack_details['Capacity_calculated_dchg']=(pack_details[pack_details['State']==1]['Cap_inst']).cumsum()

pack_details['Capacity_calculated_chg']=pack_details['Capacity_calculated_chg'].fillna(method='bfill')
pack_details['Capacity_calculated_dchg']=pack_details['Capacity_calculated_dchg'].fillna(method='bfill')

pack_details['Energy_calculated']=pack_details['Capacity_calculated']*pack_details['Pack Voltage']
pack_details['Energy_calculated_chg']=pack_details['Capacity_calculated_chg']*pack_details['Pack Voltage']
pack_details['Energy_calculated_dchg']=pack_details['Capacity_calculated_dchg']*pack_details['Pack Voltage']
#%%
voltage_data['delV']=voltage_data.loc[:,'V_1':'V_15'].max(axis=1)-voltage_data.loc[:,'V_1':'V_15'].min(axis=1)
voltage_data['delV_check']=voltage_data['Max_V']-voltage_data['Min_V']

dt_merged=pd.merge(pack_details,voltage_data,how='left')

# for i in range(1,16):
# #     voltage_data['V_'+str(i)]=voltage_data['V_'+str(i)].astype(str).str.extract(r'(\d{5,})').fillna(method='ffill').astype(int)
#     dt_merged['Rest_Std_deviation_V_'+str(i)]=np.where(dt_merged['Pack Current']==0,np.sqrt(np.sum((dt_merged['V_'+str(i)]-dt_merged['V_'+str(i)].mean())**2)/len(dt_merged)),np.nan)
    
# dt_merged['BMS_PV_Std_deviation']=np.where(dt_merged['Pack Current']==0,np.sqrt(np.sum((dt_merged['Pack Voltage']-dt_merged['Pack Voltage'].mean())**2)/len(dt_merged)),np.nan)
# dt_merged.loc[:,'Rest_Std_deviation_V_1':'BMS_PV_Std_deviation']=dt_merged.loc[:,'Rest_Std_deviation_V_1':'BMS_PV_Std_deviation'].fillna(method='ffill')
# dt_merged.loc[:,'Rest_Std_deviation_V_1':'BMS_PV_Std_deviation']=dt_merged.loc[:,'Rest_Std_deviation_V_1':'BMS_PV_Std_deviation'].fillna(method='bfill')

#%%
dt_merged_PC=pd.merge(pack_details,tester_data,left_on='DateTime',right_on='Date',how='left')
dt_merged_PC['Pack_Current_diff']=dt_merged_PC['Pack Current']-dt_merged_PC['Current(A)']
dt_merged_PC['Pack_Voltage_diff']=dt_merged_PC['Pack Voltage']-dt_merged_PC['Voltage(V)']
dt_merged_PC['Pack_Capacity_diff']=dt_merged_PC['Capacity(Ah)_x']-dt_merged_PC['Capacity(Ah)_y']

#%%
# plt.plot()
# f, ax = plt.subplots()
# ax.plot(pack_details['DateTime'],pack_details['Voltage Flag'])

# plt.grid(linestyle='dotted')
# plt.title('Voltage Flag',fontweight='bold')

# #%%
# plt.plot()
# f, ax = plt.subplots()
# ax.plot(pack_details['DateTime'],pack_details['Temperature Flag'])

# plt.grid(linestyle='dotted')
# plt.title('Temperature Flag',fontweight='bold')

# #%%
# plt.plot()
# f, ax = plt.subplots()
# ax.plot(pack_details['DateTime'],pack_details['Current Flag'])

# plt.grid(linestyle='dotted')
# plt.title('Current Flag',fontweight='bold')
#%%
# plt.plot()
f, ax = plt.subplots()
ax.plot(voltage_data['DateTime'],voltage_data.loc[:,'V_1':'V_15']*0.1)

plt.ylabel('Voltage(mV)',fontweight='bold')
plt.xlabel('DateTime',fontweight='bold')
plt.legend([f'V_{x}' for x in range(1,16)])
plt.grid(linestyle='dotted')
plt.title('Cell Voltage',fontweight='bold')
plt.show()


#%%
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Pack Current'],label='BMS Current')
ax.plot(tester_data['Date'],tester_data['Current(A)'],label='Tester Current')

plt.legend()
plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Current(A)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Current',fontweight='bold')
plt.show()
#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Pack Voltage'],label='BMS Voltage')
ax.plot(tester_data['Date'],tester_data['Voltage(V)'],label='Tester Voltage')

plt.legend()
plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Voltage(V)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Voltage',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Capacity(Ah)'],label='BMS Capacity')
ax.plot(tester_data['Date'],tester_data['Capacity(Ah)'],label='Tester Capacity')

plt.legend()
plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Voltage(V)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Capacity',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Capacity_calculated_chg_dt'])

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Capacity(Ah)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Charging Capacity_datetime(Calculated)',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Capacity_calculated_chg']*0.001)

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Capacity(Ah)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Charging Capacity_Ltime(Calculated)',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Capacity_calculated_dchg_dt'])

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Capacity(Ah)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Discharging Capacity_datetime (Calculated)',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Capacity_calculated_dchg']*0.001)

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Capacity(Ah)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Discharging Capacity_Ltime (Calculated)',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Energy_calculated_chg']*0.001)

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Energy(kWh)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Charging Energy_Ltime (Calculated)',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Energy_calculated_dchg']*0.001)

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Energy(kWh)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Discharging Energy_Ltime (Calculated)',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Energy_calculated_chg_dt']*0.001)

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Energy(kWh)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Charging Energy_datetime (Calculated)',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Energy_calculated_dchg_dt']*0.001)

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Energy(kWh)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Discharging Energy_datetime (Calculated)',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(voltage_data['DateTime'],(voltage_data['delV'])*0.1,label='delV')
ax.plot(max_min_data['DateTime'],max_min_data['delmlV_BMS'],label='delV_BMS')
plt.ylabel('Voltage(mV)',fontweight='bold')
plt.xlabel('DateTime',fontweight='bold')
plt.grid(linestyle='dotted')
plt.legend()
plt.title('Voltage difference(delV)',fontweight='bold')
plt.show()

#%% ,,'junk',,'junk',
plt.plot()
f, ax = plt.subplots()
ax.plot(voltage_data['DateTime'],voltage_data['Mean_V']*0.1)
plt.ylabel('Voltage(V)',fontweight='bold')
plt.xlabel('DateTime',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Average Voltage_calculated',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(voltage_data['DateTime'],voltage_data['Min_V'],label='Min_V')
ax.plot(max_min_data['DateTime'],max_min_data['Cell_Min_V_BMS'],label='Min_V_BMS')
ax.ticklabel_format(useOffset=False,axis='y')
plt.ylabel('Voltage(V)',fontweight='bold')
plt.xlabel('DateTime',fontweight='bold')
plt.grid(linestyle='dotted')
plt.legend()
plt.title('Minimum Voltage',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(voltage_data['DateTime'],voltage_data['Max_V'],label='Max_V')
ax.plot(max_min_data['DateTime'],max_min_data['Cell_Max_V_BMS'],label='Max_V_BMS')
plt.ylabel('Voltage(V)',fontweight='bold')
plt.xlabel('DateTime',fontweight='bold')
plt.legend()
plt.grid(linestyle='dotted')
plt.title('Maximum Voltage',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(dt_merged_PC['DateTime'],dt_merged_PC['Pack_Current_diff'])
plt.ylabel('Current(A)',fontweight='bold')
plt.xlabel('DateTime',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('BMS and Tester Pack Current Difference',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(dt_merged_PC['DateTime'],dt_merged_PC['Pack_Capacity_diff'])
plt.ylabel('Capacity(Ah)',fontweight='bold')
plt.xlabel('DateTime',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('BMS and Tester Pack Capacity Difference',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(dt_merged_PC['DateTime'],dt_merged_PC['Pack_Voltage_diff'])
plt.ylabel('Voltage(V)',fontweight='bold')
plt.xlabel('DateTime',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('BMS and Tester Pack Voltage Difference',fontweight='bold')
plt.show()

# %%
# path=file.rsplit('.',1)[0]+'_modified.xlsx'
# writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
# voltage_data.to_excel(writer, sheet_name = 'Cell Voltage',index=False)
# temperature_data.to_excel(writer, sheet_name = 'Cell Temperature',index=False)
# pack_details.to_excel(writer,sheet_name='Pack pack_details',index=False)
# # status_data.to_excel(writer,sheet_name='Pack Status',index=False)
# max_min_data.to_excel(writer,sheet_name='Max Min Mean',index=False)
# dt_merged.loc[:0,'Rest_Std_deviation_V_1':'BMS_PV_Std_deviation'].to_excel(writer,sheet_name='Standard Deviation',index=False)
# writer.close()

# #%%
# f=open(file.rsplit('.',1)[0]+'_observations.txt',"w")

# print('======================================================================',file=f)
# print('---------------------Current Data---------------------',file=f)
# print('Datapoints:%s' % (len(voltage_data)),file=f)
# print('Total Time Spent:%s minutes' % ((voltage_data['DateTime'].iloc[-1]-voltage_data['DateTime'].iloc[0])/np.timedelta64(1,'m')),file=f)
# print('Maximum Charging Current:%s ; Minimum Charging Current:%s' % (pack_details[pack_details['State']==0]['Pack Current'].max(),pack_details[pack_details['State']==0]['Pack Current'].min()),file=f)
# print('Maximum Discharging Current:%s ; Minimum Discharging Current:%s' % (pack_details[pack_details['State']==1]['Pack Current'].max(),pack_details[pack_details['State']==1]['Pack Current'].min()),file=f)
# print('Maximum Charging Capacity:%s ; Minimum Charging Capacity:%s' % (pack_details['Capacity_calculated_chg'].max(),pack_details['Capacity_calculated_chg'].min()),file=f)
# print('Maximum Discharging Capacity:%s ; Minimum Discharging Capacity:%s' % (pack_details['Capacity_calculated_dchg'].max(),pack_details['Capacity_calculated_dchg'].min()),file=f)
# print('Maximum Charging Energy:%s ; Minimum Charging Energy:%s' % (pack_details['Energy_calculated_chg'].max(),pack_details['Energy_calculated_chg'].min()),file=f)
# print('Maximum Discharging Energy:%s ; Minimum Discharging Energy:%s' % (pack_details['Energy_calculated_dchg'].max(),pack_details['Energy_calculated_dchg'].min()),file=f)
# # print('Maximum Charging Energy(BMS):%s ; Minimum Charging Energy(BMS):%s' % (pack_details['Charging Energy'].max(),pack_details['Charging Energy'].min()),file=f)
# # print('Maximum Discharging Energy(BMS):%s ; Minimum Discharging Energy(BMS):%s' % (pack_details['Discharging Energy'].max(),pack_details['Discharging Energy'].min()),file=f)
# # print('Maximum delT:%s' %(temperature_data['delT'].max()),file=f)
# print('======================================================================',file=f)

# f.close()
