import time
start=time.time()
import pickle
import pandas as pd
import numpy as np
with open("D:\\New folder (2)\\PHY\\PHY_21.1_25Deg_AllCycles_897Cycles_OCV.pkl",'rb') as f:
    data = pickle.load(f)
    a=pd.DataFrame()
    a['Time_in_Sec']=data['Time_in_Sec']
    a['OCV']=data['OCV']
    a['Step_Type']=data['Step_Type']
    a['Voltage']=data['Voltage']
    a['Current']=data['Current']
    a['New_Cycle_No']=data['New_Cycle_No']
    a['T_amb']=data['T_amb']
    a['OCV_State_No']=pd.cut(x=a.OCV,bins=[0,3,3.3,3.5,3.6,3.7,3.8,3.9,4,5],include_lowest=True,labels=[0,1,2,3,4,5,6,7,8]).astype(object)
    a['Time_in_Sec_s']=a['Time_in_Sec'].shift(-1)
    a['Time_in_Sec_Step']=a['Time_in_Sec_s']-a['Time_in_Sec']
    print('1/4..........')
    a.loc[(a['OCV_State_No']==0) & (a['Current']>0), 'OCV_s0_Chg'] = (a['Time_in_Sec_Step']);a['OCV_s0_Chg'] = a['OCV_s0_Chg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==1) & (a['Current']>0), 'OCV_s1_Chg'] = (a['Time_in_Sec_Step']);a['OCV_s1_Chg'] = a['OCV_s1_Chg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==2) & (a['Current']>0), 'OCV_s2_Chg'] = (a['Time_in_Sec_Step']);a['OCV_s2_Chg'] = a['OCV_s2_Chg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==3) & (a['Current']>0), 'OCV_s3_Chg'] = (a['Time_in_Sec_Step']);a['OCV_s3_Chg'] = a['OCV_s3_Chg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==4) & (a['Current']>0), 'OCV_s4_Chg'] = (a['Time_in_Sec_Step']);a['OCV_s4_Chg'] = a['OCV_s4_Chg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==5) & (a['Current']>0), 'OCV_s5_Chg'] = (a['Time_in_Sec_Step']);a['OCV_s5_Chg'] = a['OCV_s5_Chg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==6) & (a['Current']>0), 'OCV_s6_Chg'] = (a['Time_in_Sec_Step']);a['OCV_s6_Chg'] = a['OCV_s6_Chg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==7) & (a['Current']>0), 'OCV_s7_Chg'] = (a['Time_in_Sec_Step']);a['OCV_s7_Chg'] = a['OCV_s7_Chg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==8) & (a['Current']>0), 'OCV_s8_Chg'] = (a['Time_in_Sec_Step']);a['OCV_s8_Chg'] = a['OCV_s8_Chg'].replace(np.NaN,0)
    print('2/4..........')
    a.loc[(a['OCV_State_No']==0) & (a['Current']<0), 'OCV_s0_DChg'] = (a['Time_in_Sec_Step']);a['OCV_s0_DChg'] = a['OCV_s0_DChg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==1) & (a['Current']<0), 'OCV_s1_DChg'] = (a['Time_in_Sec_Step']);a['OCV_s1_DChg'] = a['OCV_s1_DChg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==2) & (a['Current']<0), 'OCV_s2_DChg'] = (a['Time_in_Sec_Step']);a['OCV_s2_DChg'] = a['OCV_s2_DChg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==3) & (a['Current']<0), 'OCV_s3_DChg'] = (a['Time_in_Sec_Step']);a['OCV_s3_DChg'] = a['OCV_s3_DChg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==4) & (a['Current']<0), 'OCV_s4_DChg'] = (a['Time_in_Sec_Step']);a['OCV_s4_DChg'] = a['OCV_s4_DChg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==5) & (a['Current']<0), 'OCV_s5_DChg'] = (a['Time_in_Sec_Step']);a['OCV_s5_DChg'] = a['OCV_s5_DChg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==6) & (a['Current']<0), 'OCV_s6_DChg'] = (a['Time_in_Sec_Step']);a['OCV_s6_DChg'] = a['OCV_s6_DChg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==7) & (a['Current']<0), 'OCV_s7_DChg'] = (a['Time_in_Sec_Step']);a['OCV_s7_DChg'] = a['OCV_s7_DChg'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==8) & (a['Current']<0), 'OCV_s8_DChg'] = (a['Time_in_Sec_Step']);a['OCV_s8_DChg'] = a['OCV_s8_DChg'].replace(np.NaN,0)
    print('3/4..........')
    a.loc[(a['OCV_State_No']==0) & (a['Current']==0), 'OCV_s0_Rst'] = (a['Time_in_Sec_Step']);a['OCV_s0_Rst'] = a['OCV_s0_Rst'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==1) & (a['Current']==0), 'OCV_s1_Rst'] = (a['Time_in_Sec_Step']);a['OCV_s1_Rst'] = a['OCV_s1_Rst'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==2) & (a['Current']==0), 'OCV_s2_Rst'] = (a['Time_in_Sec_Step']);a['OCV_s2_Rst'] = a['OCV_s2_Rst'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==3) & (a['Current']==0), 'OCV_s3_Rst'] = (a['Time_in_Sec_Step']);a['OCV_s3_Rst'] = a['OCV_s3_Rst'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==4) & (a['Current']==0), 'OCV_s4_Rst'] = (a['Time_in_Sec_Step']);a['OCV_s4_Rst'] = a['OCV_s4_Rst'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==5) & (a['Current']==0), 'OCV_s5_Rst'] = (a['Time_in_Sec_Step']);a['OCV_s5_Rst'] = a['OCV_s5_Rst'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==6) & (a['Current']==0), 'OCV_s6_Rst'] = (a['Time_in_Sec_Step']);a['OCV_s6_Rst'] = a['OCV_s6_Rst'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==7) & (a['Current']==0), 'OCV_s7_Rst'] = (a['Time_in_Sec_Step']);a['OCV_s7_Rst'] = a['OCV_s7_Rst'].replace(np.NaN,0)
    a.loc[(a['OCV_State_No']==8) & (a['Current']==0), 'OCV_s8_Rst'] = (a['Time_in_Sec_Step']);a['OCV_s8_Rst'] = a['OCV_s8_Rst'].replace(np.NaN,0)
    print('4/4..........')
    a.to_pickle('PHY_21.1_25Deg_AllCycles_897Cycles_OCV_StatesOnly.pkl')
print ('---------%s seconds----------' % (time.time()-start))
