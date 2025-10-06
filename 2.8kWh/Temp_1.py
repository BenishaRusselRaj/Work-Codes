# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 08:54:14 2022

@author: IITM
"""

"""
glob read all files to change it to one format
To analyze the 2.8kWh pack data
The data shared is of .xls format and there are three different files
Open the file, change file extension by "Save as" option and change to .xlsx
Use the .xlsx files in this code(as of now, it couldn't read .xls format)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

#%%
'''
In this block, the path to the files are added;
I_file is the "periodic_graph_data" file
T_file is the "temperature_graph_data" file
V_file is the "voltage_graph_data" file

'''

ff="D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_5\\22_02_28\\pack5_cycle2_10\\*"
folders=glob.glob(ff)

for fd in folders:
    files=glob.glob(fd+'\\*.xlsx')
    for f in files:
        if 'temperature' in f.rsplit('\\',1)[1].lower():
            T_file=f
        elif 'voltage' in f.rsplit('\\',1)[1].lower():
            V_file=f
        else:
            I_file=f

#%%
# I_file="D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_1\\22_02_10\\pack1_cycle2_9\\Driving Data\\-battery_periodic_graph_data.xlsx"
# T_file="D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_1\\22_02_10\\pack1_cycle2_9\\Driving Data\\-battery_periodic_temperature_graph_data.xlsx"
# V_file="D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_1\\22_02_10\\pack1_cycle2_9\\Driving Data\\-battery_periodic_voltage_graph_data.xlsx"

# Check the commented ones
    path=I_file.rsplit('\\',1)[0]
    
    #%%
    pack_no=I_file.split('\\',4)[3]
    
    if ((pack_no=='Pack_1') | (pack_no=='Pack_3')):
        dod=0.85
        
    elif ((pack_no=='Pack_2') | (pack_no=='Pack_4') | (pack_no=='Pack_5')):
        dod=0.9
    
    elif (pack_no=='Pack_6'):
        dod=0.8
    
    #%%
    # df_I=pd.read_excel(I_file,sheet_name=0,header=0) #1
    df_I=pd.read_excel(I_file,sheet_name=0,header=1)
    
    #%%
    #df_I=df_I.rename(columns={'Date Time':'DateTime','Battery Inst Current(A)':'Battery inst Current'})
    
    
    #%%
    df_I['DateTime']=pd.to_datetime(df_I['DateTime'],format='%Y-%m-%d %H:%M:%S',errors='coerce')# change "format" parameter if date format is changed in original file
    # df_I['Time']=pd.to_datetime(df_I['Time'],format='%H:%M:%S',errors='coerce')# change "format" parameter if date format is changed in original file
    
    #%% plots pack voltage and pack current in the same graph;only for charging data
    x0='Time_in_sec'
    try:
        y0='Charger Output Current'
        df_I=df_I.dropna(subset=[y0])
        df_I=df_I.reset_index(drop=True) 
        
        df_I['Time_in_sec_s']=(df_I['DateTime']-df_I['DateTime'].shift(1))/np.timedelta64(1,'s')
        df_I['Time_in_sec']=(df_I['DateTime']-df_I['DateTime'].iloc[0])/np.timedelta64(1,'s')
        
        plt.figure()
        plt.plot(df_I['DateTime'],df_I[y0],'o-',label=y0,markersize=2)
        plt.plot(df_I['DateTime'],df_I['Battery Measured Voltage'],label='Battery Measured Voltage')
        plt.plot(df_I['DateTime'],df_I['Battery Demand Current'],'o-',label='Battery Demand Current',markersize=2)
        plt.xlabel('Time(in sec)',size=14)
        plt.grid(linestyle='dotted')
        plt.legend(loc='best',prop={'size':10})
      
    #%% Discharge Battery current
    except KeyError:
        y0='Battery inst Current' #'Inst Current(A)' #
        
        df_I=df_I.dropna(subset=[y0])
        df_I=df_I.reset_index(drop=True)
        df_I['DateTime']=pd.to_datetime(df_I['DateTime'],format='%Y-%m-%d %H:%M:%S',errors='coerce')
        
        df_I['Time_in_sec_s']=(df_I['DateTime']-df_I['DateTime'].shift(1))/np.timedelta64(1,'s')# time difference b/w every datapt
        df_I['Time_in_sec']=(df_I['DateTime']-df_I['DateTime'].iloc[0])/np.timedelta64(1,'s')
        
    #%% plots the "charger output current" in charging file; or the "Battery inst current" in dchg file
        
    plt.figure()
    plt.plot(df_I['Time_in_sec'],df_I[y0],'o-',markersize=2)
    plt.xlabel('Time(in sec)',size=14)
    plt.ylabel('Current(A)',size=14)
    plt.title(y0,size=16,fontweight='bold')
    plt.grid(linestyle='dotted')
    
    
    #%% Plots current Vs. datetime
    plt.figure()
    plt.plot(df_I['DateTime'],df_I[y0],'o-',markersize=2)
    plt.xlabel('DateTime',size=14)
    plt.ylabel('Current(A)',size=14)
    plt.title(y0,size=16,fontweight='bold')
    plt.grid(linestyle='dotted')
    
    #%% Capacity and SoC & Plot
    df_I['Time_in_sec_s_cap']=np.where((df_I['Time_in_sec_s']>300),np.nan,df_I['Time_in_sec_s'])
    df_I['Cap_inst']=df_I['Time_in_sec_s_cap']*df_I[y0]/3600
    df_I['Capacity']=df_I['Cap_inst'].cumsum()
    df_I['SoC']=((df_I['Capacity'])/(56*dod))*100  #
    try:
        df_I['SoC']=df_I['SoC']+df_I['State Of Charge'].iloc[0]
    except KeyError:
        pass
    
    plt.figure()
    plt.plot(df_I['Time_in_sec'],df_I['Capacity'],label='Capacity')
    plt.xlabel('Time(in sec)',size=14)
    plt.grid(linestyle='dotted')
    plt.legend(loc=2,prop={'size':10})
    
    plt.figure()
    plt.plot(df_I['Time_in_sec'],df_I['SoC'],label='SoC')
    plt.xlabel('Time(in sec)',size=14)
    plt.grid(linestyle='dotted')
    plt.legend(loc=2,prop={'size':10})
    
    df_I=df_I.drop(columns=['Time_in_sec_s_cap'])
    #%% Save as excel file
    df_I.to_excel(path+'\\'+I_file.rsplit('\\',1)[1]+'_modified.xlsx')
    
    #%%
    df_T=pd.read_excel(T_file,sheet_name=0,header=1)
    # df_T=pd.read_excel(T_file,sheet_name=0,header=0)
    
    #%%
    df_T=df_T.rename(columns={'datetime':'DateTime'})
    #%%
    df_T['DateTime']=pd.to_datetime(df_T['DateTime'],format='%Y-%m-%d %H:%M:%S',errors='coerce')# change "format" parameter if date format is changed in original file
    # df_T['DateTime']=pd.to_datetime(df_T['DateTime'],format='%H:%M:%S',errors='coerce')
    df_T['Time_in_sec_s']=(df_T['DateTime']-df_T['DateTime'].shift(1))/np.timedelta64(1,'s') # time difference b/w every datapt
    df_T['Time_in_sec']=(df_T['DateTime']-df_T['DateTime'].iloc[0])/np.timedelta64(1,'s')
    
    #%% Plots the cell temperatures
    
    plt.figure()
    try:
        plt.plot(df_T['DateTime'],df_T.loc[:,'t0':'t5'],'o-',markersize=2)
        plt.legend(['t0','t1','t2','t3','t4','t5'],prop={'size':10})
    except KeyError:
        plt.plot(df_T['DateTime'],df_T.loc[:,'T0':'T5'],'o-',markersize=2)
        plt.legend(['T0','T1','T2','T3','T4','T5'],prop={'size':10})
    plt.xlabel('Time(in sec)',size=14)
    plt.ylabel('Temperature('+u'\N{DEGREE SIGN}'+'C)',size=14)
    plt.title('Cell Temperature',size=16,fontweight='bold')
    plt.grid(linestyle='dotted')
    
    
    #%% Save as excel file
    df_T.to_excel(path+'\\'+T_file.rsplit('\\',1)[1]+'_modified.xlsx')
    
    #%%
    df_V=pd.read_excel(V_file,sheet_name=0,header=1)
    # df_V=pd.read_excel(V_file,sheet_name=0,header=0)
    
    #%%
    df_V=df_V.rename(columns={'datetime':'DateTime'})
    #%%
    
    df_V['DateTime']=pd.to_datetime(df_V['DateTime'],format='%Y-%m-%d %H:%M:%S',errors='coerce')# change "format" parameter if date format is changed in original file
    # df_V['DateTime']=pd.to_datetime(df_V['DateTime'],format='%H:%M:%S',errors='coerce')
    df_V['Time_in_sec_s']=(df_V['DateTime']-df_V['DateTime'].shift(1))/np.timedelta64(1,'s')# time difference b/w every datapt
    df_V['Time_in_sec']=(df_V['DateTime']-df_V['DateTime'].iloc[0])/np.timedelta64(1,'s')
    df_V['Inst_Mean_Voltage']=df_V.loc[:,'C0':'C13'].mean(axis=1)
    
    #%% Plots the cell voltages
    plt.figure()
    plt.plot(df_V[x0],df_V.loc[:,'C0':'C13'],'o-',markersize=2)
    plt.plot(df_V[x0],df_V['Inst_Mean_Voltage'],'^-',color='black',markersize=4)
    #plt.plot(df_V[x0],df_V.loc[:,'c0':'c13'],'o-',markersize=2)
    plt.xlabel('Time(in sec)',size=14)
    plt.ylabel('Voltage(V)',size=14)
    plt.title('Cell Voltage',size=16,fontweight='bold')
    plt.grid(linestyle='dotted')
    plt.legend(['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','Mean Voltage'],prop={'size':10})
    
    
    
    #%% Plots the cell voltages Vs. Datetime
    plt.figure()
    plt.plot(df_V['DateTime'],df_V.loc[:,'C0':'C13'],'o-',markersize=2)
    #plt.plot(df_V['DateTime'],df_V.loc[:,'c0':'c13'],'o-',markersize=2)
    plt.xlabel('DateTime',size=14)
    plt.ylabel('Voltage(V)',size=14)
    plt.title('Cell Voltage',size=16,fontweight='bold')
    plt.grid(linestyle='dotted')
    plt.legend(['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13'],prop={'size':10})
    
    #%%
    df_V['del_V']=(df_V.loc[:,'C0':'C13'].max(axis=1)-df_V.loc[:,'C0':'C13'].min(axis=1))*1000
    
    plt.figure()
    plt.plot(df_V['DateTime'],df_V['del_V'],'o-',markersize=2)
    plt.xlabel('DateTime',size=14)
    plt.ylabel('Voltage(mV)',size=14)
    plt.title('Del V',size=16,fontweight='bold')
    plt.grid(linestyle='dotted')
    
    #%% Save as excel file
    df_V.to_excel(path+'\\'+V_file.rsplit('\\',1)[1]+'_modified.xlsx')

