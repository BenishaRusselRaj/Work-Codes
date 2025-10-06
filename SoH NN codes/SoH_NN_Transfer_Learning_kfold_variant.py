# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:55:02 2022

@author: IITM
"""



import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score  #,KFold
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import joblib

import time
start=time.time()

#%%

# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\SoH_Calculated_summary_files_delsoc_smooth\\LCH_AllCells_Combined_SoH_Calculated_summary_files_delsoc_smooth.csv"
f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\Raw files\\SoH_Calculated_summary_files\\SoH_smooth\\LCH_AllCycles_Timestates_added_soh_summary_smooth.csv"

cell_no='LCH_AllCells'
model_info='elu_1layer'

# f="D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_3.1_4.1_6.1_21.1_22.1_22.2_AllCells_Combined_soh_summary.csv"
data=pd.read_csv(f) 

#%%
data=data[(data['SoH_calculated']>=80) & (data['SoH_calculated']<=110)] # to clean the data
data=data[(data['SoC_calculated']<=140)] #(data['SoC_calculated']>=35) & 

data=data.fillna(0)

#%%
x_array=['Cycle_No','Vol_s0_CCCV_Chg', 'Vol_s1_CCCV_Chg', 'Vol_s2_CCCV_Chg','Vol_s3_CCCV_Chg', 'Vol_s4_CCCV_Chg', 'Vol_s5_CCCV_Chg','Vol_s6_CCCV_Chg', 'Vol_s7_CCCV_Chg', 'Vol_s8_CCCV_Chg','Vol_s0_CC_DChg', 'Vol_s1_CC_DChg', 'Vol_s2_CC_DChg', 'Vol_s3_CC_DChg','Vol_s4_CC_DChg', 'Vol_s5_CC_DChg', 'Vol_s6_CC_DChg', 'Vol_s7_CC_DChg','Vol_s8_CC_DChg','Vol_s0_Rest', 'Vol_s1_Rest', 'Vol_s2_Rest','Vol_s3_Rest', 'Vol_s4_Rest', 'Vol_s5_Rest', 'Vol_s6_Rest','Vol_s7_Rest', 'Vol_s8_Rest','T_amb','DoD','mean_SoC', 'Temp_s0_CCCV_Chg', 'Temp_s1_CCCV_Chg',
        'Temp_s2_CCCV_Chg', 'Temp_s3_CCCV_Chg', 'Temp_s4_CCCV_Chg','Temp_s5_CCCV_Chg', 'Temp_s6_CCCV_Chg', 'Temp_s0_CC_DChg','Temp_s1_CC_DChg', 'Temp_s2_CC_DChg', 'Temp_s3_CC_DChg',
        'Temp_s4_CC_DChg', 'Temp_s5_CC_DChg', 'Temp_s6_CC_DChg', 'Temp_s0_Rest','Temp_s1_Rest', 'Temp_s2_Rest', 'Temp_s3_Rest', 'Temp_s4_Rest', 'Temp_s5_Rest', 'Temp_s6_Rest']

x=data[x_array]
y=data['SoH_calculated']

#%%
def model_build():
    model=Sequential()
    
    model.add(Dense(10,input_dim=52,activation='elu',kernel_initializer='normal')) #input_dim=30, 31
    # model.add(Dense(10,activation='relu',kernel_initializer='normal'))
    # model.add(Dense(10,activation='elu',kernel_initializer='normal'))
    model.add(Dense(1,kernel_initializer='normal')) 
    opt=keras.optimizers.adam(learning_rate=0.0001) 
    model.compile(loss='mean_squared_error',optimizer=opt)
    return (model)
#   Since the data is used for training the model, the validation set is also given;
#   So, the Actual Vs. Predicted plot is much accurate; 
#   Actual validation is only done when we try the model on different data-done in the Soh_NN_Transfer_loadMod code
  
#%% Splits data to training and test sets   
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33)
#%% Calling model function
# model, history=model_build(x_train,x_test,y_train,y_test)
estimators=KerasRegressor(build_fn=model_build,epochs=1500,batch_size=25,verbose=1)
score=cross_val_score(estimators,x_train,y_train,cv=10)

estimators.fit(x_train,y_train)
result=estimators.predict(x_test)
#%% predicting test data using model to verify

result=estimators.predict(x_test)

#%%
cols=['y_test','result']
map_res=pd.DataFrame(index=range(0,len(y_test)), columns=cols)


y_test=y_test.reset_index(drop=True)
map_res['y_test']=y_test
map_res['result']=result

#%%
map_res=map_res.sort_values(by='y_test', ascending=False)
map_res['Smooth_result']=map_res['result'].rolling(15).mean()

#%% Plot for visualization
plt.figure()
plt.plot(range(0,len(map_res)),map_res.y_test,label='Actual')
plt.plot(range(0,len(map_res)),map_res.result,label='Predicted')
# plt.plot(range(0,len(result)),map_res.Smooth_result,label='Smoothened')
plt.xlabel('Index',size=14)
plt.ylabel('SoH',size=14)
plt.title('SoH Actual Vs. Predicted')
plt.legend()

#%%
mse=mean_squared_error(map_res.y_test,map_res.result)
rmse=mean_squared_error(map_res.y_test,map_res.result, squared=False)
mae=mean_absolute_error(map_res.y_test,map_res.result)

#%%
map_res=map_res.dropna(subset=['Smooth_result'])
mse_smooth=mean_squared_error(map_res.y_test,map_res.Smooth_result)
rmse_smooth=mean_squared_error(map_res.y_test,map_res.Smooth_result, squared=False)
mae_smooth=mean_absolute_error(map_res.y_test,map_res.Smooth_result)

#%%

f2=open(f.rsplit('\\',1)[0]+"\\"+cell_no+"_Error_metrics_soh_smooth_KerasRegressor_"+model_info+".csv","w")
# print('Features and their importances (in Percentage):', file=f2)
# for i,n in enumerate(importance):
#     print('Feature: %s; Importance: %f' %(x_array[i],n), file=f2)  ##n*100; for percentage
print('mse: %s' %(mse), file=f2)
print('mae: %s' %(mae), file=f2)
print('rmse: %s' %(rmse), file=f2)
print('mse_smooth: %s' %(mse_smooth), file=f2)
print('mae_smooth: %s' %(mae_smooth), file=f2)
print('rmse_smooth: %s' %(rmse_smooth), file=f2)
print('rmse_smooth: %s' %(rmse_smooth), file=f2)
# print('SoH from Capacity Test:%s' %(SoH_test), file=f2)
# print('End SoH predicted: %s' %(map_res['result'].iloc[-1]), file=f2)
f2.close()
#%% Saving Model; you have to install h5py beorehand: "pip install h5py" in cmd
# model.save(f.rsplit('\\',2)[0]+'\\Lch_model.h5')
joblib.dump(estimators,f.rsplit('\\',1)[0]+'\\Lch_kerasregressor_model_temptimestates_'+model_info+'.joblib')


print('------------------%s seconds-------------' %(time.time()-start))