import time
start = time.time()
import pandas as pd
df_Chg= pd.read_excel("D:\\Benisha\\Phy13 new cell diff rates.xlsx", sheet_name='Charging')
df_DChg= pd.read_excel("D:\\Benisha\\Phy13 new cell diff rates.xlsx", sheet_name='Discharge')
data=pd.read_excel("D:\\Benisha\\Code files\\PHY.xlsx",sheet_name='Sheet1')
data=data[data.Cycle_No==2];d1=pd.DataFrame(); d2=pd.DataFrame()
#x=['0.5','1','1.5','2','3','0.3']
x=['0.5','1','1.5','2','3','0.1']
df1=data[data.Current>0].reset_index(drop=True)
df2=data[data.Current<0].reset_index(drop=True)
df1['SOC']=(df1['Q_in_out']/df1['Q_in_out'].iloc[-1])*100
df2['SOC']=(df2['Q_in_out']/df2['Q_in_out'].iloc[-1])*100
df1['SOC']=round(df1['SOC'],2)
df2['SOC']=round(df2['SOC'],2)
print('.............1/5')
for a in range(0,6):
        df1['SOC_'+x[a]+'C']=round(df_Chg['SOC_'+x[a]+'C'],2).dropna()
        df1['V_'+x[a]+'C']=df_Chg['V_'+x[a]+'C'].dropna()
        df1['I_'+x[a]+'C']=df_Chg['I_'+x[a]+'C'].dropna()
        df1['SOC_flag'+x[a]+'C']=df1['SOC'].isin(df1['SOC_'+x[a]+'C'])
        df1['Soc_vt_flag'+x[a]+'C']=df1['SOC_'+x[a]+'C'].duplicated(keep='first')
        df1['Soc_ocv_flag'+x[a]+'C']=df1['SOC'].duplicated(keep='first')
        df1.loc[(df1['SOC_flag'+x[a]+'C']==True) & (df1['Soc_ocv_flag'+x[a]+'C']==False),'OCV_Vtg_Cmp'+x[a]+'C']=df1['Voltage']
        df1.loc[(df1['SOC_flag'+x[a]+'C']==True) & (df1['Soc_ocv_flag'+x[a]+'C']==False),'OCV_I_Cmp'+x[a]+'C']=df1['Current']
        df1.loc[(df1['SOC_flag'+x[a]+'C']==True) & (df1['Soc_ocv_flag'+x[a]+'C']==False),'OCV_SOC_Cmp'+x[a]+'C']=df1['SOC']
        df1.loc[(df1['Soc_vt_flag'+x[a]+'C']==False),'Vt_Vtg_Cmp'+x[a]+'C']=df1['V_'+x[a]+'C']
        df1.loc[(df1['Soc_vt_flag'+x[a]+'C']==False),'Vt_I_Cmp'+x[a]+'C']=df1['I_'+x[a]+'C']
        df1.loc[(df1['Soc_vt_flag'+x[a]+'C']==False),'Vt_SOC_Cmp'+x[a]+'C']=df1['SOC_'+x[a]+'C']
print('.............2/5')
for a in range (0,6):
        df2['SOC_'+x[a]+'C']=round(df_DChg['SOC_'+x[a]+'C'],2).dropna()
        df2['V_'+x[a]+'C']=df_DChg['V_'+x[a]+'C'].dropna()
        df2['I_'+x[a]+'C']=df_DChg['I_'+x[a]+'C'].dropna()
        df2['SOC_flag'+x[a]+'C']=df2['SOC'].isin(df2['SOC_'+x[a]+'C'])
        df2['Soc_vt_flag'+x[a]+'C']=df2['SOC_'+x[a]+'C'].duplicated(keep='first')
        df2['Soc_ocv_flag'+x[a]+'C']=df2['SOC'].duplicated(keep='first') 
        df2.loc[(df2['SOC_flag'+x[a]+'C']==True) & (df2['Soc_ocv_flag'+x[a]+'C']==False),'OCV_Vtg_Cmp'+x[a]+'C']=df2['Voltage']
        df2.loc[(df2['SOC_flag'+x[a]+'C']==True) & (df2['Soc_ocv_flag'+x[a]+'C']==False),'OCV_I_Cmp'+x[a]+'C']=df2['Current']
        df2.loc[(df2['SOC_flag'+x[a]+'C']==True) & (df2['Soc_ocv_flag'+x[a]+'C']==False),'OCV_SOC_Cmp'+x[a]+'C']=df2['SOC']
        df2.loc[(df2['Soc_vt_flag'+x[a]+'C']==False),'Vt_Vtg_Cmp'+x[a]+'C']=df2['V_'+x[a]+'C']
        df2.loc[(df2['Soc_vt_flag'+x[a]+'C']==False),'Vt_I_Cmp'+x[a]+'C']=df2['I_'+x[a]+'C']
        df2.loc[(df2['Soc_vt_flag'+x[a]+'C']==False),'Vt_SOC_Cmp'+x[a]+'C']=df2['SOC_'+x[a]+'C']
print('.............3/5')
df1=df1.apply(lambda x: pd.Series(x.dropna().values))
df2=df2.apply(lambda x: pd.Series(x.dropna().values))
for a in range (0,6):
    d1['OCV_Vtg_Cmp'+x[a]+'C']=df1['OCV_Vtg_Cmp'+x[a]+'C']
    d1['OCV_I_Cmp'+x[a]+'C']=df1['OCV_I_Cmp'+x[a]+'C']
    d1['Vt_Vtg_Cmp'+x[a]+'C']=df1['Vt_Vtg_Cmp'+x[a]+'C']
    d1['Vt_SOC_Cmp'+x[a]+'C']=df1['Vt_SOC_Cmp'+x[a]+'C']
    d1['Vt_I_Cmp'+x[a]+'C']=df1['Vt_I_Cmp'+x[a]+'C']
    d1['IR_Loss_'+x[a]+'C']=d1['Vt_Vtg_Cmp'+x[a]+'C']-d1['OCV_Vtg_Cmp'+x[a]+'C']
    d1['Cum_IRLoss'+x[a]+'C']=''
    d1['Cum_IRLoss'+x[a]+'C'].iloc[0]=d1['IR_Loss_'+x[a]+'C'].sum()
    d1['R_'+x[a]+'C']=d1['IR_Loss_'+x[a]+'C']/d1['Vt_I_Cmp'+x[a]+'C']
    d1['Heating_Loss_'+x[a]+'C']=d1['IR_Loss_'+x[a]+'C']*d1['Vt_I_Cmp'+x[a]+'C']
    d1['Cum_Heating_Loss_'+x[a]+'C']=''
    d1['Cum_Heating_Loss_'+x[a]+'C'].iloc[0]=d1['Heating_Loss_'+x[a]+'C'].sum()
    d2['OCV_Vtg_Cmp'+x[a]+'C']=df2['OCV_Vtg_Cmp'+x[a]+'C']
    d2['OCV_I_Cmp'+x[a]+'C']=df2['OCV_I_Cmp'+x[a]+'C']
    d2['Vt_Vtg_Cmp'+x[a]+'C']=df2['Vt_Vtg_Cmp'+x[a]+'C']
    d2['Vt_SOC_Cmp'+x[a]+'C']=df2['Vt_SOC_Cmp'+x[a]+'C']
    d2['Vt_I_Cmp'+x[a]+'C']=df2['Vt_I_Cmp'+x[a]+'C']
    d2['IR_Loss_'+x[a]+'C']=d2['Vt_Vtg_Cmp'+x[a]+'C']-d2['OCV_Vtg_Cmp'+x[a]+'C']
    d2['Cum_IRLoss'+x[a]+'C']=''
    d2['Cum_IRLoss'+x[a]+'C'].iloc[0]=d2['IR_Loss_'+x[a]+'C'].sum()
    d2['R_'+x[a]+'C']=d2['IR_Loss_'+x[a]+'C']/d2['Vt_I_Cmp'+x[a]+'C']
    d2['Heating_Loss_'+x[a]+'C']=d2['IR_Loss_'+x[a]+'C']*d2['Vt_I_Cmp'+x[a]+'C'] 
    d2['Cum_Heating_Loss_'+x[a]+'C']=''
    d2['Cum_Heating_Loss_'+x[a]+'C'].iloc[0]=d2['Heating_Loss_'+x[a]+'C'].sum()
print('.............4/5')
d1.to_excel('Chg7_PHY.xlsx')
d2.to_excel('DChg7_PHY.xlsx')
print('.............5/5')
print("--- %s seconds ---" % (time.time() - start))