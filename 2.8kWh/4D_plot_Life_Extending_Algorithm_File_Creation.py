# -*- coding: utf-8 -*-
"""
Created on Tue May 16 09:52:54 2023

@author: IITM
"""

'''
This code creates a csv file representing the life extending algorithm and plots a 4D plot from that data
'''

#%% Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.plot as plt

#%% Defining the column names
cols=['Voltage_1_2','Temperature_1_2','SoH_1_2','Current_1_2','Voltage_3_4','Temperature_3_4','SoH_3_4','Current_3_4','Voltage_5_6','Temperature_5_6','SoH_5_6','Current_5_6']
p_index=['1_2','3_4','5_6']

#%% Setting limits/thresholds for each parameter
V=[0,2.5,3,3.5,4,4.14]  # Voltage "buckets"-> 0 to 2.5, 2.5 to 3.5, 3.5 to 4 and 4 to 4.14
T=[15,35,45]    # Temperature "buckets"-> 15 to 35, 35 to 45
S=[80,90,100]   # SoC limits-> 80 to 90, 90 to 100
C=[2.24,5.6,11.2,16.8]  # Current values--constant
v_list=[]
t_list=[]
s_list=[]

v_split_list=[]
t_set=len(T)-1
s_set=len(S)-1
#%% Interpolating voltage values
for i in range(len(V)):
    try:
        v_series=np.arange(V[i],V[i+1],1)   # numpy's arange function gives values between the specified upper and lower limits, in the interval specified
        v_split_list.append(v_series)
        v_list.extend(v_series)
    except IndexError:
        continue

#%% Interpolating Temperature values
for i in range(len(T)):
    try:
        x=((T[i+1]-T[i])/len(v_list))
        t_series=np.arange(T[i],T[i+1],x)
        t_series=np.around(t_series,2)
        t_list.extend(t_series)
    except IndexError:
        continue

#%% Interpolating SoC values 
for i in range(len(S)):
    try:
        y=((S[i+1]-S[i])/len(t_list))
        s_series=np.arange(S[i],S[i+1],y)
        s_series=np.around(s_series,2)
        s_list.extend(s_series)
    except IndexError:
        continue
#%% Setting a dataframe

df=pd.DataFrame(columns=cols,index=range(len(v_list)*t_set*s_set))
v_final=[]
t_final=[]

for i in range(t_set*s_set):
    v_final.extend(v_list)
for i in range(s_set):
    t_final.extend(t_list)
    

for i in range(len(p_index)):
    df['Voltage_'+p_index[i]]=v_final
    df['Temperature_'+p_index[i]]=t_final
    df['SoH_'+p_index[i]]=s_list

#%% Setting current values for each combination of voltage,temperature and SoC values

for i in p_index:
    if i=='1_2':
        df['Current_'+i]=np.where((df['Voltage_'+i]<=3),2.24,df['Current_'+i])
        df['Current_'+i]=np.where(((df['Voltage_'+i]>3) & (df['Voltage_'+i]<=4.2)),16.8,df['Current_'+i])
    elif i=='3_4':
        df['Current_'+i]=np.where((df['Voltage_'+i]<=2.5),0.56,df['Current_'+i])
        df['Current_'+i]=np.where(((df['Voltage_'+i]>2.5) & (df['Voltage_'+i]<=3)),2.24,df['Current_'+i])
        df['Current_'+i]=np.where(((df['Voltage_'+i]>3) & (df['Voltage_'+i]<=4.2) & (df['Temperature_'+i]<=35)),11.2,df['Current_'+i])
        df['Current_'+i]=np.where(((df['Voltage_'+i]>3) & (df['Voltage_'+i]<=3.5) & (df['Temperature_'+i]>35)),5.6,df['Current_'+i])
        df['Current_'+i]=np.where(((df['Voltage_'+i]>3.5) & (df['Voltage_'+i]<=4.2) & (df['Temperature_'+i]>35)),8.4,df['Current_'+i])
    elif i=='5_6':
        df['Current_'+i]=np.where((df['Voltage_'+i]<=2.5),0.56,df['Current_'+i])
        df['Current_'+i]=np.where(((df['Voltage_'+i]>2.5) & (df['Voltage_'+i]<=3)),2.24,df['Current_'+i])
        df['Current_'+i]=np.where(((df['Voltage_'+i]>3) & (df['Voltage_'+i]<=3.5) & (df['Temperature_'+i]<=35)),11.2,df['Current_'+i])
        df['Current_'+i]=np.where(((df['Voltage_'+i]>3) & (df['Voltage_'+i]<=3.5) & (df['Temperature_'+i]>35)),5.6,df['Current_'+i])
        df['Current_'+i]=np.where(((df['Voltage_'+i]>3.5) & (df['Voltage_'+i]<=4) & (df['Temperature_'+i]<=35)),16.8,df['Current_'+i])
        df['Current_'+i]=np.where(((df['Voltage_'+i]>3.5) & (df['Voltage_'+i]<=4) & (df['Temperature_'+i]>35)),11.2,df['Current_'+i])
        df['Current_'+i]=np.where(((df['Voltage_'+i]>4) & (df['Voltage_'+i]<=4.2)),11.2,df['Current_'+i])

#%% Save file
df=df.sort_values(by='Voltage_1_2')
df.to_csv("D:\\Benisha\\2.8kWh_4D_plot_data.csv",index=False)

#%% Plotting a 4D graph
x_label='Temperature'
y_label='SoH'
z_label='Voltage'
c_label='Current'
cmap_name='winter'


for i in p_index:
    x=df[x_label+'_'+i]
    y=df[y_label+'_'+i]
    z=df[z_label+'_'+i]
    c1=df['Current_'+i]
    
    X,Y,Z,C=np.meshgrid(x,y,z,c1) #this creates a matrix like values for the fourth variable i.e., current
    
    fig=plt.figure()
    ax=plt.subplot(111,projection='3d')
    img=ax.scatter(X,Y,Z,c=C,cmap='winter')
    ax.set_xlabel(x_label,fontweight='bold')
    ax.set_ylabel(y_label,fontweight='bold')
    ax.set_zlabel(z_label,fontweight='bold')
    cbar=plt.colorbar(img)
    cbar.ax.get_yaxis().labelpad=17
    cbar.ax.set_ylabel(c_label,rotation=270,fontweight='bold')
    plt.title('Packs_'+i,fontweight='bold',size=13)
    plt.show()
    
    del X,Y,Z,C #to clear space for the next iteration

