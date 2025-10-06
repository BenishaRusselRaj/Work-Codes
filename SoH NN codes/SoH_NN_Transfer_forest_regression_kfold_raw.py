# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 11:31:00 2022

@author: IITM
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:13:16 2022

@author: IITM
"""


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import joblib

import time
start=time.time()

#%%
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_SoH_Calculated_summary_files\\LCH_14.1_15.1_16.1_17.1_18.1_19.1_Combined_soh_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_3.1_4.1_6.1_21.1_22.1_22.2_AllCells_Combined_soh_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\25deg\\modified_arranged\\Processed files\\AllCycles\\LCH_SoH_Calculated_summary_files\\LCH60Ah_CYC_1.2_25deg_All_cycles_Combined_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\SoH_Calculated_summary_files_delsoc_smooth\\LCH_AllCells_Combined_SoH_Calculated_summary_files_delsoc_smooth.csv"#dod and actual temperature included
# f="D:\\Benisha\\SoH_NN\\Data\\LCH_PHY_Combined_Timestates_added_SoH_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\25deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60Ah_1.2_CYC_AllCycles_Combined_soh_summary_soh_smooth.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\45deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60_CYC_1.3_AllCycles_Combined_soh_summary_soh_smooth.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\PHY\\SoH_summary_smooth\\PHY_Combined_SoH_Calculated_summary_files_delsoc_smooth.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_3.1_4.1_6.1_21.1_22.1_22.2_Combined_soh_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\SoH_Calculated_summary_files_delsoc_smooth\\LCH_AllCells_Combined_soh_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_14.1_15.1_16.1_17.1_18.1_Combined_soh_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\SoH_calculated_summary_meansoc_soh_smooth\\LCH_AllCycles_Timestates_added_soh_summary_soh_soc_smooth.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\LCH_AllCycles_AllCells_Timestates_added_soh_summary_soh_smooth.csv"
f="D:\\Benisha\\SoH_NN\\Data\\PHY\\SoH_Summary_Smooth\\PHY_3.1_4.1_6.1_21.1_AllCycles_Timestates_added_soh_summary_smooth.csv"

data=pd.read_csv(f)

# f="D:\\Benisha\\SoH_NN\\Data\\RandomForest_decision_regression_test_set_LCH.xlsx"
# f="D:\\Benisha\\SoH_NN\\Data\\RandomForest_decision_regression_test_set_PHY.xlsx"
# data=pd.read_excel(f)

#%%
data=data[(data['SoH_calculated']>=80) & (data['SoH_calculated']<=120)] # to clean the data
data=data[(data['SoC_calculated']<=140)]

data=data.fillna(0)
#%%'Cycle_No',  ,'SoC_calculated'
x_array=['Cycle_No','Vol_s0_CCCV_Chg', 'Vol_s1_CCCV_Chg', 'Vol_s2_CCCV_Chg','Vol_s3_CCCV_Chg', 'Vol_s4_CCCV_Chg', 'Vol_s5_CCCV_Chg','Vol_s6_CCCV_Chg', 'Vol_s7_CCCV_Chg', 'Vol_s8_CCCV_Chg','Vol_s0_CC_DChg', 'Vol_s1_CC_DChg', 'Vol_s2_CC_DChg', 'Vol_s3_CC_DChg','Vol_s4_CC_DChg', 'Vol_s5_CC_DChg', 'Vol_s6_CC_DChg', 'Vol_s7_CC_DChg','Vol_s8_CC_DChg','Vol_s0_Rest', 'Vol_s1_Rest', 'Vol_s2_Rest','Vol_s3_Rest', 'Vol_s4_Rest', 'Vol_s5_Rest', 'Vol_s6_Rest','Vol_s7_Rest', 'Vol_s8_Rest','T_amb','DoD','mean_SoC', 'Temp_s0_CCCV_Chg', 'Temp_s1_CCCV_Chg',
        'Temp_s2_CCCV_Chg', 'Temp_s3_CCCV_Chg', 'Temp_s4_CCCV_Chg','Temp_s5_CCCV_Chg', 'Temp_s6_CCCV_Chg', 'Temp_s0_CC_DChg','Temp_s1_CC_DChg', 'Temp_s2_CC_DChg', 'Temp_s3_CC_DChg',
        'Temp_s4_CC_DChg', 'Temp_s5_CC_DChg', 'Temp_s6_CC_DChg', 'Temp_s0_Rest','Temp_s1_Rest', 'Temp_s2_Rest', 'Temp_s3_Rest', 'Temp_s4_Rest', 'Temp_s5_Rest', 'Temp_s6_Rest']
#%%
x=data[x_array]
y=data['SoH_calculated']

#%% PHY test data
# x_train=x.drop(x.index[111:151])
# x_test=x[111:151]
# y_train=y.drop(y.index[111:151])
# y_test=y[111:151]

#%% LCH test data
# x_train=x.drop(x.index[81:191])
# x_test=x[81:191]
# y_train=y.drop(y.index[81:191])
# y_test=y[81:191]

#%%
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33)

#%%
# forest_params = [{'n_estimators': list(range(10, 400)), 'min_samples_split': list(range(2,10)), 'max_features':list(range(1,30))}]
#%%
# f=open("D:\\Benisha\\SoH_NN\\Trees_samples_test_error_metrics_higher_sample_depths.csv","w")
# l1=[3,10,30,50,100,150,200,250,300,350,400,450,500] # 
# l2=[70,100,150,200,250]
# for t in l1:
#     for x in l2:
model1=RandomForestRegressor(n_estimators=100,min_samples_split=25,verbose=1) #split leaf
score=cross_val_score(model1,x_train,y_train,cv=20)
# model1=GridSearchCV(model,forest_params,cv=15,scoring='r2')

model1.fit(x_train,y_train)
result1=model1.predict(x_test)

#%%
# f=open("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_SoH_Calculated_summary_files\\LCH_bestparams.txt","w")
# print(model1.best_params_,file=f)
# print(model1.best_score_,file=f)

#%%
cols=['y_test','result']

#%% the dataframe map_res is created to see the predicted and test data better; also, it is better to use it to arrange the test values in descending order (i.e., 100% SoH to 80% or lower)
map_res=pd.DataFrame(index=range(0,len(y_test)), columns=cols)


y_test=y_test.reset_index(drop=True)
map_res['y_test']=y_test
map_res['result']=result1

#%%
map_res=map_res.sort_values(by='y_test', ascending=False)

mse=mean_squared_error(map_res.y_test,map_res.result)
rmse=mean_squared_error(map_res.y_test,map_res.result, squared=False)
mae=mean_absolute_error(map_res.y_test,map_res.result)

#%%
# print("=========================================================", file=f)
# print("Trees: %s" %t, file=f)
# print("Min no of samples: %s" %(x), file=f)
# print("mse: %s"  %(mse), file=f)
# print("rmse: %s" %(rmse), file=f)
# print("mae: %s"  %(mae), file=f)

#%% Plot for visualization
plt.figure()
plt.plot(range(0,len(y_test)),map_res.y_test,label='Actual')
plt.plot(range(0,len(result1)),map_res.result,label='Predicted')
plt.xlabel('Index',size=14)
plt.ylabel('SoH',size=14)
plt.title('SoH Actual Vs. Predicted')
plt.legend()
# plt.savefig("D:\\Benisha\\SoH_NN\\Graphs\\Trees_leaves_ error_metrics_higher_samples\\Trees_"+str(t)+"Min_samples_"+str(x)+".png")

#%%
plt.figure()
plt.plot(range(0,len(data)),data['SoH_calculated'])
plt.title('SoH_calculated')


#%% Feature Importance

# f1=open(f.rsplit('\\',1)[0]+"\\RF_Feature_Importance_PHY_soh_smooth_temptimestates.csv",'w')
# importance=model1.feature_importances_
# for i,n in enumerate(importance):
#     print('Feature: %s; Importance: %f' %(x_array[i],n),file=f1)
# f1.close()

#%% Saving Model
joblib.dump(model1,f.rsplit('\\',1)[0]+'\\PHY_ForestRegressor_3.1_4.1_6.1_21.1_kfold_soh_smooth_temptimestates.joblib')
# joblib.dump(model1,"D:\\Benisha\\SoH_NN\\Data\\LCH_ForestRegressor_kfold_meansoc.joblib")


print('------------------%s seconds-------------' %(time.time()-start))