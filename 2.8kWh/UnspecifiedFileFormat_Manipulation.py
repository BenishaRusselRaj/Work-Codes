# -*- coding: utf-8 -*-
"""
Created on Sat May 21 15:15:50 2022

@author: IITM
"""

import pandas as pd
import matplotlib.pyplot as plt


#%%

# No DateTime And with SoC
# cols=['PV','Pack Voltage','Hall_Current','Pack Current','PE','Pack Energy','CV','C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','CT','T0','T1','T2','T3','T4','T5','SOC_x','SoC','SOH_x','SoH']
# HALL_current

# No DateTime And No SoC
# cols=['PV','Pack Voltage','Hall_Current','Pack Current','PE','Pack Energy','CV','C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13']
    
# With Datetime form:[2022-05-11	12:53:40.223]; No SoC
cols=['Date','Time','PV','Pack Voltage','Hall_Current','Pack Current','PE','Pack Energy','CV','C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13']
# HALL_current

    
# With datetime And With temperature; form:[2022-03-28	15:26:02.000]
# cols=['Date','Time','PV','Pack Voltage','Hall_Current','Pack Current','PE','Pack Energy','CV','C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','CT','T0','T1','T2','T3','T4','T5','SOC_x','SoC','SOH_x','SoH']
# # HALL_current

f1="D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_1\\IDC_Test_March_3\\pack 1_1C_IDC\\IDC_3_3_23_Pack 1_Pulse_Chg_cyc 1.xlsx"
df=pd.read_excel(f1,names=cols)

name=f1.split('\\',5)[4]+'_'+f1.rsplit('\\',1)[1].rsplit('.',1)[0]


pack_no=f1.split('\\',4)[3]
#%%
if ((pack_no=='Pack_1') | (pack_no=='Pack_3')):
    dod=0.85
    
elif ((pack_no=='Pack_2') | (pack_no=='Pack_4') | (pack_no=='Pack_5') | (pack_no=='Pack_7') | (pack_no=='Pack_8')| (pack_no=='Pack_9')):
    dod=0.9

elif (pack_no=='Pack_6'):
    dod=0.8

# dod=1
#%%
Q_init=56

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


df_CV=df[df.CV=='CV']
df_I=df[df.Hall_Current=='HALL_current:']

# only if applicable; Temperature comes with this

#%%
df_CV=df_CV.rename(columns={'Hall_Current':'PC'})
df_CV=df_CV.drop(columns=['PV','PC','PE','CV']) #,'SOC_x','SOH_x'

df_CV.loc[:,'C0':'C13']=df_CV.loc[:,'C0':'C13'].apply(pd.to_numeric,errors='coerce')
df_CV['delV']=df_CV.loc[:,'C0':'C13'].max(axis=1)-df_CV.loc[:,'C0':'C13'].min(axis=1)

#%%

df_I=df_I.rename(columns={'PV':'X','Pack Voltage':'Shunt_Current','Hall_Current':'Y','Pack Current':'Hall_Current'})
df_I=df_I.drop(columns=['X','Y'],axis=1)

# df_I=df_I.drop(df_I.iloc[:,2:],axis=1) # No datetime
df_I=df_I.drop(df_I.iloc[:,7:],axis=1) # With datetime


#%%
plt.figure()
plt.plot(range(0,len(df_CV)),df_CV.loc[:,'C0':'C13'],'o-',markersize=2)
plt.ylabel('Voltage(mV)',size=11)
plt.title(name+'_Cell Voltage',size=13)
plt.legend(['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13'],prop={'size':8})
plt.grid(linestyle='dotted')


#%%
plt.figure()
plt.plot(range(0,len(df_CV)),df_CV['delV'],'o-',markersize=2)
plt.ylabel('Voltage(mV)',size=11)
plt.title(name+'_delV',size=13)
plt.grid(linestyle='dotted')

#%%
# plt.figure()
# plt.plot(range(0,len(df_CV)),df_CV.SoC,'o-',markersize=2)
# plt.ylabel('SoC(%)',size=11)
# plt.title(name+'_SOC',size=13)
# plt.grid(linestyle='dotted')

#%%
df_I['Hall_Current']=df_I['Hall_Current'].sort_values(ascending=True)
plt.figure()
plt.plot(range(0,len(df_I)),df_I.Hall_Current,'o-',markersize=2)
# plt.plot(range(0,len(df_I)),df_I.Current,'o-',markersize=2)
plt.ylabel('Current(A)',size=11)
plt.title(name+'_Current',size=13)
plt.grid(linestyle='dotted')
plt.show()

#%%
# plt.figure()
# plt.plot(range(0,len(df_soc)),df_soc.SOC,'o-',markersize=2)
# plt.ylabel('SoC(%)',size=14)
# plt.title(name+'_SOC',size=18)
# plt.grid(linestyle='dotted')

#%% Only if applicable

df_soc=df[df.C7=='SOC'] 
df_soc=df_soc.rename(columns={'PV':'X','Pack Voltage':'T0','Hall_Current':'T1','Pack Current':'T2','PE':'T3','Pack Energy':'T4','CV':'T5','C0':'T6','C1':'T7','C2':'T8','C3':'T9','C4':'T10','C5':'T11','C6':'T12','C7':'Y','C8':'SOC','C9':'Z','C10':'SOH'})

df_soc=df_soc.drop(columns=['X','Y','Z'],axis=1)
df_soc=df_soc.drop(df_soc.iloc[:,-3:],axis=1)
df_soc.to_excel(f1.rsplit('.',1)[0]+'_Temperature.xlsx') 

plt.figure()
plt.plot(range(0,len(df_soc)),df_soc.loc[:,'T0':'T5'],'o-',markersize=2)
plt.ylabel('Temperature'+u'\N{DEGREE SIGN}'+'C')
plt.legend(['T0','T1','T2','T3','T4','T5'],prop={'size':8})
plt.title(name+'_Cell Temperature')
plt.grid(linestyle='dotted')

#%%   Only if applicable

# plt.figure()
# plt.plot(range(0,len(df_CV)),df_CV.loc[:,'T0':'T5'],'o-',markersize=2)
# plt.ylabel('Temperature ('+u'\N{DEGREE SIGN}'+'C)', size=11)
# plt.legend(['T0','T1','T2','T3','T4','T5'],prop={'size':8})
# plt.title(name+'_Cell Temperature',size=13)
# plt.grid(linestyle='dotted')

#%%
df_CV.to_excel(f1.rsplit('.',1)[0]+'_CV.xlsx')
df_I.to_excel(f1.rsplit('.',1)[0]+'_Current.xlsx')
    

#%%

df_CV['Max_Cell']=df_CV.loc[:,'C0':'C13'].idxmax(axis=1) 
df_CV['Min_Cell']=df_CV.loc[:,'C0':'C13'].idxmin(axis=1)

df_CV['V_max']=df_CV.loc[:,'C0':'C13'].max(axis=1) 
df_CV['V_min']=df_CV.loc[:,'C0':'C13'].min(axis=1)


#%%
f=open(f1.rsplit('.',1)[0]+'_observations.txt','w')

print('Start Minimum Cell: %s ; Voltage: %s' %(df_CV['Min_Cell'].iloc[0],df_CV['V_min'].iloc[0]),file=f)
print('Start Maximum Cell: %s ;  Voltage: %s' %(df_CV['Max_Cell'].iloc[0],df_CV['V_max'].iloc[0]),file=f)
print('Avg Minimum Cell: %s' % (df_CV['Min_Cell'].mode()[0]), file=f)
print('End Minimum Cell: %s ; Voltage: %s' %(df_CV['Min_Cell'].iloc[-1],df_CV['V_min'].iloc[-1]),file=f)
print('Avg Maximum Cell: %s' %(df_CV['Max_Cell'].mode()[0]), file=f)
print('End Maximum Cell: %s ;  Voltage: %s' %(df_CV['Max_Cell'].iloc[-1],df_CV['V_max'].iloc[-1]),file=f)
print('End DelV: %s mV' %(df_CV['delV'].iloc[-1]), file=f)
print('Max DelV: %s mV' %(df_CV['delV'].max()),file=f)
print('Max Current: %s' %(df_I['Hall_Current'].max()), file=f)
print('Min Current: %s' %(df_I['Hall_Current'].min()), file=f)
print('Tapering End Current: %s' %(df_I[df_I['Hall_Current']>4]['Hall_Current'].min()), file=f)
print('================================================',file=f)
print('Observations:',file=f)

f.close()