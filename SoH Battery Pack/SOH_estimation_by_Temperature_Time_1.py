"""
==============================================================================================
File name: SOH_estimation_by_Temperature_Time_1.py
Desription:
Comments:
==============================================================================================
"""

import numpy as np
import pandas as pd
EOL_Degadation_Value_prcnt = 20


"""
==============================================================================================
Function name: PHY15_SOH_estimation_by_Temperature_Time
Desription:
Argument:
Returns:
Comments:
==============================================================================================
"""

def PHY15_SOH_estimation_by_Temperature_Time(df1): #time estimate is in minutes
    for i in range (0,len(df1)):
        df1[i]['Cyc_Deg_Prcnt_this_session'] = 0
        df1[i]['Cal_Deg_Prcnt_this_session'] = 0
        df1[i]['Other_Deg_Prcnt__this_session'] = 0
        df1[i]['SOH_states'] = 0
        df1[i]['Predicted_Life'] = 0
        df1[i]['Max_Cycles_Session'] = 0
        df1[i]['Total_Degradation'] = 0
        df1[i]['Other_Deg_Prcnt__this_session'] = 0
        df1[i]['SOC_at_Rest'] = np.nan;



        for j in range (2,len(df1[i].SOH_states)):
            if df1[i].Session_Type.iloc[j] == 'Rest':
                df1[i].SOC_at_Rest.iloc[j] = 94.175*pow(df1[i].end_Avg_Vtg.iloc[j], 2) - 589.25* df1[i].end_Avg_Vtg.iloc[j] + 921.06 #this is not yet updated for 15Ah cell
                if df1[i].SOC_at_Rest.iloc[j] < 0 : df1[i].SOC_at_Rest.iloc[j] = 0;
                if df1[i].SOC_at_Rest.iloc[j] > 100 : df1[i].SOC_at_Rest.iloc[j] = 100;


            if df1[i].Avg_temp.iloc[j] < 25:
                if df1[i].Session_Type.iloc[j] == 'Rest': df1[i].Cal_Deg_Prcnt_this_session.iloc[j] = df1[i].Time_Estimate.iloc[j]*(3.8051/1000000);


            if (df1[i].Avg_temp.iloc[j] >= 25) & (df1[i].Avg_temp.iloc[j] < 35):
                if df1[i].Session_Type.iloc[j] == 'Rest': df1[i].Cal_Deg_Prcnt_this_session.iloc[j] = df1[i].Time_Estimate.iloc[j]*(((0.0951*df1[i].Avg_temp.iloc[j]) + 1.4269)/100000);


            if df1[i].Avg_temp.iloc[j] > 35:
                if df1[i].Session_Type.iloc[j] == 'Rest': df1[i].Cal_Deg_Prcnt_this_session.iloc[j] = df1[i].Time_Estimate.iloc[j]*(((0.0679*df1[i].Avg_temp.iloc[j]) + 2.3782)/100000);

            Deg_Percent = round(np.nansum([df1[i].Cyc_Deg_Prcnt_this_session.iloc[j] , df1[i].Cal_Deg_Prcnt_this_session.iloc[j] , df1[i].Other_Deg_Prcnt__this_session.iloc[j]]),3)
            df1[i].Total_Degradation.iloc[j] = Deg_Percent +  df1[i].Total_Degradation.iloc[j-1]
            df1[i].SOH_states.iloc[j] = 100 - df1[i].Total_Degradation.iloc[j]
            if ((df1[i].Cycle_No_session.iloc[j] - df1[i].Cycle_No_session.iloc[j-1]) == 1):
               if df1[i].Session_Type.iloc[j] == 'Chg': df1[i].Cyc_Deg_Prcnt_this_session.iloc[j] = (((-0.0127*df1[i].Avg_temp.iloc[j]*df1[i].Avg_temp.iloc[j]) +(1.3333*df1[i].Avg_temp.iloc[j]) - 12.063)/1000);
               #df1[i].Predicted_Life.iloc[j] = (df1[i].Cycle_No.iloc[j]*(EOL_Degadation_Value_prcnt/df1[i].Total_Degradation.iloc[j])).astype(int)
            #else:
                #df1[i].Predicted_Life.iloc[j] =  df1[i].Predicted_Life.iloc[j-1]

        #Deg_Percent = round(np.nansum([df1[i]['Cyc_Deg_Prcnt_this_session'] , df1[i]['Cal_Deg_Prcnt_this_session'],df1[i]['Other_Deg_Prcnt__this_session']]),3)
        Max_Cycles_Session = max(df1[i]['Cycle_No_session']) #len(df1[i])/2

        #Life = (Cycles*(EOL_Degadation_Value_prcnt/Deg_Percent)).astype(int) # will b changed

        print(" Battery No: ", i , "    Cycles: ", df1[i].Cycle_No_session.iloc[-1])

        #df1[i]['Predicted_Life'] = Life
        df1[i]['Max_Cycles_Session'] = Max_Cycles_Session
# =============================================================================
#         dfnew[i]['Cycles'] = Cycles
#         dfnew[i]['Predicted_Life'] = Life
#         dfnew[i]['Cycles'] = Cycles
# =============================================================================
    return df1



"""
==============================================================================================
Function name: PHY13_SOH_estimation_by_Temperature_Time
Desription:
Argument:
Returns:
Comments:
==============================================================================================
"""
def PHY13_SOH_estimation_by_Temperature_Time(df1): #time estimate is in minutes
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
        df1[i]['SOC_at_Rest'] = np.nan

        for j in range (2,len(df1[i].SOH)):
            if df1[i].Session_Type.iloc[j] == 'Rest':
                df1[i].SOC_at_Rest.iloc[j] = 94.175*pow(df1[i].end_Avg_Vtg.iloc[j], 2) - 589.25* df1[i].end_Avg_Vtg.iloc[j] + 921.06
                if df1[i].SOC_at_Rest.iloc[j] < 0 : df1[i].SOC_at_Rest.iloc[j] = 0;
                if df1[i].SOC_at_Rest.iloc[j] > 100 : df1[i].SOC_at_Rest.iloc[j] = 100;

            if df1[i].Avg_temp.iloc[j] < 25:
                if df1[i].Session_Type.iloc[j] == 'Rest': df1[i].Cal_Deg_Prcnt_this_session_avg.iloc[j] = df1[i].Time_Estimate.iloc[j]*(4.7564/1000000);

            if (df1[i].Avg_temp.iloc[j] >= 25) & (df1[i].Avg_temp.iloc[j] < 35):
                if df1[i].Session_Type.iloc[j] == 'Rest': df1[i].Cal_Deg_Prcnt_this_session_avg.iloc[j] = df1[i].Time_Estimate.iloc[j]*(((0.2854*df1[i].Avg_temp.iloc[j]) - 2.3782)/100000);

            if df1[i].Avg_temp.iloc[j] > 35:
                if df1[i].Session_Type.iloc[j] == 'Rest': df1[i].Cal_Deg_Prcnt_this_session_avg.iloc[j] = df1[i].Time_Estimate.iloc[j]*(((4.3125*df1[i].Avg_temp.iloc[j]) - 143.33)/100000);

            if ((df1[i].Cycle_No_session.iloc[j] - df1[i].Cycle_No_session.iloc[j-1]) == 1):
               if df1[i].Session_Type.iloc[j] == 'Chg': df1[i].Cyc_Deg_Prcnt_this_session.iloc[j] = (((0.0611*df1[i].Avg_temp.iloc[j]*df1[i].Avg_temp.iloc[j]) -(3.1111*df1[i].Avg_temp.iloc[j]) + 56.25)/1000);

            Deg_Percent = round(np.nansum([df1[i].Cyc_Deg_Prcnt_this_session.iloc[j] , df1[i].Cal_Deg_Prcnt_this_session_avg.iloc[j] , df1[i].Other_Deg_Prcnt__this_session.iloc[j]]),3)
            df1[i].Total_Degradation_avg.iloc[j] = Deg_Percent +  df1[i].Total_Degradation_avg.iloc[j-1]
            df1[i].SOH.iloc[j] = 100 - df1[i].Total_Degradation_avg.iloc[j]
            
#            if ((df1[i].Cycle_No_session.iloc[j] - df1[i].Cycle_No_session.iloc[j-1]) == 1):
#               if df1[i].Session_Type.iloc[j] == 'Chg': df1[i].Cyc_Deg_Prcnt_this_session.iloc[j] = (((0.0611*df1[i].Avg_temp.iloc[j]*df1[i].Avg_temp.iloc[j]) -(3.1111*df1[i].Avg_temp.iloc[j]) + 56.25)/1000);
        
        Cycles = max(df1[i]['Cycle_No_session']) #len(df1[i])/2
        print(" Battery No: ", i , "    Cycles: ", df1[i].Cycle_No_session.iloc[-1])
        df1[i]['Total_Cycles'] = Cycles
# =============================================================================
#         dfnew[i]['Cycles'] = Cycles
#         dfnew[i]['Predicted_Life'] = Life
#         dfnew[i]['Cycles'] = Cycles
# =============================================================================
    return df1


"""
==============================================================================================
Function name: Sample_SOH_estimation_by_Temperature_Time
Desription:
Argument:
Returns:
Comments:
==============================================================================================
"""
def Sample_SOH_estimation_by_Temperature_Time(df1):
    for i in range (0,len(df1)):
        df1[i]['Cyc_Deg_Prcnt_this_session'] = 0
        df1[i]['Cal_Deg_Prcnt_this_session'] = 0
        df1[i]['Other_Deg_Prcnt__this_session'] = 0
        df1[i]['SOH'] = 0

        df1[i].loc[df1[i]['Session_Type'] == 'chg', 'Cyc_Deg_Prcnt_this_session'] = ((0.11*df1[i]['Avg_temp']*df1[i]['Avg_temp'] - 6.11*df1[i]['Avg_temp'] + 100)/1000)/2;
        df1[i].loc[df1[i]['Session_Type'] == 'DChg', 'Cyc_Deg_Prcnt_this_session'] = ((0.11*df1[i]['Avg_temp']*df1[i]['Avg_temp'] - 6.11*df1[i]['Avg_temp'] + 100)/1000)/2;
        df1[i].loc[df1[i]['Session_Type'] == 'rst', 'Cal_Deg_Prcnt_this_session'] = (df1[i]['Time_Estimate']/60)*((0.0734*df1[i]['Avg_temp']*df1[i]['Avg_temp'] - 3.42*df1[i]['Avg_temp'] + 62.582)/100000);
        df1[i]['Cal_Deg_Prcnt_this_session']=(df1[i]['Time_Estimate']/60)*((0.0734*df1[i]['Avg_temp']*df1[i]['Avg_temp'] - 3.42*df1[i]['Avg_temp'] + 62.582)/100000);
        df1[i]['Cyc_Deg_Prcnt_this_session']=((0.11*df1[i]['Avg_temp']*df1[i]['Avg_temp'] - 6.11*df1[i]['Avg_temp'] + 100)/1000)/2; #crude way
        df1[i]['Other_Deg_Prcnt__this_session'] = 0
        for j in range (2,len(df1[i].SOH)):
            df1[i].SOH.iloc[j] = 100 - np.sum([df1[i].Cal_Deg_Prcnt_this_session.iloc[:j]]) - np.sum([df1[i].Cyc_Deg_Prcnt_this_session.iloc[:j]]) - np.sum([df1[i].Other_Deg_Prcnt__this_session.iloc[:j]]);

        Deg_Percent = round(np.nansum([df1[i]['Cyc_Deg_Prcnt_this_session'] , df1[i]['Cal_Deg_Prcnt_this_session'],df1[i]['Other_Deg_Prcnt__this_session']]),3)
        Cycles = len(df1[i])
        Life = (Cycles*(20/Deg_Percent)).astype(int)
        if Life > 1200:
            Life = 1200;
        print("% Degradation = ", Deg_Percent , " ::  Cycles = ", Cycles , " :: Predicted Life = ", Life )
    return df1





'''
            if df1[i].Avg_temp.iloc[j] < 25:
                if chg_taken == 0:
                    if df1[i].Session_Type.iloc[j] == 'Chg': df1[i].Cyc_Deg_Prcnt_this_session.iloc[j] = 25
                   #df1[i].loc[df1[i]['Session_Type'] == 'Chg', 'Cyc_Deg_Prcnt_this_session'] = 25;#(((0.0611*df1[i].Avg_temp.iloc[j]*df1[i].Avg_temp.iloc[j]) -(3.1111*df1[i].Avg_temp.iloc[j]) + 56.25)/2000);
                    print(i,j,(((0.0611*df1[i].Avg_temp.iloc[j]*df1[i].Avg_temp.iloc[j]) -(3.1111*df1[i].Avg_temp.iloc[j]) + 56.25)/2000))
                    chg_taken = 1;
                df1[i].loc[df1[i]['Session_Type'] == 'DChg', 'Cyc_Deg_Prcnt_this_session'] = 25;#(((0.0611*df1[i].Avg_temp.iloc[j]*df1[i].Avg_temp.iloc[j]) -(3.1111*df1[i].Avg_temp.iloc[j]) + 56.25)/2000);
                df1[i].loc[df1[i]['Session_Type'] == 'Rest', 'Cal_Deg_Prcnt_this_session'] = 25;#df1[i].Time_Estimate.iloc[j]*(4.7564/1000000);


            if (df1[i].Avg_temp.iloc[j] >= 25) & (df1[i].Avg_temp.iloc[j] < 35):
                if chg_taken == 0:
                   df1[i].loc[df1[i]['Session_Type'] == 'Chg', 'Cyc_Deg_Prcnt_this_session'] = 35;#(((0.0611*df1[i].Avg_temp.iloc[j]*df1[i].Avg_temp.iloc[j]) -(3.1111*df1[i].Avg_temp.iloc[j]) + 56.25)/2000);
                   chg_taken = 1;
                df1[i].loc[df1[i]['Session_Type'] == 'DChg', 'Cyc_Deg_Prcnt_this_session'] = 35;#(((0.0611*df1[i].Avg_temp.iloc[j]*df1[i].Avg_temp.iloc[j]) -(3.1111*df1[i].Avg_temp.iloc[j]) + 56.25)/2000);
                df1[i].loc[df1[i]['Session_Type'] == 'Rest', 'Cal_Deg_Prcnt_this_session'] = 35;#df1[i].Time_Estimate.iloc[j]*(((0.2854*df1[i].Avg_temp.iloc[j]) - 2.3782)/100000);


            if df1[i].Avg_temp.iloc[j] > 35:
                if chg_taken == 0:
                   df1[i].loc[df1[i]['Session_Type'] == 'Chg', 'Cyc_Deg_Prcnt_this_session'] = 45;#(((0.0611*df1[i].Avg_temp.iloc[j]*df1[i].Avg_temp.iloc[j]) -(3.1111*df1[i].Avg_temp.iloc[j]) + 56.25)/2000);
                   chg_taken = 1;
                df1[i].loc[df1[i]['Session_Type'] == 'DChg', 'Cyc_Deg_Prcnt_this_session'] =45;# (((0.0611*df1[i].Avg_temp.iloc[j]*df1[i].Avg_temp.iloc[j]) -(3.1111*df1[i].Avg_temp.iloc[j]) + 56.25)/2000);
                df1[i].loc[df1[i]['Session_Type'] == 'Rest', 'Cal_Deg_Prcnt_this_session'] =45;#df1[i].Time_Estimate.iloc[j]*(((4.3125*df1[i].Avg_temp.iloc[j]) - 143.33)/100000);

'''