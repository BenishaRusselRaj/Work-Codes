# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 14:57:17 2022

@author: IITM
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 17:39:16 2022

@author: IITM
"""


import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from keras.models import load_model
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score
import joblib
import numpy as np

import time
start=time.time()

#%%
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_SoH_Calculated_summary_files\\LCH_14.1_15.1_16.1_17.1_18.1_19.1_Combined_soh_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_3.1_4.1_6.1_21.1_22.1_22.2_AllCells_Combined_soh_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\LCH60Ah_AllCycles_Timestates_added_soh_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\LCH_SoH_Calculated_summary_files\\LCH_AllCycles_Combined_Timestates_added_soh_summary.csv" #dod and actual temperature included
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\25deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60Ah_1.2_CYC_AllCycles_Combined_soh_summary_soh_smooth.csv"#dod and actual temperature included
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\45deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60_CYC_1.3_AllCycles_Combined_soh_summary_soh_smooth.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\PHY\\SoH_summary_smooth\\PHY_Combined_SoH_Calculated_summary_files_delsoc_smooth.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\SoH_Calculated_summary_files_delsoc_smooth\\LCH_AllCells_Combined_SoH_Calculated_summary_files_delsoc_smooth.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\BRD\\SoH Summary Files\\BRD_AllCells_AllCycles_Timestates_added_soh_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\25deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60Ah_1.2_CYC_25deg_modified_arranged_Timestates_added_soh_summary_soh_soc_smooth.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\45deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60_CYC_1.3_45deg_modified_arranged_Timestates_added_soh_summary_soh_soc_smooth.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_3.1_4.1_6.1_21.1_22.1_22.2_Combined_soh_summary.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\BRD\\SoH Summary Files\\BRD_4.2_AllCycles_Timestates_added_soh_summary_soh_smooth.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\Raw files\\SoH_Calculated_summary_files\\SoH_smooth\\LCH_AllCycles_Timestates_added_soh_summary_smooth.csv"

# f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\Raw files\\SoH_Calculated_summary_files\\SoH_smooth\\LCH_AllCycles_Timestates_added_soh_summary_smooth.csv"
f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\Raw files\\SoH_Calculated_summary_files\\SoH_smooth\\LCH_14.1_35Deg_AllCycles_AllCycles_raw(1)_Timestates_added_soh_summary_soh_smooth.csv"
cell_no='LCH_14.1_Deg%_notemptimestates_nodod' ## change map_res sort by y_test to descending

data=pd.read_csv(f) 
map_res=pd.DataFrame()


#%%
data=data[(data['SoH_calculated']>=80) & (data['SoH_calculated']<=110)] # to clean the data
data=data[(data['SoC_calculated']<=140)] #(data['SoC_calculated']>=35) & 

data=data.fillna(0)

#%% 'Cycle_No',
x_array=['Cycle_No','Vol_s0_CCCV_Chg', 'Vol_s1_CCCV_Chg', 'Vol_s2_CCCV_Chg','Vol_s3_CCCV_Chg', 'Vol_s4_CCCV_Chg', 'Vol_s5_CCCV_Chg','Vol_s6_CCCV_Chg', 'Vol_s7_CCCV_Chg', 'Vol_s8_CCCV_Chg','Vol_s0_CC_DChg', 'Vol_s1_CC_DChg', 'Vol_s2_CC_DChg', 'Vol_s3_CC_DChg','Vol_s4_CC_DChg', 'Vol_s5_CC_DChg', 'Vol_s6_CC_DChg', 'Vol_s7_CC_DChg','Vol_s8_CC_DChg','Vol_s0_Rest', 'Vol_s1_Rest', 'Vol_s2_Rest','Vol_s3_Rest', 'Vol_s4_Rest', 'Vol_s5_Rest', 'Vol_s6_Rest','Vol_s7_Rest', 'Vol_s8_Rest','T_amb','mean_SoC']
            # ,'DoD']#, 'Temp_s0_CCCV_Chg', 'Temp_s1_CCCV_Chg',
        # 'Temp_s2_CCCV_Chg', 'Temp_s3_CCCV_Chg', 'Temp_s4_CCCV_Chg','Temp_s5_CCCV_Chg', 'Temp_s6_CCCV_Chg', 'Temp_s0_CC_DChg','Temp_s1_CC_DChg', 'Temp_s2_CC_DChg', 'Temp_s3_CC_DChg',
        # 'Temp_s4_CC_DChg', 'Temp_s5_CC_DChg', 'Temp_s6_CC_DChg', 'Temp_s0_Rest','Temp_s1_Rest', 'Temp_s2_Rest', 'Temp_s3_Rest', 'Temp_s4_Rest', 'Temp_s5_Rest', 'Temp_s6_Rest']
        
x=data[x_array]
y=abs(100-data['SoH_calculated'])

#%%
# model=np.poly1d(x,y,3)


#%%
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33)

# x_train=data[x_array]
# y_train=data['SoH_calculated']


#%% Linear regression
# poly_regr=PolynomialFeatures(degree=4,include_bias=False)
# x_poly=poly_regr.fit_transform(x) #.reshape(-1,1)

# x_train,x_test,y_train,y_test=train_test_split(x_poly,y,test_size=0.33)


# lin_regr=LinearRegression() #,fit_intercept=False positive=True,fit_intercept=False
# lin_regr.fit(x_train,y_train)
# result=lin_regr.predict(x_test)

#%% Sequential NN
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\PHY_ForestRegressor_kfold_dod_soh_smooth.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH60Ah_ForestRegressor_kfold_dod_soh_smooth.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_ForestRegressor_kfold_dod_soh_smooth_25split.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\PHY\\LCH_25split_PHY.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_PHY_25split_LCH25deg.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_PHY_25split_LCH25deg_LCH45deg.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\SoH_calculated_summary_meansoc_soh_smooth\\LCH_ForestRegressor_kfold_meansoc_smooth.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH_PHY_ForestRegressor_kfold_dod__.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH_PHY_LCH60_ForestRegressor_kfold_dod__.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH_ForestRegressor_kfold_dod__noCycleNo.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH_ForestRegressor_kfold_dod__noCycleNo_nosoc.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH_ForestRegressor_kfold_dod__nosoc.joblib")
# model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\LCH_ForestRegressor_kfold_soh_smooth_temptimestates.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\PHY\\SoH_Summary_Smooth\\PHY_ForestRegressor_3.1_4.1_6.1_21.1_kfold_soh_smooth_temptimestates.joblib")
# # score=cross_val_score(model,x_train,y_train,cv=20)
# model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\Raw files\\SoH_Calculated_summary_files\\SoH_smooth\\LCH_LinearRegressor_temptimestates.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\Raw files\\SoH_Calculated_summary_files\\SoH_smooth\\Lch_kerasregressor_model_temptimestates_relu_1layer.joblib")
# model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\Raw files\\LCH_AllCells_Deg%_poscoeff__LinearRegressor.joblib")
model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\Raw files\\LCH_AllCells_Deg%_notemptimestates_nodod_LinearRegressor.joblib")

model.fit(x_train,y_train)

result=model.predict(x_test)

#%%
# map_res['Cycle_No']=x_test['Cycle_No'] #### only in 2.8kWh packs
map_res['y_test']=y_test
map_res['result']=result

# map_res=map_res.sort_values(ascending=False,by='y_test')#####uncomment
map_res=map_res.sort_values(ascending=True,by='y_test')
# map_res=map_res.sort_values(ascending=True,by='Cycle_No')
# map_res=map_res[(map_res['result']>0) & (map_res['result']<=120)]

map_res['Smooth_result']=map_res['result'].rolling(10).mean()
# map_res['Smooth_result']=map_res['result'].rolling(10).min()
map_res['Smooth_result']=map_res['Smooth_result'].fillna(method='bfill')


#%%
plt.figure()
plt.plot(range(len(map_res)),map_res.y_test,label='Actual') #,markersize=3
plt.plot(range(len(map_res)),map_res.result,label='Predicted')
plt.xlabel('No. of Cycles')
plt.ylabel('SoH(%)')
# plt.plot(range(0,len(map_res)),map_res.Smooth_result,label='Predicted_Smoothened')
plt.legend()
plt.grid(linestyle='dotted')
plt.title('SoH_'+cell_no)

#%%
plt.figure()
plt.plot(range(len(map_res)),map_res.y_test,label='Actual') #,markersize=3
plt.plot(range(len(map_res)),map_res.Smooth_result,label='Predicted_Smoothened')
plt.xlabel('No. of Cycles')
plt.ylabel('SoH(%)')
plt.legend()
plt.grid(linestyle='dotted')
plt.title('SoH_'+cell_no)
#%%
mse=mean_squared_error(map_res.y_test,map_res.result)
rmse=mean_squared_error(map_res.y_test,map_res.result, squared=False)
mae=mean_absolute_error(map_res.y_test,map_res.result)

#%%
map_res=map_res.dropna(subset=['Smooth_result'])
mse_smooth=mean_squared_error(map_res.y_test,map_res.Smooth_result)
rmse_smooth=mean_squared_error(map_res.y_test,map_res.Smooth_result, squared=False)
mae_smooth=mean_absolute_error(map_res.y_test,map_res.Smooth_result)

# #%%
# plt.figure()
# plt.plot(range(0,len(data)),data['SoH_calculated'])
# plt.title('SoH_calculated')

#%%'Cycle_No', UNCOMMENT

# # # importance=model.feature_importances_
try:
    importance=lin_regr.coef_
except NameError:
    importance=model.coef_
l1=[0,1,2,3,4,5,6,7,8]
l2=['CCCV_Chg','CC_DChg','Rest']
f2=open(f.rsplit('\\',1)[0]+"\\"+cell_no+"_Feature_Importance_Error_metrics_soh_smooth_LinearRegressor.csv","w")
# print('Features and their importances (in Percentage):', file=f2)
for i,n in enumerate(importance):
    print('Feature: %s; Importance: %f' %(x_array[i],n), file=f2)  ##n*100; for percentage
for s in l2:
    for n in l1:
        print('Time spent in '+str(s)+' state '+ str(n)+': %s' %((data['Vol_s'+str(n)+'_'+str(s)]).sum()), file=f2)
print('mse: %s' %(mse), file=f2)
print('mae: %s' %(mae), file=f2)
print('rmse: %s' %(rmse), file=f2)
print('mse_smooth: %s' %(mse_smooth), file=f2)
print('mae_smooth: %s' %(mae_smooth), file=f2)
print('rmse_smooth: %s' %(rmse_smooth), file=f2)
# print('SoH from Capacity Test:%s' %(SoH_test), file=f2)
# print('End SoH predicted: %s' %(map_res['result'].iloc[-1]), file=f2)
f2.close()
#%%
# #joblib.dump(model,"D:\\Benisha\\SoH_NN\\Data\\LCH_PHY_LCH60_ForestRegressor_kfold_dod__.joblib")
# joblib.dump(lin_regr,f.rsplit('\\',3)[0]+'\\'+cell_no+'_LinearRegressor.joblib')
# #joblib.dump(lin_regr,f.rsplit('\\',1)[0]+'\\LCH_PolyRegressor_temptimestates_3deg.joblib')





#%%
# -*- coding: utf-8 -*-
# """
# Created on Thu Oct 27 15:56:45 2022

# @author: IITM
# """

# # -*- coding: utf-8 -*-
# """
# Created on Fri Jul  8 14:57:17 2022

# @author: IITM
# """

# # -*- coding: utf-8 -*-
# """
# Created on Thu Mar 24 17:39:16 2022

# @author: IITM
# """


# import pandas as pd
# import keras
# from keras.models import Sequential
# from keras.layers import Dense
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.linear_model import LinearRegression
# import matplotlib.pyplot as plt
# from keras.models import load_model
# from sklearn.metrics import mean_squared_error
# from sklearn.metrics import mean_absolute_error
# from sklearn.model_selection import cross_val_score
# import joblib
# import numpy as np

# import time
# start=time.time()

# #%%
# # f="D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_SoH_Calculated_summary_files\\LCH_14.1_15.1_16.1_17.1_18.1_19.1_Combined_soh_summary.csv"
# # f="D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_3.1_4.1_6.1_21.1_22.1_22.2_AllCells_Combined_soh_summary.csv"
# # f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\LCH60Ah_AllCycles_Timestates_added_soh_summary.csv"
# # f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\LCH_SoH_Calculated_summary_files\\LCH_AllCycles_Combined_Timestates_added_soh_summary.csv" #dod and actual temperature included
# # f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\25deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60Ah_1.2_CYC_AllCycles_Combined_soh_summary_soh_smooth.csv"#dod and actual temperature included
# # f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\45deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60_CYC_1.3_AllCycles_Combined_soh_summary_soh_smooth.csv"
# # f="D:\\Benisha\\SoH_NN\\Data\\PHY\\SoH_summary_smooth\\PHY_Combined_SoH_Calculated_summary_files_delsoc_smooth.csv"
# # f="D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\SoH_Calculated_summary_files_delsoc_smooth\\LCH_AllCells_Combined_SoH_Calculated_summary_files_delsoc_smooth.csv"
# f="D:\\Benisha\\SoH_NN\\Data\\BRD\\SoH Summary Files\\BRD_3.2_AllCycles_Timestates_added_soh_summary_soh_smooth.csv"
# # f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\25deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60Ah_1.2_CYC_25deg_modified_arranged_Timestates_added_soh_summary_soh_soc_smooth.csv"
# # f="D:\\Benisha\\SoH_NN\\Data\\LCH\\60Ah\\45deg\\modified_arranged\\Processed files\\AllCycles\\SoH_Calculated_summary_files_delsoc\\LCH60_CYC_1.3_45deg_modified_arranged_Timestates_added_soh_summary_soh_soc_smooth.csv"
# # f="D:\\Benisha\\SoH_NN\\Data\\PHY\\PHY_3.1_4.1_6.1_21.1_22.1_22.2_Combined_soh_summary.csv"
# # f="D:\\Benisha\\SoH_NN\\Data\\PHY\\SoH_Summary_Smooth\\PHY_3.1_4.1_6.1_21.1_AllCycles_Timestates_added_soh_summary_smooth.csv"


# data=pd.read_csv(f) 
# map_res=pd.DataFrame()

# cell_no='BRD_3.1'
# f1="D:\\Benisha\\SoH_NN\\Data\\BRD\\SoH Summary Files\\BRD_3.1_AllCycles_Timestates_added_soh_summary_soh_smooth.csv"
# df=pd.read_csv(f1)
# df=df.fillna(0)

# #%%
# data=data[(data['SoH_calculated']>=80) & (data['SoH_calculated']<=110)] # to clean the data
# data=data[(data['SoC_calculated']<=140)] #(data['SoC_calculated']>=35) & 

# data=data.fillna(0)

# #%% 'Cycle_No',
# x_array=['Cycle_No','Vol_s0_CCCV_Chg', 'Vol_s1_CCCV_Chg', 'Vol_s2_CCCV_Chg','Vol_s3_CCCV_Chg', 'Vol_s4_CCCV_Chg', 'Vol_s5_CCCV_Chg','Vol_s6_CCCV_Chg', 'Vol_s7_CCCV_Chg', 'Vol_s8_CCCV_Chg','Vol_s0_CC_DChg', 'Vol_s1_CC_DChg', 'Vol_s2_CC_DChg', 'Vol_s3_CC_DChg','Vol_s4_CC_DChg', 'Vol_s5_CC_DChg', 'Vol_s6_CC_DChg', 'Vol_s7_CC_DChg','Vol_s8_CC_DChg','Vol_s0_Rest', 'Vol_s1_Rest', 'Vol_s2_Rest','Vol_s3_Rest', 'Vol_s4_Rest', 'Vol_s5_Rest', 'Vol_s6_Rest','Vol_s7_Rest', 'Vol_s8_Rest','T_amb','DoD','mean_SoC', 'Temp_s0_CCCV_Chg', 'Temp_s1_CCCV_Chg',
#         'Temp_s2_CCCV_Chg', 'Temp_s3_CCCV_Chg', 'Temp_s4_CCCV_Chg','Temp_s5_CCCV_Chg', 'Temp_s6_CCCV_Chg', 'Temp_s0_CC_DChg','Temp_s1_CC_DChg', 'Temp_s2_CC_DChg', 'Temp_s3_CC_DChg',
#         'Temp_s4_CC_DChg', 'Temp_s5_CC_DChg', 'Temp_s6_CC_DChg', 'Temp_s0_Rest','Temp_s1_Rest', 'Temp_s2_Rest', 'Temp_s3_Rest', 'Temp_s4_Rest', 'Temp_s5_Rest', 'Temp_s6_Rest']


# #%%
# # model=np.poly1d(x,y,3)


# #%%
# # x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33)

# x_train=data[x_array]
# y_train=data['SoH_calculated']


# x_test=df[x_array]
# y_test=df['SoH_calculated']

# #%% Linear regression
# # poly_regr=PolynomialFeatures(degree=3,include_bias=False)
# # x_poly=poly_regr.fit_transform(x) #.reshape(-1,1)

# # x_train,x_test,y_train,y_test=train_test_split(x_poly,y,test_size=0.33)
# # map_res['y_test']=y_test


# # lin_regr=LinearRegression()
# # lin_regr.fit(x_train,y_train)
# # result=lin_regr.predict(x_test)

# #%% Sequential NN
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\PHY_ForestRegressor_kfold_dod_soh_smooth.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH60Ah_ForestRegressor_kfold_dod_soh_smooth.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_ForestRegressor_kfold_dod_soh_smooth_25split.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\PHY\\LCH_25split_PHY.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_PHY_25split_LCH25deg.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_PHY_25split_LCH25deg_LCH45deg.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\SoH_calculated_summary_meansoc_soh_smooth\\LCH_ForestRegressor_kfold_meansoc_smooth.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH_PHY_ForestRegressor_kfold_dod__.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH_PHY_LCH60_ForestRegressor_kfold_dod__.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH_ForestRegressor_kfold_dod__noCycleNo.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH_ForestRegressor_kfold_dod__noCycleNo_nosoc.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH_ForestRegressor_kfold_dod__nosoc.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\LCH_ForestRegressor_kfold_soh_smooth_temptimestates.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\PHY\\SoH_Summary_Smooth\\PHY_ForestRegressor_3.1_4.1_6.1_21.1_kfold_soh_smooth_temptimestates.joblib")
# # model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\LCH_ForestRegressor_kfold_soh_smooth_temptimestates.joblib")
# model=joblib.load("D:\\Benisha\\SoH_NN\\Data\\LCH\\New folder\\Raw files\\SoH_Calculated_summary_files\\SoH_smooth\\LCH_LinearRegressor_temptimestates.joblib")
# # score=cross_val_score(model,x_train,y_train,cv=20)

# model.fit(x_train,y_train) #

# result=model.predict(x_test)

# #%%
# map_res['result']=result
# map_res['y_test']=y_test
# map_res=map_res.sort_values(ascending=False,by='y_test') #####uncomment
# # map_res=map_res.sort_values(ascending=True,by='Cycle_No')
# map_res=map_res[(map_res['result']>0) & (map_res['result']<=120)]

# map_res['Smooth_result']=map_res['result'].rolling(10).mean()
# # map_res['Smooth_result']=map_res['result'].rolling(10).min()
# map_res['Smooth_result']=map_res['Smooth_result'].fillna(method='bfill')
# #%%
# plt.figure()
# plt.plot(range(len(map_res)),map_res.y_test,label='Actual') #,markersize=3
# plt.plot(range(len(map_res)),map_res.result,label='Predicted')
# plt.xlabel('No. of Cycles')
# plt.ylabel('SoH(%)')
# # plt.plot(range(0,len(map_res)),map_res.Smooth_result,label='Predicted_Smoothened')
# plt.legend()
# plt.grid(linestyle='dotted')
# plt.title('SoH_'+cell_no)

# #%%
# plt.figure()
# plt.plot(range(len(map_res)),map_res.y_test,label='Actual') #,markersize=3
# plt.plot(range(len(map_res)),map_res.Smooth_result,label='Predicted_Smoothened')
# plt.xlabel('No. of Cycles')
# plt.ylabel('SoH(%)')
# plt.legend()
# plt.grid(linestyle='dotted')
# plt.title('SoH_smooth'+cell_no)

# #%%
# plt.figure()
# plt.plot(range(len(data)),data.SoH_calculated)
# plt.xlabel('No. of Cycles')
# plt.ylabel('SoH(%)')
# plt.grid(linestyle='dotted')
# plt.title('SoH_training_data_'+cell_no)
# #%%
# mse=mean_squared_error(map_res.y_test,map_res.result)
# rmse=mean_squared_error(map_res.y_test,map_res.result, squared=False)
# mae=mean_absolute_error(map_res.y_test,map_res.result)

# #%%
# map_res=map_res.dropna(subset=['Smooth_result'])
# mse_smooth=mean_squared_error(map_res.y_test,map_res.Smooth_result)
# rmse_smooth=mean_squared_error(map_res.y_test,map_res.Smooth_result, squared=False)
# mae_smooth=mean_absolute_error(map_res.y_test,map_res.Smooth_result)

# # #%%
# # plt.figure()
# # plt.plot(range(0,len(data)),data['SoH_calculated'])
# # plt.title('SoH_calculated')

# #%%'Cycle_No', UNCOMMENT

# # importance=model.feature_importances_
# importance=model.coef_
# f2=open(f1.rsplit('\\',1)[0]+"\\"+cell_no+"_LinearRegressor_Feature_importances_meansoc_soh_smooth.csv","w")
# # print('Features and their importances (in Percentage):', file=f2)
# for i,n in enumerate(importance):
#     print('Feature: %s; Importance: %f' %(x_array[i],n), file=f2)  ##n*100; for percentage
# print('mse: %s' %(mse), file=f2)
# print('mae: %s' %(mae), file=f2)
# print('rmse: %s' %(rmse), file=f2)
# print('mse_smooth: %s' %(mse_smooth), file=f2)
# print('mae_smooth: %s' %(mae_smooth), file=f2)
# print('rmse_smooth: %s' %(rmse_smooth), file=f2)
# print('rmse_smooth: %s' %(rmse_smooth), file=f2)
# f2.close()
# # #%%
# # joblib.dump(model,"D:\\Benisha\\SoH_NN\\Data\\LCH_PHY_LCH60_ForestRegressor_kfold_dod__.joblib")
# joblib.dump(lin_regr,f.rsplit('\\',3)[0]+'\\LCH_PolynomialRegressor_3deg.joblib')
