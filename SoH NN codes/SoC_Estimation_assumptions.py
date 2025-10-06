# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 15:00:02 2021

@author: IITM

This code is to assign soc values based on V_min values
"""

import pandas as pd
import numpy as np

df=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\IITM-Driving\\Charging_Files_Added Timestates\\91CBE0010102D1200209_Combined_sessions_timestates.csv")
df_ref=pd.read_csv("D:\\Benisha\\SoH_NN\\SoC_and_Voltage_ref.csv")
df['SoC_Assumption']=''
for i in range(0,len(df_ref)):
    df['SoC_Assumption']=np.where(np.isclose(df['V_Min'],df_ref['Voltage_ref'][i],rtol=0.001),df_ref['SoC_ref'][i],
                                  df['SoC_Assumption'])

