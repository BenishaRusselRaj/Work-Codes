# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 12:14:26 2022

@author: IITM
"""

import pandas as pd
import glob
import numpy as np

#%% Merging files
# files=glob.glob("D:\\Benisha\\SoH_NN\Data\\PHY\\SoH_Summary files\\*.csv")

# df=pd.DataFrame()

# for f in files:
#     data=pd.read_csv(f)
#     df=pd.concat([df,data])

# file_path=files[0].rsplit('\\',1)[0]
# df.to_csv(file_path+'\\PHY_AllCycles_Timestates_added_soh_summary.csv')

#%% Manipulating file
df=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\PHY\\SoH_Summary files\\PHY_AllCycles_Timestates_added_soh_summary.csv")

df['SoC_calculated']=np.where(df['SoC_calculated']<3,np.nan,df['SoC_calculated'])
df['SoC_calculated']=df['SoC_calculated'].fillna(method='ffill')

df.to_csv("D:\\Benisha\\SoH_NN\\Data\\PHY\\SoH_Summary files\\PHY_AllCycles_Timestates_added_soh_summary_soc_corrected.csv")
