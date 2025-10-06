# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 08:58:18 2019

@author: IITM
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import pickle

##dfcolumns = pd.read_csv('D:\Academic\Python ML\Data files\t6.txt', nrows = 1)
##dfcolumns = pd.read_csv('D:\Academic\Python ML\Data files\t6.txt')


def movingaverage(values,window):
    weights = np.repeat(1.0,window)/window
    smas = np.convolve(values,weights,'valid')
    return smas



df=pd.read_excel("D:\\Benisha\\Code files\\PHY.xlsx",sheet_name='Sheet3')
df[['Voltage','Current','Power','Q_in_out','Start_Voltage','End_Voltage','Chg_Mid_Vtg']] = df[['Voltage','Current','Power','Q_in_out','Start_Voltage','End_Voltage','Chg_Mid_Vtg']].astype(float)
df = df[pd.notnull(df['RTC'])] # to remove step start/end rows
df=df[(df.Voltage>0)] # to remove step start/end rows


Vs = np.array(df.Voltage); V=np.asfarray(Vs,float)
Is = np.array(df.Current); I=np.asfarray(Is,float)
#chgs = np.array(df.Charge_mAh_in_out); chg = np.asfarray(chgs,float)
chgs = np.array(df.Q_in_out); chg = np.asfarray(chgs,float)
dQs = np.array(df.a4); dQ=np.asfarray(dQs,float)
dVs = np.array(df.a4); dV=np.asfarray(dVs,float)
dQbydVs = np.array(df.a4); dQbydV=np.asfarray(dQbydVs,float)
dVbydQs = np.array(df.a4); dVbydQ=np.asfarray(dVbydQs,float)
filtered_dQbydVs = np.array(df.a4); filtered_dQbydV=np.asfarray(filtered_dQbydVs,float)
j=0
for i in range(1, len(chg)): 
    x1= V[i] - V[j]
#    x1= V[j] - V[i] #Dchg
    if x1>0.5:
        dV[i]=V[i]-V[j]
        dQ[i]= (chg[i] - chg[j])/1000
#        dQ[i]= (chg[j] - chg[i])/1000 #Dchg
        j=j+1
        dQbydV[i] = dQ[i]/dV[i]
        dVbydQ[i] = dV[i]/dQ[i]


       
df['chg'] = chg; df['V'] = V; df['dQ'] = dQ; df['dV'] = dV; df['dVbydQ'] = dVbydQ; df['dQbydV'] = dQbydV

df=df.apply(lambda x: pd.Series(x.dropna().values))

print(df.dtypes)
plt.plot(df.Voltage,df.Current)

dQbydV_MovAvg = movingaverage(df.dQbydV,100)
a = np.zeros(99)

dQbydV_MovAvg = pd.Series(dQbydV_MovAvg)
a = pd.Series(a)

dQbydV_MovAvg = dQbydV_MovAvg.append(a)

smooth = pd.Series.rolling(dQbydV_MovAvg, 200, center = True).mean()
ss = np.array(smooth); sss=np.asfarray(ss,float)

df['Smooth_dQbydV'] = sss
 



df.to_pickle('phy_13Ah_dchg_new.pkl') # save the sorted txt file as a pickle file