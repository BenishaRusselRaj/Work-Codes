# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 17:07:24 2019

@author: IITM
"""

import pickle
import pandas as pd
with open("D:\\New folder (2)\\Text file manipulation Codes\\PHY_13Ah_AllCycles_AllCycles_raw.pkl",'rb') as f:
    data= pickle.load(f)
    df=pd.DataFrame()
    x=[0.5,1,1.5,2,3,0.3]
    data['SOC']=''
    data['Q_in_out']=data['Q_in_out'].astype(float)
    df[['Step_No','Step_Type','Voltage','Current','Q_in_out']]=data[['Step_No','Step_Type','Voltage','Current','Q_in_out']]  
    df['SOC']=''; df['SOC_Inter_Vtg']=''; IR_Loss=[];df['cum_IRLoss']='';df['IR_Loss']=''
    df_Chg= pd.read_excel("D:\\New folder (2)\\Phy13 new cell diff rates.xlsx", sheet_name='Charging')
    df_DChg= pd.read_excel("D:\\New folder (2)\\Phy13 new cell diff rates.xlsx", sheet_name='Discharge')
    grouped=data.groupby(['Step_No'])
    