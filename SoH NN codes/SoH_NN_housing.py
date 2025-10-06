# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 10:40:06 2022

@author: IITM
"""

import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

import time
start=time.time()

# data=pd.read_csv("D:\\Benisha\\SoH_NN\\Data\\Housing_test.txt",delim_whitespace=True,header=None)
f="D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_SoH_Calculated_summary_files\\Combined_Summary_14,15,16_35deg.csv"
data=pd.read_csv(f) #)

# data=data[data['Step_Type']=='CC_DChg']
# data=data.dropna(subset=['SoH_calculated'])
# data=data[(data['SoH_calculated']>=50)] # and (data['SoH_calculated']<=100)
data=data.fillna(0)
# data['RTC']=pd.to_datetime(data['RTC'],errors='coerce',format='%Y-%m-%d %H:%M:%S')
# data=data.sort_values(by=['RTC'],ascending=True)
# x=data.iloc[:,0:13]
# y=data.iloc[:,13]
#%%
x=data[['Vol_s0_CCCV_Chg', 'Vol_s1_CCCV_Chg', 'Vol_s2_CCCV_Chg','Vol_s3_CCCV_Chg', 'Vol_s4_CCCV_Chg', 'Vol_s5_CCCV_Chg','Vol_s6_CCCV_Chg', 'Vol_s7_CCCV_Chg', 'Vol_s8_CCCV_Chg','Vol_s0_CC_DChg', 'Vol_s1_CC_DChg', 'Vol_s2_CC_DChg', 'Vol_s3_CC_DChg','Vol_s4_CC_DChg', 'Vol_s5_CC_DChg', 'Vol_s6_CC_DChg', 'Vol_s7_CC_DChg','Vol_s8_CC_DChg','Vol_s0_Rest', 'Vol_s1_Rest', 'Vol_s2_Rest','Vol_s3_Rest', 'Vol_s4_Rest', 'Vol_s5_Rest', 'Vol_s6_Rest','Vol_s7_Rest', 'Vol_s8_Rest','SoC_calculated','T_amb']]
# x=data[['Vol_s0_CC_DChg','Vol_s1_CC_DChg', 'Vol_s2_CC_DChg', 'Vol_s3_CC_DChg','Vol_s4_CC_DChg', 'Vol_s5_CC_DChg', 'Vol_s6_CC_DChg', 'Vol_s7_CC_DChg','Vol_s8_CC_DChg','SoC_calculated','T_amb']]
y=data['SoH_calculated']

#%%
def model_build():
    model=Sequential()
    
    model.add(Dense(10,input_dim=29,activation='relu',kernel_initializer='normal'))
    # model.add(Dense(10,activation='relu',kernel_initializer='normal'))
    model.add(Dense(1,kernel_initializer='normal')) # ,activation='softmax'
    opt=keras.optimizers.adam(learning_rate=0.0001) #RMSprop
    model.compile(loss='mean_squared_error',optimizer=opt)
    
    return(model)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33)
estimators=KerasRegressor(build_fn=model_build,epochs=150,batch_size=20,verbose=1)
kfolds=KFold(n_splits=10)
result=cross_val_score(estimators,x,y,cv=kfolds)
# estimators.fit(x_train,y_train) #,learning_rate=0.001
# result=estimators.predict(x_test)
# error=(abs(y_test-result)/y_test)*100
plt.plot(range(0,len(y_test)),y_test,label='Actual')
plt.plot(range(0,len(result)),result,label='Predicted')
plt.legend()

#%% Saving Model
# estimators.save(f.rsplit('\\',2)[0]+'\\Lch_model.h5')

# plt.figure()
# plt.plot(range(0,len(result)),error)
# print(accuracy_score(result,y_test))
# print(result.std())

print('------------------%s seconds-------------' %(time.time()-start))