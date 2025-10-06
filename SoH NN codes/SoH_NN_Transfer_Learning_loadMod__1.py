# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 15:14:43 2022

@author: IITM
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.layers import Dense
import keras
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import numpy as np

import time
start=time.time()

#%%
f="D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_3.1_4.1_6.1_21.1_22.1_22.2_AllCells_Combined_soh_summary.csv"
data=pd.read_csv(f)

data=data[(data['SoH_calculated']>=80) & (data['SoH_calculated']<=110)]
data=data[(data['SoC_calculated']<=130)]
# data=data[data['SoC_calculated']>=20]
data=data.fillna(0)

#%%
x=data[['Cycle_No','Vol_s0_CCCV_Chg', 'Vol_s1_CCCV_Chg', 'Vol_s2_CCCV_Chg','Vol_s3_CCCV_Chg', 'Vol_s4_CCCV_Chg', 'Vol_s5_CCCV_Chg','Vol_s6_CCCV_Chg', 'Vol_s7_CCCV_Chg', 'Vol_s8_CCCV_Chg','Vol_s0_CC_DChg', 'Vol_s1_CC_DChg', 'Vol_s2_CC_DChg', 'Vol_s3_CC_DChg','Vol_s4_CC_DChg', 'Vol_s5_CC_DChg', 'Vol_s6_CC_DChg', 'Vol_s7_CC_DChg','Vol_s8_CC_DChg','Vol_s0_Rest', 'Vol_s1_Rest', 'Vol_s2_Rest','Vol_s3_Rest', 'Vol_s4_Rest', 'Vol_s5_Rest', 'Vol_s6_Rest','Vol_s7_Rest', 'Vol_s8_Rest','SoC_calculated','T_amb','DoD']]
y=data['SoH_calculated']

#%%
def fit_model(x_train,x_test,y_train,y_test):
    model=load_model("D:\\Benisha\\SoH_NN\\Data\\LCH\\Lch_model.h5")
    
    # model.add(Dense(10,activation='elu',kernel_initializer='normal'))
    # model.add(Dense(1,activation='elu',kernel_initializer='normal'))
    opt=keras.optimizers.adam(learning_rate=0.0001) # learning_rate as low as possible to get better results
    model.compile(loss='mean_squared_error',optimizer=opt,metrics=['accuracy'])
    history=model.fit(x_train,y_train, epochs=3000, batch_size=30) # validation_data not given so as to see the efficiency of model
    
    return model, history

#%%

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33)
model, history=fit_model(x_train,x_test,y_train,y_test)
#%%
result=model.predict(x_test)

#%%
cols=['y_test','result']
map_res=pd.DataFrame(index=range(0,len(y_test)), columns=cols)


y_test=y_test.reset_index(drop=True)
map_res['y_test']=y_test
map_res['result']=result

map_res=map_res.sort_values(by='y_test', ascending=False)

#%%
map_res=map_res[(map_res['result']>0) &(map_res['result']<=120)]
kernel_size=15
kernel=np.ones(kernel_size)/kernel_size
map_res['Smooth_result']=np.convolve(map_res['result'],kernel,mode='same')

#%% Plot for visualization
plt.figure()
plt.plot(range(0,len(map_res)),map_res.y_test,label='Actual')
plt.plot(range(0,len(map_res)),map_res.result,label='Predicted')
plt.plot(range(0,len(map_res)),map_res.Smooth_result,label='Smoothened')
plt.xlabel('Index',size=14)
plt.ylabel('SoH',size=14)
plt.title('SoH Actual Vs. Predicted')
plt.legend()


print('------------------%s seconds-------------' %(time.time()-start))

#%%

# def model_build():
#     model=load_model("D:\\Benisha\\SoH_NN\\Data\\LCH\\Lch_model.h5")
    
#     opt=keras.optimizers.adam(learning_rate=0.0001) #RMSprop
#     model.compile(loss='mean_squared_error',optimizer=opt)
    
#     return(model)
# #%%

# x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33)
# estimators=KerasRegressor(build_fn=model_build,epochs=2500,batch_size=30,verbose=1)
# kfolds=KFold(n_splits=10)
# result=cross_val_score(estimators,x_train,y_train,cv=kfolds)
# print("Results: %.2f (%.2f) MSE" % (result.mean(), result.std()))

# estimators.fit(x,y)
# prediction=estimators.predict(x_test)

# #%%
# cols=['y_test','result']
# map_res=pd.DataFrame(index=range(0,len(y_test)), columns=cols)


# y_test=y_test.reset_index(drop=True)
# map_res['y_test']=y_test
# map_res['prediction']=prediction

# map_res=map_res.sort_values(by='y_test', ascending=False)

# #%% Plot for visualization
# plt.figure()
# plt.plot(range(0,len(y_test)),map_res.y_test,label='Actual')
# plt.plot(range(0,len(y_test)),map_res.prediction,label='Predicted')
# plt.xlabel('Index',size=14)
# plt.ylabel('SoH',size=14)
# plt.title('SoH Actual Vs. Predicted')
# plt.legend()


# print('------------------%s seconds-------------' %(time.time()-start))