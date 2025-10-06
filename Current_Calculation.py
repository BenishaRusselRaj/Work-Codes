# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 09:01:10 2020

@author: IITM

To calculate current in files without current
"""
#def calculate_current(x):
import time
start=time.time()
import pandas as pd
import numpy as np

data1 = pd.read_csv("D:\\Benisha\\Battery DCA\\Mohali Monthly data\\2018_M8_Aug_charging_temperature_voltage_sortedCombined_timestates.csv",header=0, sep=',',index_col=False,error_bad_lines=False)   
C=26
data1['V_Max']=data1.loc[:,'CV0':'CV13'].max(axis=1)
data1['time']=pd.to_datetime(data1['time'], errors='coerce') # ,format= "%d/%m/%Y %H:%M:%S"
data1=data1.sort_values(by='time',ascending=True)
data1['current']=''
df=pd.DataFrame()
data=pd.DataFrame()
data1=data1[data1.V_Max<4.5]
g1=data1.groupby('session',sort=False)
dff=[f[1] for f in list(g1)]
for i in range (0,len(dff)):
    dff[i]['Flag1']=(abs(dff[i]['V_Max']-dff[i]['V_Max'].shift())>0.15).cumsum()
    data=pd.concat([data,dff[i]])
data=data.sort_values(by='time',ascending=True)
grouped=data.groupby(['session','Flag1'], sort=False)
df1=[g[1] for g in list(grouped)]
for i in range (0, len(df1)):
    df1[i]=df1[i].reset_index(drop=True)
    df1[i]['Flag']= ((df1[i]['V_Max']>4.05))   # & ((df1[i]['V_Max'].shift()-df1[i]['V_Max'])<0.008)
    a=df1[i]['Flag'][df1[i]['Flag']==True].first_valid_index()
    try:
        t_hr=(df1[i]['time'].loc[a]-df1[i]['time'].iloc[0])/np.timedelta64(1,'h')
        if (t_hr<=1.5):
            crate=1*C
    
        elif (t_hr>1.5 and t_hr<=2.5):
            crate=0.5*C
    
        elif (t_hr>2.5 and t_hr<=4.5):
            crate=0.25*C
        df1[i]['current']=df1[i].groupby((((df1[i]['Flag']) != (df1[i]['Flag'].shift())) & ((df1[i]['Flag'].shift(-3)) != (df1[i]['Flag'].shift(3)))).cumsum()).cumcount()+1   #   
        df1[i].loc[(df1[i]['Flag']==False), 'current'] = crate
        div=((crate)-(0.1*C))/(df1[i]['Flag'].sum())
        df1[i].loc[(df1[i]['Flag']==True), 'current']= (crate - (df1[i]['current']*div))
        df1[i]['current']=df1[i]['current'].where(df1[i]['current']>0, df1[i]['current'].shift())
    except KeyError:
        pass
    df=pd.concat([df,df1[i]])
df=df.drop(['Flag1','Flag'], axis=1)
#x=x.split('.')
#df.to_csv(x[0]+'_current_calculated.csv')
#return(x[0]+'_current_calculated.csv')
print('-----------%s seconds----------' % (time.time()-start))