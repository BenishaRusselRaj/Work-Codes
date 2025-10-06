# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 16:04:54 2023

@author: IITM
"""
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_excel("C:\\Users\\IITM\\Downloads\\Capacity test v2 19-09-2023.xlsx",sheet_name='record')

v_names=[f'V{x}(V)' for x in range(1,16)]

#%%
data['delV']=data.loc[:,'V1(V)':'V15(V)'].max(axis=1)-data.loc[:,'V1(V)':'V15(V)'].min(axis=1)

#%%
plt.figure()
plt.plot(data['DataPoint'],data['Current(A)'])
plt.ylabel('Current(A)',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Pack Current',fontweight='bold')
plt.show()

#%%
plt.figure()
plt.plot(data['DataPoint'],data['Capacity(Ah)'])
plt.ylabel('Capacity(Ah)',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Pack Capacity',fontweight='bold')
plt.show()

#%%
plt.figure()
plt.plot(data['DataPoint'],data['Chg. Cap.(Ah)'])
plt.ylabel('Capacity(Ah)',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Pack Charging Capacity',fontweight='bold')
plt.show()

#%%
plt.figure()
plt.plot(data['DataPoint'],data['DChg. Cap.(Ah)'])
plt.ylabel('Capacity(Ah)',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Pack Discharging Capacity',fontweight='bold')
plt.show()

#%%
plt.figure()
plt.plot(data['DataPoint'],data['Voltage(V)'])
plt.ylabel('Voltage(V)',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Pack Voltage',fontweight='bold')
plt.show()

#%%
plt.figure()
plt.plot(data['DataPoint'],data['delV']*1000)
plt.ylabel('Voltage(mV)',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('delV',fontweight='bold')
plt.show()

#%%
plt.figure()
plt.plot(data['DataPoint'],data.loc[:,'V1(V)':'V15(V)'])
plt.ylabel('Voltage(V)',fontweight='bold')
plt.legend(v_names)
plt.grid(linestyle='dotted')
plt.title('Cell Voltage',fontweight='bold')
plt.show()