# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 16:18:07 2020

@author: IITM
"""

import pandas as pd
df1=pd.read_csv("D:\\Benisha\\Battery DCA\\Mohali Monthly data\\OTD\\Mohali data chg_dis_rest states till aug 2018 except july.csv") # Sessions summary
df2=pd.read_csv("D:\\Benisha\\Battery DCA\\Mohali Monthly data\\OTD\\mohali_charging_session_onetime_all_bin.tsv", sep='\t') # OTD

df2.rename(columns={'bin':'bin_1','session':'session_1'}, inplace=True)
cols2=list(df2)
df1=df1.sort_values(by='start_Time')
data=pd.DataFrame()
grouped=df1.groupby('Session_Type')
df=[g[1] for g in list(grouped)]
for i in range(0, len(df)):
    if ((df[i]['Session_Type']).all()=='Chg'):
        df[i]=df[i].merge(df2,left_on='session',right_on='session_1',how='left')   
    else:
        for newcol in cols2:
            df[i][newcol]=''
    data=pd.concat([data,df[i]])
data=data.sort_values(by='start_Time')
data=data.reset_index(drop=True)