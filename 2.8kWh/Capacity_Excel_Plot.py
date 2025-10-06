# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 13:07:19 2023

@author: IITM
"""

import pandas as pd
import matplotlib.pyplot as plt

#%%
f="D:\\Benisha\\2.8kWh_Charging Algorithm\\Capacity Test Excel\\Data\\2.8kWh_Phase_1_2_3_with_SoH_20 April.xlsx" # Add file path here
data=pd.read_excel(f,header=1)
#%% To remove empty rows
data=data.dropna(how='all')
data=data.dropna(subset=['Pack_1_SoH(%)'])

#%% c refers to the color codes; m refers to the marker codes; these can be changes as per preference
c=['b','g','r','c','y']
m=['o','x','d','s','^']

#%% Plots all the three phases together-- Soh Vs Cycle No
plt.figure()
for i in range(len(c)):
    plt.plot(data.loc[:1]['Pack_'+str(i+1)+'_Cycle No'],data.loc[:1]['Pack_'+str(i+1)+'_SoH(%)'],c[i]+m[i]+':') #.loc[:1] because phase 1 has only 1 datapointfor all packs
    plt.plot(data.loc[1:2]['Pack_'+str(i+1)+'_Cycle No'],data.loc[1:2]['Pack_'+str(i+1)+'_SoH(%)'],c[i]+m[i]+'-',label='Pack '+str(i+1)) #.loc[1:2] because phase 2 also has only 1 datapoint for all packs
    plt.plot(data.loc[2:]['Pack_'+str(i+1)+'_Cycle No'],data.loc[2:]['Pack_'+str(i+1)+'_SoH(%)'],c[i]+m[i]+'-.')
    plt.grid(linestyle='dotted')
    plt.xlabel('Cycle No.',fontweight='bold',size=11)
    plt.ylabel('SoH(%)',fontweight='bold',size=11)
    plt.legend()
    plt.title('SoH(%) Vs Cycle No',fontweight='bold',size=13)
    plt.show()
plt.savefig(f.rsplit('\\',1)[0]+'\\SoH(%) Vs Cycle No_Phase_1_2_and_3.png',dpi=1200)
#%%Plots all the three phases together-- Soh Vs Time
plt.figure()
for i in range(len(c)):
    plt.plot(data.loc[:1]['Pack_'+str(i+1)+'_Time (in days)'],data.loc[:1]['Pack_'+str(i+1)+'_SoH(%)'],c[i]+m[i]+':')
    plt.plot(data.loc[1:2]['Pack_'+str(i+1)+'_Time (in days)'],data.loc[1:2]['Pack_'+str(i+1)+'_SoH(%)'],c[i]+m[i]+'-',label='Pack '+str(i+1))
    plt.plot(data.loc[2:]['Pack_'+str(i+1)+'_Time (in days)'],data.loc[2:]['Pack_'+str(i+1)+'_SoH(%)'],c[i]+m[i]+'-.')
    plt.grid(linestyle='dotted')
    plt.xlabel('Time(in days)',fontweight='bold',size=11)
    plt.ylabel('SoH(%)',fontweight='bold',size=11)
    plt.legend()
    plt.title('SoH(%) Vs Time',fontweight='bold',size=13)
    plt.show()
plt.savefig(f.rsplit('\\',1)[0]+'\\SoH(%) Vs Time_Phase_1_2_and_3.png',dpi=1200)    
#%% To separate phase 2 and 3, extra columns are created by considering the respective phase startings as 100% SoH
for i in range(len(c)):
    data['Pack_'+str(i+1)+'_Cycle No_Phase_2_3']=data['Pack_'+str(i+1)+'_Cycle No']-data.loc[1]['Pack_'+str(i+1)+'_Cycle No']
    data['Pack_'+str(i+1)+'_SoH(%)_Phase_2_3']=100-(data.loc[1]['Pack_'+str(i+1)+'_SoH(%)']-data['Pack_'+str(i+1)+'_SoH(%)'])
    data['Pack_'+str(i+1)+'_Time (in days)_Phase_2_3']=data['Pack_'+str(i+1)+'_Time (in days)']-data.loc[1]['Pack_'+str(i+1)+'_Time (in days)']
    
    data['Pack_'+str(i+1)+'_Cycle No_Phase_3']=data['Pack_'+str(i+1)+'_Cycle No']-data.loc[2]['Pack_'+str(i+1)+'_Cycle No']
    data['Pack_'+str(i+1)+'_SoH(%)_Phase_3']=100-(data.loc[2]['Pack_'+str(i+1)+'_SoH(%)']-data['Pack_'+str(i+1)+'_SoH(%)'])
    data['Pack_'+str(i+1)+'_Time (in days)_Phase_3']=data['Pack_'+str(i+1)+'_Time (in days)']-data.loc[2]['Pack_'+str(i+1)+'_Time (in days)']
    
    
#%% Plots phases 2 and 3 together-- Soh Vs Cycle No
plt.figure()
for i in range(len(c)):
    plt.plot(data.loc[1:2]['Pack_'+str(i+1)+'_Cycle No_Phase_2_3'],data.loc[1:2]['Pack_'+str(i+1)+'_SoH(%)_Phase_2_3'],c[i]+m[i]+'-',label='Pack '+str(i+1))
    plt.plot(data.loc[2:]['Pack_'+str(i+1)+'_Cycle No_Phase_2_3'],data.loc[2:]['Pack_'+str(i+1)+'_SoH(%)_Phase_2_3'],c[i]+m[i]+'-.')
    plt.grid(linestyle='dotted')
    plt.xlabel('Cycle No.',fontweight='bold',size=11)
    plt.ylabel('SoH(%)',fontweight='bold',size=11)
    plt.legend()
    plt.title('SoH(%) Vs Cycle No',fontweight='bold',size=13)
    plt.show()
plt.savefig(f.rsplit('\\',1)[0]+'\\SoH(%) Vs Cycle No_Phase_2_and_3.png',dpi=1200)
#%% Plots phases 2 and 3 together-- Soh Vs Time
plt.figure()
for i in range(len(c)):
    plt.plot(data.loc[1:2]['Pack_'+str(i+1)+'_Time (in days)_Phase_2_3'],data.loc[1:2]['Pack_'+str(i+1)+'_SoH(%)_Phase_2_3'],c[i]+m[i]+'-',label='Pack '+str(i+1))
    plt.plot(data.loc[2:]['Pack_'+str(i+1)+'_Time (in days)_Phase_2_3'],data.loc[2:]['Pack_'+str(i+1)+'_SoH(%)_Phase_2_3'],c[i]+m[i]+'-.')
    plt.grid(linestyle='dotted')
    plt.xlabel('Time(in days)',fontweight='bold',size=11)
    plt.ylabel('SoH(%)',fontweight='bold',size=11)
    plt.legend()
    plt.title('SoH(%) Vs Time',fontweight='bold',size=13)
    plt.show()
plt.savefig(f.rsplit('\\',1)[0]+'\\SoH(%) Vs Time_Phase_2_and_3.png',dpi=1200)   
    
#%% Plots phase 3 alone-- Soh Vs Cycle No
plt.figure()
for i in range(len(c)):
    plt.plot(data.loc[2:]['Pack_'+str(i+1)+'_Cycle No_Phase_3'],data.loc[2:]['Pack_'+str(i+1)+'_SoH(%)_Phase_3'],c[i]+m[i]+'-.',label='Pack '+str(i+1))
    plt.grid(linestyle='dotted')
    plt.xlabel('Cycle No.',fontweight='bold',size=11)
    plt.ylabel('SoH(%)',fontweight='bold',size=11)
    plt.legend()
    plt.title('SoH(%) Vs Cycle No',fontweight='bold',size=13)
    plt.show()
plt.savefig(f.rsplit('\\',1)[0]+'\\SoH(%) Vs Cycle No_Phase_3.png',dpi=1200)
#%% Plots phase 3 alone-- Soh Vs Time
plt.figure()
for i in range(len(c)):
    plt.plot(data.loc[2:]['Pack_'+str(i+1)+'_Time (in days)_Phase_3'],data.loc[2:]['Pack_'+str(i+1)+'_SoH(%)_Phase_3'],c[i]+m[i]+'-.',label='Pack '+str(i+1))
    plt.grid(linestyle='dotted')
    plt.xlabel('Time(in days)',fontweight='bold',size=11)
    plt.ylabel('SoH(%)',fontweight='bold',size=11)
    plt.legend()
    plt.title('SoH(%) Vs Time',fontweight='bold',size=13)
    plt.show()
plt.savefig(f.rsplit('\\',1)[0]+'\\SoH(%) Vs Time_Phase_3.png',dpi=1200)      
    
    