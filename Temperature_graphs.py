# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:58:32 2020

@author: IITM
"""
"""
Script to plot temperatures of timepacks to check their distribution
"""

import time
start=time.time()
import pandas as pd
import matplotlib.pyplot as plt
data1=pd.read_csv("D:\\Benisha\\Battery DCA\\Monthly data\\2019_M6_Jun_charging_temperature_voltage_sorted.csv")
data1['V_Max']=data1.loc[:,'CV0':'CV12'].max(axis=1)
data1['T_Max']=data1.loc[:,'T0':'T16'].max(axis=1)

#data1=data1.dropna(subset=['C1'])
for j in ['T0','T1','T2','T3','T4','T5','T6','T7','T8','T9','T10','T11','T12','T13','T14','T15','T16']:
    data1[j]=data1[j].where(data1[j]!=119,0)
data1=data1[(data1.T_Max<100)]
data1['Avg_Temp']=data1.loc[:,'T0':'T16'].mean(axis=1)
grouped=data1.groupby('session',sort=False)
result=[g[1]for g in list(grouped)]
for i in range (0,len(result)):
#    if(i>130 and i<200):
        result[i]=result[i].reset_index(drop=True)
        plt.figure(i+1)
        plt.scatter(result[i].index, result[i]['T_Max'], s=2)
        plt.grid(linestyle='dotted')
        plt.xlabel('Index')
        plt.ylabel('Temperature')
#    else:
#        pass
plt.show()
print('----------%s seconds---------' % (time.time()-start))