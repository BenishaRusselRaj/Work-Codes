# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 16:25:49 2024

@author: IITM
"""
#%% Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

#%% File paths are assigned
files=glob.glob("D:\\Benisha\\15kW_LTO_Pack\\24_01_22\\Idle_Data\\*.xlsx")

# Set empty dataframes to save files
status_df=pd.DataFrame()
details_df=pd.DataFrame()
temp_df=pd.DataFrame()
v_df=pd.DataFrame()

# Set column names
cols=['Date','Time','MV_MT_tag','PV_V_T_status_tag','val1','val_t2','val2','val_t3',
      'val_3','junk','val_4','junk','val_5','junk','val_6','junk','val_7','junk','val_8','junk',
      'val_9','junk','val_10','junk','val_11','junk','val_12','junk','val_13','junk','val_14','junk']

#%%
for f in files:
    data=pd.read_excel(f,names=cols,index_col=False)
    file=files[0]
    # data=pd.read_excel(file,names=cols,index_col=False) #,sheet_name='chg and dchg 20-09-2023 (2)'
    img_path=file.rsplit('\\',1)[0]
    
    #%%
    data['Date']=data['Date'].str.replace('[','',regex=True)
    data['Time']=data['Time'].str.replace(']','',regex=True)
    
    data['Time']=data['Time'].astype(str)
    data[['Time_format','string']]=data['Time'].str.split('.',expand=True)
    
    data['DateTime']=data['Date'].astype(str)+' '+data['Time_format']
    data['DateTime']=pd.to_datetime(data['DateTime'],format='%Y-%m-%d %H:%M:%S',errors='coerce')
    
    data=data[['DateTime'] + [col for col in data.columns if col!='DateTime']]
    data=data.drop(['Time_format','string'],axis=1)
    data=data.sort_values(['DateTime'])
    
    #%%
    status_data=data[data['PV_V_T_status_tag']=='STATUS:'].dropna(how='all',axis=1)
    # max_min_data=data[data['PV_V_T_status_tag']=='V:'].reset_index(drop=True)
    # max_min_data=pd.concat([max_min_data,data[data['PV_V_T_status_tag']=='T:'].drop(['DateTime','Date','Time'],axis=1).reset_index(drop=True)],axis=1).dropna(how='all',axis=1) # try to concatenate in same file
    details=data[data['PV_V_T_status_tag']=='voltage:'].dropna(how='all',axis=1)
    
    #%% Column names
    v_names=[f'MV_{x}' for x in range(1,169)] 
    t_names=[f'MT_{x}' for x in range(1,49)]
    status=['DateTime','Date','Time','junk','junk','Pack Status','junk','Shutdown','Normal','junk','junk','Precharge Relay','junk','junk','Main Relay']
    # detail_names=['DateTime','Date','Time','junk','junk','Pack Voltage','junk','junk','Pack Current','junk','SoH','junk','junk','Charging Energy','junk','junk','Discharging Energy','junk','junk','junk','Pack Available Energy','junk']
    # detail_names=['DateTime','Date','Time','junk','junk','Pack Voltage','junk','junk','Pack Current','junk','SoH','junk','junk','Charging Energy','junk','junk','junk','Discharging Energy','junk','junk','junk','junk','Pack Available Energy','junk']
    detail_names=['DateTime','Date','Time','junk','junk','Pack Voltage','junk','junk','Pack Current','junk','SoH','junk','junk','Charging Energy','junk','junk','junk','Discharging Energy','junk']
    # max_min_names=['DateTime','Date','Time','junk','junk','Min_V_BMS','','junk','junk','Max_V_BMS','','junk','junk','Average_CellV_BMS','junk','junk','junk','delV_BMS(mV)','junk','junk','junk','junk','junk','junk','junk','junk','junk'] #,'Min_T_BMS','','junk','junk','Max_T_BMS','']
    
    status=['DateTime','Date','Time','junk','junk','Pack Status','junk','Shutdown','Normal','junk','junk','Precharge Relay','junk','junk','Main Relay']
    status_data.columns=status
    details.columns=detail_names
    # max_min_data.columns=max_min_names
    
    status_data['Main Relay']=status_data['Main Relay'].astype(str).str.extract(r'([A-Z][a-z]{3,})') #[Open][close][open] 
    status_data['Precharge Relay']=status_data['Precharge Relay'].astype(str).str.extract(r'([A-Z][a-z]{3,})')
    status_data['Precharge Relay']=status_data['Precharge Relay'].fillna(method='ffill')
    status_data=status_data.drop([col for col in status_data.columns if "junk" in col], axis=1)
    details=details.drop([col for col in details.columns if "junk" in col], axis=1)
    # max_min_data=max_min_data.drop([col for col in max_min_data.columns if "junk" in col], axis=1)
    
    #%% Clean data entries to remove any junk values
    details['Pack Current']=details['Pack Current'].str.replace('A','',regex=True)
    details['Pack Current']=details['Pack Current'].str.extract(r'(\d{2}.\d{3})')
    
    details['Pack Voltage']=details['Pack Voltage'].astype(int)
    # details['Pack Voltage']=details['Pack Voltage'].str.extract(r'(\d{3})')
    
    status_data['Precharge Relay']=status_data['Precharge Relay'].str.replace(',','',regex=True)
    details['Charging Energy']=details['Charging Energy'].str.replace('engy:','',regex=True)
    details['Discharging Energy']=details['Discharging Energy'].str.replace('engy:','',regex=True)
    details['Charging Energy']=details['Charging Energy'].astype(float)
    details['Discharging Energy']=details['Discharging Energy'].astype(float)
    
    #%%
    voltage_data=data[data['MV_MT_tag']=='MV1'].reset_index(drop=True)
    for i in range(2,13):
        voltage_data=pd.concat([voltage_data,data[data['MV_MT_tag']=='MV'+str(i)].drop(['DateTime','Date','Time'],axis=1).reset_index(drop=True)],axis=1)
    
    voltage_data=voltage_data.drop([col for col in voltage_data.columns if "junk" in col], axis=1)
    voltage_data=voltage_data.drop([col for col in voltage_data.columns if "tag" in col], axis=1)
    voltage_data=voltage_data.drop(['val_t2','val_t3'],axis=1)
    
    #%%
    for i,n in enumerate(['DateTime','Date','Time']):
        v_names.insert(i,n)
        t_names.insert(i,n)
    
    voltage_data.columns=v_names
    
    #%%
    temperature_data=data[data['MV_MT_tag']=='MT1'].loc[:,:'val_t3'].reset_index(drop=True)
    
    #%%
    
    for i in range(2,13):
        temperature_data=pd.concat([temperature_data,data[data['MV_MT_tag']=='MT'+str(i)].loc[:,:'val_t3'].drop(['DateTime','Date','Time'],axis=1).reset_index(drop=True)],axis=1)
        
    
    temperature_data=temperature_data.dropna(how='all',axis=1)
    temperature_data=temperature_data.drop([col for col in temperature_data.columns if "tag" in col], axis=1)
    
    temperature_data.columns=t_names
    
    for i in range(1,49):
        temperature_data['MT_'+str(i)]=temperature_data['MT_'+str(i)].astype(str).str.extract(r'(\d{2}.\d{5})')
        
    
    #%%
    voltage_data.loc[:,'MV_1':'MV_168']=voltage_data.loc[:,'MV_1':'MV_168'].replace('_0',np.nan)
    voltage_data.loc[:,'MV_1':'MV_168']=voltage_data.loc[:,'MV_1':'MV_168'].fillna(method='ffill')
    
    for i in range(1,169):
        voltage_data['MV_'+str(i)]=voltage_data['MV_'+str(i)].astype(str).str.extract(r'(\d{5})')
    
    voltage_data.loc[:,'MV_1':'MV_168']=voltage_data.loc[:,'MV_1':'MV_168'].fillna(method='ffill')
    voltage_data.loc[:,'MV_1':'MV_168']=voltage_data.loc[:,'MV_1':'MV_168'].astype(int)
    voltage_data['Mean_V']=voltage_data.loc[:,'MV_1':'MV_168'].mean(axis=1)
    
    #%%
    temperature_data.loc[:,'MT_1':'MT_48']=temperature_data.loc[:,'MT_1':'MT_48'].astype(float)
    temperature_data.loc[:,'MT_1':'MT_48']=temperature_data.loc[:,'MT_1':'MT_48'].fillna(method='ffill')
    temperature_data['Mean_T']=temperature_data.loc[:,'MT_1':'MT_48'].mean(axis=1)
    
    temperature_data['delT']=temperature_data.loc[:,'MT_1':'MT_48'].max(axis=1)-temperature_data.loc[:,'MT_1':'MT_48'].min(axis=1)
    
    #%% Calculating Capacity_calculated and energy
    
    details['Time_in_sec_s']=(details['DateTime']-details['DateTime'].shift(1))/np.timedelta64(1,'s')# time difference b/w every datapt
    details['Time_in_sec']=(details['DateTime']-details['DateTime'].iloc[0])/np.timedelta64(1,'s')
    
    
    details['Pack Current']=details['Pack Current'].astype(float)
    
    #%%
    details['State']=np.nan
    details['Time_in_sec_s_cap']=np.where((details['Time_in_sec_s']>300),np.nan,details['Time_in_sec_s'])
    details['State']=np.where(details['Pack Current']>0,0,details['State']) # 1
    details['State']=np.where(details['Pack Current']<0,1,details['State']) # 2
    # details['State']=details['State'].astype(str)
    
    
    # details['State']=details['State'].fillna(method='ffill')
    # details['State']=details['State'].fillna(method='bfill')
    
    #%%
    details['Cap_inst']=details['Time_in_sec_s_cap']*abs(details['Pack Current'])/3600
    details['Capacity_calculated']=details['Cap_inst'].groupby(details['State']).cumsum()
    details['Capacity_calculated_chg']=(details[details['State']==0]['Cap_inst']).cumsum()
    details['Capacity_calculated_dchg']=(details[details['State']==1]['Cap_inst']).cumsum()
    
    details['Capacity_calculated_chg']=details['Capacity_calculated_chg'].fillna(method='bfill')
    details['Capacity_calculated_dchg']=details['Capacity_calculated_dchg'].fillna(method='bfill')
    
    details['Energy_calculated']=details['Capacity_calculated']*details['Pack Voltage']
    details['Energy_calculated_chg']=details['Capacity_calculated_chg']*details['Pack Voltage']
    details['Energy_calculated_dchg']=details['Capacity_calculated_dchg']*details['Pack Voltage']
    
    #%%
    voltage_data['delV']=voltage_data.loc[:,'MV_1':'MV_168'].max(axis=1)-voltage_data.loc[:,'MV_1':'MV_168'].min(axis=1)
    status_data['Main Relay']=status_data['Main Relay'].fillna(method='ffill')
    status_data['Main Relay']=status_data['Main Relay'].astype(str)
    
    status_df=pd.concat([status_df,status_data])
    details_df=pd.concat([details_df,details])
    temp_df=pd.concat([temp_df,temperature_data])
    v_df=pd.concat([v_df,voltage_data])

l=6.98
b=3.98
x_axis='DateTime'

#%%
# status_data['Precharge Relay']=status_data['Precharge Relay'].replace('Open','OFF')
# document.add_page_break()
# document.add_paragraph().add_run('Precharge Relay:').bold=True

# # plt.plot()
# plt.figure(figsize=(l,b))
# # plt.rcParams["figure.figsize"] = [7.00, 4.25]
# # plt.rcParams["figure.autolayout"] = True

# plt.plot(status_data[x_axis],status_data['Precharge Relay'])
# # ax.plot(status_data['Time'],status_data['Precharge Relay'])

# # xmin, xmax = ax.get_xlim()
# # ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))
# plt.xlabel(x_axis,fontweight='bold')
# plt.grid(linestyle='dotted')
# plt.title('Precharge Relay',fontweight='bold')
# plt.tight_layout()
# # plt.savefig(img_path+'\\Precharge Relay.png',dpi=1200)

# # document.add_picture(img_path+'\\Precharge Relay.png')
# document.add_paragraph().add_run('As is known already, “open” means the precharge relay is off and “Close” means it is on.')

#%%
# document.add_paragraph().add_run('Main Relay:').bold=True

# plt.figure(figsize=(l,b))
# plt.plot(status_data[x_axis],status_data['Main Relay'])
# # ax.plot(status_data['Time'],status_data['Main Relay'])

# # xmin, xmax = ax.get_xlim()
# # ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))
# plt.xlabel(x_axis,fontweight='bold')
# plt.grid(linestyle='dotted')
# plt.title('Main Relay',fontweight='bold')
# plt.tight_layout()
# # plt.savefig(img_path+'\\Main Relay.png',dpi=1200)

# # document.add_picture(img_path+'\\Main Relay.png')
# document.add_paragraph('As is known already, “Close” means the main relay is on. ')

#%%

# plt.savefig(img_path+'\\Pack Status.png',dpi=1200)

# document.add_picture(img_path+'\\Pack Status.png')

#%%
plt.figure(figsize=(l,b))
plt.plot(details_df[x_axis],details_df['Pack Current'])
# ax.plot(details['Time'],details['Pack Current'])

# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))

plt.xlabel(x_axis,fontweight='bold')
plt.ylabel('Current(A)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Current',fontweight='bold')
plt.tight_layout()
# plt.savefig(img_path+'\\Pack Current.png',dpi=1200)

# document.add_picture(img_path+'\\Pack Current.png')

#%%

plt.figure(figsize=(l,b))
plt.plot(details_df[x_axis],details_df['Capacity_calculated_dchg'])
# ax.plot(details['Time'],details['Capacity_calculated_dchg'])

# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))

plt.xlabel(x_axis,fontweight='bold')
plt.ylabel('Capacity(Ah)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Discharging Capacity (Calculated)',fontweight='bold')
plt.tight_layout()
# plt.savefig(img_path+'\\Pack Discharging Capacity_calculated.png',dpi=1200)

# document.add_picture(img_path+'\\Pack Discharging Capacity_calculated.png')

#%%


plt.figure(figsize=(l,b))
plt.plot(details[x_axis],details['Capacity_calculated_chg'])
# ax.plot(details['Time'],details['Capacity_calculated_chg'])


# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))

plt.xlabel(x_axis,fontweight='bold')
plt.ylabel('Capacity(Ah)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Charging Capacity (Calculated)',fontweight='bold')
plt.tight_layout()

# plt.savefig(img_path+'\\Pack Charging Capacity_calculated.png',dpi=1200)

#%%
plt.figure(figsize=(l,b))
plt.plot(details[x_axis],details['Energy_calculated_dchg']*0.001)
# ax.plot(details['Time'],details['Energy_calculated_dchg']*0.001)

# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))

plt.xlabel(x_axis,fontweight='bold')
plt.ylabel('Energy(kWh)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Discharging Energy (Calculated)',fontweight='bold')
plt.tight_layout()
# plt.savefig(img_path+'\\Pack Discharging Energy_calculated.png',dpi=1200)

# document.add_picture(img_path+'\\Pack Discharging Energy_calculated.png')

#%%
plt.figure(figsize=(l,b))
plt.plot(details[x_axis],details['Energy_calculated_chg']*0.001)
# ax.plot(details['Time'],details['Energy_calculated_chg']*0.001)

# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))

plt.xlabel(x_axis,fontweight='bold')
plt.ylabel('Energy(kWh)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Charging Energy (Calculated)',fontweight='bold')
plt.tight_layout()
# plt.savefig(img_path+'\\Pack Charging Energy_calculated.png',dpi=1200)

# document.add_picture(img_path+'\\Pack Charging Energy_calculated.png')

#%%

plt.figure(figsize=(l,b))
plt.plot(details[x_axis],details['Discharging Energy'])
# ax.plot(details['Time'],details['Discharging Energy'])

# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))
# ymin, ymax = ax.get_ylim()
# ax.set_yticks(np.round(np.linspace(ymin, ymax, 20), 2))

plt.xlabel(x_axis,fontweight='bold')
plt.ylabel('Energy(Wh)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Discharging Energy (BMS)',fontweight='bold')
plt.tight_layout()
# plt.savefig(img_path+'\\Pack Discharging Energy_BMS.png',dpi=1200)

# document.add_picture(img_path+'\\Pack Discharging Energy_BMS.png')

#%%
plt.figure(figsize=(l,b))
plt.plot(details[x_axis],details['Charging Energy'])
# ax.plot(details['Time'],details['Charging Energy'])

# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))

# ymin, ymax = ax.get_ylim()
# ax.set_yticks(np.round(np.linspace(ymin, ymax, 20), 2))

plt.xlabel(x_axis,fontweight='bold')
plt.ylabel('Energy(Wh)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Charging Energy (BMS)',fontweight='bold')
plt.tight_layout()
# plt.savefig(img_path+'\\Pack Charging Energy_BMS.png',dpi=1200)

# document.add_picture(img_path+'\\Pack Charging Energy_BMS.png')


#%%
plt.figure(figsize=(l,b))
plt.plot(details[x_axis],details['Pack Voltage'])
# ax.plot(details['Time'],details['Pack Voltage'])

# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))

plt.xlabel(x_axis,fontweight='bold')
plt.ylabel('Voltage(V)',fontweight='bold')

plt.grid(linestyle='dotted')
plt.title('Pack Voltage',fontweight='bold')
plt.tight_layout()
# plt.savefig(img_path+'\\Pack Voltage.png',dpi=1200)

# document.add_picture(img_path+'\\Pack Voltage.png')
#%%

plt.figure(figsize=(l,b))
plt.plot(voltage_data[x_axis],voltage_data.loc[:,'MV_1':'MV_168'])
# ax.plot(voltage_data['Time'],voltage_data.loc[:,'MV_1':'MV_168'])

# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))
plt.ylabel('Voltage(mV)',fontweight='bold')
plt.xlabel(x_axis,fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Cell Voltage',fontweight='bold')
plt.tight_layout()


#%%
# #%%
# plt.plot()
# f, ax = plt.subplots()
# ax.plot(temperature_data[x_axis],temperature_data.loc[:,'MT_1':'MT_48'])

# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))
# plt.ylabel('Temperature('+u'\N{DEGREE SIGN}'+'C)',fontweight='bold')
# plt.xlabel('Time',fontweight='bold')
# plt.legend(t_names)
# plt.grid(linestyle='dotted')
# plt.title('Cell Temperature',fontweight='bold')

#%%
#%%
plt.figure(figsize=(l,b))
plt.plot(voltage_data[x_axis],(voltage_data['Mean_V'])) #*0.0001

# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))
plt.ylabel('Voltage(V)',fontweight='bold')
plt.xlabel(x_axis,fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Average Voltage',fontweight='bold')
plt.tight_layout()
# plt.savefig(img_path+'\\Average Voltage.png',dpi=1200)


#%%
plt.figure(figsize=(l,b))
plt.plot(voltage_data[x_axis],(voltage_data['delV'])*0.1)

# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))
plt.ylabel('Voltage(mV)',fontweight='bold')
plt.xlabel(x_axis,fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Voltage difference (delV)',fontweight='bold')
plt.tight_layout()
# plt.savefig(img_path+'\\delV.png',dpi=1200)



#%%
# plt.plot()
# f, ax = plt.subplots()
# ax.plot(details[x_axis],details['Capacity_calculated'])

# # xmin, xmax = ax.get_xlim()
# # ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))

# plt.xlabel('Time',fontweight='bold')
# plt.ylabel('Capacity(Ah)',fontweight='bold')

# plt.grid(linestyle='dotted')
# plt.title('Pack Capacity (Calculated)',fontweight='bold')



#%%
# plt.plot()
# f, ax = plt.subplots()
# ax.plot(details[x_axis],details['Energy_calculated']*0.001)

# # xmin, xmax = ax.get_xlim()
# # ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))

# plt.xlabel('Time',fontweight='bold')
# plt.ylabel('Energy(kWh)',fontweight='bold')

# plt.grid(linestyle='dotted')
# plt.title('Pack Energy (Calculated)',fontweight='bold')


plt.figure(figsize=(l,b))
plt.plot(temperature_data[x_axis],temperature_data['Mean_T'])

# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))
plt.ylabel('Temperature('+u'\N{DEGREE SIGN}'+'C)',fontweight='bold')
plt.xlabel(x_axis,fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Average Temperature',fontweight='bold')
plt.tight_layout()
# plt.savefig(img_path+'\\Average Temperature.png',dpi=1200)


#%%
plt.figure(figsize=(l,b))
plt.plot(temperature_data[x_axis],temperature_data['delT'])

# xmin, xmax = ax.get_xlim()
# ax.set_xticks(np.round(np.linspace(xmin, xmax, 18), 2))
plt.ylabel('Temperature('+u'\N{DEGREE SIGN}'+'C)',fontweight='bold')
plt.xlabel(x_axis,fontweight='bold')
plt.grid(linestyle='dotted')
plt.title('Temperature difference (delT)',fontweight='bold')
plt.tight_layout()
# plt.savefig(img_path+'\\delT.png',dpi=1200)


#%%
# path=file.rsplit('.',1)[0]+'_modified.xlsx'

# #%%
# writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
# voltage_data.to_excel(writer, sheet_name = 'Cell Voltage',index=False)
# temperature_data.to_excel(writer, sheet_name = 'Cell Temperature',index=False)
# details.to_excel(writer,sheet_name='Pack Details',index=False)
# status_data.to_excel(writer,sheet_name='Pack Status',index=False)
# # max_min_data.to_excel(writer,sheet_name='Max Min Mean',index=False)
# writer.close()


# #%%
# f=open(file.rsplit('.',1)[0]+'_raw_observations.txt',"w")

# print('======================================================================',file=f)
# print('---------------------Current Data---------------------',file=f)
# print('Datapoints:%s' % (len(voltage_data)),file=f)
# print('Total Time Spent:%s minutes' % ((voltage_data[x_axis].iloc[-1]-voltage_data[x_axis].iloc[0])/np.timedelta64(1,'m')),file=f)
# print('Maximum Charging Current:%s ; Minimum Charging Current:%s' % (details[details['State']==0]['Pack Current'].max(),details[details['State']==0]['Pack Current'].min()),file=f)
# print('Maximum Discharging Current:%s ; Minimum Discharging Current:%s' % (details[details['State']==1]['Pack Current'].max(),details[details['State']==1]['Pack Current'].min()),file=f)
# print('Maximum Charging Capacity:%s ; Minimum Charging Capacity:%s' % (details['Capacity_calculated_chg'].max(),details['Capacity_calculated_chg'].min()),file=f)
# print('Maximum Discharging Capacity:%s ; Minimum Discharging Capacity:%s' % (details['Capacity_calculated_dchg'].max(),details['Capacity_calculated_dchg'].min()),file=f)
# print('Maximum Charging Energy:%s ; Minimum Charging Energy:%s' % (details['Energy_calculated_chg'].max(),details['Energy_calculated_chg'].min()),file=f)
# print('Maximum Discharging Energy:%s ; Minimum Discharging Energy:%s' % (details['Energy_calculated_dchg'].max(),details['Energy_calculated_dchg'].min()),file=f)
# print('Maximum Charging Energy(BMS):%s ; Minimum Charging Energy(BMS):%s' % (details['Charging Energy'].max(),details['Charging Energy'].min()),file=f)
# print('Maximum Discharging Energy(BMS):%s ; Minimum Discharging Energy(BMS):%s' % (details['Discharging Energy'].max(),details['Discharging Energy'].min()),file=f)
# print('Maximum delT:%s degC' %(temperature_data['delT'].max()),file=f)
# print('Maximum Temperature:%s degC' %((temperature_data.loc[:,'MT_1':'MT_48'].max(axis=1)).max()),file=f)
# print('======================================================================',file=f)

# f.close()


#%%
cells=['MV_3','MV_71','MV_73','MV_96']
for c in cells:
    plt.figure(figsize=(l,b))
    plt.plot(voltage_data[x_axis],voltage_data[c])
    plt.ylabel('Voltage(mV)',fontweight='bold')
    plt.xlabel(x_axis,fontweight='bold')
    plt.grid(linestyle='dotted')
    plt.title('Cell Voltage ('+str(c)+')',fontweight='bold')
    plt.tight_layout()