# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 09:47:23 2019

@author: IITM
"""
import time
start = time.time()
import pickle
import pandas as pd
import numpy as np
with open("D:\\New folder (2)\\Text file manipulation Codes\\PHY_13Ah_AllCycles_AllCycles_raw.pkl",'rb') as f:
    data= pickle.load(f)
    df=pd.DataFrame(); dff1=pd.DataFrame(); dff2=pd.DataFrame()
    data[['Cycle_No','Current','Q_in_out']]=data[['Cycle_No','Current','Q_in_out']].astype(float)
    x=['0.5','1','1.5','2','3','0.3'];x1=['0.5','1','1.5','2','3','0.1'] 
    df_Chg= pd.read_excel("D:\\New folder (2)\\Phy13 new cell diff rates.xlsx", sheet_name='Charging')
    df_DChg= pd.read_excel("D:\\New folder (2)\\Phy13 new cell diff rates.xlsx", sheet_name='Discharge')
    data=data[data.Cycle_No==2]
    grouped=data.groupby(['Step_No'])
    print('.............1/3')
    def conc_df(df2):
        global df
        df=df.append(df2)
    for name,group in grouped:
        group['SOC']=(group['Q_in_out']/(group['Q_in_out'].iloc[-1]))*100; j=len(group)
        df['SOC']=group['SOC']
        if ((group.Step_Type=='CCCV_Chg').all()):
            for a in range(0,6):
                df_Chg['SOC_Inter_Vtg_Chg_'+x[a]+'C']=np.interp(df_Chg['SOC_'+x[a]+'C'],group['SOC'],group['Voltage'])
                group['SOC_Inter_Vtg_Chg_'+x[a]+'C']=df_Chg['SOC_Inter_Vtg_Chg_'+x[a]+'C'].truncate(before=None,after=j).fillna(0)
                group['V_'+x[a]+'C']=df_Chg['V_'+x[a]+'C'].truncate(before=None,after=j).fillna(0)
                group['IR_Loss_Chg_'+x[a]+'C']= (group['V_'+x[a]+'C'].astype(float))-(group['SOC_Inter_Vtg_Chg_'+x[a]+'C']).astype(float)
                group['R_Chg_'+x[a]+'C']=group['IR_Loss_Chg_'+x[a]+'C']/(group['Current'])
                group['Cum_R_Chg_step'+x[a]+'C']=group['R_Chg_'+x[a]+'C'].sum() 
                group['Heating_Loss_Chg'+x[a]+'C']=(group['Current']*group['Current']*group['R_Chg_'+x[a]+'C'])*0.000000001
                group['cum_IRLoss_Chg_step'+x[a]+'C']=(group['IR_Loss_Chg_'+x[a]+'C'].sum())*0.000001
                group['Heating_Loss_Chg_step'+x[a]+'C']=group['Heating_Loss_Chg'+x[a]+'C'].sum()
            conc_df(group);i=0
            continue
        elif ((group.Step_Type=='CC_DChg').all()):
            for a in range(0,6):
                df_DChg['SOC_Inter_Vtg_DChg_'+x1[a]+'C']=np.interp(df_DChg['SOC_'+x1[a]+'C'],group['SOC'],group['Voltage'])
                group['SOC_Inter_Vtg_DChg_'+x1[a]+'C']=df_DChg['SOC_Inter_Vtg_DChg_'+x1[a]+'C'].truncate(before=None, after=j).fillna(0)
                group['V_'+x1[a]+'C']=df_DChg['V_'+x1[a]+'C'].truncate(before=None, after=j).fillna(0)
                group['IR_Loss_DChg_'+x1[a]+'C']= ((df_DChg['V_'+x1[a]+'C']).astype(float)-(group['SOC_Inter_Vtg_DChg_'+x1[a]+'C']).astype(float))
                group['R_DChg_'+x1[a]+'C']=group['IR_Loss_DChg_'+x1[a]+'C']/(group['Current'])*(-1)
                group['Heating_Loss_DChg'+x1[a]+'C']=(group['Current']*group['Current']*group['R_DChg_'+x1[a]+'C'])*0.000000001
                group['Cum_R_DChg_step'+x1[a]+'C']=group['R_DChg_'+x1[a]+'C'].sum() 
                group['cum_IRLoss_DChg_step'+x1[a]+'C']=(group['IR_Loss_DChg_'+x1[a]+'C'].sum())*0.000001  
                group['Heating_Loss_DChg_step'+x1[a]+'C']=(group['Heating_Loss_DChg'+x1[a]+'C']).sum()
            i=0
            conc_df(group)
            continue
        else:
            conc_df(group)
            continue
    print('.............2/3')
    df=df.reset_index()
    df=df.fillna(0)
    df=df.drop(['level_0','Chg_Mid_Vtg','DCIR(mO)','DCIR(mO).1','DChg_IR(mO)','DChg_Mid_Vtg','End Temperature','End_Temp','Energy(mWh)','Energy_Chg','Energy_DChg','Energy_Net_DChg','IR','Net_Engy_DChg(mWh)','OCV','OriStepID','Q_Chg','Q_Net_DChg','Q_Net_DChg(mAh)','Q_in_Step','Q_in_Step(mAh/g)','ShowAuxTemp','ShowAuxVolt','Temperature','Time_Elapsed','Time_Spent_in_Step','a1','a2','a3','a4','a5','a6','a7','y'],axis=1)
    
print("--- %s seconds ---" % (time.time() - start))