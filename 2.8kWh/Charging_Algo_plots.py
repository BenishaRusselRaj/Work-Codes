# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 12:30:01 2021

@author: IITM
"""

"""
To analyze the 2.8kWh pack data
The data shared is of .xls format and there are three different files
Open the file, change file extension by "Save as" option and change to .xlsx
Use the .xlsx files in this code(as of now, it couldn't read .xls format)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
'''
In this block, the path to the files are added;
I_file is the "periodic_graph_data" file
T_file is the "temperature_graph_data" file
V_file is the "voltage_graph_data" file

'''

I_file="D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_3\\23_04_25\\PACK3Data_21-04-2023\\PACK3Data_21-04-2023\\Charging Data\\-charging_periodic_graph_data (2).xlsx"
T_file="D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_3\\23_04_25\\PACK3Data_21-04-2023\\PACK3Data_21-04-2023\\Charging Data\\-charging_temperature_graph_data- (2).xlsx"
V_file="D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_3\\23_04_25\\PACK3Data_21-04-2023\\PACK3Data_21-04-2023\\Charging Data\\-charging_voltage_graph_data (3).xlsx"

path=I_file.rsplit('\\',1)[0]

#%%
pack_no=I_file.split('\\',4)[3]

if ((pack_no=='Pack_1') | (pack_no=='Pack_3')):
    dod=0.85
    
elif ((pack_no=='Pack_2') | (pack_no=='Pack_4') | (pack_no=='Pack_5') | (pack_no=='Pack_7') | (pack_no=='Pack_8')| (pack_no=='Pack_9')):
    dod=0.9

elif (pack_no=='Pack_6'):
    dod=0.8

#%% The initial capacity values are hard-coded in this block; these values are obtained from the initial capacity tests of each pack

Q_init=56 # The expected capacity of the packs

if (pack_no=='Pack_1'):
    Q_init=53.78
    
elif (pack_no=='Pack_2'):
    Q_init=49.04
    
elif (pack_no=='Pack_3'):
    Q_init=50.17
    
elif (pack_no=='Pack_4'):
    Q_init=49.42

elif (pack_no=='Pack_5'):
    Q_init=50.58
    
elif (pack_no=='Pack_7'):
    Q_init=54.55
    
elif (pack_no=='Pack_8'):
    Q_init=53.14
    
elif (pack_no=='Pack_9'):
    Q_init=55.36
    
#%%
df_I=pd.read_excel(I_file,sheet_name=0,header=1)

#%%
df_I['DateTime']=pd.to_datetime(df_I['DateTime'],format='%Y-%m-%d %H:%M:%S',errors='coerce')# change "format" parameter if date format is changed in original file

#%% Plots pack voltage and pack current in the same graph;only for charging data
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
    plt.savefig(path+'\\'+I_file.rsplit('\\',4)[1]+'_'+I_file.rsplit('\\',3)[1]+'_'+I_file.rsplit('\\',2)[1]+'_Pack voltage, Current and Demand Current.png',dpi=1200)
  
#%% Discharge Battery current
except KeyError:
    y0='Battery inst Current'   
    df_I=df_I.dropna(subset=[y0])
    df_I=df_I.reset_index(drop=True)
    df_I['DateTime']=pd.to_datetime(df_I['DateTime'],format='%Y-%m-%d %H:%M:%S',errors='coerce')
    
    df_I['Time_in_sec_s']=(df_I['DateTime']-df_I['DateTime'].shift(1))/np.timedelta64(1,'s')# time difference b/w every datapt
    df_I['Time_in_sec']=(df_I['DateTime']-df_I['DateTime'].iloc[0])/np.timedelta64(1,'s')
    
#%% Plots the "charger output current" in charging file; or the "Battery inst current" in dchg file   
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
plt.savefig(path+'\\'+I_file.rsplit('\\',4)[1]+'_'+I_file.rsplit('\\',3)[1]+'_'+I_file.rsplit('\\',2)[1]+'_'+y0+'.png',dpi=1200)

#%% Capacity and SoC & Plot
df_I['Time_in_sec_s_cap']=np.where((df_I['Time_in_sec_s']>300),np.nan,df_I['Time_in_sec_s'])
df_I['Cap_inst']=df_I['Time_in_sec_s_cap']*df_I[y0]/3600
df_I['Capacity']=df_I['Cap_inst'].cumsum()
df_I['SoC']=((df_I['Capacity'])/(Q_init*dod))*100  
try:
    df_I['SoC']=df_I['SoC']+df_I['State Of Charge'].iloc[0]
except KeyError:
    pass

#%%
plt.figure()
plt.plot(df_I['Time_in_sec'],df_I['Capacity'],label='Capacity')
plt.xlabel('Time(in sec)',size=14)
plt.ylabel('Capacity(Ah)',size=14)
plt.grid(linestyle='dotted')
plt.legend(loc=2,prop={'size':10})
plt.savefig(path+'\\'+I_file.rsplit('\\',4)[1]+'_'+I_file.rsplit('\\',3)[1]+'_'+I_file.rsplit('\\',2)[1]+'_Capacity.png',dpi=1200)

#%%
plt.figure()
plt.plot(df_I['Time_in_sec'],df_I['SoC'],label='SoC')
plt.xlabel('Time(in sec)',size=14)
plt.ylabel('SoC(%)',size=14)
plt.grid(linestyle='dotted')
plt.legend(loc=2,prop={'size':10})
plt.savefig(path+'\\'+I_file.rsplit('\\',4)[1]+'_'+I_file.rsplit('\\',3)[1]+'_'+I_file.rsplit('\\',2)[1]+'_SoC.png',dpi=1200)  

df_I=df_I.drop(columns=['Time_in_sec_s_cap'])
#%% Save as excel file
df_I.to_excel(path+'\\'+I_file.rsplit('\\',1)[1]+'_modified.xlsx')

#%%
df_T=pd.read_excel(T_file,sheet_name=0,header=1)

#%%
df_T=df_T.rename(columns={'datetime':'DateTime'})
#%%
df_T['DateTime']=pd.to_datetime(df_T['DateTime'],format='%Y-%m-%d %H:%M:%S',errors='coerce')# change "format" parameter if date format is changed in original file
df_T['Time_in_sec_s']=(df_T['DateTime']-df_T['DateTime'].shift(1))/np.timedelta64(1,'s') # time difference b/w every datapt
df_T['Time_in_sec']=(df_T['DateTime']-df_T['DateTime'].iloc[0])/np.timedelta64(1,'s')

#%% Plots the cell temperatures

plt.figure()
try:
    plt.plot(df_T['DateTime'],df_T.loc[:,'t0':'t5'],'o-',markersize=2)
    plt.legend(['t0','t1','t2','t3','t4','t5'],prop={'size':10}) #,'t6','t7','t8','t9','t10','t11','t12'
except KeyError:
    plt.plot(df_T['DateTime'],df_T.loc[:,'T0':'T5'],'o-',markersize=2)
    plt.legend(['T0','T1','T2','T3','T4','T5'],prop={'size':10})
plt.xlabel('Time',size=14)
plt.ylabel('Temperature('+u'\N{DEGREE SIGN}'+'C)',size=14)
plt.title('Cell Temperature',size=16,fontweight='bold')
plt.grid(linestyle='dotted')
plt.savefig(path+'\\'+I_file.rsplit('\\',4)[1]+'_'+I_file.rsplit('\\',3)[1]+'_'+I_file.rsplit('\\',2)[1]+'_Cell Temperature.png',dpi=1200)

#%%
df_V=pd.read_excel(V_file,sheet_name=0,header=1)

#%%
df_V=df_V.rename(columns={'datetime':'DateTime'})

#%%
df_V['DateTime']=pd.to_datetime(df_V['DateTime'],format='%Y-%m-%d %H:%M:%S',errors='coerce')# change "format" parameter if date format is changed in original file
df_V['Time_in_sec_s']=(df_V['DateTime']-df_V['DateTime'].shift(1))/np.timedelta64(1,'s')# time difference b/w every datapt
df_V['Time_in_sec']=(df_V['DateTime']-df_V['DateTime'].iloc[0])/np.timedelta64(1,'s')
df_V['Inst_Mean_Voltage']=df_V.loc[:,'C0':'C13'].mean(axis=1)

#%% Plots the cell voltages
plt.figure()
plt.plot(df_V[x0],df_V.loc[:,'C0':'C13'],'o-',markersize=2)
plt.plot(df_V[x0],df_V['Inst_Mean_Voltage'],'^-',color='black',markersize=4)
plt.xlabel('Time(in sec)',size=14)
plt.ylabel('Voltage(V)',size=14)
plt.title('Cell Voltage',size=16,fontweight='bold')
plt.grid(linestyle='dotted')
plt.legend(['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','Mean Voltage'],prop={'size':10})
plt.savefig(path+'\\'+I_file.rsplit('\\',4)[1]+'_'+I_file.rsplit('\\',3)[1]+'_'+I_file.rsplit('\\',2)[1]+'_Cell Voltage_with_mean_Voltage.png',dpi=1200)

#%% Plots the cell voltages Vs. Datetime
plt.figure()
plt.plot(df_V['DateTime'],df_V.loc[:,'C0':'C13'],'o-',markersize=2)
plt.xlabel('DateTime',size=14)
plt.ylabel('Voltage(V)',size=14)
plt.title('Cell Voltage',size=16,fontweight='bold')
plt.grid(linestyle='dotted')
plt.legend(['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13'],prop={'size':10})
plt.savefig(path+'\\'+I_file.rsplit('\\',4)[1]+'_'+I_file.rsplit('\\',3)[1]+'_'+I_file.rsplit('\\',2)[1]+'_Cell Voltage.png',dpi=1200)

#%%
df_V['del_V']=(df_V.loc[:,'C0':'C13'].max(axis=1)-df_V.loc[:,'C0':'C13'].min(axis=1))*1000
plt.figure()
plt.plot(df_V['DateTime'],df_V['del_V'],'o-',markersize=2)
plt.xlabel('DateTime',size=14)
plt.ylabel('Voltage(mV)',size=14)
plt.title('Del V',size=16,fontweight='bold')
plt.grid(linestyle='dotted')
plt.savefig(path+'\\'+I_file.rsplit('\\',4)[1]+'_'+I_file.rsplit('\\',3)[1]+'_'+I_file.rsplit('\\',2)[1]+'_Delta Voltage.png',dpi=1200)

#%% Save as excel file
df_V.to_excel(path+'\\'+V_file.rsplit('\\',1)[1]+'_modified.xlsx')

#%% This block prints the time when the large time intervals of data are missing; 
# Gives an idea about missing data

f=open(path+'\\'+I_file.rsplit('\\',4)[1]+'_'+I_file.rsplit('\\',3)[1]+'_'+I_file.rsplit('\\',2)[1]+'.txt',"w")

print('======================================================================',file=f)
print('---------------------Periodic Data---------------------',file=f)
print('Datapoints:%s' % (len(df_I)),file=f)
print('Total Time Spent:%s hours' % ((df_I['DateTime'].iloc[-1]-df_I['DateTime'].iloc[0])/np.timedelta64(1,'h')),file=f)
print('Maximum Current:%s ; Minimum Current:%s' % (df_I[y0].max(),df_I[y0].min()),file=f)
print('Maximum Capacity:%s ; Minimum Capacity:%s' % (df_I['Capacity'].max(),df_I['Capacity'].min()),file=f)
print('Maximum SoC:%s ; Minimum SoC:%s' % (df_I['SoC'].max(),df_I['SoC'].min()),file=f)
print('-------------------------------------------------------------------',file=f)
print('Start time:%s ; Current:%s' % (df_I['DateTime'].iloc[0] , df_I[y0].iloc[0]),file=f)
x= df_I['DateTime'].iloc[0]
l0=df_I[df_I['Time_in_sec_s']>3600].index.tolist()
for i in l0:
    print('End time:%s ; Current:%s' % (df_I['DateTime'].iloc[i-1] , df_I[y0].iloc[i-1]),file=f)
    print('Time Spent:%s minutes' % ((df_I['DateTime'].iloc[i-1]-x)/np.timedelta64(1,'m')),file=f)
    print('-------------------------------------------------------------------',file=f)
    print('Start time:%s ; Current:%s' % (df_I['DateTime'].iloc[i] , df_I[y0].iloc[i]),file=f)
    x=df_I['DateTime'].iloc[i]
print('End time:%s ; Current_final:%s' % (df_I['DateTime'].iloc[-1] , df_I[y0].iloc[-1]),file=f)
print('Time Spent:%s minutes' % ((df_I['DateTime'].iloc[-1]-x)/np.timedelta64(1,'m')),file=f)
print('Current Fluctuations:',file=f)
print('Observations:',file=f)
print('======================================================================',file=f)

#%% This block prints the time when the large time intervals of data are missing; 

print('---------------------Temperature Data---------------------',file=f)
print('Datapoints:%s' % (len(df_T)),file=f)
print('Total Time Spent:%s hours' % ((df_T['DateTime'].iloc[-1]-df_T['DateTime'].iloc[0])/np.timedelta64(1,'h')),file=f)

l1=df_T[df_T['Time_in_sec_s']>3600].index.tolist()

try:
    print('Start time:%s\nStart:H.Temp:%s(%s) ; L.Temp:%s(%s) ; diff: %s (deg C)' % (df_T['DateTime'].iloc[0] , df_T.loc[0,'t0':'t3'].max() , pd.to_numeric(df_T.loc[0,'t0':'t3']).idxmax() , df_T.loc[0,'t0':'t3'].min() , pd.to_numeric(df_T.loc[0,'t0':'t3']).idxmin() , (df_T.loc[0,'t0':'t3'].max()-df_T.loc[0,'t0':'t3'].min())),file=f)
    x= df_T['DateTime'].iloc[0]
    for i in l1:
        print('End time:%s\nEnd:H.Temp:%s(%s) ; L.Temp:%s(%s) ; diff:%s(deg C)' % (df_T['DateTime'].iloc[i-1] , df_T.loc[i-1,'t0':'t3'].max() , pd.to_numeric(df_T.loc[i-1,'t0':'t3']).idxmax(), df_T.loc[i-1,'t0':'t3'].min() , pd.to_numeric(df_T.loc[i-1,'t0':'t3']).idxmin() , (df_T.loc[i-1,'t0':'t3'].max()-df_T.loc[i-1,'t0':'t3'].min())),file=f)
        print('Time Spent:%s minutes' % ((df_T['DateTime'].iloc[i-1]-x)/np.timedelta64(1,'m')),file=f)
        print('-------------------------------------------------------------------',file=f)
        print('Start time:%s\nStart:H.Temp:%s(%s) ; L.Temp:%s(%s) ; diff:%s(deg C)' % (df_T['DateTime'].iloc[i] , df_T.loc[i,'t0':'t3'].max() , pd.to_numeric(df_T.loc[i,'t0':'t3']).idxmax(), df_T.loc[i,'t0':'t3'].min() , pd.to_numeric(df_T.loc[i,'t0':'t3']).idxmin() , (df_T.loc[i,'t0':'t3'].max()-df_T.loc[i,'t0':'t3'].min())),file=f)
        x=df_T['DateTime'].iloc[i]
    print('End time:%s\nEnd:H.Temp:%s(%s) ; L.Temp:%s(%s) ; diff:%s(deg C)' % (df_T['DateTime'].iloc[-1] , df_T.loc[len(df_T)-1,'t0':'t3'].max() , pd.to_numeric(df_T.loc[len(df_T)-1,'t0':'t3']).idxmax(), df_T.loc[len(df_T)-1,'t0':'t3'].min() , pd.to_numeric(df_T.loc[len(df_T)-1,'t0':'t3']).idxmin(),(df_T.loc[len(df_T)-1,'t0':'t3'].max()-df_T.loc[len(df_T)-1,'t0':'t3'].min())),file=f)
    print('Time Spent:%s minutes' % ((df_T['DateTime'].iloc[-1]-x)/np.timedelta64(1,'m')),file=f)
    print('Highest Temperatures:\n%s' % (df_T.loc[:,'t0':'t5'].max()),file=f)
    print('Lowest Temperatures:\n%s' % (df_T.loc[:,'t0':'t5'].min()), file=f)
    print('Observations:',file=f)
    print('======================================================================',file=f)

except KeyError:
    print('Start time:%s\nStart:H.Temp:%s(%s) ; L.Temp:%s(%s) ; diff:%s(deg C)' % (df_T['DateTime'].iloc[0] , df_T.loc[0,'T0':'T3'].max() , pd.to_numeric(df_T.loc[0,'T0':'T3']).idxmax() , df_T.loc[0,'T0':'T3'].min() , pd.to_numeric(df_T.loc[0,'T0':'T3']).idxmin(),(df_T.loc[0,'T0':'T3'].max()-df_T.loc[0,'T0':'T3'].min())),file=f)
    x= df_T['DateTime'].iloc[0]
    for i in l1:
        print('End time:%s\nEnd:H.Temp:%s(%s) ; L.Temp:%s(%s) ; diff:%s(deg C)' % (df_T['DateTime'].iloc[i-1] , df_T.loc[i-1,'T0':'T3'].max() , pd.to_numeric(df_T.loc[i-1,'T0':'T3']).idxmax() , df_T.loc[i-1,'T0':'T3'].min() , pd.to_numeric(df_T.loc[i-1,'T0':'T3']).idxmin(),(df_T.loc[i-1,'T0':'T3'].max()-df_T.loc[i-1,'T0':'T3'].min())),file=f)
        print('Time Spent:%s minutes' % ((df_T['DateTime'].iloc[i-1]-x)/np.timedelta64(1,'m')),file=f)
        print('-------------------------------------------------------------------',file=f)
        print('Start time:%s\nStart:H.Temp:%s(%s) ; L.Temp:%s(%s) ; diff:%s(deg C)' % (df_T['DateTime'].iloc[i] , df_T.loc[i,'T0':'T3'].max() , pd.to_numeric(df_T.loc[i,'T0':'T3']).idxmax() , df_T.loc[i,'T0':'T3'].min() , pd.to_numeric(df_T.loc[i,'T0':'T3']).idxmin(),(df_T.loc[i,'T0':'T3'].max()-df_T.loc[i,'T0':'T3'].min())),file=f)
        x=df_T['DateTime'].iloc[i]
    print('End time:%s\nEnd:H.Temp:%s(%s) ; L.Temp:%s(%s) ; diff:%s(deg C)' % (df_T['DateTime'].iloc[-1] , df_T.loc[len(df_T)-1,'T0':'T3'].max() , pd.to_numeric(df_T.loc[len(df_T)-1,'T0':'T3']).idxmax() , df_T.loc[len(df_T)-1,'T0':'T3'].min() , pd.to_numeric(df_T.loc[len(df_T)-1,'T0':'T3']).idxmin(),(df_T.loc[len(df_T)-1,'T0':'T3'].max()-df_T.loc[len(df_T)-1,'T0':'T3'].min())),file=f)
    print('Time Spent:%s minutes' % ((df_T['DateTime'].iloc[-1]-x)/np.timedelta64(1,'m')),file=f)
    print('Highest temperatures:\n%s' % (df_T.loc[:,'T0':'T5'].max()),file=f)
    print('lowest Temperatures:\n%s' % (df_T.loc[:,'T0':'T5'].min()), file=f)
    print('Observations:',file=f)
    print('======================================================================',file=f)
    
#%%
print('---------------------Voltage Data---------------------',file=f)
print('Datapoints:%s' % (len(df_V)),file=f)
print('Total Time Spent:%s hours' % ((df_V['DateTime'].iloc[-1]-df_V['DateTime'].iloc[0])/np.timedelta64(1,'h')),file=f)
print('Start time:%s\nStart:H.Volt:%sV(%s) ; L.Volt:%sV(%s) ; diff: %smV' % (df_V['DateTime'].iloc[0] , df_V.loc[0,'C0':'C13'].max() , pd.to_numeric(df_V.loc[0,'C0':'C13']).idxmax() , df_V.loc[0,'C0':'C13'].min() , pd.to_numeric(df_V.loc[0,'C0':'C13']).idxmin(),(df_V.loc[0,'C0':'C13'].max()-df_V.loc[0,'C0':'C13'].min())*1000),file=f)
x= df_V['DateTime'].iloc[0]
l2=df_V[df_V['Time_in_sec_s']>3600].index.tolist()
for i in l2:
    print('End time:%s\nEnd:H.Volt:%sV(%s) ; L.Volt:%sV(%s) ; diff: %smV' % (df_V['DateTime'].iloc[i-1] , df_V.loc[i-1,'C0':'C13'].max() , pd.to_numeric(df_V.loc[i-1,'C0':'C13']).idxmax() , df_V.loc[i-1,'C0':'C13'].min() , pd.to_numeric(df_V.loc[i-1,'C0':'C13']).idxmin(),(df_V.loc[i-1,'C0':'C13'].max()-df_V.loc[i-1,'C0':'C13'].min())*1000),file=f)
    print('Time Spent:%s minutes' % ((df_V['DateTime'].iloc[i-1]-x)/np.timedelta64(1,'m')),file=f)
    print('Voltage Fluctuations:',file=f)
    print('Observations:',file=f)
    print('End Del V:%s mV' % (df_V['del_V'].iloc[i-1]),file=f)
    print('-------------------------------------------------------------------',file=f)
    print('Start time:%s\nStart:H.Volt:%sV(%s) ; L.Volt:%sV(%s) ; diff: %smV' % (df_V['DateTime'].iloc[i] , df_V.loc[i,'C0':'C13'].max() , pd.to_numeric(df_V.loc[i,'C0':'C13']).idxmax() , df_V.loc[i,'C0':'C13'].min() , pd.to_numeric(df_V.loc[i,'C0':'C13']).idxmin(),(df_V.loc[i,'C0':'C13'].max()-df_V.loc[i,'C0':'C13'].min())*1000),file=f)
    x=df_V['DateTime'].iloc[i]
print('End time:%s\nEnd:H.Volt:%sV(%s) ; L.Volt:%sV(%s) ; diff: %smV' % (df_V['DateTime'].iloc[-1] , df_V.loc[len(df_V)-1,'C0':'C13'].max() , pd.to_numeric(df_V.loc[len(df_V)-1,'C0':'C13']).idxmax() , df_V.loc[len(df_V)-1,'C0':'C13'].min() , pd.to_numeric(df_V.loc[len(df_V)-1,'C0':'C13']).idxmin(),(df_V.loc[len(df_V)-1,'C0':'C13'].max()-df_V.loc[len(df_V)-1,'C0':'C13'].min())*1000),file=f)
print('Time Spent:%s minutes' % ((df_V['DateTime'].iloc[-1]-x)/np.timedelta64(1,'m')),file=f)
print('Highest Voltages:\n%s'% (df_V.loc[:,'C0':'C13'].max()), file=f)
print('Lowest Voltages:\n%s' % (df_V.loc[:,'C0':'C13'].min()), file=f)
print('Voltage Fluctuations:',file=f)
print('Observations:',file=f)
print('End Del V:%s mV' % (df_V['del_V'].iloc[-1]),file=f)
print('Max delV:%s mV' % (df_V['del_V'].max()), file=f)
print('======================================================================',file=f)
f.close()
