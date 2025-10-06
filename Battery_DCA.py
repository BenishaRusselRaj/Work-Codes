# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:05:02 2019

@author: IITM
"""
"""
Code to perform DCA on Battery packs; 00005.2019041609174403.004 has data

"""

import time
start=time.time()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def movingaverage(values,window):
    weights = np.repeat(1.0,window)/window
    smas = np.convolve(values,weights,'valid')
    return smas

df=pd.read_csv("D:\\Benisha\\Battery DCA\\charging_data_mohali_INEXC0010202K2303809_new.tsv",header=0, sep='\t',index_col=False,error_bad_lines=False)
df['C_Max']=df[['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12']].max(axis=1)
df['a4']=0
df1=pd.DataFrame()
df = df.astype(str)
print(df.dtypes)
df['time']=pd.to_datetime(df['time'])

grouped=df.groupby('session', sort=False)
result = [g[1] for g in list(grouped)]

#%%
for i in range (0,len(result)):
    
    result[i][['C_Max','current']]=result[i][['C_Max','current']].astype(float)
#    result[i]=result[i][(result[i].C_Max>0)] # to remove step start/end rows
    
    t=np.array(result[i]['time'])
    Vs = np.array(result[i].C_Max); V=np.asfarray(Vs,float)
    Is = np.array(result[i].current); I=np.asfarray(Is,float)
    #chgs = np.array(df.Charge_mAh_in_out); chg = np.asfarray(chgs,float)
#    chgs = np.array(result[i].energy); chg = np.asfarray(chgs,float)
    dQts = np.array(result[i].a4); dQt=np.asfarray(dQts,float)
    dVts = np.array(result[i].a4); dVt=np.asfarray(dVts,float)
    dQs = np.array(result[i].a4); dQ=np.asfarray(dQs,float)
    dVs = np.array(result[i].a4); dV=np.asfarray(dVs,float)
    dEngys = np.array(result[i].a4); dEngy=np.asfarray(dQts,float)
    dQbydVs = np.array(result[i].a4); dQbydV=np.asfarray(dQbydVs,float)
    dVbydQs = np.array(result[i].a4); dVbydQ=np.asfarray(dVbydQs,float)
    dQbydVts = np.array(result[i].a4); dQbydVt=np.asfarray(dQbydVts,float)
    dVbydQts = np.array(result[i].a4); dVbydQt=np.asfarray(dVbydQts,float)
    filtered_dQbydVs = np.array(result[i].a4); filtered_dQbydV=np.asfarray(filtered_dQbydVs,float)
    l=1
    
#%%
    for k in range(2, len(V)): 
    #    x1= V[i] - V[j]
#        x1= V[j] - V[k] #Dchg
        x2= (t[k] - t[l])/np.timedelta64(1, 's')

#        if x1>0.5:
#            dV[k]=V[k]-V[j]
#            dQ[k]= (chg[k] - chg[j])/1000
#    #        dQ[k]= (chg[j] - chg[k])/1000 #Dchg
#            j=j+1
#            dQbydV[k] = dQ[k]/dV[k]
#            dVbydQ[k] = dV[k]/dQ[k]
        if x2>=10:
            dVt[k]= V[k] - V[l]
            dQt[k]= (I[l] - I[k])*x2
            dEngy[k]= dVt[k]*dQt[k]*x2
            l=l+1
            dQbydVt[k] = dQt[k]/dVt[k]
            dVbydQt[k] = dVt[k]/dQt[k]
    
    
    plt.plot(result[i].C_Max,result[i].current)       
#    result[i]['chg'] = chg; result[i]['V'] = V; result[i]['dQ'] = dQ; result[i]['dV'] = dV; result[i]['dVbydQ'] = dVbydQ; result[i]['dQbydV'] = dQbydV
#%%
    result[i]['dQ_t_'] = dQt; result[i]['dV_t_'] = dVt; result[i]['dVbydQ_t_'] = dVbydQt; result[i]['dQbydV_t_'] = dQbydVt
    result[i]['V'] = V; result[i]['dEngy_t_']=dEngy
    result[i]=result[i].replace([np.inf, -np.inf], 0)
    result[i]=result[i].apply(lambda x: pd.Series(x.dropna().values))
#%%   
    try:
        dQbydV_MovAvg = movingaverage(result[i]['dQbydV_t_'],50)
        a = np.zeros(49)
        
        dQbydV_MovAvg = pd.Series(dQbydV_MovAvg)
        a = pd.Series(a)
        
        dQbydV_MovAvg = dQbydV_MovAvg.append(a)
        
        smooth = pd.Series.rolling(dQbydV_MovAvg, 50, center = True).mean()
        ss = np.array(smooth); sss=np.asfarray(ss,float)
        
        result[i]['Smooth_dQbydV_t']= sss
        
        dVbydQ_MovAvg = movingaverage(result[i]['dVbydQ_t_'],50)
        a = np.zeros(49)
        
        dVbydQ_MovAvg = pd.Series(dVbydQ_MovAvg)
        a = pd.Series(a)
        
        dVbydQ_MovAvg = dVbydQ_MovAvg.append(a)
        
        smooth1 = pd.Series.rolling(dVbydQ_MovAvg, 50, center = True).mean()
        ss1 = np.array(smooth1); sss1=np.asfarray(ss1,float)
        
        result[i]['Smooth_dVbydQ_t']= sss1
   
    except ValueError:
        
        result[i]['Smooth_dQbydV_t']= result[i]['dQbydV_t_']
        
        result[i]['Smooth_dVbydQ_t']= result[i]['dVbydQ_t_'] 
     
    x=str(i)
    result[i]['Engy_t_cum']=result[i]['dEngy_t_'].sum()
    df1=pd.concat([df1,result[i]])
    result[i].to_pickle('ChargingData_mohali_new_'+x+'_test_11.pkl')

#%%
df1.reset_index()
df1.to_pickle('ChargingData_mohali_new_test_11.pkl') # save the sorted txt file as a pickle file
print('--------%s seconds--------' %(time.time()-start))