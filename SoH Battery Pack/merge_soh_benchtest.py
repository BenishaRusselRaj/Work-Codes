# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:04:44 2020

@author: IITM
"""

import time
start=time.time()
import glob
import sys
import pandas as pd
import numpy as np

df1 = pd.read_excel(r"D:\Sushant\soh\Data\Bench Testing.xlsx")
df1 = df1[['bin','Date  (dd-mm-yyyy)','Cell Type','Configuration','SOH_bench (%)']]
df2 = pd.read_csv(r"D:\Sushant\soh\Results\Final_Cycle_Nos_and SOH_time_included.csv")


df3 = df2.copy()
df3 = df3.merge(df1,left_on='bin',right_on='bin',how='left')
df3.to_csv("D:\Sushant\soh\Results\Final.csv")