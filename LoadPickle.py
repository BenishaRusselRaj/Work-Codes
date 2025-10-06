import time
start=time.time()
import pickle
file="D:\\Benisha\\SoH_NN\\Data\\BRD\\Sample 3.1\\BRD_3.1_25Deg_AllCycles_AllCycles_raw.pkl"
with open(file,'rb') as f:
    data = pickle.load(f)
    data.to_csv(file.rsplit('\\',1)[0]+'\\'+file.rsplit('\\',1)[1].rsplit('.',1)[0]+'.csv')
    d1=data.head(10000)
    d2=data.tail(10000)
#    print(data)
#    a=data[data.New_Cycle_No==0]
#    print(data['Realtime'])
#    print(data['RTC'])
##    print(data['Timeflag'].value_counts())
#    print(data['Temp_Ch1'])
#    print(data['Temp_Ch17'])
#    print(data[(data.New_Cycle_No==1) & (data.Current<0)])
#    print(data['RTC'])
#    data['s']=data.loc[:,'OCV_s0_Chg':'OCV_s8_DChg'].sum(axis=1)
#    for i in data.index:
#        if (data.s[i]!=0):
#             data['Csum']=data.s[i]+data.s[i-1]
#         else:
#            x=x+1
#             if (x==1):
#                 
#            data.s[i]=data.loc[i,'OCV_s0_Rst':'OCv_s8_Rst'].sum(axis=1)
#    s1=data['s'].sum()
#    s2=s1/5000
#    data['Temperature']=35
#    data['Tc']= data['Temperature']+(1*s2)
#    data['Q']=(data['Current']*(data['Voltage']-data['OCV']))+(data['Current']*data['Tc']*((-1)*data['OCV']*96485.332))
#    a1=data[data.Current>0]
#    a2=data[data.Current==0]
#    a3=data[data.Current<0]
#    print('Chg:', a1['Q'].mean())
#    print('DChg:', a3['Q'].mean())
#    print('Rst:', a2['Q'].mean())
#    print(a1['Q'].min())
#    print(data['Tc'])
#    print(a1['OCV_s8_Chg'])
#    print(data['s'])
#    data=data[data.New_Cycle_No<=500]
#    print(a1['Current'])
#    print(a1['Current'].max())
#    print(a1['Voltage'])
#    print(a1['OCV'])
#    print(data['Sample_Name'])
#    print ('PHY-6.1- Chg_1')
#    print(data['Vol_s0_Chg'].sum())
#    print(data['Vol_s1_Chg'].sum())
#    print(data['Vol_s2_Chg'].sum())
#    print(data['Vol_s3_Chg'].sum())
#    print(data['Vol_s4_Chg'].sum())
#    print(data['Vol_s5_Chg'].sum())
#    print(data['Vol_s6_Chg'].sum())
#    print(data['Vol_s7_Chg'].sum())
#    print(data['Vol_s8_Chg'].sum())
#    print ('PHY-6.1- DChg_1')
#    print(data['Vol_s0_DChg'].sum())
#    print(data['Vol_s1_DChg'].sum())
#    print(data['Vol_s2_DChg'].sum())
#    print(data['Vol_s3_DChg'].sum())
#    print(data['Vol_s4_DChg'].sum())
#    print(data['Vol_s5_DChg'].sum())
#    print(data['Vol_s6_DChg'].sum())
#    print(data['Vol_s7_DChg'].sum())
#    print(data['Vol_s8_DChg'].sum())
#    print ('PHY-6.1- Rst_1')
#    print(data['Vol_s0_Rst'].sum())
#    print(data['Vol_s1_Rst'].sum())
#    print(data['Vol_s2_Rst'].sum())
#    print(data['Vol_s3_Rst'].sum())
#    print(data['Vol_s4_Rst'].sum())
#    print(data['Vol_s5_Rst'].sum())
#    print(data['Vol_s6_Rst'].sum())
#    print(data['Vol_s7_Rst'].sum())
#    print(data['Vol_s8_Rst'].sum())
print('-----------%s seconds------------' % (time.time()-start))   
    
    
