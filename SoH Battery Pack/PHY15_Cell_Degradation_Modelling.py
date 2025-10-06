"""
==============================================================================================
File name: Cell_Degradation_Modelling.py
Desription:
Comments:
==============================================================================================
"""

import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
import matplotlib.colors


def PHY15_Cal_Degradation_model_fitting_90Days():
    temp = np.array([25,35,45,55])
    deg_soc_60 = np.array([0.08,1.2554,1.6641,15.955])
    deg_soc_80 = np.array([0.24,1.3,1.9624,21.751]) #1.0572 changed to 1.3
    deg_soc_100 = np.array([0.26,1.3625,4.5802,23.652])
    f1 = interpolate.interp1d(temp, deg_soc_60, kind='linear')
    f2 = interpolate.interp1d(temp, deg_soc_80, kind='linear')
    f3 = interpolate.interp1d(temp, deg_soc_100, kind='linear')
    return f1, f2, f3


def PHY15_Cal_Degradation_model_fitting_90Days_25to45():
    temp = np.array([25,35,45])#,55])
    deg_soc_60 = np.array([0.08,1.2554,1.6641])#,15.955])
    deg_soc_80 = np.array([0.24,1.3,1.9624])#,21.751]) #1.0572 changed to 1.3
    deg_soc_100 = np.array([0.26,1.3625,4.5802])#,23.652])
    f11 = interpolate.interp1d(temp, deg_soc_60, kind='linear')
    f21 = interpolate.interp1d(temp, deg_soc_80, kind='linear')
    f31 = interpolate.interp1d(temp, deg_soc_100, kind='linear')
    return f11, f21, f31

def PHY15_Cal_Degradation_model_fitting_200Days():
    temp = np.array([25,35,45,55])
    deg_soc_60 = np.array([0.08,1.2554,1.6641,15.955])
    deg_soc_80 = np.array([0.24,1.3,1.9624,21.751]) #1.0572 changed to 1.3
    deg_soc_100 = np.array([0.26,1.3625,4.5802,23.652])
    f1 = interpolate.interp1d(temp, deg_soc_60, kind='linear')
    f2 = interpolate.interp1d(temp, deg_soc_80, kind='linear')
    f3 = interpolate.interp1d(temp, deg_soc_100, kind='linear')
    return f1, f2, f3


def PHY15_Cal_Degradation_model_fitting_200Days_25to45():
    temp = np.array([25,35,45])#,55])
    deg_soc_60 = np.array([0.08,1.2554,1.6641])#,15.955])
    deg_soc_80 = np.array([0.24,1.3,1.9624])#,21.751]) #1.0572 changed to 1.3
    deg_soc_100 = np.array([0.26,1.3625,4.5802])#,23.652])
    f11 = interpolate.interp1d(temp, deg_soc_60, kind='linear')
    f21 = interpolate.interp1d(temp, deg_soc_80, kind='linear')
    f31 = interpolate.interp1d(temp, deg_soc_100, kind='linear')
    return f11, f21, f31


#find deg at 30degC 70%soc
def PHY15_Cal_Degradation_from_SOC_Temperature(SOCx, Tx, f1, f2, f3, time_min):
    if Tx < 25: Tx = 25;
    if Tx > 55: Tx = 55;

    if SOCx < 60: SOCx = 60;
    if SOCx > 100: SOCx = 100;

    No_of_days = 90
    soc = np.array([60,80,100])
    deg_Tx = np.array([f1(Tx),f2(Tx),f3(Tx)])
    f = interpolate.interp1d(soc, deg_Tx, kind='linear')
    degradation1 = f(SOCx)
    degradation = time_min * (degradation1 / (No_of_days*24*60))
    Life_yrs = np.square(20*np.sqrt(No_of_days)/degradation1) / 365 # Deg is proportional to k*sqrt(t)
    return degradation , Life_yrs ; # uncomment to plot thn contour



def PHY15_Plot_Cal_Degradation_Contour():
    Tnew = np.arange(35, 46, 1)
    SOCnew = np.arange(60, 101, 1)
   
    #Tnew = np.arange(35, 56, 1)
    #SOCnew = np.arange(60, 101, 1)
   
    
    Degarr = np.zeros([len(Tnew),len(SOCnew)])
    Life_yrs = np.zeros([len(Tnew),len(SOCnew)])
    f1, f2, f3 = PHY15_Cal_Degradation_model_fitting_90Days_25to45()
    #f1, f2, f3 = PHY15_Cal_Degradation_model_fitting_90Days()
    
    
    for i in range(len(Tnew)):
        print(i)
        for j in range(len(SOCnew)):
            Degarr[i][j], Life_yrs[i][j]  = PHY15_Cal_Degradation_from_SOC_Temperature(SOCnew[j], Tnew[i], f1, f2, f3, 90*24*60);
            
    fig, ax = plt.subplots()
    cf = ax.contourf(SOCnew,Tnew,Degarr)
    fig.colorbar(cf, ax=ax)
    plt.xlabel('SOC (%)', fontweight='bold',size=10)
    plt.ylabel('Storage Temperature (Deg C)', fontweight='bold',size=10)
    plt.title('% Calander Degradation',fontweight='bold',size=14)
    plt.savefig('PHY15_Cal_Deg_25to45.png', format='png', dpi=1200)

    fig, ax = plt.subplots()
    cf = ax.contourf(SOCnew,Tnew,Life_yrs)
    fig.colorbar(cf, ax=ax)
    plt.xlabel('SOC (%)', fontweight='bold',size=10)
    plt.ylabel('Storage Temperature (Deg C)', fontweight='bold',size=10)
    plt.title('Estimated Life (in years)',fontweight='bold',size=14)
    plt.savefig('PHY15_cal_life_25to45.png', format='png', dpi=1200)



def PHY15_Cyc_Degradation_model_fitting():
    temp = np.array([25,35,45])
    deg_dod_80 = np.array([20/2250 , 20/1250, 20/950])
    deg_dod_100 = np.array([20/1500, 20/1050, 20/700])
    
    f4 = interpolate.interp1d(temp, deg_dod_80, kind='linear')
    f5 = interpolate.interp1d(temp, deg_dod_100, kind='linear')
    
    return f4, f5




def PHY15_Cyc_Degradation_from_SOC_Temperature(DoDx, Tx, f4, f5, no_of_cycles):
    if Tx < 25: Tx = 25;
    if Tx > 45: Tx = 45;

    if DoDx < 80: DoDx = 60;
    if DoDx > 100: DoDx = 100;

    dod = np.array([80,100])
    deg_Tx = np.array([f4(Tx),f5(Tx)])
    
    f = interpolate.interp1d(dod, deg_Tx, kind='linear')
    degradation1 = f(DoDx)
    degradation = no_of_cycles * degradation1
    Life_cycles = (no_of_cycles * 20)/degradation
    return degradation , Life_cycles ; # uncomment to plot thn contour




def PHY15_Plot_Cyc_Degradation_Contour():
    Tnew = np.arange(25, 46, 1)
    DoDnew = np.arange(80, 101, 1)
    Degarr = np.zeros([len(Tnew),len(DoDnew)])
    Life_cycles = np.zeros([len(Tnew),len(DoDnew)])
    f1, f2, f3 = PHY15_Cal_Degradation_model_fitting_90Days()
    for i in range(len(Tnew)):
        print(i)
        for j in range(len(DoDnew)):
            Degarr[i][j], Life_cycles[i][j]  = PHY15_Cyc_Degradation_from_SOC_Temperature(DoDnew[j], Tnew[i], f4, f5, 90*24*60);
            
    fig, ax = plt.subplots()
    cf = ax.contourf(DoDnew,Tnew,Degarr)
    fig.colorbar(cf, ax=ax)
    plt.xlabel('DoD (%)', fontweight='bold',size=10)
    plt.ylabel('Cycling Temperature (Deg C)', fontweight='bold',size=10)
    plt.title('% Cyclic Degradation',fontweight='bold',size=14)
    plt.savefig('PHY15_Cyc_Deg.png', format='png', dpi=1200)

    fig, ax = plt.subplots()
    cf = ax.contourf(DoDnew,Tnew,Life_cycles)
    fig.colorbar(cf, ax=ax)
    plt.xlabel('DoD (%)', fontweight='bold',size=10)
    plt.ylabel('Cycling Temperature (Deg C)', fontweight='bold',size=10)
    plt.title('No of cycles for 20% Degradation',fontweight='bold',size=14)
    plt.savefig('PHY15_cyc_life.png', format='png', dpi=1200)





def PHY15_SOH_estimation(df1): #time estimate is in minutes
    f1, f2, f3 = PHY15_Cal_Degradation_model_fitting_90Days()
    for i in range (0,len(df1)):
        df1[i]['Cyc_Deg_Prcnt_this_session'] = 0
        
        df1[i]['Cal_Deg_Prcnt_this_session_avg'] = 0
        df1[i]['Cal_Deg_Prcnt_this_session_min'] = 0
        df1[i]['Cal_Deg_Prcnt_this_session_max'] = 0
        
        
        df1[i]['Other_Deg_Prcnt__this_session'] = 0
        df1[i]['SOH_states'] = 0
        df1[i]['Predicted_Life'] = 0
        df1[i]['Max_Cycles_Session'] = 0
        
        df1[i]['Total_Degradation_avg'] = 0 # average temp
        df1[i]['Total_Degradation_min'] = 0 # min temp
        df1[i]['Total_Degradation_max'] = 0 # max temp
        
        df1[i]['Other_Deg_Prcnt__this_session'] = 0
        df1[i]['SOC_at_Rest'] = np.nan;

        for j in range (2,len(df1[i].SOH_states)):
            Tx_avg = df1[i].T_pack_Avg.iloc[j]
            Tx_min = df1[i].T_pack_Min.iloc[j]
            Tx_max = df1[i].T_pack_Max.iloc[j]            
            
            if df1[i].Session_Type.iloc[j] == 'Rest':
               df1[i].SOC_at_Rest.iloc[j] = 94.175*pow(df1[i].end_Avg_Vtg.iloc[j], 2) - 589.25* df1[i].end_Avg_Vtg.iloc[j] + 921.06;
               SOCx = df1[i].SOC_at_Rest.iloc[j]
               df1[i].Cal_Deg_Prcnt_this_session_avg.iloc[j] =  PHY15_Cal_Degradation_from_SOC_Temperature(SOCx, Tx_avg, f1, f2, f3, df1[i].Time_Estimate.iloc[j]);
               df1[i].Cal_Deg_Prcnt_this_session_min.iloc[j] =  PHY15_Cal_Degradation_from_SOC_Temperature(SOCx, Tx_min, f1, f2, f3, df1[i].Time_Estimate.iloc[j]);
               df1[i].Cal_Deg_Prcnt_this_session_max.iloc[j] =  PHY15_Cal_Degradation_from_SOC_Temperature(SOCx, Tx_max, f1, f2, f3, df1[i].Time_Estimate.iloc[j]);


            if ((df1[i].Cycle_No_session.iloc[j] - df1[i].Cycle_No_session.iloc[j-1]) == 1):
               if df1[i].Session_Type.iloc[j] == 'Chg': df1[i].Cyc_Deg_Prcnt_this_session.iloc[j] = (((-0.0127*df1[i].Avg_temp.iloc[j]*df1[i].Avg_temp.iloc[j]) +(1.3333*df1[i].Avg_temp.iloc[j]) - 12.063)/1000);


            Deg_Percent_avg = round(np.nansum([df1[i].Cyc_Deg_Prcnt_this_session.iloc[j] , df1[i].Cal_Deg_Prcnt_this_session_avg.iloc[j] , df1[i].Other_Deg_Prcnt__this_session.iloc[j]]),3)
            Deg_Percent_min = round(np.nansum([df1[i].Cyc_Deg_Prcnt_this_session.iloc[j] , df1[i].Cal_Deg_Prcnt_this_session_min.iloc[j] , df1[i].Other_Deg_Prcnt__this_session.iloc[j]]),3)
            Deg_Percent_max = round(np.nansum([df1[i].Cyc_Deg_Prcnt_this_session.iloc[j] , df1[i].Cal_Deg_Prcnt_this_session_max.iloc[j] , df1[i].Other_Deg_Prcnt__this_session.iloc[j]]),3)
            
            df1[i].Total_Degradation_avg.iloc[j] = Deg_Percent_avg +  df1[i].Total_Degradation_avg.iloc[j-1]
            df1[i].SOH_states.iloc[j] = 100 - df1[i].Total_Degradation_avg.iloc[j]

            df1[i].Total_Degradation_min.iloc[j] = Deg_Percent_min +  df1[i].Total_Degradation_min.iloc[j-1]

            df1[i].Total_Degradation_max.iloc[j] = Deg_Percent_max +  df1[i].Total_Degradation_max.iloc[j-1]


#            if ((df1[i].Cycle_No_session.iloc[j] - df1[i].Cycle_No_session.iloc[j-1]) == 1):
#               if df1[i].Session_Type.iloc[j] == 'Chg': df1[i].Cyc_Deg_Prcnt_this_session.iloc[j] = (((-0.0127*df1[i].Avg_temp.iloc[j]*df1[i].Avg_temp.iloc[j]) +(1.3333*df1[i].Avg_temp.iloc[j]) - 12.063)/1000);

        Max_Cycles_Session = max(df1[i]['Cycle_No_session']) #len(df1[i])/2
        print(" Battery No: ", i , "    Cycles: ", df1[i].Cycle_No_session.iloc[-1])
        df1[i]['Max_Cycles_Session'] = Max_Cycles_Session
    return df1


    