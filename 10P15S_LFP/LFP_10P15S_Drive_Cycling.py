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
# file="D:\\Benisha\\10p15s_LFP\\Drive_Test_Data\\drive_test_07-11-2023.xlsx"
file="D:\\Benisha\\10p15s_LFP\\Static Test\\23_11_09\\pack_static_test 08-11-2023.xlsx"

cols=['Date','Time','CV_PV_tag','val1','val2','val_3','val_4','val_5','val_6_PV','val_7','val_8','val_9','val_10','val_11','val_12','val_13','val_14','val_15','ADC_tag','ADC_value','junk','junk']

data=pd.read_excel(file,names=cols,index_col=False) #,sheet_name='chg and dchg 20-09-2023 (2)'
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
temperature_data=data[data['CV_PV_tag']=='Temp:'].dropna(how='all',axis=1).reset_index(drop=True)
max_min_data=data[data['CV_PV_tag']=='OV/UV'].reset_index(drop=True).dropna(how='all',axis=1)
pack_details=data[data['CV_PV_tag']=='LTime(ms):'].dropna(how='all',axis=1).reset_index(drop=True)
acc_data=data[data['CV_PV_tag']=='accX:'].dropna(how='all',axis=1).reset_index(drop=True)
flag_data=data[data['CV_PV_tag']=='PC_S:'].dropna(how='all',axis=1).reset_index(drop=True)

#%% columns names
v_names=[f'V_{x}' for x in range(1,16)]
t_names=['DateTime','Date','Time','junk','T1','T2','T3','T4','T5','T6','junk','junk','Die_Temperature'] # junk *9
# Final detail_names:
# detail_names=['DateTime','Date','Time','junk','LTime(ms)','junk','junk','junk','junk','junk','junk','Pack Voltage','junk','Pack Current','junk','Pack State','junk','Capacity(Ah)','junk','Cycle No','junk','junk']

detail_names=['DateTime','Date','Time','junk','Ltime(ms)','junk','junk','junk','junk','junk','junk','Pack Voltage','junk','Pack Current','junk','Pack State','junk','Capacity(Ah)','junk','Cycle','junk','Ah_int']

max_min_names=['DateTime','Date','Time','junk','junk','OV/UV_Flag1','OV/UV_Flag2','OV/UV_Flag3','junk','junk','junk','OV/UV_Flags','junk','Cell_Max_V_BMS','junk','Cell_Min_V_BMS','junk','delmlV_BMS'] #14 junk

acc=['DateTime','Date','Time','junk','acc_X','junk','acc_Y','junk','acc_Z','junk','IMU_Temperature']

flag=['DateTime','Date','Time','junk','Pre_Contactor_state','junk','Main_Contactor_state','junk','Voltage_flag','junk','Temperature_flag','junk','Current_flag','junk','Prot_flag','junk','Rest_flag','junk','ProtCnt','junk','main_CC','junk','M_FB']


pack_details.columns=detail_names
max_min_data.columns=max_min_names
temperature_data.columns=t_names
acc_data.columns=acc
flag_data.columns=flag

pack_details=pack_details.drop([col for col in pack_details.columns if "junk" in col], axis=1)
max_min_data=max_min_data.drop([col for col in max_min_data.columns if "junk" in col], axis=1)
flag_data=flag_data.drop([col for col in flag_data.columns if "junk" in col], axis=1)

#%%
voltage_data=data[data['CV_PV_tag']=='CV:'].dropna(how='all',axis=1).reset_index(drop=True)

voltage_data=voltage_data.drop([col for col in voltage_data.columns if "junk" in col], axis=1)
voltage_data=voltage_data.drop([col for col in voltage_data.columns if "tag" in col], axis=1)

#%%
for i,n in enumerate(['DateTime','Date','Time']):
    v_names.insert(i,n)
v_names.append('ADC_value')
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
max_min_data['delmlV_BMS']=max_min_data['delmlV_BMS'].astype(str).str.extract(r'(\d{1,})').fillna(method='ffill').astype(int)

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
# voltage_data['delV']=voltage_data.loc[:,'V_1':'V_15'].max(axis=1)-voltage_data.loc[:,'V_1':'V_15'].min(axis=1)
voltage_data['delV']=voltage_data['Max_V']-voltage_data['Min_V']

voltage_data['Capacity_diff']=pack_details['Capacity(Ah)']-(abs(pack_details['Capacity_calculated_dchg_dt']-pack_details['Capacity_calculated_dchg_dt'].max()))

dt_merged=pd.merge(pack_details,voltage_data,how='left')

#%%
temperature_data['delT']=temperature_data.loc[:,'T1':'T6'].max(axis=1)-temperature_data.loc[:,'T1':'T6'].min(axis=1)

#%%
flag_data['Contactor_Feedback']=np.where(flag_data['M_FB']>1000,'Open','Close')
flag_data['Current_flag']=flag_data['Current_flag'].astype(str).str.extract(r'(\d{1,})').fillna(method='ffill').astype(str)

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
plt.figure()
plt.plot(temperature_data['DateTime'],temperature_data.loc[:,'T1':'T6'])
plt.ylabel('Temperature('+u'\N{DEGREE SIGN}'+'C)',fontweight='bold')
plt.xlabel('DateTime',fontweight='bold')
plt.legend([f'T_{x}' for x in range(1,7)])
plt.grid(linestyle='dotted')
plt.title('Cell Temperature',fontweight='bold')
plt.show()

#%%
plt.figure()
plt.plot(temperature_data['DateTime'],temperature_data['delT'])
plt.ylabel('Temperature('+u'\N{DEGREE SIGN}'+'C)',fontweight='bold')
plt.xlabel('DateTime',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Temperature difference(delT)',fontweight='bold')
plt.show()
#%%
plt.figure()
plt.plot(temperature_data['DateTime'],temperature_data['Die_Temperature'])
plt.ylabel('Temperature('+u'\N{DEGREE SIGN}'+'C)',fontweight='bold')
plt.xlabel('DateTime',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Die Temperature',fontweight='bold')
plt.show()

#%%
plt.figure()
plt.plot(acc_data['DateTime'],acc_data['IMU_Temperature'])
plt.ylabel('Temperature('+u'\N{DEGREE SIGN}'+'C)',fontweight='bold')
plt.xlabel('DateTime',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('IMU Temperature',fontweight='bold')
plt.show()

#%%
plt.figure()
plt.plot(flag_data['DateTime'],flag_data['Current_flag'])
plt.xlabel('DateTime',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Current Flag',fontweight='bold')
plt.show()
#%%
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Pack Current'])

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Current(A)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Current',fontweight='bold')
plt.show()
#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Pack Voltage'],marker='o',markersize=4)

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Voltage(V)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Voltage',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Capacity(Ah)'])

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Capacity(Ah)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Capacity',fontweight='bold')
plt.show()

#%%
plt.figure()
plt.plot(voltage_data['DateTime'],voltage_data['Capacity_diff'])

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Capacity (Ah)',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Capacity Difference',fontweight='bold')
plt.show()

#%%
f,ax=plt.subplots(3)

ax[0].plot(flag_data['DateTime'],flag_data['Pre_Contactor_state'],marker='o',markersize=4)
ax[0].set_title('Pre Contactor State',fontweight='bold')
ax[0].grid()

ax[1].plot(flag_data['DateTime'],flag_data['Main_Contactor_state'],marker='o',markersize=4)
ax[1].set_title('Main Contactor State',fontweight='bold')
ax[1].grid()

ax[2].plot(flag_data['DateTime'],flag_data['Contactor_Feedback'],marker='o',markersize=4)
ax[2].set_title('Contactor Feedback',fontweight='bold')

plt.xlabel('DateTime',fontweight='bold')
plt.tight_layout()
plt.show()

#%%
f,ax=plt.subplots(3)

ax[0].plot(acc_data['DateTime'],acc_data['acc_X'])
ax[0].set_title('X-axis acceleration',fontweight='bold')
ax[0].grid()

ax[1].plot(acc_data['DateTime'],acc_data['acc_Y'])
ax[1].set_ylabel('Acceleration(g)',fontweight='bold')
ax[1].set_title('Y-axis acceleration',fontweight='bold')
ax[1].grid()

ax[2].plot(acc_data['DateTime'],acc_data['acc_Z'])
ax[2].set_title('Z-axis acceleration',fontweight='bold')
ax[2].grid()

plt.grid(linestyle='dotted')
plt.xlabel('DateTime',fontweight='bold')
plt.tight_layout()
plt.show()

#%%
# plt.plot()
# f, ax = plt.subplots()
# ax.plot(pack_details['DateTime'],pack_details['Capacity_calculated_chg_dt'])

# plt.xlabel('DateTime',fontweight='bold')
# plt.ylabel('Capacity(Ah)',fontweight='bold')

# plt.grid(linestyle='dotted')
# plt.title('Pack Charging Capacity_datetime(Calculated)',fontweight='bold')
# plt.show()


#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],pack_details['Capacity_calculated_dchg_dt'])

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Capacity(Ah)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Discharging Capacity (Calculated)',fontweight='bold')
plt.show()

#%%
plt.plot()
f, ax = plt.subplots()
ax.plot(pack_details['DateTime'],abs(pack_details['Capacity_calculated_dchg_dt']-pack_details['Capacity_calculated_dchg_dt'].max()))

plt.xlabel('DateTime',fontweight='bold')
plt.ylabel('Capacity(Ah)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack-Capacity (Calculated)',fontweight='bold')
plt.show()
#%%
# plt.plot()
# f, ax = plt.subplots()
# ax.plot(pack_details['DateTime'],pack_details['Energy_calculated_chg_dt']*0.001)

# plt.xlabel('DateTime',fontweight='bold')
# plt.ylabel('Energy(kWh)',fontweight='bold')

# plt.grid(linestyle='dotted')
# plt.title('Pack Charging Energy_datetime (Calculated)',fontweight='bold')
# plt.show()

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
plt.ylabel('Voltage(mV)',fontweight='bold')
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
plt.ylabel('Voltage(10^-1*mV)',fontweight='bold')
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
plt.ylabel('Voltage(10^-1*mV)',fontweight='bold')
plt.xlabel('DateTime',fontweight='bold')
plt.legend()
plt.grid(linestyle='dotted')
plt.title('Maximum Voltage',fontweight='bold')
plt.show()


# %%
path=file.rsplit('.',1)[0]+'_modified.xlsx'
writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
voltage_data.to_excel(writer, sheet_name = 'Cell Voltage',index=False)
temperature_data.to_excel(writer, sheet_name = 'Cell Temperature',index=False)
pack_details.to_excel(writer,sheet_name='Pack details',index=False)
# status_data.to_excel(writer,sheet_name='Pack Status',index=False)
max_min_data.to_excel(writer,sheet_name='Max Min Mean',index=False)
# dt_merged.loc[:0,'Rest_Std_deviation_V_1':'BMS_PV_Std_deviation'].to_excel(writer,sheet_name='Standard Deviation',index=False)
writer.close()

#%%
f=open(file.rsplit('.',1)[0]+'_observations.txt',"w")

print('======================================================================',file=f)
print('---------------------Current Data---------------------',file=f)
print('Datapoints:%s' % (len(voltage_data)),file=f)
print('Total Time Spent:%s minutes' % ((voltage_data['DateTime'].iloc[-1]-voltage_data['DateTime'].iloc[0])/np.timedelta64(1,'m')),file=f)
print('Maximum Charging Current:%s ; Minimum Charging Current:%s' % (pack_details[pack_details['State']==0]['Pack Current'].max(),pack_details[pack_details['State']==0]['Pack Current'].min()),file=f)
print('Maximum Discharging Current:%s ; Minimum Discharging Current:%s' % (pack_details[pack_details['State']==1]['Pack Current'].max(),pack_details[pack_details['State']==1]['Pack Current'].min()),file=f)
print('Maximum Charging Capacity:%s ; Minimum Charging Capacity:%s' % (pack_details['Capacity_calculated_chg_dt'].max(),pack_details['Capacity_calculated_chg_dt'].min()),file=f)
print('Maximum Discharging Capacity:%s ; Minimum Discharging Capacity:%s' % (pack_details['Capacity_calculated_dchg_dt'].max(),pack_details['Capacity_calculated_dchg_dt'].min()),file=f)
print('Maximum Charging Energy:%s ; Minimum Charging Energy:%s' % (pack_details['Energy_calculated_chg_dt'].max(),pack_details['Energy_calculated_chg_dt'].min()),file=f)
print('Maximum Discharging Energy:%s ; Minimum Discharging Energy:%s' % (pack_details['Energy_calculated_dchg_dt'].max(),pack_details['Energy_calculated_dchg_dt'].min()),file=f)
print('Maximum Capacity(BMS):%s ; Minimum Capacity(BMS):%s' % (pack_details['Capacity(Ah)'].max(),pack_details['Capacity(Ah)'].min()),file=f)

print('Maximum delT:%s' %(temperature_data['delT'].max()),file=f)
print('======================================================================',file=f)

f.close()
