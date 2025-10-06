# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 19:42:35 2019

@author: IITM
"""

import pandas as pd
df1=pd.read_excel('C:\\Users\\IITM\Desktop\\AMBEDKAR\\cccv and cc\\finaldoc_TimebaseMatchedtest2.xlsx',sheet_name='Sheet1')
df1 = df1.filter(['RTC','Time_Elapsed', 'Step_No','Temp_Ch1', 'Temp_Ch2', 'Temp_Ch3', 'Temp_Ch4', 'Temp_Ch5', 'Temp_Ch6', 'Temp_Ch7', 'Temp_Ch8', 'Temp_Ch9', 'Temp_Ch10', 'Temp_Ch11', 'Temp_Ch12', 'Temp_Ch13', 'Temp_Ch14', 'Temp_Ch15', 'Temp_Ch16', 'Temp_Ch17'])
df1=df1.dropna(subset=['Temp_Ch1'])
df1.to_excel('C:\\Users\\IITM\Desktop\\AMBEDKAR\\cccv and cc\\finaldoc_TimebaseMatched_Tempdataonly.xlsx')
