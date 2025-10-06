# -*- coding: utf-8 -*-
"""
Created on Mon May 13 12:20:53 2024

@author: IITM
"""
import pandas as pd


#%%
df_v=pd.read_excel(r"D:\Benisha\LTVS\3.6kWh\Cycle_Test\BMS_log\Combined_File_log\Cycle_Test_05.06_06.06_07.06_Complete_log_modified.xlsx",sheet_name='Cell Voltage')

df_t=pd.read_excel(r"D:\Benisha\LTVS\3.6kWh\Cycle_Test\BMS_log\Combined_File_log\Cycle_Test_05.06_06.06_07.06_Complete_log_modified.xlsx",sheet_name='Cell Temperature')

df_d=pd.read_excel(r"D:\Benisha\LTVS\3.6kWh\Cycle_Test\BMS_log\Combined_File_log\Cycle_Test_05.06_06.06_07.06_Complete_log_modified.xlsx",sheet_name='Pack Details')


#%%


start=[219,
3480,
3878,
6472,
7410,
10928,
11600,
23979,
28979,
30112,
43086,
44373,
45939,
46478,
47808,
48880,
57536,
58437,
74194,
74892,
]

end=[3474
,3874
,6470
,7407
,10926
,11598
,23813
,28977
,30090
,43084
,44367
,45936
,46450
,47800
,48872
,57534
,58432
,74182
,74887
,78638
]

for s,e in zip(start,end):
    print('The Capacity at start pos %s is: %s' %(s, df_d.loc[s,'Capacity_calculated']))
    print('The Capacity at end pos %s is: %s' %(e, df_d.loc[e,'Capacity_calculated']))
    print("Capacity transfered: %s" %(df_d.loc[e,'Capacity_calculated']-df_d.loc[s,'Capacity_calculated']))
    print("The Energy at start pos %s is: %s" %(s,df_d.loc[s,'Energy_calculated']))
    print("The Energy at end pos %s is: %s" %(e,df_d.loc[e,'Energy_calculated']))
    print("Energy transfered: %s" %(df_d.loc[e,'Energy_calculated']-df_d.loc[s,'Energy_calculated']))
    print("Average cell voltage: %s to ", (df_v.loc[s,'Mean_V'],df_v.loc[e,'Mean_V']))
    print("Min delV: %s" % df_v.loc[s:e,'delV'].min())
    print("Max delV: %s" %df_v.loc[s:e,'delV'].max())
    print("Average delV: %s" %df_v.loc[s:e,'delV'].mean())
    print('Maximum cellT: %s' % df_t.loc[s:e,'Max_T'].max())
    print('Minimum cellT: %s' % df_t.loc[s:e,'Min_T'].min())
    print('Average cellT: %s' % df_t.loc[s:e,'Mean_T'].mean())
    print('Minimum delT: %s' % df_t.loc[s:e,'delT'].min())
    print('Maximum delT: %s' % df_t.loc[s:e,'delT'].max())
    print("Average delT: %s" % df_t.loc[s:e,'delT'].mean())

    