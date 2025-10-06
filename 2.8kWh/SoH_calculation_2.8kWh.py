# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 16:01:59 2022

@author: IITM
"""

import pandas as pd
import numpy as np
import time

start=time.time()

V_file="D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_1\\22_02_18_s\\pack1_cycle2_11\\Driving Data\\-battery_periodic_voltage_graph_data.xlsx_modified.xlsx"
T_file="D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_1\\22_02_18_s\\pack1_cycle2_11\\Driving Data\\-battery_periodic_temperature_graph_data.xlsx_modified.xlsx"

data1=pd.read_excel(V_file)
data2=pd.read_excel(T_file)

#%% clean data
data=pd.concat([data1,data2],axis=1)
data=data.loc[:,~data.columns.duplicated()]
data=data.dropna(how='all',axis=1)

#%% Loading the necessary files
chg_data_25=pd.read_csv("E:\\Davis-6A\\Phylion 14Ah\\25deg\\phy14_25_chg.csv") #25 deg PHY 14 Ah data
dchg_data_25=pd.read_csv("E:\\Davis-6A\\Phylion 14Ah\\25deg\\Phy14_25_dchg.csv")

chg_data_25['T_amb']=25
dchg_data_25['T_amb']=25


chg_data_35=pd.read_csv("E:\\Davis-6A\\Phylion 14Ah\\35deg\\phy14_35_chg.csv") #35 deg PHY 14 Ah data
dchg_data_35=pd.read_csv("E:\\Davis-6A\\Phylion 14Ah\\35deg\\phy14_35_dchg.csv")

chg_data_35['T_amb']=35
dchg_data_35['T_amb']=35


chg_data_45=pd.read_csv("E:\\Davis-6A\\Phylion 14Ah\\45deg\\phy14_45_chg.csv") #45 deg PHY 14 Ah data
dchg_data_45=pd.read_csv("E:\\Davis-6A\\Phylion 14Ah\\45deg\\phy14_45_dchg.csv")

chg_data_45['T_amb']=45
dchg_data_45['T_amb']=45

#%%

chg_data=pd.concat([chg_data_25,chg_data_35,chg_data_45])
dchg_data=pd.concat([dchg_data_25,dchg_data_35,dchg_data_45])

chg_data=chg_data.reset_index(drop=True)
dchg_data=dchg_data.reset_index(drop=True)

#%% Getting minimum voltage and temperature

data['V_min']=data.loc[:,'C0':'C13'].min(axis=1)
try:
    data['T_min']=data.loc[:,'t0':'t3'].min(axis=1)
except KeyError:
    data['T_min']=data.loc[:,'T0':'T3'].min(axis=1)
data['SoC_assumed']=''
data['Temp_flag']=pd.cut(data['T_min'],bins=[0,35,45,100],include_lowest=True,labels=[25,35,45])

#%%

# for i in range(0, len(data)):
    # if ref data is separate for chg and dchg, then how do we do it?
if (V_file.rsplit('\\',2)[1]=='Charging Data'):
    for i in range(0,len(chg_data)):
        
        data['SoC_assumed']=np.where((np.isclose(data['V_min'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==25) & (data['Temp_flag']==25)),chg_data['chg_soc'][i],data['SoC_assumed'])
        data['SoC_assumed']=np.where((np.isclose(data['V_min'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==35) & (data['Temp_flag']==35)),chg_data['chg_soc'][i],data['SoC_assumed'])
        data['SoC_assumed']=np.where((np.isclose(data['V_min'],chg_data['chg_Voltage'][i],rtol=0.01) & (chg_data['T_amb'][i]==45) & (data['Temp_flag']==45)),chg_data['chg_soc'][i],data['SoC_assumed'])
        
elif (V_file.rsplit('\\',2)[1]=='Driving Data'):
    for i in range(0,len(dchg_data)):
        data['SoC_assumed']=np.where((np.isclose(data['V_min'],dchg_data['dis_Voltage'][i],rtol=0.01) & (dchg_data['T_amb'][i]==25) & (data['Temp_flag']==25)),dchg_data['dis_soc'][i],data['SoC_assumed'])
        data['SoC_assumed']=np.where((np.isclose(data['V_min'],dchg_data['dis_Voltage'][i],rtol=0.01) & (dchg_data['T_amb'][i]==35) & (data['Temp_flag']==35)),dchg_data['dis_soc'][i],data['SoC_assumed'])
        data['SoC_assumed']=np.where((np.isclose(data['V_min'],dchg_data['dis_Voltage'][i],rtol=0.01) & (dchg_data['T_amb'][i]==45) & (data['Temp_flag']==45)),dchg_data['dis_soc'][i],data['SoC_assumed'])

#%%
data=data.drop('Temp_flag',axis=1)    
        
print('------------%s seconds------------' % (time.time()-start))