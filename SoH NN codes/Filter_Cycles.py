# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 16:53:36 2022

@author: IITM
"""

import pandas as pd

df_4=pd.read_excel("D:\\Benisha\\SoH_NN\\Data\\PHY13_CYC+RPT_Degradation_3.x_4.x_25 Deg SoH Only.xlsx",sheet_name='4.1 report')

Cycles_4=df_4[(df_4.filter(regex='Cycle|cycle').columns)].values

df=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_4.1\\Timestates_files_TimeStepSec\\PHY_4.1_25Deg_AllCycles_AllCycles_raw_1_Timestates_added.csv")

df=df.loc[df['Cycle_No'].isin(Cycles_4)]