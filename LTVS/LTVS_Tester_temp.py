# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:15:43 2024

@author: IITM
"""

#%% Code Description

"""
1. This code is used to check the BMS and datalogger data obtained during test
"""

#%% Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

#%% Read the tester excel file

tester_data = pd.read_excel(
    r"D:\Benisha\LTVS\2.8kWh\At_LTVS\2.8kwh nmc battery bms data\04-06-2024\20240604_30A dchrg_15A chrg_2.5KW NMC.xlsx",
                            sheet_name = 'record')

tester_data['Date'] = pd.to_datetime(tester_data['Date'], errors = 'coerce')
chg_data = tester_data[tester_data['Step Type']=='CCCV Chg']
dchg_data = tester_data[tester_data['Step Type']=='CC DChg']

# dchg_data = dchg_data[dchg_data['Date']<pd.to_datetime('2024-06-18 11:21:17')]

# chg_data = chg_data[chg_data['Date']<=pd.to_datetime('2024-06-14 18:43:08')]

# '2024-06-14 18:43:08'


#%% Plot charge Current
plt.figure()
# plt.plot(range(len(chg_data)),chg_data['Current(A)'])
plt.plot(chg_data['Date'],chg_data['Current(A)'])

plt.ylabel('Current(A)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Tester Current',fontweight='bold')
plt.tight_layout()

#%% Plot discharge Current
plt.figure()
# plt.plot(range(len(dchg_data)),dchg_data['Current(A)'])
plt.plot(dchg_data['Date'],dchg_data['Current(A)'])

plt.ylabel('Current(A)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Tester Current',fontweight='bold')
plt.tight_layout()


#%% Plot Charge Voltage
plt.figure()
# plt.plot(range(len(chg_data)),chg_data['Voltage(V)'])
plt.plot(chg_data['Date'],chg_data['Voltage(V)'])

plt.ylabel('Voltage(V)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Voltage (Tester)',fontweight='bold')
plt.tight_layout()

#%% Plot Discharge Voltage
plt.figure()
plt.plot(range(len(dchg_data)),dchg_data['Voltage(V)'])
# plt.plot(dchg_data['Date'],dchg_data['Voltage(V)'])

plt.ylabel('Voltage(V)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Voltage (Tester)',fontweight='bold')
plt.tight_layout()

#%% Plot Charge Capacity
plt.figure()
plt.plot(range(len(chg_data)),chg_data['Capacity(Ah)'])
# plt.plot(chg_data['Date'],chg_data['Capacity(Ah)'])

plt.ylabel('Capacity(Ah)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Capacity (Tester)',fontweight='bold')
plt.tight_layout()

#%% Plot Discharge Capacity
plt.figure()
plt.plot(range(len(dchg_data)),dchg_data['Capacity(Ah)'])
# plt.plot(dchg_data['Date'],dchg_data['Capacity(Ah)'])

plt.ylabel('Capacity(Ah)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Capacity (Tester)',fontweight='bold')
plt.tight_layout()

#%% Plot Charge Energy
plt.figure()
plt.plot(range(len(chg_data)),chg_data['Energy(Wh)']*0.01)
# plt.plot(chg_data['Date'],dchg_data['Energy(Wh)']*0.01)

plt.ylabel('Energy(kWh)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Energy (Tester)',fontweight='bold')
plt.tight_layout()

#%% Plot Discharge Energy
plt.figure()
plt.plot(range(len(dchg_data)),dchg_data['Energy(Wh)']*0.01)
# plt.plot(dchg_data['Date'],dchg_data['Energy(Wh)']*0.01)

plt.ylabel('Energy(kWh)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Energy (Tester)',fontweight='bold')
plt.tight_layout()