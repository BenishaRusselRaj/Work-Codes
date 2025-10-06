"""
==============================================================================================
File name: Merge_otd_file_bitwise.py
Desription:
Comments:
==============================================================================================
"""


import numpy as np
import pandas as pd

EOL_Degadation_Value_prcnt = 20



"""
==============================================================================================
Function name: Add_Cycle_nos_to_One_time_data
Desription:
Argument:
Returns:
Comments:
==============================================================================================
"""
def Add_Cycle_nos_to_One_time_data(df_temp):
    for i in range (0,(len(df_temp))):
     arr=np.zeros((len(df_temp[i]))) #, 1
     for j in range(0,len(df_temp[i])):
       arr[j] = j+1
     df_temp[i]['New_cycle_no']=arr
    return df_temp




"""
==============================================================================================
Function name: Clean_One_time_data
Desription:
Argument:
Returns:
Comments:
==============================================================================================
"""
def Clean_One_time_data(df_temp):
    for i in range (0,(len(df_temp))):  #clean charging energy
     df_temp[i] = df_temp[i].replace([np.inf, -np.inf], np.nan)
     df_temp[i] = df_temp[i].dropna(subset=['time'])
     df_temp[i] = df_temp[i].replace(np.nan,0)
     # df_temp[i] = df_temp[i][(df_temp[i][['time']] != 0).all(axis=1)] #anywhr time is 0, delete that row
     df_temp[i] = df_temp[i][(df_temp[i][['chargingEnergy']] < 5000).all(axis=1)]
     df_temp[i] = df_temp[i][(df_temp[i]['time'].diff()/np.timedelta64(1,'s'))>300]
    return df_temp





"""
==============================================================================================
Function name: Estimate_Pack_Capacity_One_time_data
Desription:
Argument:
Returns:
Comments:
==============================================================================================
"""
def Estimate_Pack_Capacity_One_time_data(df_temp):
    for i in range (0,(len(df_temp))): #estimate the pack capacity
        if (((df_temp[i].chargingEnergy).mean())/((df_temp[i].endSOC).mean() -(df_temp[i].startSOC).mean()) ) < 11:
            pack_usable_kWh = 1000;
        if (((((df_temp[i].chargingEnergy).mean())/((df_temp[i].endSOC).mean() -(df_temp[i].startSOC).mean()) ) > 11)&((((df_temp[i].chargingEnergy).mean())/((df_temp[i].endSOC).mean() -(df_temp[i].startSOC).mean()) ) < 13)):
            pack_usable_kWh = 1300;
        if (((df_temp[i].chargingEnergy).mean())/((df_temp[i].endSOC).mean() -(df_temp[i].startSOC).mean()) ) > 13:
            pack_usable_kWh = (df_temp[i].chargingEnergy).mean();
    return df_temp,pack_usable_kWh




"""
==============================================================================================
Function name: Add_BMS_SOH_estimate
Desription:
Argument:
Returns:
Comments:
==============================================================================================
"""
def Add_BMS_SOH_estimate(df_temp):
    for i in range (0,len(df_temp)):
      Max_cycles = 1200
      EOL_percent = 80
      print('Processing Battery No : ', i)
      df_temp[i]['BMS_SOH'] = df_temp[i]['Cycle_No']
      offset = 0
      for j in range (2,len(df_temp[i].Cycle_No)):
          df_temp[i].BMS_SOH.iloc[j] = 100-((EOL_percent/Max_cycles)*df_temp[i].Cycle_No.iloc[j]);
    return df_temp




"""
==============================================================================================
Function name: Add_Cycle_nos_to_chg_dis_rst_states_data
Desription:
Argument:
Returns:
Comments:
==============================================================================================
"""
def Add_Cycle_nos_to_chg_dis_rst_states_data(df_temp):
    for i in range (0,len(df_temp)):
     print('Processing Battery No : ', i)
     df_temp[i]['New_Cyc_no'] = df_temp[i]['Cycle_No']
     offset = 0
     for j in range (2,len(df_temp[i].Cycle_No)):
        del_cycle = df_temp[i].Cycle_No.iloc[j] -  df_temp[i].Cycle_No.iloc[j-1]
        if del_cycle < 0:
            offset = offset + df_temp[i].Cycle_No.iloc[j-1]
        df_temp[i].New_Cyc_no.iloc[j] = df_temp[i].Cycle_No.iloc[j] + offset
     df_temp[i]['Cycle_No'] = df_temp[i]['New_Cyc_no']
    return df_temp

def movingaverage(values,window):
    weights = np.repeat(1.0,window)/window
    smas = np.convolve(values,weights,'valid')
    return smas


"""
==============================================================================================
Function name: SOH_Estimation_by_SOC_window
Desription:
Argument:
Returns:
Comments:
==============================================================================================
"""
def SOH_Estimation_by_SOC_window(chg_E, Start_SOC, End_SOC, pack_rated_capacity ):
    estimate = -1*((chg_E*(100/(Start_SOC- End_SOC)))/pack_rated_capacity) * 100  #
    return estimate



"""
==============================================================================================
Function name: CyclicDegradation
Desription:
Argument:
Returns:
Comments:
==============================================================================================
"""
def CyclicDegradation(chg_E, Start_SOC, End_SOC, pack_rated_capacity):
    estimate = -1*((chg_E*(100/(Start_SOC- End_SOC)))/pack_rated_capacity) * 100  #
    return estimate
