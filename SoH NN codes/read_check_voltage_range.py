# -*- coding: utf-8 -*-
"""
Created on Tue May  6 17:38:59 2025

@author: IITM
"""
import pandas as pd

#%%
file = r"D:\Benisha\SoH_NN\PHY_4.1_25Deg_AllCycles_AllCycles_raw_4.csv"

data = pd.read_csv(file)
#%
d1 = data.head(5000)

d2 = data.tail(5000)

#%%
# d1_chg = d1[d1['Step_Type'] == 'CCCV_Chg']

# print('Chg min: %s; Max: %s' %(d1_chg['Voltage'].min(), d1_chg['Voltage'].max()))

# d1_dchg = d1[d1['Step_Type'] == 'CC_DChg']

# print('DChg min: %s; Max: %s' %(d1_dchg['Voltage'].min(), d1_dchg['Voltage'].max()))

#
#%% Step data read

# file = r"D:\Benisha\SoH_NN\LCH_18.1_25Deg_AllCycles_Steps_Info_raw(1).csv"

# data = pd.read_csv(file)