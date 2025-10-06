# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 14:27:57 2021

@author: IITM
"""
"""
DESCRIPTION:
[STEP TWO]
This code calculates the SoH, SoC, mean SoC
The input to this code is the "_Timestates_added.csv" 


"""

import pandas as pd
import os
import numpy as np
import time
start=time.time()

#%%
#files=glob.glob()

'''''''''''''CHECK Q_NOM, FOLDER NAME, CELL NUMBER AND CYCLE NUMBERS'''''''''''''

# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\25deg\\modified_arranged\\Processed files\\AllCycles\\LCH_60Ah_Timestates_files\\LCH60Ah_1.2_CYC_25deg_600cycles_modified_arranged_25Deg_AllCycles_AllCycles_raw(1)_Timestates_added.csv"
f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\Raw files\\Timestates_files\\LCH_14.1_35Deg_AllCycles_AllCycles_raw(1)_Timestates_added.csv"

fin_path=f.rsplit('\\',2)[0]+'\\SoH_Calculated_files'
summary_path=f.rsplit('\\',2)[0]+'\\SoH_Calculated_summary_files'

#%%
# df_excel=pd.read_excel("D:\\Benisha\\SoH_NN\\Data\\PHY13_CYC+RPT_Degradation_3.x_4.x_25 Deg SoH Only.xlsx",sheet_name='3.1 report') # for cell 3.1
# df_excel=pd.read_excel("D:\\Benisha\\SoH_NN\\Data\\PHY13_CYC+RPT_Degradation_3.x_4.x_25 Deg SoH Only.xlsx",sheet_name='4.1 report') # for cell 4.1
# df_excel=pd.read_excel("D:\\Benisha\\SoH_NN\\Data\\PHY13_CYC+RPT_Degradation_3.x_4.x_25 Deg SoH Only.xlsx",sheet_name='6.1 report') # for cell 6.1
# df_excel=pd.read_excel("D:\\Benisha\\SoH_NN\\Data\\PHY13_CYC+RPT_Degradation_21.x_22.x_45 Deg SoH only.xlsx",sheet_name='21.1') # for cell 21.1
# df_excel=pd.read_excel("D:\\Benisha\\SoH_NN\\Data\\PHY13_CYC+RPT_Degradation_21.x_22.x_45 Deg SoH only.xlsx",sheet_name='22.1') # for cell 22.1

# Cycles=df_excel[(df_excel.filter(regex='Cycle|cycle').columns)].values


#%%
if not os.path.exists(fin_path):
    os.makedirs(fin_path)
    
if not os.path.exists(summary_path):
    os.makedirs(summary_path)

#%%    
df=pd.read_csv(f)

# df=df.loc[df['Cycle_No'].isin(Cycles)]

#%%
# df=df.drop(columns=['Unnamed: 0', 'Record_ID', 'Chg_Mid_Vtg', 'Power','DChg_Mid_Vtg', 'a1', 'a2', 'a3', 'a4', 'a5', 'DCIR', 'y', 'OCV', 'IR','Sample_Name','Unnamed: 25', 'Unnamed: 26', 'Unnamed: 27', 'Unnamed: 28','Unnamed: 29','OCV', 'IR', 'Sample_Name'])
# df=df.drop(columns=['dQm/dV(mAh/V.g)','Q_Net_DChg(mAh)','Auxiliary_Channel_TU4 U(V)','Net Engy_DChg(mWh)','Auxiliary_Channel_TU4 T','Charge IR(O)','U4 Start(V)','Discharge IR(O)','U4 End(V)','End Temp','T4 StartTemp','Net Cap_DChg(mAh)','T1 EndTemp','Net Engy_DChg(mWh).1','Energy Efficiency','Unnamed: 56','Unnamed: 57','Unnamed: 58','Unnamed: 59','Unnamed: 60','Unnamed: 61','Unnamed: 62','Unnamed: 63','Unnamed: 64','Unnamed: 65']) #, 'a1', 'a2', 'a3', 'a4', 'a5', 'y','Unnamed: 25', 'Unnamed: 26', 'Unnamed: 27', 'Unnamed: 28','Unnamed: 29'

#%%
df['Time_Spent_in_Step_s']=np.nan
df['SoC_calculated']=np.nan
df['SoH_calculated']=np.nan
df['del_SoC']=np.nan
df['mean_SoC']=np.nan

data=pd.DataFrame()

Q_series=abs(df.loc[(df['New_Cycle_No']<=10) & (df['Step_Type']=='CC_DChg'), 'Q_in_Step'])
Q_nom=(Q_series[Q_series>10]).mean()

#%% PHY
# Q_nom=9383.346780607813  #3.1  
# Q_nom=11910.996358466135 #4.1
# Q_nom=13147.482321172354 #6.1
# Q_nom=10969.376691350284 #21.1 
# Q_nom=13291.924055981852 #22.1
# Q_nom=13418.856385424739 #22.2

#%% LCH
# Q_nom=46.1653253721706 #14.1
# Q_nom=40.3018685991037 #15.1
# Q_nom=45.92507636327079 #16.1
# Q_nom=37.352613950446994 #17.1
# Q_nom=35.856739031883095 #18.1
# Q_nom=37.75658407533482 #19.1

#%% LCH 60Ah
# Q_nom=56397.95923633333  # 25 deg
# Q_nom=61195.11375888258 #45 deg

#%% BRD
# Q_nom=1722.9767140404583 #3.1
# Q_nom=1698.7440406343974 #3.2
# Q_nom=1892.3954306969702 #4.2
# Q_nom=2351.521852332948 #5.1
# Q_nom=2130.7601704790222 #6.1
# Q_nom=2173.825348665568 #7.1
# Q_nom=1874.3670407143904 #8.1
# Q_nom=2059.766694238588 #10.1
# Q_nom=2078.8644667652857 #10.2

print('1/3..........')
#%%
df['RTC']=pd.to_datetime(df['RTC'],errors='coerce',format='%Y-%m-%d %H:%M:%S')
grouped=df.groupby(['New_Cycle_No','Step_No'],sort=False)
result=[f[1] for f in grouped]

#%%
cols=['Cell_No','Cycle_No','Step_Type','Start_time','End_Time','Time_in_Step_Datetime','Vol_s0_CCCV_Chg', 'Vol_s1_CCCV_Chg', 'Vol_s2_CCCV_Chg','Vol_s3_CCCV_Chg', 'Vol_s4_CCCV_Chg', 'Vol_s5_CCCV_Chg',
      'Vol_s6_CCCV_Chg', 'Vol_s7_CCCV_Chg', 'Vol_s8_CCCV_Chg','Vol_s0_CC_DChg', 'Vol_s1_CC_DChg', 'Vol_s2_CC_DChg', 'Vol_s3_CC_DChg',
      'Vol_s4_CC_DChg', 'Vol_s5_CC_DChg', 'Vol_s6_CC_DChg', 'Vol_s7_CC_DChg','Vol_s8_CC_DChg',
      'Vol_s0_Rest', 'Vol_s1_Rest', 'Vol_s2_Rest','Vol_s3_Rest', 'Vol_s4_Rest', 'Vol_s5_Rest', 'Vol_s6_Rest','Vol_s7_Rest', 'Vol_s8_Rest',
      'Temp_s0_CCCV_Chg', 'Temp_s1_CCCV_Chg', 'Temp_s2_CCCV_Chg','Temp_s3_CCCV_Chg', 'Temp_s4_CCCV_Chg', 'Temp_s5_CCCV_Chg','Temp_s6_CCCV_Chg',
      'Temp_s0_CC_DChg', 'Temp_s1_CC_DChg', 'Temp_s2_CC_DChg','Temp_s3_CC_DChg', 'Temp_s4_CC_DChg', 'Temp_s5_CC_DChg','Temp_s6_CC_DChg',
      'Temp_s0_Rest', 'Temp_s1_Rest', 'Temp_s2_Rest','Temp_s3_Rest', 'Temp_s4_Rest', 'Temp_s5_Rest','Temp_s6_Rest',
      'T_amb','DoD','SoC_calculated','SoH_calculated','mean_SoC']#,'Step_Type' ,'SoC_calculated'
dff=pd.DataFrame(index=range(0,len(result)),columns=cols,dtype=float) # 

#%%
k=0
print('2/3..........')
#%%
for i in range(0, len(result)):
    
    result[i]['Time_Spent_in_Step_s']=(result[i]['RTC'].shift(-1)-result[i]['RTC'])/np.timedelta64(1,'s')
    result[i]['Time_Spent_in_Step_s']=np.where(result[i]['Time_Spent_in_Step_s']>1000,1,result[i]['Time_Spent_in_Step_s'])
    ## result[i]['SoC_calculated']=((((result[i]['Current'].abs())*result[i]['Time_Spent_in_Step_s']/3600).cumsum())/Q_nom)*100
    result[i]['SoC_calculated']=(((result[i]['Current']*result[i]['Time_Spent_in_Step_s']/3600).cumsum())/Q_nom)*100
    
    result[i]['del_SoC']=result[i]['SoC_calculated'].max()-result[i]['SoC_calculated'].min()
    result[i]['mean_SoC']=np.where(result[i]['Step_Type']=='CCCV_Chg',result[i]['SoC_calculated'].mean(),result[i]['mean_SoC'])
    
    result[i]['SoH_calculated']=np.where(result[i]['Step_Type']=='CC_DChg',(abs(result[i]['Q_in_Step'])/Q_nom)*100,result[i]['SoH_calculated']) 	 
    result[i]['SoC_calculated']=np.where(((result[i]['SoC_calculated']>0)&(result[i]['SoC_calculated']<3)),np.nan,result[i]['SoC_calculated'])
  
    dff.iloc[k]['Cycle_No']=result[i].iloc[-1]['New_Cycle_No']
    dff.iloc[k]['Step_Type']=result[i].iloc[-1]['Step_Type']
    dff.iloc[k]['SoH_calculated']=result[i]['SoH_calculated'].max()
    dff.iloc[k]['Start_time']=result[i].iloc[0]['RTC']
    dff.iloc[k]['End_Time']=result[i].iloc[-1]['RTC']
    dff.iloc[k]['Time_in_Step_Datetime']=result[i].iloc[-1]['RTC']-result[i].iloc[0]['RTC']

    dff.loc[k,'Vol_s0_CCCV_Chg':'Temp_s6_Rest']=result[i].iloc[-1]['Vol_s0_CCCV_Chg':'Temp_s6_Rest']
    dff.iloc[k]['mean_SoC']=result[i].iloc[-1]['mean_SoC']
    dff.iloc[k]['SoC_calculated']=np.where(result[i]['Step_Type'].all()=='CC_DChg',result[i]['SoC_calculated'].min(),result[i]['SoC_calculated'].max())
    dff.iloc[k]['T_amb']=result[i].iloc[-1]['T_amb']
    
    k=k+1
    data=pd.concat([data,result[i]])
print('3/3..........')
#%%
data=data.drop(data.filter(like='Unnamed',axis=1).columns,axis=1)
#%%
data=data.sort_values(by=['RTC'],ascending=True)

# dff['Cycle_No']=dff['Cycle_No']+445
#%%
file_name=f.rsplit('.',1)[0].rsplit('\\',1)[1]
dff=dff.sort_values(by=['Cycle_No'],ascending=True)
dff=dff.dropna(how='all')

print('Processing..........')
#%%
# dff['SoC_calculated']=np.where(dff['SoC_calculated']<10,np.nan,dff['SoC_calculated'])
dff['SoH_calculated']=dff['SoH_calculated'].fillna(method='bfill')
dff['SoH_calculated']=dff['SoH_calculated'].fillna(method='ffill')

dff['SoC_calculated']=dff['SoC_calculated'].fillna(method='ffill')
dff['mean_SoC']=dff['mean_SoC'].fillna(method='ffill')
dff['mean_SoC']=dff['mean_SoC'].fillna(method='bfill')

dff['SoC_calculated']=np.where(dff['SoC_calculated']<0,dff['SoC_calculated']+100,dff['SoC_calculated'])
dff['SoC_calculated']=np.where(dff['SoC_calculated']<0,0,dff['SoC_calculated'])

#
dff['Cell_No']='LCH_14.1'
dff['DoD']=100

#%%
data.to_csv(fin_path+'\\'+file_name+'_soh_calculated.csv')
dff.to_csv(summary_path+'\\'+file_name+'_soh_summary.csv')

print('------------------%s seconds-------------' %(time.time()-start))


