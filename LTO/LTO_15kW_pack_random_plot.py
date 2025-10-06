# -*- coding: utf-8 -*-

#%% Code Description

"""
USE THIS CODE WHEN:
    1. Putty log data needs to be processed and report generated
    
"""

"""
PRE-REQUISITES:
    1. The putty log need to be imported into MS Excel first
    2. While opening in Excel, open it by mentioning the "comma", "space" and in "other" - ":", as the delimiters
    3. Save the file as an Excel file (i.e., with .xlsx extension)
"""

"""
NOTE:
    1. This code generally needs multiple changes for it to work without errors
    2. It is because the data collection process is highly irregular
    3. Proceed with caution at every cell, otherwise useful data may be lost.
    4. Check and double-check the data after executing every cell
"""

#%% Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the excel file that contains the log
data=pd.read_excel("D:\\Benisha\\15kW_LTO_Pack\\23_12_21\\chg and dchg 20-12-2023.xlsx")

#%% Date pre-processing to ensure correct formatting of data entries
data['batteryStatus']=data['batteryStatus'].astype(str)
data['batteryStatus']=data['batteryStatus'].replace('nan',np.nan)
data['batteryStatus']=data['batteryStatus'].fillna(method='ffill')
data['recordTimestamp']=pd.to_datetime(data['recordTimestamp'],format='%Y-%m-%d %H:%M:%S',errors='coerce')
data=data.sort_values(by='recordTimestamp')

#%% 
data['State']=np.nan
data['Time_in_sec_s']=(data['recordTimestamp']-data['recordTimestamp'].shift(1))/np.timedelta64(1,'s')
data['Time_in_sec_s_cap']=np.where((data['Time_in_sec_s']>300),np.nan,data['Time_in_sec_s'])
data['State']=np.where(data['batteryCurrent']>0,0,data['State'])
data['State']=np.where(data['batteryCurrent']<0,1,data['State'])

# Capacity is calculated through coulomb counting
data['Cap_inst']=data['Time_in_sec_s_cap']*abs(data['batteryCurrent'])/3600
data['Capacity_calculated']=data['Cap_inst'].groupby(data['State']).cumsum()
data['Energy_calculated']=data['Capacity_calculated']*data['batteryVoltage']

#%% Plot Pack status
plt.figure()
plt.plot(data['recordTimestamp'],data['batteryStatus'])
plt.xlabel('DateTime', fontweight='bold')
plt.title('Pack Status', fontweight='bold')
plt.grid(linestyle='dotted')
plt.show()

#%% Plot Pack Voltage
plt.figure()
plt.plot(data['recordTimestamp'],data['batteryVoltage'])
plt.xlabel('DateTime', fontweight='bold')
plt.ylabel('Voltage (V)', fontweight='bold')
plt.title('Pack Voltage', fontweight='bold')
plt.grid(linestyle='dotted')
plt.show()

#%% Plot Pack Current
plt.figure()
plt.plot(data['recordTimestamp'],data['batteryCurrent'])
plt.xlabel('DateTime', fontweight='bold')
plt.ylabel('Current(A)', fontweight='bold')
plt.title('Pack Current', fontweight='bold')
plt.grid(linestyle='dotted')
plt.show()

#%% Plot pack capacity
plt.figure()
plt.plot(data['recordTimestamp'],data['Capacity_calculated'])
plt.xlabel('DateTime', fontweight='bold')
plt.ylabel('Capacity(Ah)', fontweight='bold')
plt.title('Pack Capacity (calculated)', fontweight='bold')
plt.grid(linestyle='dotted')
plt.show()

#%% Plot pack energy
plt.figure()
plt.plot(data['recordTimestamp'],data['Energy_calculated']*0.001)
plt.xlabel('DateTime', fontweight='bold')
plt.ylabel('Energy(kWh)', fontweight='bold')
plt.title('Pack Energy (calculated)', fontweight='bold')
plt.grid(linestyle='dotted')
plt.show()

#%% Plot discharging energy
plt.figure()
plt.plot(data['recordTimestamp'],data['dischargingEnergy']*0.001)
plt.xlabel('DateTime', fontweight='bold')
plt.ylabel('Energy(kWh)', fontweight='bold')
plt.title('Pack Discharging Energy (BMS)', fontweight='bold')
plt.grid(linestyle='dotted')
plt.show()