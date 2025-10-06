import time
start=time.time()
import pickle
with open("D:\\New folder (2)\\PHY\\PHY_21.1_25Deg_AllCycles_897Cycles_processed.pkl",'rb') as f:
    data = pickle.load(f)
#    data=data[data.New_Cycle_No<=500]
    if (data['Sample_Name'].iloc[0]=='PHY_3.1'):
        d1=8
    elif (data['Sample_Name'].iloc[0]=='PHY_4.1'):
        d1=11
    elif (data['Sample_Name'].iloc[0]=='PHY_6.1'):
        d1=25
    elif (data['Sample_Name'].iloc[0]=='PHY_21.1'):
        d1=20
    elif (data['Sample_Name'].iloc[0]=='PHY_22.2'):
        d1=18
    r1=((0.35*d1)+7)*0.001
    r2=((0.125*d1)+2.5)*0.001
    r3=((0.15*d1)+3)*0.001
    data['OCV']=''
    data['Volt_1']=data['Voltage']+0.2
    data.loc[(data['Volt_1']<3.5) & (data['Current']!=0), 'OCV'] = (data['Voltage']-(data['Current']*0.001*r1))
    data.loc[(data['Volt_1']>=3.5) & (data['Volt_1']<3.9) & (data['Current']!=0), 'OCV'] = (data['Voltage']-(data['Current']*0.001*r2))
    data.loc[(data['Volt_1']>=3.9) & (data['Current']!=0), 'OCV'] = (data['Voltage']-(data['Current']*0.001*r3))

    data.loc[data['Current']==0, 'OCV'] = data['Voltage']
    print (data['OCV'].max())
    data= data.drop('Volt_1',axis=1)
    data.to_pickle('PHY_21.1_25Deg_AllCycles_897Cycles_OCV_2.pkl')
    
print('-------%s seconds---------'% (time.time()-start))
