# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 14:34:05 2022

@author: IITM
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 13:16:41 2022

@author: IITM
"""

import pandas as pd
# import numpy as np
# import os
import glob

#%% Crude way to concat files
#summary files
d1=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\45deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60_CYC_1.3_45deg_100cycles_modified_arranged_AllCycles_AllCycles_raw(1)_Timestates_added_soh_summary.csv")
d2=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\45deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60_CYC_1.3_45deg_200cycles_modified_arranged_AllCycles_AllCycles_raw(1)_Timestates_added_soh_summary.csv")
d3=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\45deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60_CYC_1.3_45deg_400cycles_modified_arranged_AllCycles_AllCycles_raw(1)_Timestates_added_soh_summary.csv")
d4=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\45deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60_CYC_1.3_45deg_460cycles_modified_arranged_AllCycles_AllCycles_raw(1)_Timestates_added_soh_summary.csv")
d5=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\45deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60_CYC_1.3_45deg_500cycles_modified_arranged_AllCycles_AllCycles_raw(1)_Timestates_added_soh_summary.csv")
d6=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\45deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60_CYC_1.3_45deg_600cycles_modified_arranged_AllCycles_AllCycles_raw(1)_Timestates_added_soh_summary.csv")
# d7=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\25deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60Ah_1.2_CYC_25deg_600cycles_modified_arranged_25Deg_AllCycles_AllCycles_raw(1)_Timestates_added_soh_summary.csv")
# d8=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\25deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60Ah_1.2_CYC_25deg_657cycles_modified_arranged_25Deg_AllCycles_AllCycles_raw(1)_Timestates_added_soh_summary.csv")
# d9=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\25deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60Ah_1.2_CYC_25deg_673cycles_modified_arranged_25Deg_AllCycles_AllCycles_raw(1)_Timestates_added_soh_summary.csv")
# d10=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\25deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60Ah_1.2_CYC_25deg_715cycles_modified_arranged_25Deg_AllCycles_AllCycles_raw(1)_Timestates_added_soh_summary.csv")

# file_path="C:\\Users\\IITM\\Downloads\\Average_temperatures_\\Temperature_Added_files"

# if not os.path.exists(file_path):
#     os.makedirs(file_path)
#%%
# d_zom=pd.read_csv("D:\\Benisha\\Battery Pack Data\\Zomato\\zomato_driving_charging_data\\Combined_Summary_files\\INCYG0010203H0108709_Combined_cyclesData_filtered_test.csv")
# d_iitm=pd.read_csv("D:\\Benisha\\Battery Pack Data\\IITM data\\iitm_driving_charging_data\\OTD_Merged_Summary_files\\OTD_Merged_Summary_file_INCYG0010203H0108709.csv")

df=pd.concat([d1,d2,d3,d4,d5,d6]) # ,d5,d6

# df=df.sort_values(by='Cycle_No',ascending=True)
df=df[df['Cycle_No']>=0]

df.to_csv("D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\45deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60_CYC_1.3_45deg_modified_arranged_Timestates_added_soh_summary.csv")

#%% Same folder filles
# files=glob.glob("D:\\Benisha\\SoH_NN\\Data\\PHY\\SoH_summary_smooth\\*.csv")

# data=pd.DataFrame()
# for f in files:
#     df=pd.read_csv(f)
#     data=pd.concat([data,df])

# data.to_csv("D:\\Benisha\\SoH_NN\\Data\\PHY\\SoH_summary_smooth\\PHY_Combined_SoH_Calculated_summary_files_delsoc_smooth.csv")
#%% Manipulate file according to temperature
# d1=d1[d1['T_pack_Min']>=10]
# l=[d1,d2,d3,d4,d5,d6,d8,d9] 
# l1=['Bin','Session_Type','Bin_Max_Temp','Bin_Min_Temp','Bin_Avg_Temp']
# l2=['Bin_Max_Temp','Bin_Min_Temp','Bin_Avg_Temp']
# df_binwise=pd.DataFrame(index=range(0,40),columns=l1)
# x=0
    
# #%%
# for f in l:
#     grouped=f.groupby(['Session_Type'],sort=False)
#     result=[g[1] for g in grouped]
#     for i in range(0,len(result)):
#         # if (result[i]['Session_Type'].all()=='Rest'):
#         #     pass
#         # else:
#         result[i]=result[i].reset_index(drop=True)
#         df_binwise['Bin'].loc[x]=result[i]['bin'].iloc[0]
#         df_binwise['Session_Type'].loc[x]=result[i]['Session_Type'].iloc[0]
#         df_binwise['Bin_Max_Temp'].loc[x]=result[i]['T_pack_Max'].max()
#         df_binwise['Bin_Min_Temp'].loc[x]=result[i]['T_pack_Min'].min()
#         df_binwise['Bin_Avg_Temp'].loc[x]=result[i]['T_pack_Avg'].mean()
#         for j in l2:
#             if df_binwise[j].iloc[x]>45:
#                 df_binwise[j].iloc[x]=35
#             if df_binwise[j].iloc[x]>35:
#                 df_binwise[j].iloc[x]=30
#         x=x+1
# #%%
# df_binwise=df_binwise.dropna(subset=['Bin'])
# df_binwise.to_csv(file_path+'\\Temperature_Added_File_filtered.csv')

#%% Change DoD
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\45deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60_CYC_1.3_AllCycles_Combined_soh_summary_soh_smooth.csv"
# df=pd.read_csv(f)
# df['DoD']=100

# df.to_csv(f)
