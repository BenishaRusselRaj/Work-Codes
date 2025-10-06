# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 11:01:49 2022

@author: IITM
"""
'''
Save model is commented

'''


import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import numpy as np

import time
start=time.time()

#%%
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_14.1_15.1_16.1_17.1_18.1_Combined_soh_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_3.1_4.1_6.1_21.1_22.1_22.2_AllCells_Combined_soh_summary.csv"
f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\SoH_Calculated_summary_files_delsoc_smooth\\LCH_AllCells_Combined_SoH_Calculated_summary_files_delsoc_smooth.csv"
data=pd.read_csv(f) 

#%%
data=data[(data['SoH_calculated']>=80) & (data['SoH_calculated']<=110)] # to clean the data
data=data[(data['SoC_calculated']<=140)] #(data['SoC_calculated']>=35) & 

data=data.fillna(0)

#%%
x=data[['Cycle_No','Vol_s0_CCCV_Chg', 'Vol_s1_CCCV_Chg', 'Vol_s2_CCCV_Chg','Vol_s3_CCCV_Chg', 'Vol_s4_CCCV_Chg', 'Vol_s5_CCCV_Chg','Vol_s6_CCCV_Chg', 'Vol_s7_CCCV_Chg', 'Vol_s8_CCCV_Chg','Vol_s0_CC_DChg', 'Vol_s1_CC_DChg', 'Vol_s2_CC_DChg', 'Vol_s3_CC_DChg','Vol_s4_CC_DChg', 'Vol_s5_CC_DChg', 'Vol_s6_CC_DChg', 'Vol_s7_CC_DChg','Vol_s8_CC_DChg','Vol_s0_Rest', 'Vol_s1_Rest', 'Vol_s2_Rest','Vol_s3_Rest', 'Vol_s4_Rest', 'Vol_s5_Rest', 'Vol_s6_Rest','Vol_s7_Rest', 'Vol_s8_Rest','SoC_calculated','T_amb','DoD']] # ,'SoC_calculated'
y=data['SoH_calculated']

#%%
def model_build(x_train,x_test,y_train,y_test):
    model=Sequential()
    
    model.add(Dense(10,input_dim=31,activation='relu',kernel_initializer='normal'))
    model.add(Dense(10,activation='relu',kernel_initializer='normal'))
    model.add(Dense(10,activation='relu',kernel_initializer='normal'))
    model.add(Dense(1,kernel_initializer='normal')) 
    opt=keras.optimizers.adam(learning_rate=0.0001) 
    model.compile(loss='mean_squared_error',optimizer=opt)
    history=model.fit(x_train,y_train, epochs=3000, batch_size=30) #,validation_data=(x_test,y_test)
#   Since the data is used for training the model, the validation set is also given;
#   So, the Actual Vs. Predicted plot is much accurate; 
#   Actual validation is only done when we try the model on different data-done in the Soh_NN_Transfer_loadMod code
    return model, history
  
#%% Splits data to training and test sets   
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33)
#%% Calling model function
model, history=model_build(x_train,x_test,y_train,y_test)

#%% predicting test data using model to verify

result=model.predict(x_test)

#%%
cols=['y_test','result']
map_res=pd.DataFrame(index=range(0,len(y_test)), columns=cols)


y_test=y_test.reset_index(drop=True)
map_res['y_test']=y_test
map_res['result']=result

#%%
map_res=map_res.sort_values(by='y_test', ascending=False)
map_res=map_res[(map_res['result']>0) & (map_res['result']<=120)]

map_res['Smooth_result']=map_res['result'].rolling(10).mean()

#%% Plot for visualization
plt.figure()
plt.plot(range(0,len(map_res)),map_res.y_test,label='Actual')
plt.plot(range(0,len(map_res)),map_res.result,label='Predicted')
# plt.plot(range(0,len(map_res)),map_res.Smooth_result,label='Smoothened')
plt.xlabel('Index',size=14)
plt.ylabel('SoH',size=14)
plt.title('SoH Actual Vs. Predicted')
plt.legend()

#%%
mse=mean_squared_error(map_res.y_test,map_res.result)
rmse=mean_squared_error(map_res.y_test,map_res.result,squared=False)
mae=mean_absolute_error(map_res.y_test,map_res.result)

#%%
map_res=map_res.dropna(subset=['Smooth_result'])
mse_smooth=mean_squared_error(map_res.y_test,map_res.Smooth_result)
rmse_smooth=mean_squared_error(map_res.y_test,map_res.Smooth_result, squared=False)
mae_smooth=mean_absolute_error(map_res.y_test,map_res.Smooth_result)

#%% Saving Model; you have to install h5py beorehand: "pip install h5py" in cmd
model.save(f.rsplit('\\',2)[0]+'\\Lch_model_relu_smooth_data.h5')


print('------------------%s seconds-------------' %(time.time()-start))