# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 16:28:22 2024

@author: IITM
"""

#%% Code Description

"""
1. This code was written for a one-time case wherein the data was manually processed already
2. The data had different format compared to the usual header format
3. This specific case is unlikely to be repeated
"""

#%% Import necessary libraries
import pandas as pd
import numpy as np
import datetime

#%% Reading the file and initial processing
# Input the file path in this line; do not remove the 'r' befor the file path
f1=r"D:\Benisha\LTVS\Final_Report\Capacity Test data\pack testing with BMS for calibration-- Tester and BMS_09_12_2023.xlsx"

# Give the sheet name here
name="record"
name='Pack Tester data of current& PV'

# Read the excel file using read_excel() command of the pandas library
vol_data=pd.read_excel(f1,sheet_name=name)

# Give the number of cells here
v_no=17 # number of cells
t_no=17 # number of thermistor values available; sometimes it is less than the # of cells, so it is given separately

# Change the date column to the proper format
vol_data['Date']=pd.to_datetime(vol_data['Date'],format='%Y-%m-%d %H:%M:%S',errors='coerce')

#%% Calculate the mean voltage, mean temperature and delV/delT values

vol_data['Mean_V']=vol_data.loc[:,'V1':'V'+str(v_no-1)].mean(axis=1)
vol_data['delV']=vol_data.loc[:,'V1':'V'+str(v_no-1)].max(axis=1)-vol_data.loc[:,'V1':'V'+str(v_no-1)].min(axis=1)
    
vol_data['Mean_T']=vol_data.loc[:,'T1':'T'+str(t_no-1)].mean(axis=1)
vol_data['delT']=vol_data.loc[:,'T1':'T'+str(t_no-1)].max(axis=1)-vol_data.loc[:,'T1':'T'+str(t_no-1)].min(axis=1)

#%% The pack state is defined from the pack current values
# '0' refers to the charge state
# '1' refers to the discharge state
# '2' refers to the rest state

vol_data['State']=np.nan
vol_data['State']=np.where(vol_data['Current(A)']>0,0,vol_data['State'])
vol_data['State']=np.where(vol_data['Current(A)']<0,1,vol_data['State'])
vol_data['State']=np.where(vol_data['Current(A)']==0,2,vol_data['State'])

#%% 
# df=pd.DataFrame(columns=vol_data.columns)
# grouped=vol_data.groupby(['State'])
# result=[g[1] for g in grouped]

# for i in range(len(result)):
#     result[i]['Time_in_sec_s']=(result[i]['Date']-result[i]['Date'].shift(1))/np.timedelta64(1,'s')# time difference b/w every datapt
#     df=pd.concat([df,result[i]])

#%% The Capacity/Energy of the pack is calculated using the "Coulomb-counting" technique

vol_data['Time_in_sec_s_cap']=np.where((vol_data['Time_in_sec_s']>300),np.nan,vol_data['Time_in_sec_s'])
 

vol_data['Cap_inst']=vol_data['Time_in_sec_s_cap']*abs(vol_data['Current(A)'])/3600

vol_data['Capacity_calculated']=vol_data['Cap_inst'].groupby(by=vol_data['State']).cumsum()
vol_data['Capacity_calculated_chg']=(vol_data[vol_data['State']==0]['Cap_inst']).cumsum()
vol_data['Capacity_calculated_dchg']=(vol_data[vol_data['State']==1]['Cap_inst']).cumsum()

vol_data['Capacity_calculated_chg']=vol_data['Capacity_calculated_chg'].fillna(method='bfill')
vol_data['Capacity_calculated_dchg']=vol_data['Capacity_calculated_dchg'].fillna(method='bfill')

vol_data['Energy_calculated']=vol_data['Capacity_calculated']*vol_data['Voltage(V)']
vol_data['Energy_calculated_chg']=vol_data['Capacity_calculated_chg']*vol_data['Voltage(V)']
vol_data['Energy_calculated_dchg']=vol_data['Capacity_calculated_dchg']*vol_data['Voltage(V)']


vol_data['Capacity_calculated']=vol_data['Capacity_calculated'].fillna(method='ffill')
vol_data['Energy_calculated']=vol_data['Energy_calculated'].fillna(method='ffill')

#%% Save the modified file in the excel format

vol_data.to_excel(f1.rsplit('.')[0]+'_modified.xlsx')

#%% Record the observations in the form of a text file

f=open(f1.rsplit('.')[0]+'_observations.txt',"w")
vol_col_check=vol_data.columns[3:105]
print('======================================================================',file=f)
print('Datapoints:%s' % (len(vol_data)),file=f)
print('Timeframe: %s to %s' % (vol_data['Date'].iloc[0],vol_data['Date'].iloc[-1]),file=f)
print('Total Time Spent:%s' % (datetime.timedelta(seconds=(vol_data['Date'].iloc[-1]-vol_data['Date'].iloc[0])/np.timedelta64(1,'s'))),file=f)
print('---------------------------',file=f)

if len(vol_data[vol_data['State']==0])!=0:
    print('Chg Time Spent:%s' % (datetime.timedelta(seconds=(vol_data[vol_data['State']==0]['Time_in_sec_s'].sum()))),file=f)
    print('Maximum Charging Current:%.3fA ; Minimum Charging Current:%.3fA' % (vol_data[vol_data['State']==0]['Current(A)'].max(),vol_data[vol_data['State']==0]['Current(A)'].min()),file=f)
    print('Chg Pack Voltage range:%sV to %sV' %(vol_data[vol_data['State']==0]['Voltage(V)'].iloc[0],vol_data[vol_data['State']==0]['Voltage(V)'].iloc[-1]),file=f)
    print('---------------------------',file=f)

    print('Chg Min Vol:%.3fV' %((vol_data[vol_data['State']==0].loc[:,'V1':'V'+str(v_no-1)]).min(axis=1).min()),file=f)
    print('Chg Max Vol:%.3fV' %((vol_data[vol_data['State']==0].loc[:,'V1':'V'+str(v_no-1)]).max(axis=1).max()),file=f)
    print('Chg Average Vol:%.3fV' %((vol_data[vol_data['State']==0]['Mean_V'])).mean(),file=f)
    
    print('Chg Minimum delV:%.3fmV' %((vol_data[vol_data['State']==0]['delV'])).min(),file=f)
    print('Chg Maximum delV:%.3fmV' %((vol_data[vol_data['State']==0]['delV'])).max(),file=f)
    print('Chg Average delV:%.3fmV' %((vol_data[vol_data['State']==0]['delV'])).mean(),file=f)
    print('---------------------------',file=f)
 
    c_dt=pd.to_datetime(vol_data[vol_data['State']==0]['Date'].tolist())
    chg_temp=vol_data[vol_data['Date'].isin(c_dt)]
    print('Chg Min Temp:%.3f degC' %(chg_temp.loc[:,'T1':'T'+str(t_no-1)].min(axis=1).min()),file=f)
    print('Chg Max Temp:%.3f degC' %(chg_temp.loc[:,'T1':'T'+str(t_no-1)].max(axis=1).max()),file=f)
    print('Chg Average Temp:%.3f degC' %(chg_temp['Mean_T'].mean()),file=f)
    
    print('Chg Minimum delT:%.3f degC' %(chg_temp['delT'].min()),file=f)
    print('Chg Maximum delT:%.3f degC' %(chg_temp['delT'].max()),file=f)
    print('Chg Average delT:%.3f degC' %(chg_temp['delT'].mean()),file=f)
    print('---------------------------',file=f)
print('---------------------------',file=f)
if len(vol_data[vol_data['State']==1])!=0:

    print('Dchg Time Spent:%s' % (datetime.timedelta(seconds=(vol_data[vol_data['State']==1]['Time_in_sec_s'].sum()))),file=f)
    print('Maximum Discharging Current:%.3fA ; Minimum Discharging Current:%.3fA' % (vol_data[vol_data['State']==1]['Current(A)'].max(),vol_data[vol_data['State']==1]['Current(A)'].min()),file=f)
    print('DChg Pack Voltage range:%sV to %sV' %(vol_data[vol_data['State']==1]['Voltage(V)'].iloc[0],vol_data[vol_data['State']==1]['Voltage(V)'].iloc[-1]),file=f)
    print('---------------------------',file=f)

    print('Dchg Min Vol:%.3fV' %((vol_data[vol_data['State']==1].loc[:,'V1':'V'+str(v_no-1)]).min(axis=1).min()),file=f)
    print('Dchg Max Vol:%.3fV' %((vol_data[vol_data['State']==1].loc[:,'V1':'V'+str(v_no-1)]).max(axis=1).max()),file=f)
    print('Dchg Average Vol:%.3fV' %((vol_data[vol_data['State']==1]['Mean_V'])).mean(),file=f)
    
    print('Dchg Minimum delV:%.3fmV' %((vol_data[vol_data['State']==1]['delV'])).min(),file=f) 
    print('Dchg Maximum delV:%.3fmV' %((vol_data[vol_data['State']==1]['delV'])).max(),file=f) 
    print('Dchg Average delV:%.3fmV' %((vol_data[vol_data['State']==1]['delV'])).mean(),file=f) 
    print('---------------------------',file=f)
    
    d_dt=pd.to_datetime(vol_data[vol_data['State']==1]['Date'].tolist())
    dchg_temp=vol_data[vol_data['Date'].isin(d_dt)]  
    print('Dchg Min Temp:%.3f degC' %(dchg_temp.loc[:,'T1':'T'+str(t_no-1)].min(axis=1).min()),file=f)
    print('Dchg Max Temp:%.3f degC' %(dchg_temp.loc[:,'T1':'T'+str(t_no-1)].max(axis=1).max()),file=f)
    print('Dchg Average Temp:%.3f degC' %(dchg_temp['Mean_T'].mean()),file=f)
    print('Dchg Minimum delT:%.3f degC' %(dchg_temp['delT'].min()),file=f)
    print('Dchg Maximum delT:%.3f degC' %(dchg_temp['delT'].max()),file=f)
    print('Dchg Average delT:%.3f degC' %(dchg_temp['delT'].mean()),file=f)
    print('---------------------------',file=f)
print('---------------------------',file=f)
if len(vol_data[vol_data['State']==2])!=0:

    print('Rest Time Spent:%s' % (datetime.timedelta(seconds=(vol_data[vol_data['State']==2]['Time_in_sec_s'].sum()))),file=f)
    print('Rest Pack Voltage range:%sV to %sV' %(vol_data[vol_data['State']==2]['Voltage(V)'].iloc[0],vol_data[vol_data['State']==2]['Voltage(V)'].iloc[-1]),file=f)
    print('---------------------------',file=f)
    print('Rest Min Vol:%.3fV' %((vol_data[vol_data['State']==2].loc[:,'V1':'V'+str(v_no-1)]).min(axis=1).min()),file=f)
    print('Rest Max Vol:%.3fV' %((vol_data[vol_data['State']==2].loc[:,'V1':'V'+str(v_no-1)]).max(axis=1).max()),file=f)
    print('Rest Average Vol:%.3fV' %((vol_data[vol_data['State']==2]['Mean_V'])).mean(),file=f)
    
    print('Rest Minimum delV:%.3fmV' %((vol_data[vol_data['State']==2]['delV'])).min(),file=f)
    print('Rest Maximum delV:%.3fmV' %((vol_data[vol_data['State']==2]['delV'])).max(),file=f) 
    print('Rest Average delV:%.3fmV' %((vol_data[vol_data['State']==2]['delV'])).mean(),file=f) 
    print('---------------------------',file=f)
    
    r_dt=pd.to_datetime(vol_data[vol_data['State']==2]['Date'].tolist())
    rst_temp=vol_data[vol_data['Date'].isin(r_dt)]
    print('Rest Min Temp:%.3f degC' %(rst_temp.loc[:,'T1':'T'+str(t_no-1)].min(axis=1).min()),file=f)
    print('Rest Max Temp:%.3f degC' %(rst_temp.loc[:,'T1':'T'+str(t_no-1)].max(axis=1).max()),file=f)
    print('Rest Average Temp:%.3f degC' %(rst_temp['Mean_T'].mean()),file=f)
    
    print('Rest Minimum delT:%.3f degC' %(rst_temp['delT'].min()),file=f)
    print('Rest Maximum delT:%.3f degC' %(rst_temp['delT'].max()),file=f)
    print('Rest Average delT:%.3f degC' %(rst_temp['delT'].mean()),file=f)
    print('---------------------------',file=f)
print('---------------------------',file=f)
print('Maximum Charging Capacity:%.3fAh ; Minimum Charging Capacity:%.3fAh' % (vol_data['Capacity_calculated_chg'].max(),vol_data['Capacity_calculated_chg'].min()),file=f)
print('Maximum Discharging Capacity:%.3fAh ; Minimum Discharging Capacity:%.3fAh' % (vol_data['Capacity_calculated_dchg'].max(),vol_data['Capacity_calculated_dchg'].min()),file=f)
print('Maximum Charging Energy:%.3fkWh ; Minimum Charging Energy:%.3fkWh' % ((vol_data['Energy_calculated_chg']*0.001).max(),(vol_data['Energy_calculated_chg']*0.001).min()),file=f)
print('Maximum Discharging Energy:%.3fkWh ; Minimum Discharging Energy:%.3fkWh' % ((vol_data['Energy_calculated_dchg']*0.001).max(),(vol_data['Energy_calculated_dchg']*0.001).min()),file=f)


print('======================================================================\n',file=f)
print('\n',file=f)