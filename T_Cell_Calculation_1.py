# Code to find the Cell temperature
import time
start=time.time()
import pickle
import pandas as pd
with open("D:\\New folder (2)\\New folder\\LCH_OCV\\OCV_StatesOnly_Lch\\LCH_14.1_35Deg_AllCycles_AllCycles_OCV_StatesOnly.pkl",'rb') as f:
    data = pickle.load(f)
    data['T_Cell']=''
    df1=pd.DataFrame()
    data['T_Cell']=data['T_amb']
    data['Stamp']=data.index+1
    data['Count']=1
    df_group=data.groupby('Step_Type')
    data['group_diff']=df_group['Stamp'].diff().apply(lambda v:float ('nan') if v==1 else v).ffill().fillna(0)
    df1=data.groupby(['Step_Type','group_diff'])
    df1=df1.apply(lambda _df: _df.sort_values(by=['Stamp']))
    for i,x in enumerate(df1):
        print(i)
        print (df1.iloc[i])
        print(x)
print('--------------%s seconds--------------' % (time.time()-start))
