# Code to find the Cell(arbitrary) temperature
# Optimization required; Time consuming
import time
start=time.time()
import pickle
import pandas as pd
with open("D:\\New folder (2)\\New folder\\LCH_OCV\\OCV_StatesOnly_Lch\\LCH_17.1_25Deg_AllCycles_AllCycles_OCV_StatesOnly.pkl",'rb') as f:
    data = pickle.load(f)
    data['T_Cell']=''
    df1=pd.DataFrame()
    y=data.T_amb[0]
    l=[]
    data['Step_Type_s']=data['Step_Type'].shift(-1)
    def calc_Temp(df):
        global df1,y1,y
        if(((df.Step_Type=='CCCV_Chg').all()) and ((df.Current>0).any())):
##            y1=4/(len(df.index))      #phy#Finds fraction of temperature added at each step
            y1=8/(len(df.index)-1)      #lch    
            df['T_Cell']=y+(df.index*y1)#T_Cell increases at each step  
        elif (((df.Step_Type=='CC_DChg').all()) and ((df.Current<0).any())):
##            y1=5/(len(df.index))  #phy
            y1=10/(len(df.index)-1) #lch
            df['T_Cell']=y+(df.index*y1) 
        elif (((df.Step_Type=='Rest').all()) and ((df.Current==0).any())):
            y1=(y-data.T_amb.iloc[0])/(len(df.index)-1) #Rest-Temperature decreases;so the previous step T_Cell is taken and subtracted with T_amb
            df['T_Cell']=y-(df.index*y1)
        df1=df1.append(df)
        df1=df1.reset_index(drop=True)
        y=df1.T_Cell.iloc[-2]
        df=df.drop(df.index, inplace=True)
    for i in data.index:
        if (data.Step_Type[i]==data.Step_Type_s[i]):
            l.append(data.iloc[i])                  #Set of data having the same step_type are taken;Step_type is repetitive
        else:
            df=pd.DataFrame(l,columns=data.columns) #Same step_type,consecutive data taken and made into separate dataframe 
            df=df.reset_index()
            l.clear()
            calc_Temp(df)
print('--------------%s seconds--------------' % (time.time()-start))
