# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 09:57:02 2019

@author: IITM
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

df=pd.read_csv("D:\\Benisha\\Code files\\charging_data_mohali_soc_calculated_3809.csv",header=0,sep=',')
df['time']=pd.to_datetime(df['time'],errors='coerce')
df=df.dropna(subset=['SOC_pred'])
df['adj_soc_pred']=(df['SOC_pred']-5)/0.9
df['adj_soc_pred_s']=df['adj_soc_pred'].shift(1)
for i in range(0,len(df['adj_soc_pred'])):
    if (df['adj_soc_pred'].iloc[i]>100):
        df['adj_soc_pred'].iloc[i]=100
df['adj_soc_pred'].iloc[i]=(0.8*df['adj_soc_pred'].iloc[i])+(0.2*df['adj_soc_pred_s'].iloc[i])