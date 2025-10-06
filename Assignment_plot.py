# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 15:51:54 2023

@author: IITM
"""
import numpy as np
import matplotlib.pyplot as plt

x=np.arange(0,1,0.0001)
y=[np.nan]*(len(x))
#%%
for i in range(len(x)):
    y[i]=(-(x[i]*x[i]*x[i]*x[i])/12)-(x[i]/6)+1

#%%
plt.figure()
plt.plot(x,y)
plt.grid(linestyle='dotted')
plt.show()