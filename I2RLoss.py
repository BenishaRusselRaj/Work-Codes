# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:43:16 2019

@author: IITM
"""

import time
start = time.time()
import pickle
import pandas as pd
import numpy as np
with open("D:\\New folder (2)\\Text file manipulation Codes\\PHY_13Ah_AllCycles_AllCycles_raw.pkl",'rb') as f:
    data= pickle.load(f)
    df=pd.DataFrame()
    data[['Cycle_No','Current','Q_in_out']]=data[['Cycle_No','Current','Q_in_out']].astype(float)
    x=['0.5','1','1.5','2','3','0.3'];x1=['0.5','1','1.5','2','3','0.1'] 
    df_Chg= pd.read_excel("D:\\New folder (2)\\Phy13 new cell diff rates.xlsx", sheet_name='Charging')
    df_DChg= pd.read_excel("D:\\New folder (2)\\Phy13 new cell diff rates.xlsx", sheet_name='Discharge')
    data=data[data.Cycle_No==2]
    print('.............1/3')
    grouped=data.groupby(['Step_No'])
    def conc_df(df2):
        global df
        df=df.append(df2)
    for name,group in grouped:
        group['SOC']=(group['Q_in_out']/(group['Q_in_out'].iloc[-1]))*100;j=len(group)
        group['SOC']=round(group['SOC'],2)
        if ((group.Step_Type=='CCCV_Chg').all()):
            for a in range(0,6):
                group['Vt_Chg'+x[a]+'C']=''
                df_Chg['SOC_'+x[a]+'C']=round(df_Chg['SOC_'+x[a]+'C'],2)
                for i in group.index:
                    try:
                        if(group['SOC'].iloc[i]==(df_Chg['SOC_'+x[a]+'C'].iloc[i]).astype(float)):
                            group['Vt_Chg'+x[a]+'C'].iloc[i]=df_Chg['V_'+x[a]+'C'].iloc[i]
                        else:
                            group['Vt_Chg'+x[a]+'C'].iloc[i]=np.nan
                    except IndexError:
                        break
            group=group.fillna(method='ffill')
            for a in range(0,6):
                group['IR_Loss_Chg'+x[a]+'C']=(group['Vt_Chg'+x[a]+'C'].astype(float))-(group['Voltage'].astype(float))
            conc_df(group)
        elif ((group.Step_Type=='CC_DChg').all()):
            group['Vt_DChg'+x1[a]+'C']=''
            df_DChg['SOC_'+x1[a]+'C']=round(df_DChg['SOC_'+x1[a]+'C'],2)
            for a in range(0,6):
                for i in group.index:
                    try:
                        if(group['SOC'].iloc[i]==(df_DChg['SOC_'+x1[a]+'C'].iloc[i]).astype(float)):
                            group['Vt_DChg'+x1[a]+'C'].iloc[i]=df_Chg['V_'+x1[a]+'C'].iloc[i]
                        else:
                            group['Vt_DChg'+x1[a]+'C'].iloc[i]=np.nan
                    except IndexError:
                        break
            group=group.fillna(method='ffill')
            for a in range(0,6):
                group['IR_Loss_DChg'+x1[a]+'C']=(group['Vt_DChg'+x1[a]+'C'].astype(float))-(group['Voltage'].astype(float))
            conc_df(group)
        else:
            for a in range(0,6):
               group['IR_Loss_Chg'+x[a]+'C']=0
               group['IR_Loss_DChg'+x1[a]+'C']=0
            conc_df(group)
    print('.............2/3')
    df.to_excel('IR_Loss.xlsx')

    
