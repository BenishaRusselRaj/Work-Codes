# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 12:38:51 2019

@author: IITM
"""
#import matplotlib.pyplot as plt
import pandas as pd
#import numpy as np
#def movingaverage(values,window):
#    weights = np.repeat(1.0,window)/window
#    smas = np.convolve(values,weights,'valid')
#    return smas
#cols=['S:NO','Timestamp','Profile_type','Mode of operation','Channel No','Profile no','Step No','Cycle No','Voltage','Current','charge','energy','soc','IR','Cell_temp','Error','DC_mapping']
#data=pd.read_csv("D:\\Benisha\\BLT_Data_Analysis\\BLT_Data\\26-12-19\\bltcellreadings1.csv",header=None,sep=',',names=cols, index_col=False) # ,skiprows=1
f="D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_18.1\\LCH_18.1_25Deg_AllCycles_AllCycles_raw(1)_4.csv"
data1=pd.read_csv(f) #  , header=0, index_col=False,sep='\t',error_bad_lines=False,encoding = "utf-16-le"
#data2=pd.read_csv("D:\\Benisha\\Battery DCA\\IITM data\\IIT_Monthly_data\\IIT - Charging Sorted Data\\2018_M12_Dec_charging_temperature_voltage_sorted.csv", header=0, index_col=False,sep=',',error_bad_lines=False)
#data3=pd.read_csv("D:\\Benisha\\Battery DCA\\IITM data\\IIT_Monthly_data\\IIT - Charging Sorted Data\\2019_M2_Feb_charging_temperature_voltage_sorted.csv", header=0, index_col=False,sep=',',error_bad_lines=False)
#
# data1=data1.dropna(subset=['bin'])
# data1.to_csv(f)