# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 10:26:19 2019

@author: IITM
"""

import time
start=time.time()
import pandas as pd
d1=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_SoH_Calculated_files\\LCH_14.1_35Deg_AllCycles_AllCycles_raw(1)_Timestates_added_soh_calculated.csv")
#import pickle
##with open("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_14.1_35Deg_AllCycles_AllCycles_raw(1).pkl",'rb') as f:
##    data_all = pickle.load(f) 
##with open("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_14.1_35Deg_AllCycles_Cycles_Info_raw(1).pkl",'rb') as f:
##    data_cycles = pickle.load(f) 
##with open("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_14.1_35Deg_AllCycles_Steps_Info_raw(1).pkl",'rb') as f:
##    data_step = pickle.load(f) 
##with open("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_14.1_35Deg_AllCycles_AllCycles_processed.pkl",'rb') as f:
##    data_all_processed = pickle.load(f) 
#with open("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_OCV\\LCH_15.1_35Deg_AllCycles_700Cycles_OCV.pkl",'rb') as f:
#    data_ocv = pickle.load(f) 
#with open("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_OCV\\LCH_15.1_35Deg_AllCycles_700Cycles_processed.pkl",'rb') as f:
#    data_ocv_processed = pickle.load(f) 
#print("--- %s seconds ---" % (time.time() - start))