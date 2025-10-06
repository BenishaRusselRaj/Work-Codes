# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:05:23 2020

@author: IITM
"""

"""
Main code to add temperature and voltage timestates, to combine chg and dchg files and give summary along with rest
Make sure that this main file and the other code files are in the same path
*****Check timeformat in "Pack_Timestates_test.py" (line 50)****

"""


import time
start1=time.time()
import sys
sys.path.append('D:\\Benisha\\Code files') # add the path to the code files here
from Pack_TimeStates_test import timestates
from Pack_del_duplicated_DChg import timecheck
from Combined_pack_data import combinedata

Chg_file="D:\\Benisha\\Battery DCA\\Mohali Monthly data\\2018_M7_July_charging_temperature_voltage_sorted_new.csv"# Charging data file
DChg_file="D:\\Benisha\\Battery DCA\\Mohali Monthly data\\2018_M7_July_Driving_Data_Combined_sorted_new.csv" # Discharging file


times_chg=timestates(Chg_file)
times_dchg=timestates(DChg_file)


timecheck_chg=timecheck(times_chg)
timecheck_dchg=timecheck(times_dchg)

combinedata(timecheck_chg, timecheck_dchg)
print('-----------%s seconds---------' % (time.time()-start1))