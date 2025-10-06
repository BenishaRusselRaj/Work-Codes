# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:04:41 2023

@author: IITM
"""
"""
LFP 10P15S current calibration test
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# from datetime import timedelta

#%%
file="D:\\Benisha\\10p15s_LFP\\Current Calibration test\\Dchg\\Dot3mOhm_CM_calibration_60A_DHG.xlsx"
file_tester="D:\\Benisha\\10p15s_LFP\\Current Calibration test\\Dchg\\Dot3mOhm_CM0_4_60A_DHG_tester_data_31-10-2023.xlsx"

# file="D:\\Benisha\\10p15s_LFP\\Current Calibration test\\Chg\\Dot3mOhm_CM_calibration_60A_CHG.xlsx"
# file_tester="D:\\Benisha\\10p15s_LFP\\Current Calibration test\\Chg\\Dot3mOhm_CM0_4_60A_CHG_tester_data_31-10-2023.xlsx"

cols=['Date','Time','junk','ADC','junk','junk','ADC_filtered','junk','Pack Current','junk','A1','junk','A2']

data=pd.read_excel(file,names=cols,index_col=False) 
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
# data['DateTime']=data['DateTime']+timedelta(minutes=7,seconds=19) #May or may not be needed

#%%
data=data.drop([col for col in data.columns if 'junk' in col],axis=1)

data['Pack Current']=data['Pack Current'].astype(float)

#%%
dt_merged=pd.merge(data,tester_data,left_on='DateTime',right_on='Date',how='right')

#%%
# dt_merged['Current(A)']=dt_merged['Current(A)']*-1
dt_merged['Pack_Current_diff']=dt_merged['Pack Current']-dt_merged['Current(A)']
dt_merged['Pack_Current_diff']=np.where((dt_merged['Pack_Current_diff']>-1)&(dt_merged['Pack_Current_diff']<0.8),dt_merged['Pack_Current_diff'],np.nan)
dt_merged['Pack_Current_diff']=dt_merged['Pack_Current_diff']*1000


dt_merged['Time_in_sec_s']=(dt_merged['DateTime']-dt_merged['DateTime'].shift(1))/np.timedelta64(1,'s')# time difference b/w every datapt
dt_merged['Time_in_sec']=(dt_merged['DateTime']-dt_merged['DateTime'].iloc[0])/np.timedelta64(1,'s')

#%%
def poly(x,a,b,c):
    return a*x**2+b*x+c

#%%
fitval,_=curve_fit(poly,dt_merged['Time_in_sec'],dt_merged['T2(℃)'])
a1,b1,c1=fitval
dt_merged['T2_fit']=a1*dt_merged['Time_in_sec']**2+b1*dt_merged['Time_in_sec']+c1

#%%

# dt_merged['d(T2)']=dt_merged['T2(℃)']-dt_merged['T2(℃)'].shift(1)
dt_merged['d(T2)/dt']=(dt_merged['T2_fit']-dt_merged['T2_fit'].shift(1))/dt_merged['Time_in_sec_s']

# dt_merged['d(T2)/dt']=np.where(dt_merged['d(T2)/dt']<0.01,np.nan,dt_merged['d(T2)/dt'])
dt_merged['d(T2)/dt']=dt_merged['d(T2)/dt'].fillna(method='ffill')
dt_merged['d(T2)/dt']=dt_merged['d(T2)/dt'].fillna(method='bfill')
# dt_merged['d(T2)/dt']=(dt_merged['T2(℃)'].rolling(5).median()-dt_merged['T2(℃)'].shift(1).rolling(5).median())/dt_merged['Time_in_sec_s']
# dt_merged['d(T2)/dt']=dt_merged['d(T2)/dt'].fillna(0)
# dt_merged['d(T2)/dI']=dt_merged['d(T2)']/(dt_merged['Current(A)']-dt_merged['Current(A)'].shift(1))

#%%
def linear(x,a,b):
    return a*x+b

#%%
# dt_merged['ADC_filtered_c']=np.where((dt_merged['ADC_filtered']>25000),dt_merged['ADC_filtered'],np.nan) #chg
dt_merged['ADC_filtered_c']=np.where((dt_merged['ADC_filtered']<24800),dt_merged['ADC_filtered'],np.nan) #dchg
dt_merged['ADC_filtered_c']=dt_merged['ADC_filtered_c'].fillna(method='ffill')
dt_merged['ADC_filtered_c']=dt_merged['ADC_filtered_c'].fillna(method='bfill')

#%%
dt_merged['ADC_diff']=dt_merged['ADC_filtered_c']-dt_merged['ADC_filtered_c'].shift(1)

while (dt_merged['ADC_diff']<-1400).any(): # change numbers as per need (dt_merged['ADC_diff']>1400).any() #chg
    l1=dt_merged.index[dt_merged['ADC_diff']<-1400].tolist() #dt_merged.index[dt_merged['ADC_diff']>1400].tolist() #chg
    # print(l1)
    for n,i in enumerate(l1):
        dt_merged.loc[i,'ADC_filtered_c']=dt_merged.loc[i-1,'ADC_filtered_c']
    dt_merged['ADC_diff']=dt_merged['ADC_filtered_c'].shift(1)-dt_merged['ADC_filtered_c']

# dt_merged['ADC_filtered_c']=dt_merged['ADC_filtered_c'].rolling(25).mean()
dt_merged['ADC_filtered_c']=dt_merged['ADC_filtered_c'].fillna(method='bfill')
dt_merged['ADC_filtered_c']=dt_merged['ADC_filtered_c'].fillna(method='ffill')

                                                          #%%
# dt_merged['Current(A)_c']=np.where((dt_merged['Current(A)']>0.3),dt_merged['Current(A)'],np.nan) #chg
dt_merged['Current(A)_c']=np.where((dt_merged['Current(A)']<-0.3),dt_merged['Current(A)'],np.nan) #dchg
dt_merged['Current(A)_c']=dt_merged['Current(A)_c'].fillna(method='ffill')
dt_merged['Current(A)_c']=dt_merged['Current(A)_c'].fillna(method='bfill')

fitval_I,_=curve_fit(linear,dt_merged['ADC_filtered_c'],dt_merged['Current(A)_c'])
a_i,b_i=fitval_I
dt_merged['ADC_filtered_fit']=a_i*dt_merged['ADC_filtered_c']+b_i

#%%
dt_merged['ADC_R_squared_num']=(dt_merged['ADC_filtered_fit']-dt_merged['Current(A)_c'])**2
dt_merged['ADC_R_squared_denom']=(dt_merged['ADC_filtered_fit']-dt_merged['Current(A)_c'].mean())**2
ADC_R_Squared=1-(dt_merged['ADC_R_squared_num'].sum()/dt_merged['ADC_R_squared_denom'].sum())

#%%Chg 
# Maximum_T=np.array(dt_merged.loc[dt_merged['Current(A)']>57,'T2_fit'])
# Maximum_T_rate=np.array(dt_merged.loc[dt_merged['Current(A)']>57,'d(T2)/dt'])

#%%DChg
Maximum_T=np.array(dt_merged.loc[dt_merged['Current(A)']<-58,'T2_fit'])
Maximum_T_rate=np.array(dt_merged.loc[dt_merged['Current(A)']<-58,'d(T2)/dt'])

#%%
dt_merged['Tester_Current_peak']=dt_merged.loc[(dt_merged['Current(A)']-dt_merged['Current(A)'].shift(1))>0, 'DateTime']
dt_merged['BMS_Current_peak']=dt_merged.loc[(dt_merged['Pack Current']-dt_merged['Pack Current'].shift(1))>0, 'DateTime']
dt_merged['Tester_Current_peak']=dt_merged['Tester_Current_peak'].fillna(method='bfill')
dt_merged['Tester_Current_peak']=dt_merged['Tester_Current_peak'].fillna(method='ffill')
dt_merged['BMS_Current_peak']=dt_merged['BMS_Current_peak'].fillna(method='bfill')
dt_merged['BMS_Current_peak']=dt_merged['BMS_Current_peak'].fillna(method='ffill')

dt_merged['Current_Offset_value']=((dt_merged['BMS_Current_peak']-dt_merged['Tester_Current_peak'])/np.timedelta64(1,'s'))
dt_merged['Current_Offset_value']=np.where(dt_merged['Current_Offset_value']<0,np.nan,dt_merged['Current_Offset_value'])
dt_merged['Current_Offset_value']=dt_merged['Current_Offset_value'].fillna(method='bfill')
dt_merged['Current_Offset_value']=dt_merged['Current_Offset_value'].fillna(method='ffill')
#%%
# plt.figure()
# plt.plot(dt_merged['DateTime'],dt_merged['T1(℃)'])
# plt.xlabel('DateTime',fontweight='bold')
# plt.ylabel('Temperature (℃)',fontweight='bold')
# plt.title('Ambient Temperature',fontweight='bold')
# plt.grid(linestyle='dotted')
# plt.show()

# #%%
# plt.figure()
# plt.plot(dt_merged['DateTime'],dt_merged['T2(℃)'],marker='o',markersize=4,label='Actual Shunt Temperature')
# plt.plot(dt_merged['DateTime'],dt_merged['T2_fit'],label='Fit')
# plt.xlabel('DateTime',fontweight='bold')
# plt.ylabel('Temperature ('+u'\N{DEGREE SIGN}'+'C)',fontweight='bold')
# plt.legend()
# plt.title('Shunt Temperature',fontweight='bold')
# plt.grid(linestyle='dotted')
# plt.show()

# #%%
# plt.figure()

# plt.plot(dt_merged['T2_fit'],dt_merged['Current(A)'])
# # plt.xlabel('DateTime',fontweight='bold')
# plt.xlabel('Temperature ('+u'\N{DEGREE SIGN}'+'C)',fontweight='bold')
# plt.ylabel('Current (A)',fontweight='bold')

# plt.title('Temperature Fit Vs. Current',fontweight='bold')
# plt.grid(linestyle='dotted')
# plt.show()

# #%%
# plt.figure()
# # plt.scatter(dt_merged['d(T2)/dt'],dt_merged['Current(A)'],s=5) ,marker='o',markersize=4
# plt.plot(dt_merged['d(T2)/dt'],dt_merged['Current(A)'])
# # plt.plot(dt_merged['DateTime'],dt_merged['Current(A)'])
# # plt.xlabel('DateTime')
# plt.xlabel('dT/dt',fontweight='bold')
# plt.ylabel('Current (A)',fontweight='bold')
# plt.title('Temperature Rate change with Current',fontweight='bold')
# plt.grid(linestyle='dotted')
# plt.show()

# #%%
# plt.figure()
# plt.plot(dt_merged['DateTime'],dt_merged['Pack Current'],label='BMS_Current')
# plt.plot(dt_merged['DateTime'],dt_merged['Current(A)'],label='Tester_Current')
# # plt.scatter(dt_merged['DateTime'],dt_merged['Pack_Current_diff'],s=5,label='Difference')
# plt.xlabel('DateTime',fontweight='bold')
# plt.ylabel('Current (A)',fontweight='bold')
# plt.legend()
# plt.title('Pack Current',fontweight='bold')
# plt.grid(linestyle='dotted')
# plt.show()

# # #%%
# # plt.figure()
# # plt.plot(dt_merged['DateTime'],dt_merged['Current(A)'])
# # plt.xlabel('DateTime')
# # plt.ylabel('Current (A)')
# # plt.grid(linestyle='dotted')
# # plt.title('Pack Current (Tester)')
# # plt.show()

# #%%
# plt.figure()
# plt.scatter(dt_merged['DateTime'],dt_merged['Pack_Current_diff'],s=5)
# plt.xlabel('DateTime',fontweight='bold')
# plt.ylabel('Current (mA)',fontweight='bold')
# plt.grid(linestyle='dotted')
# plt.title('Pack Current Peak Difference',fontweight='bold')
# plt.show()

# #%%
# plt.figure()
# plt.scatter(dt_merged['Current_Offset_value'],dt_merged['Current(A)'],s=4)
# plt.xlabel('Offset Time(seconds)',fontweight='bold')
# plt.ylabel('Tester Current (A)',fontweight='bold')
# plt.title('Time offset between BMS and tester current',fontweight='bold')
# plt.grid(linestyle='dotted')
# plt.show()

# #%%
# # plt.figure()
# # plt.plot(dt_merged['DateTime'],dt_merged['ADC_filtered'],label='ADC_filtered',marker='o',markersize=4)
# # plt.plot(dt_merged['DateTime'],dt_merged['ADC_filtered_fit'],label='Fit')
# # plt.xlabel('DateTime',fontweight='bold')
# # plt.grid(linestyle='dotted')
# # plt.title('ADC_fit',fontweight='bold')
# # plt.show()

#%%
plt.figure()
plt.plot(dt_merged['ADC_filtered_c'],dt_merged['Current(A)_c'],label='ADC_filtered_cleaned',marker='o',markersize=4)
plt.plot(dt_merged['ADC_filtered_c'],dt_merged['ADC_filtered_fit'],label='Fit')
plt.xlabel('ADC',fontweight='bold')
plt.ylabel('Tester Current(A)',fontweight='bold')
plt.legend()
plt.grid(linestyle='dotted')
plt.title('ADC_fit',fontweight='bold')
plt.show()

#%%
plt.figure()
plt.plot(dt_merged['ADC_filtered_c'],dt_merged['Current(A)_c'],label='ADC_filtered',marker='o',markersize=4)
plt.xlabel('ADC',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('ADC Vs. Tester Current',fontweight='bold')
plt.show()
#%%
f=open(file.rsplit('.',1)[0]+'_Values.txt',"w")

print('======================================================================',file=f)
print('Shunt Temperature fit Equation: y=%s*x^2+%s*x+%s' %(a1,b1,c1), file=f)
print('ADC fit Equation (y-Tester Current;x-ADC value): y=%s*x+%s' %(a_i,b_i), file=f)
print('R Squared (for ADC fit): %s' %ADC_R_Squared, file=f)
print('Maximum Temperature after 58A: \n%s' %Maximum_T, file=f)
print('Temperature rate(dT/dt) after 58A(Positive rate means an increase in temperature): \n%s' %Maximum_T_rate, file=f)
# print('Maximum Charging Energy(BMS):%s ; Minimum Charging Energy(BMS):%s' % (pack_details['Charging Energy'].max(),pack_details['Charging Energy'].min()),file=f)
# print('Maximum Discharging Energy(BMS):%s ; Minimum Discharging Energy(BMS):%s' % (pack_details['Discharging Energy'].max(),pack_details['Discharging Energy'].min()),file=f)
# print('Maximum delT:%s' %(temperature_data['delT'].max()),file=f)
print('======================================================================',file=f)

f.close()