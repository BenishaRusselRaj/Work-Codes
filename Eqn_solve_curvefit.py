# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 15:52:23 2019

@author: IITM
"""

#Code to find the mathematical expression for degradation 
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.optimize import nnls

df=pd.read_excel("E:\\CBEEV\\LCH\\Excel_Files\\LCH_TimeData.xlsx", sheet_name='Sheet6')
print('---------------------------------------------')
df['Temp_K']=df['Temperature']+273.15 #celsius to Kelvin; still didn't make much difference
l0=[];m=[];n=[];n11=[1,0,0];n12=[0,1,0];n13=[0,0,1]
for i in df.index:
    l11=df.loc[i,'OCV_s0_Chg':'OCV_s8_Chg'].tolist();l11.extend(n11);l11.append(df.loc[i,'Temperature']);#l11.append(df.loc[i,'DOD'])
    l0.append(l11)
    l12=df.loc[i,'OCV_s0_DChg':'OCV_s8_DChg'].tolist();l12.extend(n12);l12.append(df.loc[i,'Temperature']);#l12.append(df.loc[i,'DOD'])
    m.append(l12)
    l13=df.loc[i,'OCV_s0_Rst':'OCV_s8_Rst'].tolist();l13.extend(n13);l13.append(df.loc[i,'Temperature']);#l13.append(df.loc[i,'DOD'])
    n.append(l13)
p=df['Degradation'].tolist();p.extend(p);p.extend(df['Degradation'].tolist())
M1 = np.array([(l0[0]), (l0[1]), (l0[2]), (l0[3]), (l0[4]), (m[0]), (m[1]), (m[2]), (m[3]), (m[4]), (n[0]), (n[1]), (n[2]), (n[3]), (n[4])])
M2 = np.array(p)
rough_fit= nnls((M1),(M2)) #nnls-to get positive values;these parameters will be used as initial parameters for curvefit
p0 = rough_fit[0]
##p0 = np.delete(p0,-1)
##p1=np.append(p0,[0])
p1=np.take(p0,[9,10,11,12])
p2=np.delete(p0,[9,10,11,12])
##p1=np.insert(p0,-1,0)
q1=[0,0,0,0,0,0,0,0,0,0]; n3=[0,0,0,0,0]; q2=[0,0,0,0,0]
l=df['OCV_s0_Chg'].tolist()+df['OCV_s0_DChg'].tolist()+df['OCV_s0_Rst'].tolist();l1=df['OCV_s1_Chg'].tolist()+df['OCV_s1_DChg'].tolist()+df['OCV_s1_Rst'].tolist();l2=df['OCV_s2_Chg'].tolist()+df['OCV_s2_DChg'].tolist()+df['OCV_s2_Rst'].tolist();l3=df['OCV_s3_Chg'].tolist()+df['OCV_s3_DChg'].tolist()+df['OCV_s3_Rst'].tolist()
l4=df['OCV_s4_Chg'].tolist()+df['OCV_s4_DChg'].tolist()+df['OCV_s4_Rst'].tolist();l5=df['OCV_s5_Chg'].tolist()+df['OCV_s5_DChg'].tolist()+df['OCV_s5_Rst'].tolist();l6=df['OCV_s6_Chg'].tolist()+df['OCV_s6_DChg'].tolist()+df['OCV_s6_Rst'].tolist();l7=df['OCV_s7_Chg'].tolist()+df['OCV_s7_DChg'].tolist()+df['OCV_s7_Rst'].tolist();l8=df['OCV_s8_Chg'].tolist()+df['OCV_s8_DChg'].tolist()+df['OCV_s8_Rst'].tolist()
m1=[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0]; m2=[0,0,0,0,0,1,1,1,1,1,0,0,0,0,0]; m3=[0,0,0,0,0,0,0,0,0,0,1,1,1,1,1]; n1= df['Temperature'].tolist(); n1.extend(n1); n1.extend(df['Temperature'].tolist())
n4 = df['Cycles'].tolist();n4.extend(n4); n4.extend(df['Cycles'].tolist())
n4=np.sqrt(n4)
n4=np.sqrt(n4)# double sqrt of 'no. of cycles'; better to do it here as it causes overflow in the eqn function line
a1=[]
def concats (lists):
    for i in lists:
        a1==a1.append(i)
concats ([l,l1,l2,l3,l4,l5,l6,l7,l8,m1,m2,m3,n1,n4]) # constructing the input matrix from lists

p=df['Degradation'].tolist();p.extend(p);p.extend(df['Degradation'].tolist())
x = np.array(a1)
y = np.array(p)

def test1(x,a,b,c,d,e,f,g,h,i):
    return (np.power(a*(x[0])*(x[13]))+(b*(x[1])*(x[13]))+(c*(x[2])*(x[13]))+(d*(x[3])*(x[13]))+(e*(x[4])*(x[13]))+(f*(x[5])*(x[13]))+(g*(x[6])*(x[13]))+(h*(x[7])*(x[13]))+(i*(x[8])*(x[13])),4.7)
param1, param_cov1 = curve_fit(test1,x,y,p2,bounds=[[0,0,0,0,0,0,0,0,0],[np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf]]) #test1=your own function to fit the parameters,x=input matrix,y=degradation value Y matrix;p0=initial guesses from nnls; bounds to be set as we know our values are supposed to be +ve
p3=param1
p3=np.append(p3,p1)
p3=p3.append(p3,[0])

def test(x,a,b,c,d,e,f,g,h,i,j,k,u,v,w): # define the equation as per your expectation
    return ((np.power((a*(x[0])*(x[13]))+(b*(x[1])*(x[13]))+(c*(x[2])*(x[13]))+(d*(x[3])*(x[13]))+(e*(x[4])*(x[13]))+(f*(x[5])*(x[13]))+(g*(x[6])*(x[13]))+(h*(x[7])*(x[13]))+(i*(x[8])*(x[13])),4.7))+j*x[9]+k*x[10]+u*x[11]+v*(np.exp((-1)*w/(x[12]))))
q=[]    
param, param_cov = curve_fit(test1,x,y,p3,bounds=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf]])
print(param)
for d,x1 in enumerate(x) : #this section is only to get the predicted values by substituting the parameter values we got from curvefit
      i=0
      for j,x2 in enumerate(x1):
        ans=((np.power((param[0]*(x[i][j])*(x[i+13][j]))+(param[1]*(x[i+1][j])*(x[i+13][j]))+(param[2]*(x[i+2][j])*(x[i+13][j]))+(param[3]*(x[i+3][j])*(x[i+13][j]))+(param[4]*(x[i+4][j])*(x[i+13][j]))+(param[5]*(x[i+5][j])*(x[i+13][j]))+(param[6]*(x[i+6][j])*(x[i+13][j]))+(param[7]*(x[i+7][j])*(x[i+13][j]))+(param[8]*(x[i+8][j])*(x[i+13][j])),4.7))+(param[9]*x[i+9][j])+(param[10]*x[i+10][j])+(param[11]*x[i+11][j])+param[12]*np.exp((-1)*param[13]/(x[i+12][j])))
        q.append(ans)
      break
print(q)    
print(df['Degradation']) #expected-actual values

print('---------------------------------------------')
