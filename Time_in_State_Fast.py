import time
start=time.time()
import pickle
import pandas as pd
import numpy as np
with open("D:\\New folder (2)\\PHY\\PHY_21.1_25Deg_AllCycles_AllCycles_raw.pkl",'rb') as f:
    data = pickle.load(f)
    data['New_Cycle_No']=data['New_Cycle_No'].astype(object)
    data=data[data.New_Cycle_No<=897]
    print('1/4............')
    data=data.sort_values('RTC',ascending=True)
    data['Year']=data.RTC.map(lambda x: x.year)
    data=data.loc[(data.Year>=2017) & (data.Year<=2019)]
    data['RTC_s']=data['RTC'].shift(-1)
    data['Time_in_Sec_s']=data['RTC_s']-data['RTC']
    data['Time_in_Sec_s']=data['Time_in_Sec_s']/np.timedelta64(1,'s')
    data = data.reset_index(drop=True)
    print('1.5/4............')
    data['Time_in_Sec']=data.RTC-data.RTC.loc[data.index[0]]
    data['Time_in_Sec']=data['Time_in_Sec']/np.timedelta64(1,'s')
    data['Vol_State_No']=pd.cut(x=data.Voltage,bins=[0,3,3.3,3.5,3.6,3.7,3.8,3.9,4,5],include_lowest=True,labels=[0,1,2,3,4,5,6,7,8]).astype(object)
    data['Temp_State_No']=pd.cut(x=data.T_amb,bins=[25,30,35,40,45,60],include_lowest=True,labels=[1,2,3,4,5]).astype(object)
    print('2/4............')
    a1=data[data.Current>0]
    s10 = a1[a1.Vol_State_No==0]
    s10['Vol_s0_Chg']= s10['Time_in_Sec_s']; data['Vol_s0_Chg']= s10['Vol_s0_Chg']; data['Vol_s0_Chg'] = data['Vol_s0_Chg'].replace(np.NaN,0)
    s11 = a1[a1.Vol_State_No==1]
    s11['Vol_s1_Chg']= s11['Time_in_Sec_s']; data['Vol_s1_Chg']= s11['Vol_s1_Chg']; data['Vol_s1_Chg'] = data['Vol_s1_Chg'].replace(np.NaN,0)
    s12 = a1[a1.Vol_State_No==2]
    s12['Vol_s2_Chg']= s12['Time_in_Sec_s']; data['Vol_s2_Chg']= s12['Vol_s2_Chg']; data['Vol_s2_Chg'] = data['Vol_s2_Chg'].replace(np.NaN,0)
    s13 = a1[a1.Vol_State_No==3]
    s13['Vol_s3_Chg']= s13['Time_in_Sec_s']; data['Vol_s3_Chg']= s13['Vol_s3_Chg']; data['Vol_s3_Chg'] = data['Vol_s3_Chg'].replace(np.NaN,0)
    s14 = a1[a1.Vol_State_No==4]
    s14['Vol_s4_Chg']= s14['Time_in_Sec_s']; data['Vol_s4_Chg']= s14['Vol_s4_Chg']; data['Vol_s4_Chg'] = data['Vol_s4_Chg'].replace(np.NaN,0)
    s15 = a1[a1.Vol_State_No==5]
    s15['Vol_s5_Chg']= s15['Time_in_Sec_s']; data['Vol_s5_Chg']= s15['Vol_s5_Chg']; data['Vol_s5_Chg'] = data['Vol_s5_Chg'].replace(np.NaN,0)
    s16 = a1[a1.Vol_State_No==6]
    s16['Vol_s6_Chg']= s16['Time_in_Sec_s']; data['Vol_s6_Chg']= s16['Vol_s6_Chg']; data['Vol_s6_Chg'] = data['Vol_s6_Chg'].replace(np.NaN,0)
    s17 = a1[a1.Vol_State_No==7]
    s17['Vol_s7_Chg']= s17['Time_in_Sec_s']; data['Vol_s7_Chg']= s17['Vol_s7_Chg']; data['Vol_s7_Chg'] = data['Vol_s7_Chg'].replace(np.NaN,0)
    s18 = a1[a1.Vol_State_No==8]
    s18['Vol_s8_Chg']= s18['Time_in_Sec_s']; data['Vol_s8_Chg']= s18['Vol_s8_Chg']; data['Vol_s8_Chg'] = data['Vol_s8_Chg'].replace(np.NaN,0)
    t11 = a1[a1.Temp_State_No==1]
    t11['Temp_s1_Chg']= t11['Time_in_Sec_s']; data['Temp_s1_Chg']= t11['Temp_s1_Chg']; data['Temp_s1_Chg'] = data['Temp_s1_Chg'].replace(np.NaN,0)
    t12 = a1[a1.Temp_State_No==2]
    t12['Temp_s2_Chg']= t12['Time_in_Sec_s']; data['Temp_s2_Chg']= t12['Temp_s2_Chg']; data['Temp_s2_Chg'] = data['Temp_s2_Chg'].replace(np.NaN,0)
    t13 = a1[a1.Temp_State_No==3]
    t13['Temp_s3_Chg']= t13['Time_in_Sec_s']; data['Temp_s3_Chg']= t13['Temp_s3_Chg']; data['Temp_s3_Chg'] = data['Temp_s3_Chg'].replace(np.NaN,0)
    t14 = a1[a1.Temp_State_No==4]
    t14['Temp_s4_Chg']= t14['Time_in_Sec_s']; data['Temp_s4_Chg']= t14['Temp_s4_Chg']; data['Temp_s4_Chg'] = data['Temp_s4_Chg'].replace(np.NaN,0)
    t15 = a1[a1.Temp_State_No==5]
    t15['Temp_s5_Chg']= t15['Time_in_Sec_s']; data['Temp_s5_Chg']= t15['Temp_s5_Chg']; data['Temp_s5_Chg'] = data['Temp_s5_Chg'].replace(np.NaN,0)
    del (a1); del (s10); del (s11); del (s12);del (s13);del (s14);del (s15);del (s16);del (s17);del (s18);del (t11);del (t12);del (t13);del (t14);del (t15);
    print('3/4............')
    a2=data[data.Current==0]
    s20 = a2[a2.Vol_State_No==0]
    s20['Vol_s0_Rst']= s20['Time_in_Sec_s']; data['Vol_s0_Rst']= s20['Vol_s0_Rst']; data['Vol_s0_Rst'] = data['Vol_s0_Rst'].replace(np.NaN,0)
    s21 = a2[a2.Vol_State_No==1]
    s21['Vol_s1_Rst']= s21['Time_in_Sec_s']; data['Vol_s1_Rst']= s21['Vol_s1_Rst']; data['Vol_s1_Rst'] = data['Vol_s1_Rst'].replace(np.NaN,0)
    s22 = a2[a2.Vol_State_No==2]
    s22['Vol_s2_Rst']= s22['Time_in_Sec_s']; data['Vol_s2_Rst']= s22['Vol_s2_Rst']; data['Vol_s2_Rst'] = data['Vol_s2_Rst'].replace(np.NaN,0)
    s23 = a2[a2.Vol_State_No==3]
    s23['Vol_s3_Rst']= s23['Time_in_Sec_s']; data['Vol_s3_Rst']= s23['Vol_s3_Rst']; data['Vol_s3_Rst'] = data['Vol_s3_Rst'].replace(np.NaN,0)
    s24 = a2[a2.Vol_State_No==4]
    s24['Vol_s4_Rst']= s24['Time_in_Sec_s']; data['Vol_s4_Rst']= s24['Vol_s4_Rst']; data['Vol_s4_Rst'] = data['Vol_s4_Rst'].replace(np.NaN,0)
    s25 = a2[a2.Vol_State_No==5]
    s25['Vol_s5_Rst']= s25['Time_in_Sec_s']; data['Vol_s5_Rst']= s25['Vol_s5_Rst']; data['Vol_s5_Rst'] = data['Vol_s5_Rst'].replace(np.NaN,0)
    s26 = a2[a2.Vol_State_No==6]
    s26['Vol_s6_Rst']= s26['Time_in_Sec_s']; data['Vol_s6_Rst']= s26['Vol_s6_Rst']; data['Vol_s6_Rst'] = data['Vol_s6_Rst'].replace(np.NaN,0)
    s27 = a2[a2.Vol_State_No==7]
    s27['Vol_s7_Rst']= s27['Time_in_Sec_s']; data['Vol_s7_Rst']= s27['Vol_s7_Rst']; data['Vol_s7_Rst'] = data['Vol_s7_Rst'].replace(np.NaN,0)
    s28 = a2[a2.Vol_State_No==8]
    s28['Vol_s8_Rst']= s28['Time_in_Sec_s']; data['Vol_s8_Rst']= s28['Vol_s8_Rst']; data['Vol_s8_Rst'] = data['Vol_s8_Rst'].replace(np.NaN,0)
    t21 = a2[a2.Temp_State_No==1]
    t21['Temp_s1_Rst']= t21['Time_in_Sec_s']; data['Temp_s1_Rst']= t21['Temp_s1_Rst']; data['Temp_s1_Rst'] = data['Temp_s1_Rst'].replace(np.NaN,0)
    t22 = a2[a2.Temp_State_No==2]
    t22['Temp_s2_Rst']= t22['Time_in_Sec_s']; data['Temp_s2_Rst']= t22['Temp_s2_Rst']; data['Temp_s2_Rst'] = data['Temp_s2_Rst'].replace(np.NaN,0)
    t23 = a2[a2.Temp_State_No==3]
    t23['Temp_s3_Rst']= t23['Time_in_Sec_s']; data['Temp_s3_Rst']= t23['Temp_s3_Rst']; data['Temp_s3_Rst'] = data['Temp_s3_Rst'].replace(np.NaN,0)
    t24 = a2[a2.Temp_State_No==4]
    t24['Temp_s4_Rst']= t24['Time_in_Sec_s']; data['Temp_s4_Rst']= t24['Temp_s4_Rst']; data['Temp_s4_Rst'] = data['Temp_s4_Rst'].replace(np.NaN,0)
    t25 = a2[a2.Temp_State_No==5]
    t25['Temp_s5_Rst']= t25['Time_in_Sec_s']; data['Temp_s5_Rst']= t25['Temp_s5_Rst']; data['Temp_s5_Rst'] = data['Temp_s5_Rst'].replace(np.NaN,0)
    del (a2); del (s20); del (s21); del (s22);del (s23);del (s24);del (s25);del (s26);del (s27);del (s28);del (t21);del (t22);del (t23);del (t24);del (t25);
    print('3.5/4............')
    a3=data[data.Current<0]
    s0 = a3[a3.Vol_State_No==0]
    s0['Vol_s0_DChg']= s0['Time_in_Sec_s']; data['Vol_s0_DChg']= s0['Vol_s0_DChg']; data['Vol_s0_DChg'] = data['Vol_s0_DChg'].replace(np.NaN,0)
    s1 = a3[a3.Vol_State_No==1]
    s1['Vol_s1_DChg']= s1['Time_in_Sec_s']; data['Vol_s1_DChg']= s1['Vol_s1_DChg']; data['Vol_s1_DChg'] = data['Vol_s1_DChg'].replace(np.NaN,0)
    s2 = a3[a3.Vol_State_No==2]
    s2['Vol_s2_DChg']= s2['Time_in_Sec_s']; data['Vol_s2_DChg']= s2['Vol_s2_DChg']; data['Vol_s2_DChg'] = data['Vol_s2_DChg'].replace(np.NaN,0)
    s3 = a3[a3.Vol_State_No==3]
    s3['Vol_s3_DChg']= s3['Time_in_Sec_s']; data['Vol_s3_DChg']= s3['Vol_s3_DChg']; data['Vol_s3_DChg'] = data['Vol_s3_DChg'].replace(np.NaN,0)
    s4 = a3[a3.Vol_State_No==4]
    s4['Vol_s4_DChg']= s4['Time_in_Sec_s']; data['Vol_s4_DChg']= s4['Vol_s4_DChg']; data['Vol_s4_DChg'] = data['Vol_s4_DChg'].replace(np.NaN,0)
    s5 = a3[a3.Vol_State_No==5]
    s5['Vol_s5_DChg']= s5['Time_in_Sec_s']; data['Vol_s5_DChg']= s5['Vol_s5_DChg']; data['Vol_s5_DChg'] = data['Vol_s5_DChg'].replace(np.NaN,0)
    s6 = a3[a3.Vol_State_No==6]
    s6['Vol_s6_DChg']= s6['Time_in_Sec_s']; data['Vol_s6_DChg']= s6['Vol_s6_DChg']; data['Vol_s6_DChg'] = data['Vol_s6_DChg'].replace(np.NaN,0)
    s7 = a3[a3.Vol_State_No==7]
    s7['Vol_s7_DChg']= s7['Time_in_Sec_s']; data['Vol_s7_DChg']= s7['Vol_s7_DChg']; data['Vol_s7_DChg'] = data['Vol_s7_DChg'].replace(np.NaN,0)
    s8 = a3[a3.Vol_State_No==8]
    s8['Vol_s8_DChg']= s8['Time_in_Sec_s']; data['Vol_s8_DChg']= s8['Vol_s8_DChg']; data['Vol_s8_DChg'] = data['Vol_s8_DChg'].replace(np.NaN,0)
    t1 = a3[a3.Temp_State_No==1]
    t1['Temp_s1_DChg']= t1['Time_in_Sec_s']; data['Temp_s1_DChg']= t1['Temp_s1_DChg']; data['Temp_s1_DChg'] = data['Temp_s1_DChg'].replace(np.NaN,0)
    t2 = a3[a3.Temp_State_No==2]
    t2['Temp_s2_DChg']= t2['Time_in_Sec_s']; data['Temp_s2_DChg']= t2['Temp_s2_DChg']; data['Temp_s2_DChg'] = data['Temp_s2_DChg'].replace(np.NaN,0)
    t3 = a3[a3.Temp_State_No==3]
    t3['Temp_s3_DChg']= t3['Time_in_Sec_s']; data['Temp_s3_DChg']= t3['Temp_s3_DChg']; data['Temp_s3_DChg'] = data['Temp_s3_DChg'].replace(np.NaN,0)
    t4 = a3[a3.Temp_State_No==4]
    t4['Temp_s4_DChg']= t4['Time_in_Sec_s']; data['Temp_s4_DChg']= t4['Temp_s4_DChg']; data['Temp_s4_DChg'] = data['Temp_s4_DChg'].replace(np.NaN,0)
    t5 = a3[a3.Temp_State_No==5]
    t5['Temp_s5_DChg']= t5['Time_in_Sec_s']; data['Temp_s5_DChg']= t5['Temp_s5_DChg']; data['Temp_s5_DChg'] = data['Temp_s5_DChg'].replace(np.NaN,0) 
    del (a3); del (s0); del (s1); del (s2);del (s3);del (s4);del (s5);del (s6);del (s7);del (s8);del (t1);del (t2);del (t3);del (t4);del (t5);
    print('4/4............')
    data= data.drop(['RTC_s','Time_in_Sec_s','Year'], axis=1)
    data.to_pickle('PHY_21.1_25Deg_AllCycles_897Cycles_processed.pkl')
    end=time.time()
    print(end-start)
            
            
            
            
