# -*- coding: utf-8 -*-
"""
Created on Fri May 17 12:38:33 2024

@author: IITM
"""


#%%
# import pandas as pd
# f=r"D:\Benisha\IOE\24_05_14\String_01\Chg\CHG_1_13-05-2024_parallel(1,2,3,4)_modified.xlsx"
# data=pd.read_excel(f,sheet_name='Cell Voltage')

# i=len(data)//2
# j=i//2

# d1=data.loc[:j,:]
# d2=data.loc[j:i,:]
# d3=data.loc[i:i+j,:]
# d4=data.loc[i+j:,:]

# d1.to_excel(f.rsplit('.',1)[0]+'_11.xlsx',index=False)
# d2.to_excel(f.rsplit('.',1)[0]+'_22.xlsx',index=False)
# d3.to_excel(f.rsplit('.',1)[0]+'_3.xlsx',index=False)
# d4.to_excel(f.rsplit('.',1)[0]+'_4.xlsx',index=False)

#%%
# import pandas as pd
# f=r"D:\Benisha\LTVS\10kWh\Renesas_BMS\Drive_Test\04-04-2024\New folder\5-4-24  2  tvs 10kwh pack drive testteraterm 1\5-4-24  2  tvs 10kwh pack drive testteraterm 1_modified.xlsx"

# filename = f.rsplit('\\',1)[1].rsplit('.',1)[0]
# img_path = f.rsplit('\\',1)[0]+'\\'+f.rsplit('\\',1)[1].rsplit('.',1)[0]


# v_data = pd.read_excel(f, sheet_name = 'Cell Voltage')
# temperature_data = pd.read_excel(f, sheet_name = 'Cell Temperature')
# PV_data = pd.read_excel(f,sheet_name='Pack Voltage Details')
# relay_details = pd.read_excel(f,sheet_name='Relay Status')
# max_min_V_data = pd.read_excel(f,sheet_name='Voltage Max Min')
# max_min_temp_data = pd.read_excel(f,sheet_name='Temp Max Min')
# misc_details = pd.read_excel(f,sheet_name='Fault Status')
# energy_details = pd.read_excel(f,sheet_name='Energy Details')
# details = pd.read_excel(f,sheet_name='Pack Details') #DT

# v_x = pd.date_range(pd.to_datetime('04-04-2024  14:30:23'),pd.to_datetime('04-04-2024  14:30:23')+pd.Timedelta(seconds=len(v_data)-1),freq='s')
# t_x = pd.date_range(pd.to_datetime('04-04-2024  14:30:23'),pd.to_datetime('04-04-2024  14:30:23')+pd.Timedelta(seconds=len(temperature_data)-1),freq='s')
# pv_x = pd.date_range(pd.to_datetime('04-04-2024  14:30:23'),pd.to_datetime('04-04-2024  14:30:23')+pd.Timedelta(seconds=len(PV_data)-1),freq='s')
# r_x = pd.date_range(pd.to_datetime('04-04-2024  14:30:23'),pd.to_datetime('04-04-2024  14:30:23')+pd.Timedelta(seconds=len(relay_details)-1),freq='s')
# mmv_x = pd.date_range(pd.to_datetime('04-04-2024  14:30:23'),pd.to_datetime('04-04-2024  14:30:23')+pd.Timedelta(seconds=len(max_min_V_data)-1),freq='s')
# mmt_x = pd.date_range(pd.to_datetime('04-04-2024  14:30:23'),pd.to_datetime('04-04-2024  14:30:23')+pd.Timedelta(seconds=len(max_min_temp_data)-1),freq='s')
# m_x = pd.date_range(pd.to_datetime('04-04-2024  14:30:23'),pd.to_datetime('04-04-2024  14:30:23')+pd.Timedelta(seconds=len(misc_details)-1),freq='s')
# e_x = pd.date_range(pd.to_datetime('04-04-2024  14:30:23'),pd.to_datetime('04-04-2024  14:30:23')+pd.Timedelta(seconds=len(energy_details)-1),freq='s')
# d_x = pd.date_range(pd.to_datetime('04-04-2024  14:30:23'),pd.to_datetime('04-04-2024  14:30:23')+pd.Timedelta(seconds=len(details)-1),freq='s')

# v_data['DateTime'] = v_x
# temperature_data['DateTime'] = t_x
# PV_data['DateTime'] = pv_x
# relay_details['DateTime'] = r_x
# max_min_V_data['DateTime'] = mmv_x
# max_min_temp_data['DateTime'] = mmt_x
# misc_details['DateTime'] = m_x
# energy_details['DateTime'] = e_x
# details['DateTime'] = d_x


# path = img_path+'_dt.xlsx'
# writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
# v_data.to_excel(writer, sheet_name = 'Cell Voltage',index=False)
# temperature_data.to_excel(writer, sheet_name = 'Cell Temperature',index=False)
# PV_data.to_excel(writer,sheet_name='Pack Voltage Details',index=False)
# relay_details.to_excel(writer,sheet_name='Relay Status',index=False)
# max_min_V_data.to_excel(writer,sheet_name='Voltage Max Min',index=False)
# max_min_temp_data.to_excel(writer,sheet_name='Temp Max Min',index=False)
# misc_details.to_excel(writer,sheet_name='Fault Status',index=False)
# energy_details.to_excel(writer,sheet_name='Energy Details',index=False)
# details.to_excel(writer,sheet_name='Pack Details',index=False) #DT
# writer.close()

#%%
import pandas as pd
f1=r"D:\Benisha\LTVS\10kWh\Renesas_BMS\Drive_Test\04-04-2024\New folder\5-4-24 tvs 10kwh pack drive testteraterm 1\4-4-24 tvs 10kwh pack drive testteraterm 1_modified.xlsx"
f2=r"D:\Benisha\LTVS\10kWh\Renesas_BMS\Drive_Test\04-04-2024\New folder\5-4-24  2  tvs 10kwh pack drive testteraterm 1\5-4-24  2  tvs 10kwh pack drive testteraterm 1_modified_dt.xlsx"
f3=r"D:\Benisha\LTVS\10kWh\Renesas_BMS\Drive_Test\06-04-2024\New folder\6-4-24   tvs 10kwh pack drive testteraterm 1\5-4-24   tvs 10kwh pack drive testteraterm 1_modified.xlsx"
f4=r"D:\Benisha\LTVS\10kWh\Renesas_BMS\Drive_Test\06-04-2024\New folder\6-4-24 1  tvs 10kwh pack drive testteraterm 1\5-4-24 1  tvs 10kwh pack drive testteraterm 1_modified.xlsx"
f5=r"D:\Benisha\LTVS\10kWh\Renesas_BMS\Drive_Test\07-04-2024\New folder\6-4-24 2  tvs 10kwh pack drive testteraterm 1\6-4-24 2  tvs 10kwh pack drive testteraterm 1_modified.xlsx"
f6=r"D:\Benisha\LTVS\10kWh\Renesas_BMS\Drive_Test\07-04-2024\New folder\7-4-24   tvs 10kwh pack drive testteraterm 1\7-4-24   tvs 10kwh pack drive testteraterm 1_modified.xlsx"


data_v1 = pd.read_excel(f1,sheet_name='Cell Voltage')
data_v2 = pd.read_excel(f2,sheet_name='Cell Voltage')
data_v3 = pd.read_excel(f3,sheet_name='Cell Voltage')
data_v4 = pd.read_excel(f4,sheet_name='Cell Voltage')
data_v5 = pd.read_excel(f5,sheet_name='Cell Voltage')
data_v6 = pd.read_excel(f6,sheet_name='Cell Voltage')

data_t1 = pd.read_excel(f1,sheet_name='Cell Temperature')
data_t2 = pd.read_excel(f2,sheet_name='Cell Temperature')
data_t3 = pd.read_excel(f3,sheet_name='Cell Temperature')
data_t4 = pd.read_excel(f4,sheet_name='Cell Temperature')
data_t5 = pd.read_excel(f5,sheet_name='Cell Temperature')
data_t6 = pd.read_excel(f6,sheet_name='Cell Temperature')

data_pv1 = pd.read_excel(f1,sheet_name='Pack Voltage Details')
data_pv2 = pd.read_excel(f2,sheet_name='Pack Voltage Details')
data_pv3 = pd.read_excel(f3,sheet_name='Pack Voltage Details')
data_pv4 = pd.read_excel(f4,sheet_name='Pack Voltage Details')
data_pv5 = pd.read_excel(f5,sheet_name='Pack Voltage Details')
data_pv6 = pd.read_excel(f6,sheet_name='Pack Voltage Details')

data_r1 = pd.read_excel(f1,sheet_name='Relay Status')
data_r2 = pd.read_excel(f2,sheet_name='Relay Status')
data_r3 = pd.read_excel(f3,sheet_name='Relay Status')
data_r4 = pd.read_excel(f4,sheet_name='Relay Status')
data_r5 = pd.read_excel(f5,sheet_name='Relay Status')
data_r6 = pd.read_excel(f6,sheet_name='Relay Status')

data_mmv1 = pd.read_excel(f1,sheet_name='Voltage Max Min')
data_mmv2 = pd.read_excel(f2,sheet_name='Voltage Max Min')
data_mmv3 = pd.read_excel(f3,sheet_name='Voltage Max Min')
data_mmv4 = pd.read_excel(f4,sheet_name='Voltage Max Min')
data_mmv5 = pd.read_excel(f5,sheet_name='Voltage Max Min')
data_mmv6 = pd.read_excel(f6,sheet_name='Voltage Max Min')

data_mmt1 = pd.read_excel(f1,sheet_name='Temp Max Min')
data_mmt2 = pd.read_excel(f2,sheet_name='Temp Max Min')
data_mmt3 = pd.read_excel(f3,sheet_name='Temp Max Min')
data_mmt4 = pd.read_excel(f4,sheet_name='Temp Max Min')
data_mmt5 = pd.read_excel(f5,sheet_name='Temp Max Min')
data_mmt6 = pd.read_excel(f6,sheet_name='Temp Max Min')

data_m1 = pd.read_excel(f1,sheet_name='Fault Status')
data_m2 = pd.read_excel(f2,sheet_name='Fault Status')
data_m3 = pd.read_excel(f3,sheet_name='Fault Status')
data_m4 = pd.read_excel(f4,sheet_name='Fault Status')
data_m5 = pd.read_excel(f5,sheet_name='Fault Status')
data_m6 = pd.read_excel(f6,sheet_name='Fault Status')

data_e1 = pd.read_excel(f1,sheet_name='Energy Details')
data_e2 = pd.read_excel(f2,sheet_name='Energy Details')
data_e3 = pd.read_excel(f3,sheet_name='Energy Details')
data_e4 = pd.read_excel(f4,sheet_name='Energy Details')
data_e5 = pd.read_excel(f5,sheet_name='Energy Details')
data_e6 = pd.read_excel(f6,sheet_name='Energy Details')

data_d1 = pd.read_excel(f1,sheet_name='Pack Details')
data_d2 = pd.read_excel(f2,sheet_name='Pack Details')
data_d3 = pd.read_excel(f3,sheet_name='Pack Details')
data_d4 = pd.read_excel(f4,sheet_name='Pack Details')
data_d5 = pd.read_excel(f5,sheet_name='Pack Details')
data_d6 = pd.read_excel(f6,sheet_name='Pack Details')

#%%
v_data = pd.concat([data_v1,data_v2,data_v3,data_v4,data_v6])
temperature_data = pd.concat([data_t1,data_t2,data_t3,data_t4,data_t5,data_t6])
PV_data = pd.concat([data_pv1,data_pv2,data_pv3,data_pv4,data_pv5,data_pv6])
relay_details = pd.concat([data_r1,data_r2,data_r3,data_r4,data_r5,data_r6])
max_min_V_data = pd.concat([data_mmv1,data_mmv2,data_mmv3,data_mmv4,data_mmv5,data_mmv6])
max_min_temp_data = pd.concat([data_mmt1,data_mmt2,data_mmt3,data_mmt4,data_mmt5,data_mmt6])
misc_details = pd.concat([data_m1,data_m2,data_m3,data_m4,data_m5,data_m6])
energy_details = pd.concat([data_e1,data_e2,data_e3,data_e4,data_e5,data_e6])
details = pd.concat([data_d1,data_d2,data_d3,data_d4,data_d5,data_d6])

v_data = v_data.sort_values(by='DateTime',ascending=True)
temperature_data = temperature_data.sort_values(by='DateTime',ascending=True)
PV_data = PV_data.sort_values(by='DateTime',ascending=True)
relay_details = relay_details.sort_values(by='DateTime',ascending=True)
max_min_V_data = max_min_V_data.sort_values(by='DateTime',ascending=True)
max_min_temp_data = max_min_temp_data.sort_values(by='DateTime',ascending=True)
misc_details = misc_details.sort_values(by='DateTime',ascending=True)
energy_details = energy_details.sort_values(by='DateTime',ascending=True)
details = details.sort_values(by='DateTime',ascending=True)

#%%
filename = '04_04_2024_to_07_04_2024'
img_path = "D:\\Benisha\\LTVS\\10kWh\\Renesas_BMS\\Drive_Test"

path = img_path+'\\'+filename+'_modified_combined.xlsx'

#%%
writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
v_data.to_excel(writer, sheet_name = 'Cell Voltage',index=False)
temperature_data.to_excel(writer, sheet_name = 'Cell Temperature',index=False)
PV_data.to_excel(writer,sheet_name='Pack Voltage Details',index=False)
relay_details.to_excel(writer,sheet_name='Relay Status',index=False)
max_min_V_data.to_excel(writer,sheet_name='Voltage Max Min',index=False)
max_min_temp_data.to_excel(writer,sheet_name='Temp Max Min',index=False)
misc_details.to_excel(writer,sheet_name='Fault Status',index=False)
energy_details.to_excel(writer,sheet_name='Energy Details',index=False)
details.to_excel(writer,sheet_name='Pack Details',index=False) #DT
writer.close()

#%%

import pandas as pd
f1=r"D:\Benisha\LTVS\10kWh\Renesas_BMS\Drive_Test\15-04-2024\New folder\15-4-24 2  tvs 10kwh pack drive testteraterm 1\15-4-24 2  tvs 10kwh pack drive testteraterm 1_modified.xlsx"
f2=r"D:\Benisha\LTVS\10kWh\Renesas_BMS\Drive_Test\15-04-2024\New folder\15-4-24 2  1tvs 10kwh pack drive testteraterm 1\15-4-24 2  1tvs 10kwh pack drive testteraterm 1_modified.xlsx"

data_v1 = pd.read_excel(f1,sheet_name='Cell Voltage')
data_v2 = pd.read_excel(f2,sheet_name='Cell Voltage')

data_t1 = pd.read_excel(f1,sheet_name='Cell Temperature')
data_t2 = pd.read_excel(f2,sheet_name='Cell Temperature')

data_pv1 = pd.read_excel(f1,sheet_name='Pack Voltage Details')
data_pv2 = pd.read_excel(f2,sheet_name='Pack Voltage Details')

data_r1 = pd.read_excel(f1,sheet_name='Relay Status')
data_r2 = pd.read_excel(f2,sheet_name='Relay Status')

data_mmv1 = pd.read_excel(f1,sheet_name='Voltage Max Min')
data_mmv2 = pd.read_excel(f2,sheet_name='Voltage Max Min')

data_mmt1 = pd.read_excel(f1,sheet_name='Temp Max Min')
data_mmt2 = pd.read_excel(f2,sheet_name='Temp Max Min')

data_m1 = pd.read_excel(f1,sheet_name='Fault Status')
data_m2 = pd.read_excel(f2,sheet_name='Fault Status')

data_e1 = pd.read_excel(f1,sheet_name='Energy Details')
data_e2 = pd.read_excel(f2,sheet_name='Energy Details')

data_d1 = pd.read_excel(f1,sheet_name='Pack Details')
data_d2 = pd.read_excel(f2,sheet_name='Pack Details')

#%%
v_data = pd.concat([data_v1,data_v2])
temperature_data = pd.concat([data_t1,data_t2])
PV_data = pd.concat([data_pv1,data_pv2])
relay_details = pd.concat([data_r1,data_r2])
max_min_V_data = pd.concat([data_mmv1,data_mmv2])
max_min_temp_data = pd.concat([data_mmt1,data_mmt2])
misc_details = pd.concat([data_m1,data_m2])
energy_details = pd.concat([data_e1,data_e2])
details = pd.concat([data_d1,data_d2])

v_data = v_data.sort_values(by='DateTime',ascending=True)
temperature_data = temperature_data.sort_values(by='DateTime',ascending=True)
PV_data = PV_data.sort_values(by='DateTime',ascending=True)
relay_details = relay_details.sort_values(by='DateTime',ascending=True)
max_min_V_data = max_min_V_data.sort_values(by='DateTime',ascending=True)
max_min_temp_data = max_min_temp_data.sort_values(by='DateTime',ascending=True)
misc_details = misc_details.sort_values(by='DateTime',ascending=True)
energy_details = energy_details.sort_values(by='DateTime',ascending=True)
details = details.sort_values(by='DateTime',ascending=True)


#%%
filename = '15_04_2024'
img_path = "D:\\Benisha\\LTVS\\10kWh\\Renesas_BMS\\Drive_Test"

path = img_path+'\\'+filename+'_modified_combined.xlsx'

#%%
writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
v_data.to_excel(writer, sheet_name = 'Cell Voltage',index=False)
temperature_data.to_excel(writer, sheet_name = 'Cell Temperature',index=False)
PV_data.to_excel(writer,sheet_name='Pack Voltage Details',index=False)
relay_details.to_excel(writer,sheet_name='Relay Status',index=False)
max_min_V_data.to_excel(writer,sheet_name='Voltage Max Min',index=False)
max_min_temp_data.to_excel(writer,sheet_name='Temp Max Min',index=False)
misc_details.to_excel(writer,sheet_name='Fault Status',index=False)
energy_details.to_excel(writer,sheet_name='Energy Details',index=False)
details.to_excel(writer,sheet_name='Pack Details',index=False) #DT
writer.close()