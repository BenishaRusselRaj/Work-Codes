"""
==============================================================================================
File name: Merge_Soh_main.py
Desription:
Comments:
==============================================================================================
"""

"""

Check line 23 and 24 in mergefile
"""

import time
start=time.time()
import glob
import sys
import pandas as pd
import numpy as np
<<<<<<< HEAD
sys.path.append("D:\\Sushant\\soh\\Code")
=======
sys.path.append("D:\\BLT\\SOH Battery pack\\Code")
>>>>>>> 2ac5b30ec070bc4f8adbaa3617fcf8b01a87833b
from Merge_otd_file_binwise import mergefile
from SOH_Estimation_all_bins_main import SOH_estimation

cols=['bin','nc_bms','SOH_BMS','nc_otd','SOH_otd','nc_cell_testing','SOH_cell_testing_avg','SOH_cell_testing_min','SOH_cell_testing_max']
i =1
data_file=pd.DataFrame(columns=cols)
<<<<<<< HEAD
files=glob.glob("D:\\Sushant\\soh\\Data\\Combined_Summary_files\\*") # Path to the folder having the combined summary files
otd_file_path="D:\\Sushant\\soh\\Data\\iitm_charging_session_onetime_all_bin.tsv" # Path to the OTD file
=======

files=glob.glob("D:\\BLT\\SOH Battery pack\\Data\\Combined_Summary_files\\*") # Path to the folder having the combined summary files
otd_file_path="D:\\BLT\\SOH Battery pack\\Data\\iitm_charging_session_onetime_all_bin.tsv" # Path to the OTD file
>>>>>>> 2ac5b30ec070bc4f8adbaa3617fcf8b01a87833b
for f in files:
    print("Processing File ", i,"/",len(files), "..........")
    merged_file_path=mergefile(f, otd_file_path)
    temp_file = SOH_estimation(merged_file_path) 
    data_file=pd.concat([data_file,temp_file])
    i=i+1;
    

fin_path='\\'.join(otd_file_path.split('\\')[0:-2]) + '\\Results'

data_file = data_file.dropna(subset=['bin'])

data_file['start_Time'] = pd.to_datetime(data_file['start_Time'])
data_file['end_Time'] = pd.to_datetime(data_file['end_Time'])
data_file['Total_Time_spent_days'] = (data_file['end_Time'] - data_file['start_Time'])/np.timedelta64(1,'D')

data_file=data_file.reset_index(drop=True)
data_file.to_csv(fin_path+'\\Final_Cycle_Nos_and SOH_time_included.csv')
print('--------%s seconds-------' %(time.time()-start))