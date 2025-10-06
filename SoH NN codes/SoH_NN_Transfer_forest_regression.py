# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 10:46:09 2022

@author: IITM
"""



import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import joblib #to save a scikit model

import time
start=time.time()

#%% Path to the file containing the combined summary file (all the cells) 
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_SoH_Calculated_summary_files\\LCH_14.1_15.1_16.1_17.1_18.1_19.1_Combined_soh_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_3.1_4.1_6.1_21.1_22.1_22.2_AllCells_Combined_soh_summary.csv"

# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\25deg\\modified_arranged\\Processed files\\AllCycles\\LCH_SoH_Calculated_summary_files\\LCH60Ah_CYC_1.2_25deg_All_cycles_Combined_summary.csv"

# data=pd.read_csv(f) 

# f="D:\\Benisha\\SoH_NN\\Data\\RandomForest_decision_regression_test_set_LCH.xlsx"
f="D:\\Benisha\\SoH_NN\\Data\\RandomForest_decision_regression_test_set_PHY.xlsx"

data=pd.read_excel(f)

#%% 
data=data[(data['SoH_calculated']>=10) & (data['SoH_calculated']<=120)] # to clean the data
data=data[(data['SoC_calculated']<=140)] 

data=data.fillna(0)

#%% x-the names of columns containing the input parameters; y-the output data i.e., the one to be predicted
x=data[['Cycle_No','Vol_s0_CCCV_Chg', 'Vol_s1_CCCV_Chg', 'Vol_s2_CCCV_Chg','Vol_s3_CCCV_Chg', 'Vol_s4_CCCV_Chg', 'Vol_s5_CCCV_Chg','Vol_s6_CCCV_Chg', 'Vol_s7_CCCV_Chg', 'Vol_s8_CCCV_Chg','Vol_s0_CC_DChg', 'Vol_s1_CC_DChg', 'Vol_s2_CC_DChg', 'Vol_s3_CC_DChg','Vol_s4_CC_DChg', 'Vol_s5_CC_DChg', 'Vol_s6_CC_DChg', 'Vol_s7_CC_DChg','Vol_s8_CC_DChg','Vol_s0_Rest', 'Vol_s1_Rest', 'Vol_s2_Rest','Vol_s3_Rest', 'Vol_s4_Rest', 'Vol_s5_Rest', 'Vol_s6_Rest','Vol_s7_Rest', 'Vol_s8_Rest','SoC_calculated','T_amb','DoD']] 
y=data['SoH_calculated']

  
#%% Splits data to training and test sets; but this can be omitted in RF, as the training and test are split anyway   
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33)

#%%
model1=RandomForestRegressor(n_estimators=100,min_samples_split=6,verbose=1)
model1.fit(x_train,y_train)
result1=model1.predict(x_test)

#%%
cols=['y_test','result']

#%% the dataframe map_res is created to see the predicted and test data better; also, it is better to use it to arrange the test values in descending order (i.e., 100% SoH to 80% or lower)
map_res=pd.DataFrame(index=range(0,len(y_test)), columns=cols)


y_test=y_test.reset_index(drop=True)
map_res['y_test']=y_test
map_res['result']=result1

#%%
map_res=map_res.sort_values(by='y_test', ascending=False)

#%% Plot for visualization
plt.figure()
plt.plot(range(0,len(y_test)),map_res.y_test,label='Actual')
plt.plot(range(0,len(result1)),map_res.result,label='Predicted')
plt.xlabel('Index',size=14)
plt.ylabel('SoH',size=14)
plt.title('SoH Actual Vs. Predicted')
plt.legend()

#%% Error Metrics; It is not smoothened as RF has fairly good predicted results
mse=mean_squared_error(map_res.y_test,map_res.result)
rmse=mean_squared_error(map_res.y_test,map_res.result, squared=False)
mae=mean_absolute_error(map_res.y_test,map_res.result)


#%% Saving Model
# joblib.dump(model1,f.rsplit('\\',3)[0]+'\\LCH_ForestRegressor_trial_1.joblib')


print('------------------%s seconds-------------' %(time.time()-start))