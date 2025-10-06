# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 09:40:08 2019

@author: IITM
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


df=pd.DataFrame()
df1=pd.read_excel("D:\\Benisha\\Phy13 new cell diff rates.xlsx",sheet_name='Charging')
y=['0.5','1','1.5','2','3','0.1']
df1['a4']=0
t=np.array(df1['Absolute Time'])
for a in range(0,6):
    Vs = np.array(df1['V_'+y[a]+'C']); V=np.asfarray(Vs,float)
    Is = np.array(df1['I_'+y[a]+'C']); I=np.asfarray(Is,float)
    #chgs = np.array(df.Charge_mAh_in_out); chg = np.asfarray(chgs,float)
    chgs = np.array(df1['Cap_'+y[a]+'C']); chg = np.asfarray(chgs,float)
    dQs = np.array(df1.a4); dQ=np.asfarray(dQs,float)
    dVs = np.array(df1.a4); dV=np.asfarray(dVs,float)
    dQts = np.array(df1.a4); dQt=np.asfarray(dQts,float)
    dVts = np.array(df1.a4); dVt=np.asfarray(dVts,float)
    dQbydVs = np.array(df1.a4); dQbydV=np.asfarray(dQbydVs,float)
    dVbydQs = np.array(df1.a4); dVbydQ=np.asfarray(dVbydQs,float)
    dQbydVts = np.array(df1.a4); dQbydVt=np.asfarray(dQbydVts,float)
    dVbydQts = np.array(df1.a4); dVbydQt=np.asfarray(dVbydQts,float)
    filtered_dQbydVs= np.array(df1.a4); filtered_dQbydV=np.asfarray(filtered_dQbydVs,float)
    j=0; k=0
    for i in range(1, len(chg)): 
        x1= V[i] - V[j] #Chg
#        x1= V[j] - V[i]  #Dchg
        x2= (t[i] - t[k])/np.timedelta64(1, 's')   
        if x1>=0.005:
            dV[i]=V[i]-V[j]
            dQ[i]= (chg[i] - chg[j])/1000
            j=j+1
            dQbydV[i] = dQ[i]/dV[i]
            dVbydQ[i] = dV[i]/dQ[i]
        if x2>=10:
            dVt[i]=V[i] - V[k]
            dQt[i]= (chg[i] - chg[k])/1000
            k=k+1
            dQbydVt[i] = dQt[i]/dVt[i]
            dVbydQt[i] = dVt[i]/dQt[i]
           
    df['chg_'+y[a]+'C'] = chg; df['V_'+y[a]+'C'] = V; df['dQ_'+y[a]+'C'] = dQ; df['dV_'+y[a]+'C'] = dV; df['dVbydQ_'+y[a]+'C'] = dVbydQ; df['dQbydV_'+y[a]+'C'] = dQbydV
    df['dQ_t_'+y[a]+'C'] = dQt; df['dV_t_'+y[a]+'C'] = dVt; df['dVbydQ_t_'+y[a]+'C'] = dVbydQt; df['dQbydV_t_'+y[a]+'C'] = dQbydVt
    df=df.replace([np.inf, -np.inf], 0)
    df=df.apply(lambda x: pd.Series(x.dropna().values))
    
    plt.plot(df1['V_'+y[a]+'C'],df1['I_'+y[a]+'C'])
    
    dQbydV_MovAvg = movingaverage(df['dQbydV_'+y[a]+'C'],100)
    b = np.zeros(99)
    
    dQbydVt_MovAvg = movingaverage(df['dQbydV_t_'+y[a]+'C'],100)
    
    dQbydV_MovAvg = pd.Series(dQbydV_MovAvg)
    b = pd.Series(b)
    
    dQbydVt_MovAvg = pd.Series(dQbydVt_MovAvg)    
    
    dQbydV_MovAvg = dQbydV_MovAvg.append(b)
    dQbydVt_MovAvg = dQbydVt_MovAvg.append(b)
    
    smooth = pd.Series.rolling(dQbydV_MovAvg, 200, center = True).mean()
    ss = np.array(smooth); sss=np.asfarray(ss,float)
    df['Smooth_dQbydV'+y[a]+'C']=sss

    smooth1 = pd.Series.rolling(dQbydVt_MovAvg, 200, center = True).mean()
    ss1 = np.array(smooth); sss1=np.asfarray(ss1,float)
    df['Smooth_dQbydV_t_'+y[a]+'C']=sss1
    
    dVbydQ_MovAvg = movingaverage(df['dVbydQ_'+y[a]+'C'],100)
    dVbydQ_MovAvg = pd.Series(dVbydQ_MovAvg) 
    dVbydQ_MovAvg = dVbydQ_MovAvg.append(b)

    dVbydQt_MovAvg = movingaverage(df['dVbydQ_t_'+y[a]+'C'],100)
    dVbydQt_MovAvg = pd.Series(dVbydQt_MovAvg) 
    dVbydQt_MovAvg = dVbydQt_MovAvg.append(b)
    
    smooth2 = pd.Series.rolling(dVbydQ_MovAvg, 200, center = True).mean()
    ss2 = np.array(smooth2); sss2=np.asfarray(ss2,float)
    
    df['Smooth_dVbydQ'+y[a]+'C']=sss2

    smooth3 = pd.Series.rolling(dVbydQt_MovAvg, 200, center = True).mean()
    ss3 = np.array(smooth3); sss3=np.asfarray(ss3,float)
    
    df['Smooth_dVbydQ_t_'+y[a]+'C']=sss3 

df.to_pickle('phy_13Ah_chg_crates_new_test.pkl') # save the sorted txt file as a pickle file
print('---------%s seconds--------' %(time.time()-start))