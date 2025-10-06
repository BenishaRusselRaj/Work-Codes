# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 17:54:15 2020

@author: IITM
"""

"""

Check line 23 and 24 in mergefile
"""

import time
start=time.time()
import glob
import sys
import pandas as pd
sys.path.append("D:\\Benisha\\SoH_NN\\Codes")
from Merge_otd_file_binwise import mergefile
from SOH_Estimation_all_bins_main import SOH_estimation

cols=['bin','nc_bms','SOH_BMS','nc_otd','SOH_otd','nc_cell_testing','SOH_cell_testing']

data_file=pd.DataFrame(columns=cols)
files=glob.glob("D:\\Benisha\\SoH_NN\\Data\\Combined_Summary\\*")
otd_file_path="D:\\Benisha\\SoH_NN\\Data\\iitm_charging_session_onetime_all_bin.tsv"
for f in files:
    merged_file_path=mergefile(f, otd_file_path)
    temp_file = SOH_estimation(merged_file_path) 
    data_file=pd.concat([data_file,temp_file])
fin_path='\\'.join(otd_file_path.split('\\')[0:-1])
data_file=data_file.reset_index(drop=True)
data_file.to_csv(fin_path+'\\Final_Cycle_Nos_and SOH.csv')
print('--------%s seconds-------' %(time.time()-start))