# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 09:55:03 2024

@author: IITM
"""
#%% Code Description

"""
USE THIS CODE IF:
    1. Monthly data of individual strings of IoE system are available.
    2. This data generally only has higher level metrics like charge in-out for each cycle?
"""

"""
PRE-REQUISITES:
    1. The putty log need to be imported into MS Excel first
    2. While opening in Excel, open it by mentioning the "comma", "space" and in "other" - ":", as the delimiters
    3. Save the file as an Excel file (i.e., with .xlsx extension)
"""

"""
NOTE:
    1. This code generally needs multiple changes for it to work without errors
    2. It is because the data collection process is highly irregular
    3. Proceed with caution at every cell, otherwise useful data may be lost.

"""

#%%
# Importing the necessary libraries

import pandas as pd
import numpy as np
# from scipy import signal
import matplotlib.pyplot as plt
import glob
import os
import calendar

#%% get all the files that fit a particular structure using "glob"

# files = glob.glob(r"C:\Users\IITM\Downloads\ioeData\9th\ioeString*Month*.csv")

files = glob.glob(r"D:\Benisha\IOE\String_month_data\ioeData\10th\ioeString*Month*.csv")

# files = glob.glob(r"C:\Users\IITM\Downloads\ioeData\8th\ioeString1Month8.csv")
# file = r"C:\Users\IITM\Downloads\ioeString1Month4.xlsx"
# summary_path = files[0].rsplit('\\',1)[0] + '\\' + 'String_' + files[0].rsplit('\\', 1)[1].rsplit('.',1)[0].lower().split('month')[0].split('string')[1] + '_Summary.xlsx'
# q = open(summary_path,"w")
# writer = pd.ExcelWriter(summary_path, engine = 'xlsxwriter')
# all_months = []
# chg_cycles = []
# dchg_cycles = []

#%% loop through the files
# summary_excel = pd.DataFrame()
for file in files:
    data = pd.read_csv(file) # read file using read_csv()
    
    #window size of graphs; cheosen based on trial and error (depending on the size on a word document)
    l=7.5
    b=4.5
    # separate filename from the input link
    filename = file.rsplit('\\', 1)[1].rsplit('.',1)[0] 
    folder_path = file.rsplit('\\',1)[0] + '\\' + filename
    # folder_path = file.rsplit('\\',1)[0]
    
    # get month name
    month = int(filename.lower().split('month')[1])
    
    # get string number
    string = filename.lower().split('month')[0].split('string')[1]
    
    # Assign total rated energy values based on string values
    if string == '4':
        Total_engy = 156.288
    else:
        Total_engy = 170.496
    
    #%%
    # Create destination folder if it is not already present
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    #%%
    # change time to datetime format and create a column with seconds taken in each datapoint
    data['recordTimestamp'] = pd.to_datetime(data['recordTimestamp'], errors = 'coerce')
    data['Time_in_sec_s'] = (data['recordTimestamp'] - data['recordTimestamp'].shift()) / np.timedelta64(1, 's')
    data['Time_in_sec'] = data['Time_in_sec_s'].cumsum()
    
    # Changing energy from Wh to kWh and rounding off to four decimal places
    data['chargingEnergy'] = round((data['chargingEnergy']*0.001), 4)
    data['dischargingEnergy'] = round ((data['dischargingEnergy']*0.001), 4)
    
    # open the file in which observations are saved as a text file
    f=open(folder_path+ '\\' + filename + '_observations.txt',"w")
    print('File name: %s' %filename, file=f)
    print('Total Number of Datapoints: %s' % (len(data)),file=f)
    
    # data is separated (here) into weeks, so the total dataset is divided into weeks
    # the total number of seconds are counted and divided by the number of seconds in a week
    range_val = data['Time_in_sec'].max()//604800  # (7 days) 691200 (8 days)
    
    all_chg_engy = []
    all_dchg_engy = []
    
    div_val = len(data)//range_val
    div_val = int(div_val)
    x = div_val
    
    i = 0
    n = 1
    # complete_excel_data = pd.DataFrame()
    
    #%% Separate monthly data into individual weeks to process them as weekly data
    while div_val<=len(data): # divide 
        
        snip_data = data.iloc[i:div_val, :]
        
        i = div_val
        div_val = div_val + x
        
        # separate charge discharge and rest data into separate datasets
        chg_data = snip_data[snip_data['batteryStatus']=='CHG']
        dchg_data = snip_data[snip_data['batteryStatus']=='DCHG']
        idle_data = snip_data[snip_data['batteryStatus']=='IDLE']
        
        #%% Plot the charging energy per week for visualization and for manual checking of the energy values
        
        plt.figure(figsize=(l,b))
        plt.plot(range(len(chg_data)), chg_data['chargingEnergy'])
        plt.ylabel('Energy (kWh)', fontweight = 'bold')
        plt.grid(linestyle='dotted')
        plt.show()
        plt.title("Charging Energy (Week "+ str(n) + ')', fontweight = 'bold')
        plt.tight_layout()
        plt.savefig(folder_path+'\\'+filename+'Charging Energy (Week '+ str(n) +').png',dpi=1200)
        
        #%%  Plot the discharging energy per week for visualization and for manual checking of the energy values
        plt.figure(figsize=(l,b))
        plt.plot(range(len(dchg_data)), dchg_data['dischargingEnergy'])
        plt.ylabel('Energy (kWh)', fontweight = 'bold')
        plt.grid(linestyle='dotted')
        plt.show()
        plt.title("Discharging Energy (Week "+ str(n) + ')', fontweight = 'bold')
        plt.tight_layout()
        plt.savefig(folder_path+'\\'+filename+'Discharging Energy (Week '+ str(n) +').png',dpi=1200)
        
        #%% Separate charge cycles and discharging partial cycles
        
        chg_data['Charge_half_Cycles'] = ((chg_data['chargingEnergy'].diff())<-4).cumsum()
    
        dchg_data['Discharge_half_Cycles'] = ((dchg_data['dischargingEnergy'].diff())<-4).cumsum()
        
        #%% To get the maximum values achieved at each partial cycle
        
        Chg_engy_vals = chg_data.groupby(['Charge_half_Cycles'])['chargingEnergy'].max()
        
        DChg_engy_vals = dchg_data.groupby(['Discharge_half_Cycles'])['dischargingEnergy'].max()
        
        all_chg_engy.extend(Chg_engy_vals)
        all_dchg_engy.extend(DChg_engy_vals)
        
        #%%
        # chg_excel_data = pd.DataFrame(index = range(len(Chg_engy_vals)))
        # dchg_excel_data = pd.DataFrame(index = range(len(DChg_engy_vals)))
        
        # #%% Excel same sheet, different tables for different weeks
        
        # chg_excel_data['Week'] = n
        # dchg_excel_data['Week'] = n
        # chg_excel_data['Time Spent in Charging'] = str (int((chg_data['Time_in_sec_s'].sum() - (chg_data['Time_in_sec_s'].sum() % 3600))/3600)) + ' hours ' + str(int((chg_data['Time_in_sec_s'].sum() % 3600)/60)) + " minutes"
        # dchg_excel_data['Time Spent in Discharging'] = str(int((dchg_data['Time_in_sec_s'].sum() - (dchg_data['Time_in_sec_s'].sum() % 3600))/3600)) + ' hours ' + str(int((dchg_data['Time_in_sec_s'].sum() % 3600)/60)) + " minutes"
        # chg_excel_data["Charge Energies (kWh)"] = [i for i in Chg_engy_vals]
        # dchg_excel_data['Discharge Energies (kWh)'] = [i for i in DChg_engy_vals]
        # chg_excel_data['Total Charge Energy (Week '+str(n)+')'] = round(sum(Chg_engy_vals), 4)
        # dchg_excel_data['Total Discharge Energy (Week '+str(n)+')'] = round(sum(DChg_engy_vals), 4)
        # excel_data = pd.concat([chg_excel_data, dchg_excel_data], axis = 1)
        # excel_data[''] = np.nan
        # excel_data[''] = np.nan
        
#%%
        print('======================================================================',file=f)
        print("Week: %s" %n, file = f)
        
        print('Time Spent in Charging (weekly data): %s hours %s minutes' 
                        % (int((chg_data['Time_in_sec_s'].sum() - (chg_data['Time_in_sec_s'].sum() % 3600))/3600), 
                        int((chg_data['Time_in_sec_s'].sum() % 3600)/60)), file=f)
        print('Time Spent in Discharging (weekly data): %s hours %s minutes' 
                        % (int((dchg_data['Time_in_sec_s'].sum() - (dchg_data['Time_in_sec_s'].sum() % 3600))/3600), 
                        int((dchg_data['Time_in_sec_s'].sum() % 3600)/60)), file=f)
        print('Time Spent idle (weekly data): %s hours %s minutes' 
                        % (int((idle_data['Time_in_sec_s'].sum() - (idle_data['Time_in_sec_s'].sum() % 3600))/3600), 
                        int((idle_data['Time_in_sec_s'].sum() % 3600)/60)), file=f)
        
        print('Charge Energies observed (in kWh): %s' %[i for i in Chg_engy_vals], file=f)
        print('Total Charging energy delivered in Week %s is: %s kWh' %(n, round(sum(Chg_engy_vals), 4)), file = f)
        print('Discharge Energies observed (in kWh): %s' %[i for i in DChg_engy_vals],  file=f)
        print('Total Discharging energy expended in Week %s is: %s kWh' %(n, round(sum(DChg_engy_vals), 4)), file = f)
        print('======================================================================',file=f)
        
        n+=1
        
        # complete_excel_data = pd.concat([complete_excel_data, excel_data], axis = 1)
        
    print ('--*-- Monthly Summary --*--', file=f)
    print ('Total Charging energy delivered on %s is: %s kWh' %(calendar.month_name[month], round(sum(all_chg_engy), 4)), file = f)
    print ('Total Discharging energy expended on %s is: %s kWh' %(calendar.month_name[month], round(sum(all_dchg_engy), 4)), file = f)
    print ('Apparent Cycles according to charging energy data is: %s' %((round(sum(all_chg_engy), 4))//Total_engy), file=f)
    print ('Apparent Cycles according to discharging energy data is: %s' %((round(sum(all_dchg_engy), 4))//Total_engy), file=f)
    f.close()
    
    
#     complete_excel_data['Total Charging energy(monthly)'] = round(sum(all_chg_engy), 4)
#     complete_excel_data['Total Discharging energy(monthly)'] = round(sum(all_dchg_engy), 4)
#     complete_excel_data['Apparent Cycles (Charging)'] = (round(sum(all_chg_engy), 4))/Total_engy
#     complete_excel_data['Apparent Cycles (Discharging)'] = (round(sum(all_dchg_engy), 4))/Total_engy
    
#     complete_excel_data.to_excel(writer,sheet_name='String_' + string + '_'+ calendar.month_name[month],index=False)
    
#     all_months.append(calendar.month_name[month])
#     chg_cycles.append((round(sum(all_chg_engy), 4))/Total_engy)
#     dchg_cycles.append((round(sum(all_dchg_engy), 4))/Total_engy)
    

# summary_excel['Months involved'] = all_months
# summary_excel['Apparent Cycles(charging)'] = chg_cycles
# summary_excel['Apparent Cycles(discharging)'] = dchg_cycles
# summary_excel.to_excel(writer,sheet_name='Summary_String_' + string,index=False)
# writer.close()