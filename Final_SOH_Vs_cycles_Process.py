# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:27:15 2020

@author: IITM
"""

import time
start=time.time()
import pandas as pd

#%%
file_path="D:\\Benisha\\Battery DCA\\Zomato\\zomato_driving_charging_data\\Zomato_Final_Cycle_Nos_and SOH.csv"
df=pd.read_csv(file_path)
data=pd.DataFrame(index=df.index, columns=df.columns); k=0
#%%
grouped=df.groupby('bin')
result=[g[1] for g in list(grouped)]

#%%
for i in range(0,len(result)):
    data.iloc[k]=result[i].iloc[-1]
    data.iloc[k]['SOH_otd']=result[i]['SOH_otd'][-5:].mean()
    k=k+1
data=data.dropna(subset=['bin']) 
data=data.drop(['Unnamed: 0'],axis=1)
fin_path='\\'.join(file_path.split('\\')[0:-1])
data.to_csv(fin_path+'\\Zomato_Cycle_Nos_and_SOH_bins.csv')   
print('---------%s seconds-----------' % (time.time()-start))