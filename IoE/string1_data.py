# -*- coding: utf-8 -*-

#%% Code Description - need to change

"""
USE THIS CODE WHEN:
    1. Monthly log of IoE data is available for analysis.
    2. These logs have lesser columns compared to the regular logs.

"""

"""
PRE-REQUISITES:
    1. The putty log need to be imported into MS Excel first
    2. While opening in Excel, open it by mentioning the "comma", "space" and in "other" - ":", as the delimiters
    3. Save the file as an Excel file (i.e., with .xlsx extension)
"""

"""
NOTE:
    1. The data collection process is highly irregular
    2. Proceed with caution at every cell, otherwise useful data may be lost.
    3. Check and double-check the data after executing every cell
"""

#%% Import necessary libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import calendar

#%% Get all the files with names that match the pattern of the names of the files that needs processing
# Care must be taken that the files that need processing should have the same naming format

files = glob.glob(r"D:\Benisha\IOE\String_month_data\ioeData\String_5\ioeString*Month*.csv")

#%% path to the destination file in which the summary (excel) file is to be saved

summary_path = files[0].rsplit('\\',1)[0] + '\\' + 'String_' + files[0].rsplit('\\', 1)[1].rsplit('.',1)[0].lower().split('month')[0].split('string')[1] + '_Summary.xlsx'

# "writer" opens the excelwriter module of pandas library
writer = pd.ExcelWriter(summary_path, engine = 'xlsxwriter')

# Initialize a few empty lists so that values can be appended incrementally throughout the code compilation
all_months = []
chg_cycles = []
dchg_cycles = []
chg_energy = []
dchg_energy = []
min_chg_c_rate = []
max_chg_c_rate = []
min_dchg_c_rate = []
max_dchg_c_rate = []
start_dates = []
end_dates = []

#%% Loop over the files (for one string)
for file in files:
    # load file into the code using read_csv() function of the pandas library
    data = pd.read_csv(file)
    
    #%%
    # l and b are the dimensions of the plot windows
    # Chosen through trial and error; optimal value chosen for displaying in a word document
    l=7.5
    b=4.5
    
    #%%
    # get filename from the filepath for saving the observations with proper and unique tags for each file
    filename = file.rsplit('\\', 1)[1].rsplit('.',1)[0]
    
    # folder path in which the output files need to be saved
    folder_path = file.rsplit('\\',1)[0] + '\\' + filename
    
    # Get month name
    month = int(filename.lower().split('month')[1])
    
    # Get string name
    string = filename.lower().split('month')[0].split('string')[1]
    
    # create the destination path if it is not already there
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    #%%
    # Set total maximum energy and maximum current is set/hard-coded based on the string number
    if string == '4':
        Total_engy = 156.288
        max_current = 220
    else:
        Total_engy = 170.496
        max_current = 240
    

    #%%
    # change time to the pandas dateTime format for better processing
    data['recordTimestamp'] = pd.to_datetime(data['recordTimestamp'], errors = 'coerce')
    
    # Duplicate/redundant data is dropped based on the timestamp
    data = data.drop_duplicates(subset = ['recordTimestamp'], keep = 'first') 
    data = data.reset_index(drop = True)
    
    # Find the time in seconds traversed during the test
    data['Time_in_sec_s'] = (data['recordTimestamp'] - data['recordTimestamp'].shift()) / np.timedelta64(1, 's')
    data['Time_in_sec'] = data['Time_in_sec_s'].cumsum()
    
    # Converting the energy in Wh to kWh and rounding it off to four decimal places (for easier processing)
    data['chargingEnergy'] = round((data['chargingEnergy']*0.001), 4)
    data['dischargingEnergy'] = round ((data['dischargingEnergy']*0.001), 4)
    
    # Finding the approximate C-rate by dividing it with the maximum current value (assigned based on the string number)
    data['Apparent C-rate'] = round((data['batteryCurrent']/max_current), 3)
    
    #%%
    # Opening the destination text file for recording the observations
    f=open(folder_path+ '\\' + filename + '_observations.txt',"w")
    
    # Printing the dataset specifications into the file
    print('File name: %s' %filename, file=f)
    print('\n', file = f)
    print("String: %s" %string, file = f)
    print('Total Number of Datapoints: %s' % (len(data)),file=f)
    
    #%% Data is supposed to be separated (here) into weeks, so the total dataset is divided into weeks
    
    # The total number of seconds are counted and divided by the number of seconds in a week
    # "noOfWeeks" divides the total time(seconds) into groups of 7 days each
    noOfWeeks = data['Time_in_sec'].max()//669600 # no. of seconds in one week of a month of 31 days
    
    div_val = len(data)//noOfWeeks
    div_val = int(div_val)
    x = div_val
    
    #%%
    all_chg_engy = []
    all_dchg_engy = []
    all_dates = []
    all_chg_c_rates = []
    all_dchg_c_rates= []
    
    i = 0
    n = 1
    
    complete_excel_data = pd.DataFrame()
    datacheckChg = pd.DataFrame()
    datacheckDChg = pd.DataFrame()
    
    #%% Loop over separate weeks
    
    while div_val<=len(data):
        
        # separate individual week data from the complete data
        snip_data = data.iloc[i:div_val, :] 
        
        # Arrange values based on the timestamp
        snip_data = snip_data.sort_values(by=['recordTimestamp'])
        snip_data = snip_data.reset_index(drop=True)
        
        i = div_val
        div_val = div_val + x
        
        # Separate charge, discharge and rest values using the battery status already available
        chg_data = snip_data[snip_data['batteryStatus']=='CHG']
        dchg_data = snip_data[snip_data['batteryStatus']=='DCHG']
        idle_data = snip_data[snip_data['batteryStatus']=='IDLE']
        
        #Smooth the energy curve using a median filter as the data has multiple fluctuations
        chg_data['chargingEnergy'] = chg_data['chargingEnergy'].rolling(10).median()
        dchg_data['dischargingEnergy'] = dchg_data['dischargingEnergy'].rolling(10).median()
        
        #%% Plot the charging energy per week for visualization and for manual checking of the energy values
        plt.figure(figsize=(l,b))
        plt.plot(range(len(chg_data)), chg_data['chargingEnergy'])
        plt.ylabel('Energy (kWh)', fontweight = 'bold')
        plt.grid(linestyle='dotted')
        plt.show()
        plt.title("Charging Energy (Week "+ str(n) + ')', fontweight = 'bold')
        plt.tight_layout()
        plt.savefig(folder_path+'\\'+filename+'Charging Energy (Week '+ str(n) +').png',dpi=1200)
        
        #%% Plot the discharging energy per week for visualization and for manual checking of the energy values
        plt.figure(figsize=(l,b))
        plt.plot(range(len(dchg_data)), dchg_data['dischargingEnergy'])
        plt.ylabel('Energy (kWh)', fontweight = 'bold')
        plt.grid(linestyle='dotted')
        plt.show()
        plt.title("Discharging Energy (Week "+ str(n) + ')', fontweight = 'bold')
        plt.tight_layout()
        plt.savefig(folder_path+'\\'+filename+'Discharging Energy (Week '+ str(n) +').png',dpi=1200)
        
        #%% Plot the charging current value for visualization and for manual checking of the values
        plt.figure(figsize=(l,b))
        plt.plot(range(len(chg_data)), chg_data['batteryCurrent'])
        plt.ylabel('Current (A)', fontweight = 'bold')
        plt.grid(linestyle='dotted')
        plt.show()
        plt.title("Charging Current (Week "+ str(n) + ')', fontweight = 'bold')
        plt.tight_layout()
        plt.savefig(folder_path+'\\'+filename+'Charging Current (Week '+ str(n) +').png',dpi=1200)
        
        #%% Plot the discharging current value for visualization and for manual checking of the values
        plt.figure(figsize=(l,b))
        plt.plot(range(len(dchg_data)), dchg_data['batteryCurrent'])
        plt.ylabel('Current (A)', fontweight = 'bold')
        plt.grid(linestyle='dotted')
        plt.show()
        plt.title("Discharging Current (Week "+ str(n) + ')', fontweight = 'bold')
        plt.tight_layout()
        plt.savefig(folder_path+'\\'+filename+'Discharging Current (Week '+ str(n) +').png',dpi=1200)        
        #%% Separate charge cycles and discharging partial cycles
        chg_data['Charge_half_Cycles'] = ((chg_data['chargingEnergy'].diff())<-10).cumsum()
    
        dchg_data['Discharge_half_Cycles'] = ((dchg_data['dischargingEnergy'].diff())<-10).cumsum()
        
        #%%  To get the maximum values achieved at each partial cycle
        Chg_engy_vals = chg_data.groupby(['Charge_half_Cycles'])['chargingEnergy'].max()
        
        DChg_engy_vals = dchg_data.groupby(['Discharge_half_Cycles'])['dischargingEnergy'].max()
        
        dates = (snip_data['recordTimestamp'].drop_duplicates(keep='first')).to_list()
        
        chg_c_rate = chg_data['Apparent C-rate'].to_list()
        
        dchg_c_rate = dchg_data['Apparent C-rate'].to_list()
        
        # Append all the charge/discharge values 
        all_chg_engy.extend(Chg_engy_vals)
        all_dchg_engy.extend(DChg_engy_vals)
        all_dates.extend(dates)
        all_chg_c_rates.extend(chg_c_rate)
        all_dchg_c_rates.extend(dchg_c_rate)
        
        #%% Create separate empty dataframes for charging and discharging
        chg_excel_data = pd.DataFrame(index = range(len(Chg_engy_vals)))
        dchg_excel_data = pd.DataFrame(index = range(len(DChg_engy_vals)))
        
        #%% Same excel sheet, different tables for different weeks; charge and discharge side-by-side
        
        chg_excel_data['Week'] = n
        chg_excel_data['Weekly Charging Time'] = str (int((chg_data['Time_in_sec_s'].sum() - (chg_data['Time_in_sec_s'].sum() % 3600))/3600)) + ' hours ' + str(int((chg_data['Time_in_sec_s'].sum() % 3600)/60)) + " minutes"
        
        dchg_excel_data['Weekly Discharging Time'] = str(int((dchg_data['Time_in_sec_s'].sum() - (dchg_data['Time_in_sec_s'].sum() % 3600))/3600)) + ' hours ' + str(int((dchg_data['Time_in_sec_s'].sum() % 3600)/60)) + " minutes"
        
        chg_excel_data["Charge Energies (kWh)"] = [i for i in Chg_engy_vals]
        dchg_excel_data['Discharge Energies (kWh)'] = [i for i in DChg_engy_vals]
        chg_excel_data['Total Charge Energy (Week '+str(n)+'; in kWh)'] = round(sum(Chg_engy_vals), 4)
        dchg_excel_data['Total Discharge Energy (Week '+str(n)+'; in kWh)'] = round(sum(DChg_engy_vals), 4)
        
        chg_excel_data['Week'] = chg_excel_data['Week'].drop_duplicates(keep='first')
        chg_excel_data['Total Charge Energy (Week '+str(n)+'; in kWh)'] = chg_excel_data['Total Charge Energy (Week '+str(n)+'; in kWh)'].drop_duplicates(keep='first')
        dchg_excel_data['Total Discharge Energy (Week '+str(n)+'; in kWh)'] = dchg_excel_data['Total Discharge Energy (Week '+str(n)+'; in kWh)'].drop_duplicates(keep='first')
        chg_excel_data['Weekly Charging Time'] = chg_excel_data['Weekly Charging Time'].drop_duplicates(keep='first')
        dchg_excel_data['Weekly Discharging Time'] = dchg_excel_data['Weekly Discharging Time'].drop_duplicates(keep='first')
        
        excel_data = pd.concat([chg_excel_data, dchg_excel_data], axis = 1)
        excel_data[''] = np.nan
        
        
#%%
        # Print observations into text file for each week (same text file per month)
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
        
        complete_excel_data = pd.concat([complete_excel_data, excel_data], axis = 1)
        
    print ('--*-- Monthly Summary --*--', file=f)
    print ('Total Charging energy delivered on %s is: %s kWh' %(calendar.month_name[month], round(sum(all_chg_engy), 4)), file = f)
    print ('Total Discharging energy expended on %s is: %s kWh' %(calendar.month_name[month], round(sum(all_dchg_engy), 4)), file = f)
    print ('Apparent Cycles according to charging energy data is: %s' %((round(sum(all_chg_engy), 4))//Total_engy), file=f)
    print ('Apparent Cycles according to discharging energy data is: %s' %((round(sum(all_dchg_engy), 4))//Total_engy), file=f)
    f.close()
    
    # print monthly summary values in the excel file
    complete_excel_data['Total Charging energy(monthly; in kWh)'] = round(sum(all_chg_engy), 4)
    complete_excel_data['Total Discharging energy(monthly; in kWh)'] = round(sum(all_dchg_engy), 4)
    complete_excel_data['Total Monthly Apparent Cycles (Charging)'] = round(sum(all_chg_engy)/Total_engy)
    complete_excel_data['Total Monthly Apparent Cycles (Discharging)'] = round((sum(all_dchg_engy))/Total_engy)
    
    complete_excel_data['Total Charging energy(monthly; in kWh)'] = complete_excel_data['Total Charging energy(monthly; in kWh)'].drop_duplicates(keep='first')
    complete_excel_data['Total Discharging energy(monthly; in kWh)'] = complete_excel_data['Total Discharging energy(monthly; in kWh)'].drop_duplicates(keep='first')
    complete_excel_data['Total Monthly Apparent Cycles (Charging)'] = complete_excel_data['Total Monthly Apparent Cycles (Charging)'].drop_duplicates(keep='first')
    complete_excel_data['Total Monthly Apparent Cycles (Discharging)'] = complete_excel_data['Total Monthly Apparent Cycles (Discharging)'].drop_duplicates(keep='first')
    
    # Save excel file into separate sheets for each month
    # The excel file is not closed yet 
    # All month data are stored iteratively, in separate sheets in the same excel file
    complete_excel_data.to_excel(writer,sheet_name = calendar.month_name[month], index=False)
    
    all_months.append(calendar.month_name[month])
    chg_cycles.append(round(sum(all_chg_engy)/Total_engy))
    dchg_cycles.append(round((sum(all_dchg_engy))/Total_engy))
    chg_energy.append(round(sum(all_chg_engy),3))
    dchg_energy.append(round(sum(all_dchg_engy),3))
    start_dates.append(all_dates[0])
    end_dates.append(all_dates[-1])
    max_chg_c_rate.append(max(all_chg_c_rates))
    min_chg_c_rate.append(min(all_chg_c_rates))
    max_dchg_c_rate.append(max(all_dchg_c_rates))
    min_dchg_c_rate.append(min(all_dchg_c_rates))
    
#%% Final excel sheet containing all the summary data for a particular string

summary_excel = pd.DataFrame()

summary_excel['Month'] = all_months
summary_excel['Start Timestamp'] = start_dates
summary_excel['End Timestamp'] = end_dates

summary_excel['Monthly Time'] = summary_excel.loc[:,'End Timestamp'] - summary_excel.loc[:,'Start Timestamp']
summary_excel.loc[:,'Time of Operation'] = summary_excel['Monthly Time'].sum()

summary_excel['Monthly Time'] = summary_excel['Monthly Time'].astype(str)
summary_excel['Time of Operation'] = summary_excel['Time of Operation'].astype(str)

summary_excel['Monthly Charging Energy'] = chg_energy
summary_excel['Monthly Discharging Energy'] = dchg_energy
summary_excel['Apparent Cycles(charging)'] = chg_cycles
summary_excel['Apparent Cycles(discharging)'] = dchg_cycles


summary_excel['Maximum Charge C-rate'] = max_chg_c_rate
summary_excel['Minimum Charge C-rate'] = min_chg_c_rate
summary_excel['Maximum Discharge C-rate'] = max_dchg_c_rate
summary_excel['Minimum Discharge C-rate'] = min_dchg_c_rate

summary_excel['Total Charging Energy'] = sum(chg_energy)
summary_excel['Total Discharging Energy'] = sum(dchg_energy)

summary_excel['Total Apparent Cycles(charging)'] = sum(chg_cycles)
summary_excel['Total Apparent Cycles(discharging)'] = sum(dchg_cycles)

summary_excel['Overall Maximum Charge C-rate'] = max(max_chg_c_rate)
summary_excel['Overall Minimum Charge C-rate'] = min(min_chg_c_rate)
summary_excel['Overall Maximum Discharge C-rate'] = max(max_dchg_c_rate)
summary_excel['Overall Minimum Discharge C-rate'] = min(min_dchg_c_rate)

summary_excel = summary_excel.sort_values(by='Start Timestamp')

#%% Excel file is now saved and closed
# This file containes the data pertaining to one string
summary_excel.to_excel(writer,sheet_name='Summary String_' + string, index=False)
writer.close()