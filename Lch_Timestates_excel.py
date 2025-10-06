# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 17:55:48 2019

@author: IITM
"""

import pandas as pd
df1=pd.read_pickle('\\path\\14.1')
df2=pd.read_pickle('\\path\\14.2')
df=pd.concat([df1,df2])
cols=['Cell','OCV_s0_Chg','OCV_s1_Chg','OCV_s2_Chg','OCV_s3_Chg','OCV_s4_Chg','OCV_s5_Chg','OCV_s6_Chg','OCV_s7_Chg','OCV_s0_DChg','OCV_s1_DChg','OCV_s2_DChg','OCV_s3_DChg','OCV_s4_DChg','OCV_s5_DChg','OCV_s6_DChg','OCV_s7_DChg','OCV_s8_DChg','OCV_s0_Rst','OCV_s1_Rst','OCV_s2_Rst','OCV_s3_Rst','OCV_s4_Rst','OCV_s5_Rst','OCV_s6_Rst','OCV_s7_Rst','OCV_s8_Rst','Temperature','Degradation']
data=pd.DataFrame(columns=cols, index=df1.index)
l=['0','1','2','3','4','5','6','7','8']
k=0
for i in range (0,len(l)):
    data['OCV_s'+l[i]+'_Chg'].iloc[k]