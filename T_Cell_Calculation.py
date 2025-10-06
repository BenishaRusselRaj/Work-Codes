import time
start=time.time()
import pickle
with open("D:\\New folder (2)\\New folder\\LCH_OCV\\OCV_StatesOnly_Lch\\LCH_14.1_35Deg_AllCycles_AllCycles_OCV_StatesOnly.pkl",'rb') as f:
    data = pickle.load(f)
    data['T_Cell']=data['T_amb']
    data['Stamp']=data.index+1
    data['Count']=1
    df_group=data.groupby('Step_Type')
    data['group_diff']=df_group['Stamp'].diff().apply(lambda v:float ('nan') if v==1 else v).ffill().fillna(0)
    df1=data.groupby(['Step_Type','group_diff']).agg({'Count':sum,'Stamp':'first'}).reset_index().sort_values('Stamp')
    j=0;y=data.T_amb[0]
    df1=df1.reset_index()
    for i in data.index:
        if (i==0):
            continue
        else:
            if (data.Step_Type[i]==data.Step_Type[i-1]):
                if (data.Current[i]>0):
    #                y1=4/(df1.Count[j])#phy
                    y1=8/(df1.Count[j])#lch
                    data.T_Cell[i]=data.T_Cell[i-1]+y1
                elif (data.Current[i]<0):
    #                y1=5/(df1.Count[j])#phy
                    y1=10/(df1.Count[j])#lch
                    data.T_Cell[i]=data.T_Cell[i-1]+y1
                else:
                    y1=(y-data.T_amb[0])/(df1.Count[j])
                    data.T_Cell[i]=data.T_Cell[i-1]-y1
            else:
                y=data.T_Cell[i-1]
                j=j+1
                data.T_Cell[i]=data.T_Cell[i-1]
print('--------------%s seconds--------------' % (time.time()-start))
