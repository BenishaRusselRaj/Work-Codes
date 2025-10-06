# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 16:56:31 2024

@author: IITM
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob



# 25 deg
s=['2023-12-25 15:36:17','2023-12-26 03:19:50','2023-12-28 12:37:10']
e=['2023-12-26 02:29:00', '2023-12-26 14:49:35', '2023-12-28 21:27:59']

# 45 deg
# s=['2023-12-25 15:25:25','2023-12-26 01:13:05','2023-12-28 12:37:00']
# e=['2023-12-26 01:05:05', '2023-12-26 14:55:05', '2023-12-28 21:27:17']

# # 25 deg HPPC 
# s=['2023-12-26 15:35:45']
# e=['2023-12-27 13:27:53']

# # 45 deg HPPC
# s=['2023-12-26 20:19:57'] # needs 4 hour padding
# e=['2023-12-27 13:30:42']

# # 45 deg new data
# s=['2024-01-18 04:25:00','2024-01-18 15:59:00','2024-01-19 01:32:30']
# e=['2024-01-18 15:45:15','2024-01-19 01:14:30','2024-01-19 10:31:30']

'''
25 deg: c1: 0.5C/0.5C; c2: 0.3C/0.3C; c3: 0.5C/0.87C
45 deg: c1: 0.5C/0.5C; c2: 0.3C/0.3C; c3: 0.5C/0.87C
45 deg new: c1: 0.3C/0.3C; c2: 0.5C/0.5C; c3: 0.3C/0.87C


'''

c=1
    
    
# files=glob.glob(r"D:\Benisha\CALB\AL Calb Cell Test\CALB_Cell_data\Charge_discharge_files\25_deg\*.xlsx")
# # f1="D:\\Benisha\\CALB\\AL Calb Cell Test\\AL Test\\Tester Data\\Charge and Discharge Test\\45Deg_Cumulative_Test\\Calb Cell-02@45°C_overall data.xlsx"
# # f1="D:\\Benisha\\CALB\\AL Calb Cell Test\\AL Test\\Tester Data\\HPPC\\25 Deg\\3 tests 25 deg data.xlsx"
# f1=r"D:\Benisha\CALB\AL Calb Cell Test\AL Test\Tester Data\Charge and Discharge Test\0.5C_0.5C&0.3C_0.3C\25deg data.xlsx"
# f1="D:\\Benisha\\CALB\\AL Calb Cell Test\\AL Test\\Tester Data\\Welded_Busbar\\welded busbar 25 deg C_Tester_data.xlsx"
# data=pd.DataFrame()
# for f in files:
#     df=pd.read_excel(f,sheet_name='record')
#     data=pd.concat([data,df])

for i in range(len(s)): 
    files=glob.glob(r"D:\Benisha\CALB\AL Calb Cell Test\CALB_Cell_data\HPPC\45 deg data HPPC only.xlsx")
    # f1="D:\\Benisha\\CALB\\AL Calb Cell Test\\AL Test\\Tester Data\\Charge and Discharge Test\\45Deg_Cumulative_Test\\Calb Cell-02@45°C_overall data.xlsx"
    # f1="D:\\Benisha\\CALB\\AL Calb Cell Test\\AL Test\\Tester Data\\HPPC\\25 Deg\\3 tests 25 deg data.xlsx"
    f1=files[0]
    # f1="D:\\Benisha\\CALB\\AL Calb Cell Test\\AL Test\\Tester Data\\Welded_Busbar\\welded busbar 25 deg C_Tester_data.xlsx"
    data=pd.DataFrame()
    for f in files:
        df=pd.read_excel(f,sheet_name='record')
        data=pd.concat([data,df])
    
    # data=pd.read_excel(f1,sheet_name='record')
    img_path=f1.rsplit('\\',1)[0]
    name=f1.rsplit('\\',2)[1]+'_'+f1.rsplit('\\',2)[2].rsplit('.',1)[0]+'_0.5C_0.5C'
    
    data['Date']=pd.to_datetime(data['Date'],errors='coerce')
    
    print('Initial Start Time:%s' %data['Date'].iloc[0])
    print('Initial End Time:%s' %data['Date'].iloc[-1]) 
    
    data=data[data['Date']>=pd.to_datetime(s[i])]
    data=data[data['Date']<=pd.to_datetime(e[i])]
    
    print('Start Time before padding:%s' %data['Date'].iloc[0])
    print('End Time before padding:%s' %data['Date'].iloc[-1]) 
    
    # 4-hour padding to match times of the two files
    # x=pd.date_range(data['Date'].iloc[0]-pd.Timedelta(hours=4),data['Date'].iloc[0],freq='min')
    # data=data.reset_index(drop=True)
    
        
    # df=pd.DataFrame(index=range(len(x)),columns=data.columns)
    # df['Date']=x
    # data=pd.concat([df,data])
    # data=data.fillna(method='bfill')
    
    # data=data[data['Date']>=pd.to_datetime('2024-01-19 10:31:30')] # 45 deg hppc
    # data=data[data['Date']<=pd.to_datetime('2024-01-20 03:49:57')]
    
    # data=data[data['Date']>=pd.to_datetime('2023-12-26 15:35:45')] # 25 deg hppc
    # data=data[data['Date']<=pd.to_datetime('2023-12-27 13:27:53')]
    
    
    data=data.sort_values(by='Date',ascending=True)
    data['ElapsedTime']=(data['Date']-data['Date'].iloc[0])
    data['ElapsedTime']=data['ElapsedTime'].astype(str)
    data[['days','junk','ElapsedTime']]=data['ElapsedTime'].str.split(' ',expand=True)
    data[['hours','mins','sec']]=data['ElapsedTime'].str.split(':',expand=True)
    data['hours']=data['hours'].astype(int)+data['days'].astype(int)*24
    data['ElapsedTime']=data['hours'].astype(str)+':'+data['mins']+':'+data['sec']
    
    print('Start Time:%s' %data['Date'].iloc[0])
    print('End Time:%s' %data['Date'].iloc[-1])
    
    # custom filtering based on datetime (use only if required)
    # data=data[data['Date']>=pd.to_datetime('2024-01-10 13:59:00')]
    # data=data[data['Date']<=pd.to_datetime('2024-01-10 19:42:58')]
    
    # x_axis='Time'
    x_axis='Date'
    
    data['Time_in_sec_s']=(data['Date']-data['Date'].shift(1))/np.timedelta64(1,'s')# time difference b/w every datapt
    data['Time_in_sec']=(data['Date']-data['Date'].iloc[0])/np.timedelta64(1,'s')
    
    data['State']=np.nan
    data['State']=np.where(data['Current(A)']<0,1,2) 
    data['Cycle_No']=((data['State'].shift()-data['State'])<0).cumsum()
    
    
    data['Current(A)']=data['Current(A)'].astype(float)
    # data.to_csv(f1.rsplit('\\',1)[0]+'\\Dlogger_25deg_Cycle_'+str(c)+".csv")
    # c+=1
    
    l=7
    b=4
    
    #%%
    # index=data[data['Time']>10.3].index[0]
    # data.loc[index:,'Time']=data.loc[index:,'Time']-6.74
    
    #%%
    
    # timeline=['2023-12-27 00:41:22','2023-12-27 02:00:44','2023-12-27 03:20:06','2023-12-27 04:39:28','2023-12-27 05:58:50','2023-12-27 07:18:12','2023-12-27 08:37:35','2023-12-27 09:56:56','2023-12-27 11:16:18','2023-12-27 12:35:40'] # 25 deg
    # r_val=[0.41957335,0.423176096,0.424735804,0.429792183,0.43124368,0.428318584,0.438827098,0.444444444,0.449835734,0.43651998] # 25 deg
    
    # timeline=['2024-01-19 15:36:20','2024-01-19 16:55:41','2024-01-19 18:15:01','2024-01-19 19:34:24','2024-01-19 20:53:46','2024-01-19 22:13:08','2024-01-19 23:32:30','2024-01-20 00:51:51','2024-01-20 02:11:12','2024-01-20 03:30:34'] # 45 deg
    # r_val=[0.803842265,0.771370764,0.778564206,0.782828283,0.768064679,0.778958017,0.788795065,0.780981285,0.788635559,0.793410148] # 45 deg
    
    #%%
    # x=pd.date_range(data['Date'].iloc[0]-pd.Timedelta(hours=4),data['Date'].iloc[0],freq='min')
    # data=data.reset_index(drop=True)
    
    # fillval_t=data['T1(℃)'].iloc[:len(x)]
    # fillval_v=data['Voltage(V)'].iloc[:len(x)]
    
    # df=pd.DataFrame(index=range(len(x)),columns=data.columns)
    #%%
    # df['Date']=x
    # data=pd.concat([df,data])
    
    # data=data.reset_index(drop=True)
    # data['T1(℃)']=data['T1(℃)'].fillna(value=fillval_t)
    # data['Voltage(V)']=data['Voltage(V)'].fillna(value=fillval_v)
    # data=data.fillna(method='bfill')
    
    #%%
    data['Time']=(data['Date']-data['Date'].iloc[0])/np.timedelta64(1,'h')
    
    # index=data[data['Time']==4].index[0]
    # data.loc[:index,'Voltage(V)']=data.loc[:index,'Voltage(V)']-0.068
    #%% HPPC Tester data
    
    plt.figure(figsize=(l,b))
    print('Capacity ('+name+'):')
    plt.plot(data[x_axis],data['Capacity(Ah)']) #,marker='o',markersize=3
    
    plt.xlabel('Time Elapsed (in hours)',fontweight='bold')
    plt.ylabel('Capacity(Ah)',fontweight='bold')
    
    plt.grid(linestyle='dotted')
    plt.title('Cell Capacity',fontweight='bold')
    plt.tight_layout()
    # plt.savefig(img_path+'\\Capacity'+name+'.png',dpi=1200)
    
    #%%
    # fig,(ax1,ax2,ax3)=plt.subplots(3,sharex=True,figsize=(l,b)) #
    
    # ax1.plot(data[x_axis],data['Current(A)'],marker='o',markersize=3)
    
    # ax1.set_ylabel('Current(A)',fontweight='bold')
    
    # ax1.grid(linestyle='dotted')
    # ax1.set_title('Current, Cell Voltage and Cell Temperature',fontweight='bold')
    
    
    # ax2.plot(data[x_axis],data['Voltage(V)'],marker='o',markersize=3)
    
    # ax2.set_ylabel('Voltage(V)',fontweight='bold')
    
    # ax2.grid(linestyle='dotted')
    
    
    # ax3.plot(data[x_axis],data['T1(℃)'],marker='o',markersize=3)
    
    # ax3.set_ylabel('Temperature('+u'\N{DEGREE SIGN}'+'C)',fontweight='bold')
    # ax3.set_xlabel('Time Elapsed (in hours)',fontweight='bold')
    # ax3.grid(linestyle='dotted')
    # # plt.savefig(img_path+'\\Current, Cell Voltage and Cell Temperature_'+name+'_1.png',dpi=1200)
    
    # fig,(ax1,ax2,ax3)=plt.subplots(3,sharex=True,figsize=(l,b)) #
    
    # ax1.plot(data[x_axis],data['Current(A)'])
    
    # ax1.set_ylabel('Current(A)',fontweight='bold')
    
    # ax1.grid(linestyle='dotted')
    # ax1.set_title('Current, Cell Voltage and Cell Temperature',fontweight='bold')
    
    
    # ax2.plot(data[x_axis],data['Voltage(V)'])
    
    # ax2.set_ylabel('Voltage(V)',fontweight='bold')
    
    # ax2.grid(linestyle='dotted')
    
    # ax3.plot(data[x_axis],data['T1(℃)'])
    
    # ax3.set_ylabel('Temperature('+u'\N{DEGREE SIGN}'+'C)',fontweight='bold')
    # ax3.set_xlabel('Time Elapsed (in hours)',fontweight='bold')
    # ax3.grid(linestyle='dotted')
    # # plt.savefig(img_path+'\\Current, Cell Voltage and Cell Temperature_'+name+'_1.png',dpi=1200)
    
    #%%
    fig,(ax1,ax2)=plt.subplots(2,sharex=True,figsize=(l,b)) #
    
    ax1.plot(data[x_axis],data['Current(A)'],marker='o',markersize=3)
    
    ax1.set_ylabel('Current(A)',fontweight='bold')
    
    ax1.grid(linestyle='dotted')
    ax1.set_title('Current, Cell Voltage and Cell Temperature',fontweight='bold')
    
    
    ax2.plot(data[x_axis],data['Voltage(V)'],marker='o',markersize=3)
    
    ax2.set_ylabel('Voltage(V)',fontweight='bold')
    
    ax2.grid(linestyle='dotted')
    
    
    ax2.set_xlabel('Time Elapsed (in hours)',fontweight='bold')
    # plt.savefig(img_path+'\\Current, Cell Voltage and Cell Temperature_'+name+'_1.png',dpi=1200)
    
    fig,(ax1,ax2)=plt.subplots(2,sharex=True,figsize=(l,b)) #
    
    ax1.plot(data[x_axis],data['Current(A)'])
    
    ax1.set_ylabel('Current(A)',fontweight='bold')
    
    ax1.grid(linestyle='dotted')
    ax1.set_title('Current, Cell Voltage and Cell Temperature',fontweight='bold')
    
    
    ax2.plot(data[x_axis],data['Voltage(V)'])
    
    ax2.set_ylabel('Voltage(V)',fontweight='bold')
    
    ax2.grid(linestyle='dotted')
    
    ax2.set_xlabel('Time Elapsed (in hours)',fontweight='bold')
    # plt.savefig(img_path+'\\Current, Cell Voltage and Cell Temperature_'+name+'.png',dpi=1200)
    
    
    #%%
    plt.figure(figsize=(l,b))
    print('Energy ('+name+'):')
    plt.plot(data[x_axis],data['Energy(Wh)'])
    
    plt.xlabel('Time Elapsed (in hours)',fontweight='bold')
    plt.ylabel('Energy(Wh)',fontweight='bold')
    
    plt.grid(linestyle='dotted')
    plt.title('Energy Transferred',fontweight='bold')
    plt.tight_layout()
    # plt.savefig(img_path+'\\Energy'+name+'.png',dpi=1200)
    
    #%% HPPC SoC-resistance Plot
    # data['R0']=np.nan
    
    # for i,n in enumerate(timeline):
    #     data.loc[data['Date']==n,'R0']=r_val[i]
    
    #%%
    plt.figure(figsize=(l,b))
    print('Voltage and R ('+name+'):')
    plt.plot(data[x_axis],data['R0'],marker='o',markersize=3)
    
    plt.xlabel('Time Elapsed (in hours)',fontweight='bold')
    plt.ylabel('Resistance (mohms)',fontweight='bold')
    
    plt.grid(linestyle='dotted')
    plt.title('Ohmic Resistance',fontweight='bold')
    plt.tight_layout() 
    
    #%%
    fig, ax1 = plt.subplots()
    
    color ='tab:blue'
    ax1.set_xlabel('Time Elapsed (in hours)',fontweight='bold')
    ax1.set_ylabel('Voltage(V)',fontweight='bold', color=color)
    ax1.plot(data[x_axis],data['Voltage(V)'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(linestyle='dotted',axis='x')
    ax1.set_title('Ohmic Resistance and Voltage',fontweight='bold')
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    
    color = 'tab:red'
    ax2.plot(data[x_axis], data['R0'], color=color,marker='o',markersize=3)
    ax2.set_ylabel('Resistance(mohms)',fontweight='bold', color=color)
    ymin, ymax = ax2.get_ylim()
    ax2.set_yticks(np.round(np.linspace(ymin-0.100, ymax+0.100, 18),3))
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.grid(linestyle='dotted')
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
    
    #%% HPPC Temperature data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

f1="D:\\Benisha\\CALB\\AL Calb Cell Test\\AL Test\\Tester Data\\HPPC\\25 Deg\\Temperature_data\\25 deg cell temperature.xlsx"

data=pd.read_excel(f1,sheet_name='record')
img_path=f1.rsplit('\\',1)[0]
name=f1.rsplit('\\',3)[1]+'_'+f1.rsplit('\\',3)[3].rsplit('.',1)[0]+'_hppc_separated'
T='Terminal Temperature'

x_axis='Time'
# x_axis='Date'

data['Date']=pd.to_datetime(data['Date'],errors='coerce')


data=data[data['Date']>=pd.to_datetime('2023-12-26 15:35:45')]
data=data[data['Date']<=pd.to_datetime('2023-12-27 13:27:53')]
      
data=data.reset_index(drop=True)
x=pd.date_range(data['Date'].iloc[0]-pd.Timedelta(hours=4),data['Date'].iloc[0],freq='min')

fillval=data['T1(℃)'].iloc[:50]

df=pd.DataFrame(index=range(len(x)),columns=data.columns)
df['Date']=x
data=pd.concat([df,data])


data=data.reset_index(drop=True)
data['T1(℃)']=data['T1(℃)'].fillna(value=fillval)
data=data.fillna(method='bfill')

data['Time']=(data['Date']-data['Date'].iloc[0])/np.timedelta64(1,'h')

l=6.98
b=3.98

plt.figure(figsize=(l,b))
print('Temperature ('+name+'):')
plt.plot(data[x_axis],data['T1(℃)'])

plt.ylabel('Temperature('+u'\N{DEGREE SIGN}'+'C)',fontweight='bold')
plt.xlabel('Time Elapsed (in hours)',fontweight='bold')
plt.grid(linestyle='dotted')
plt.title(T,fontweight='bold')
plt.tight_layout()
# plt.savefig(img_path+'\\Cell Temperature_'+name+'.png',dpi=1200)
# 
#%% Datalogger HPPC temperature data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import glob

# 25 deg
# s=['2023-12-25 15:36:17','2023-12-26 03:19:50','2023-12-28 12:37:10']
# e=['2023-12-26 02:29:00', '2023-12-26 14:49:35', '2023-12-28 21:27:59']

# 45 deg
# s=['2023-12-25 15:25:25','2023-12-26 01:13:05','2023-12-28 12:37:00']
# e=['2023-12-26 01:05:05', '2023-12-26 14:55:05', '2023-12-28 21:27:17']

# # 25 deg HPPC 
# s=['2023-12-26 15:35:45']
# e=['2023-12-27 13:27:53']

# # 45 deg HPPC
s=['2023-12-26 20:19:57'] # needs 4 hour padding
e=['2023-12-27 13:30:42']

# # 45 deg new data
# s=['2024-01-18 04:25:00','2024-01-18 15:59:00','2024-01-19 01:32:30']
# e=['2024-01-18 15:45:15','2024-01-19 01:14:30','2024-01-19 10:31:30']

# files=glob.glob(r"D:\Benisha\CALB\AL Calb Cell Test\CALB_Cell_data\Charge_discharge_files\Datalogger\*.csv")
# # f1="D:\\Benisha\\CALB\\AL Calb Cell Test\\AL Test\\Data Loger data\\Charge & Discharge Test\\Data 8199 2391 17-Jan-24 17_32_26_25Deg cell 2_45Deg cell 1 test log\\Data 8199 2391 17-Jan-24 17_32_26_25Deg cell 2_45Deg cell 1 test log.csv"
# f1="D:\\Benisha\\CALB\\AL Calb Cell Test\\AL Test\\-20Deg\\Datalogger_Temperature and HeatFlux Data\\Data 8199 2391 09-Jan-24 22_02_29_RAW.csv"

c_no=1

for i in range(len(s)): 
    files=glob.glob(r"D:\Benisha\CALB\AL Calb Cell Test\CALB_Cell_data\HPPC\Datalogger\Raw_files\*.csv")
    # f1="D:\\Benisha\\CALB\\AL Calb Cell Test\\AL Test\\Data Loger data\\Charge & Discharge Test\\Data 8199 2391 17-Jan-24 17_32_26_25Deg cell 2_45Deg cell 1 test log\\Data 8199 2391 17-Jan-24 17_32_26_25Deg cell 2_45Deg cell 1 test log.csv"
    f1=files[0]

    cols=['Scan','Time','101 <C1_HF_Negative Terminal side> (VDC)','Alarm 101','102 <C1_TC_Negative Terminal side> (C)','Alarm 102','103 <C1_HF_Positive Terminal side> (VDC)','Alarm 103','104 <C1_TC_Positive Terminal side> (C)','Alarm 104','105 <C1_HF_Cell Center> (VDC)','Alarm 105','106 <C1_TC_Cell Center> (C)','Alarm 106','107 <C1_HF_Cell Side> (VDC)','Alarm 107','108 <C1_TC_Cell Side> (C)','Alarm 108','109 <C1_HF_Cell Bottom> (VDC)','Alarm 109','110 <C1_TC_Cell Bottom> (C)','Alarm 110','111 <C2_TC_Positive Terminal side> (C)','Alarm 111','112 <C2_HF_Positive Terminal side> (VDC)','Alarm 112','113 <C2_HF_Negative Terminal side> (C)','Alarm 113','114 <C2_TC_Negative Terminal side> (VDC)','Alarm 114','115 <C2_HF_Cell Center> (C)','Alarm 115','116 <C2_TC_Cell Center> (VDC)','Alarm 116','117 <C2_HF_Cell Side> (C)','Alarm 117','118 <C2_TC_Cell Side> (VDC)','Alarm 118','119 <C2_HF_Cell Bottom> (C)','Alarm 119','120 <C2_TC_Cell Bottom> (VDC)','Alarm 120']
    # cols=['Scan','Time','Elapsed','101 <C1_HF_Positive Terminal side> (VDC)','Alarm 101','102 <C1_TC_Positive Terminal side> (C)','Alarm 102','103 <C1_HF_Negative Terminal side> (VDC)','Alarm 103','104 <C1_TC_Negative Terminal side> (C)','Alarm 104','105 <C1_HF_Cell Center> (VDC)','Alarm 105','106 <C1_TC_Cell Center> (C)','Alarm 106','107 <C1_HF_Cell Side> (VDC)','Alarm 107','108 <C1_TC_Cell Side> (C)','Alarm 108','109 <C1_HF_Cell Bottom> (VDC)','Alarm 109','110 <C1_TC_Cell Bottom> (C)','Alarm 110','111 <C2_TC_Positive Terminal side> (C)','Alarm 111','112 <C2_HF_Positive Terminal side> (VDC)','Alarm 112','113 <C2_HF_Negative Terminal side> (VDC)','Alarm 113','114 <C2_TC_Negative Terminal side> (C)','Alarm 114','115 <C2_HF_Cell Center> (VDC)','Alarm 115','116 <C2_TC_Cell Center> (C)','Alarm 116','117 <C2_HF_Cell Side> (VDC)','Alarm 117','118 <C2_TC_Cell Side> (C)','Alarm 118','119 <C2_HF_Cell Bottom> (VDC)','Alarm 119','120 <C2_TC_Cell Bottom> (C)','Alarm 120']
    # try:
    #     data=pd.read_csv(f1,encoding='utf-8',sep=',',names=cols)
    # except:
    #     data=pd.read_csv(f1,encoding='utf-16',sep=',',names=cols)
    
    # Read files with proper encoding format
    data=pd.DataFrame()
    for f in files:
        try:
            df=pd.read_csv(f,encoding='utf-8',sep=',',names=cols)
        except:
            df=pd.read_csv(f,encoding='utf-16',sep=',',names=cols)
        df=df.reset_index(drop=True)
        df=df.loc[29:,:]
        data=pd.concat([data,df])
    
    # try:
    #     data=pd.read_csv(f,encoding='utf-8',sep=',',names=cols)
    # except:
    #     data=pd.read_csv(f,encoding='utf-16',sep=',',names=cols)
    
 
    data['Time']=data['Time'].astype(str)
    data[['DateTime','junk']]=data['Time'].str.rsplit(':',1,expand=True)
    
    data['DateTime']=pd.to_datetime(data['DateTime'],errors='coerce')
    data=data[['DateTime'] + [col for col in data.columns if col!='DateTime']]
    
    data=data.dropna(thresh=4)
    data=data.reset_index(drop=True)
    # data=data.loc[2:,:]
    
    data=data[data['DateTime']>=pd.to_datetime(s[i])]
    data=data[data['DateTime']<=pd.to_datetime(e[i])]
    
    # data=data[data['DateTime']>=pd.to_datetime('2024-01-18 15:59:00')] #0.5C
    # data=data[data['DateTime']<=pd.to_datetime('2024-01-19 01:14:30')]
    
    # data=data[data['DateTime']>=pd.to_datetime('2024-01-18 04:25:00')] # 0.3C
    # data=data[data['DateTime']<=pd.to_datetime('2024-01-18 15:45:15')]
    
    # data=data[data['DateTime']>=pd.to_datetime('2024-01-19 01:32:30')] # 0.5C/0.87C
    # data=data[data['DateTime']<=pd.to_datetime('2024-01-19 10:31:30')]
    
    # data=data[data['DateTime']>=pd.to_datetime('2024-01-19 10:31:30')] #hppc
    # data=data[data['DateTime']<=pd.to_datetime('2024-01-20 03:49:57')]
    
    # data=data[data['DateTime']>=pd.to_datetime('2024-01-09 23:40:50')] 
    # data=data[data['DateTime']<=pd.to_datetime('2024-01-10 11:28:30')]
    
    data=data.reset_index(drop=True)
    data=data.sort_values(by='DateTime',ascending=True)
    data=data.dropna(subset=['DateTime']).reset_index(drop=True)
    
    print('Start Time before padding:%s' %data['DateTime'].iloc[0])
    print('End Time before padding:%s' %data['DateTime'].iloc[-1])

    x=pd.date_range(data['DateTime'].iloc[0]-pd.Timedelta(hours=4),data['DateTime'].iloc[0],freq='min')
    data=data.reset_index(drop=True)
    
    df=pd.DataFrame(index=range(len(x)),columns=data.columns)
    df['DateTime']=x
    data=pd.concat([df,data])
    
    data=data.fillna(method='bfill')
    
    data['Time_Elapsed']=(data['DateTime']-data['DateTime'].iloc[0])/np.timedelta64(1,'h')
    
    data['ElapsedTime']=(data['DateTime']-data['DateTime'].iloc[0])
    print('Start Time:%s' %data['DateTime'].iloc[0])
    print('End Time:%s' %data['DateTime'].iloc[-1])
    
    data['ElapsedTime']=data['ElapsedTime'].astype(str)
    data[['days','junk','ElapsedTime']]=data['ElapsedTime'].str.split(' ',expand=True)
    data[['hours','mins','sec']]=data['ElapsedTime'].str.split(':',expand=True)
    data['hours']=data['hours'].astype(int)+data['days'].astype(int)*24
    data['ElapsedTime']=data['hours'].astype(str)+':'+data['mins']+':'+data['sec']
    data['Time_Elapsed']=(data['DateTime']-data['DateTime'].iloc[0])/np.timedelta64(1,'h')
    x_axis='Time_Elapsed'
    # x_axis='DateTime'
        
    img_path=f1.rsplit('\\',1)[0]
    # name=f1.rsplit('\\',2)[1]+'_'+f1.rsplit('\\',2)[2].rsplit('.',1)[0]+'_0.5C_separated'
    name='45deg_datalogger_heatflux_hppc'
    
    HF=[col for col in cols if "HF" in col]
    
    for c in HF:
        data[c]=data[c].astype(float)
        data[c]=((data[c])/(3.77))*1000
        data[c]=data[c]*1000
        data[c]=data[c].rolling(50).median()
    
    # test_col=['101 <C1_HF_Negative Terminal side> (VDC)','102 <C1_TC_Negative Terminal side> (C)','103 <C1_HF_Positive Terminal side> (VDC)','104 <C1_TC_Positive Terminal side> (C)','105 <C1_HF_Cell Center> (VDC)','106 <C1_TC_Cell Center> (C)','107 <C1_HF_Cell Side> (VDC)','108 <C1_TC_Cell Side> (C)','109 <C1_HF_Cell Bottom> (VDC)','110 <C1_TC_Cell Bottom> (C)','111 <C2_TC_Positive Terminal side> (C)','112 <C2_HF_Positive Terminal side> (VDC)','113 <C2_HF_Negative Terminal side> (C)','114 <C2_TC_Negative Terminal side> (VDC)','115 <C2_HF_Cell Center> (C)','116 <C2_TC_Cell Center> (VDC)','117 <C2_HF_Cell Side> (C)','118 <C2_TC_Cell Side> (VDC)','119 <C2_HF_Cell Bottom> (C)','120 <C2_TC_Cell Bottom> (VDC)']
    C1=[col for col in HF if "C1" in col]
    C2=[col for col in HF if 'C2' in col]
    
    l=7.5
    b=4.5
    
    # data.to_csv(f1.rsplit('\\',1)[0]+'\\Dlogger_45deg_hppc_'+str(c_no)+".csv")
    data.to_csv(r"D:\Benisha\CALB\AL Calb Cell Test\CALB_Cell_data\HPPC\Datalogger\Dlogger_45deg_hppc_"+str(c_no)+".csv")
    c_no+=1
    
    check=C2
    
    #%%
    for i in check:
        title= re.findall(r'\<.*?\>', i)[0].replace('<','').replace('>','')
        plt.figure(figsize=(l,b))
    
        print(title+'('+name+')')
        plt.plot(data[x_axis],data[i].astype(float))
        
        plt.xlabel('Time Elapsed (in hours)',fontweight='bold')
        plt.ylabel('Heat Flux (W/m^2)',fontweight='bold')
        plt.grid(linestyle='dotted')
        plt.title(title,fontweight='bold')
        plt.tight_layout()
        # plt.savefig(img_path+'\\'+title+'_'+name+'.png',dpi=1200)
    
    
    l=9.5
    b=5.5
    fig,(ax1,ax2,ax3,ax4,ax5)=plt.subplots(5,sharex=True,figsize=(l,b))
    
    # for n,i in enumerate(C1):
    title= re.findall(r'\<.*?\>', check[0])[0].replace('<','').replace('>','')
    
    print(title+'('+name+')')
    ax1.plot(data[x_axis],data[check[0]].astype(float),label=title)
    ax1.set_title('Datalogger Temperature',fontweight='bold')
    ax1.grid(linestyle='dotted')
    ax1.legend()
    
        
    title= re.findall(r'\<.*?\>', check[1])[0].replace('<','').replace('>','')
    
    print(title+'('+name+')')
    ax2.plot(data[x_axis],data[check[1]].astype(float),label=title)
    
    ax2.grid(linestyle='dotted')
    ax2.legend()
    
    title= re.findall(r'\<.*?\>', check[2])[0].replace('<','').replace('>','')
    
    print(title+'('+name+')')
    ax3.plot(data[x_axis],data[check[2]].astype(float),label=title)
    ax3.set_ylabel('Heat Flux (W/m^2)',fontweight='bold')
    ax3.grid(linestyle='dotted')
    ax3.legend()
    
    
    title= re.findall(r'\<.*?\>', check[3])[0].replace('<','').replace('>','')
    
    print(title+'('+name+')')
    ax4.plot(data[x_axis],data[check[3]].astype(float),label=title)
    ax4.grid(linestyle='dotted')
    ax4.legend()
    
    
    title= re.findall(r'\<.*?\>', check[4])[0].replace('<','').replace('>','')
    
    print(title+'('+name+')')
    ax5.plot(data[x_axis],data[check[4]].astype(float),label=title)
    ax5.set_xlabel('Time Elapsed (in hours)',fontweight='bold')
    ax5.grid(linestyle='dotted')
    ax5.legend()
    
    # plt.savefig(img_path+'\\C1_HF_all_combined'+name+'.png',dpi=1200)
    
    #%%
    plt.figure()
    title= re.findall(r'\<.*?\>', check[0])[0].replace('<','').replace('>','')
    plt.plot(data[x_axis],data[check[0]].astype(float),label=title)
    title= re.findall(r'\<.*?\>', check[1])[0].replace('<','').replace('>','')
    plt.plot(data[x_axis],data[check[1]].astype(float),label=title)
    title= re.findall(r'\<.*?\>', check[2])[0].replace('<','').replace('>','')
    plt.plot(data[x_axis],data[check[2]].astype(float),label=title)
    title= re.findall(r'\<.*?\>', check[3])[0].replace('<','').replace('>','')
    plt.plot(data[x_axis],data[check[3]].astype(float),label=title)
    title= re.findall(r'\<.*?\>', check[4])[0].replace('<','').replace('>','')
    plt.plot(data[x_axis],data[check[4]].astype(float),label=title)
    plt.title('Datalogger Temperature',fontweight='bold')
    plt.grid(linestyle='dotted')
    plt.legend()
    
