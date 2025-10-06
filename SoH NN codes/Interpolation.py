# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 13:05:20 2021

@author: IITM

This code interpolates the standard SoC values to their corresponding voltages
"""

from scipy import interpolate
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
x=[3.3,3.39,3.48,4.10,4.14,4.20]
y=[0,5,10,90,95,100]

f1=interpolate.interp1d(x,y)
xnew=np.arange(3.30,4.20,0.01)
ynew=f1(xnew)
plt.figure()
plt.plot(xnew,ynew)
plt.title('Interp1d')
plt.grid(linestyle='dotted')

#%%
f2=interpolate.InterpolatedUnivariateSpline(x,y)
xnew1=np.arange(3.30,4.20,0.001)
ynew1=f2(xnew1)
plt.figure()
plt.plot(xnew1,ynew1)
plt.title('InterpolatedUnivariateSpline')
plt.grid(linestyle='dotted')

df1=pd.DataFrame()
df1['Voltage_ref']=xnew1
df1['SoC_ref']=ynew1
