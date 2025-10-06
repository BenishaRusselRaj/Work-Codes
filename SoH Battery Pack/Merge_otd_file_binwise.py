"""
==============================================================================================
File name: Merge_otd_file_bitwise.py
Desription:
Comments:
==============================================================================================
"""



import pandas as pd
import os

"""
==============================================================================================
Function name: mergefile
Desription:
Argument:
Returns:
Comments:
==============================================================================================
"""
def mergefile(filepath, otdfilepath):


    df1=pd.read_csv(filepath) # Sessions summary
    df2=pd.read_csv(otdfilepath, sep='\t') # OTD


    folder_path='\\'.join(otdfilepath.split('\\')[0:-2]) + '\\Results'

    #%%
    f=df1['bin'].iloc[0]
#    df2=df2[df2['bin']==f]
    df2.rename(columns={'bin':'bin_1','session':'session_1'}, inplace=True)
    cols2=list(df2)
    df1=df1.sort_values(by='start_Time')
    data=pd.DataFrame()
    grouped=df1.groupby('Session_Type')
    df=[g[1] for g in list(grouped)]
    for i in range(0, len(df)):
        if ((df[i]['Session_Type']).all()=='Chg'):
            df[i]=df[i].merge(df2,left_on='session',right_on='session_1',how='left')
        else:
            for newcol in cols2:
                df[i][newcol]=''
        data=pd.concat([data,df[i]])
    data=data.sort_values(by='start_Time')
    data=data.reset_index(drop=True)
    
    
    
    
    filter1 = data["Remark"]!="--Delete--"
    filter2 = data["Remark"]!="--Overlap--"
    data.where(filter1 & filter2, inplace = True)
    data.dropna(subset = ["Session_Type"], inplace=True)
    data = data.reset_index(drop = True)
    
    
    filter1 = data["Time_in_session_mins"]!= 0 # remove all sessions with 0 time
    filter2 = data["Time_in_session_mins"] < (60*24*30*4) # 4 mo
    data.where(filter1 & filter2, inplace = True)
    data.dropna(subset = ["Session_Type"], inplace=True)
    data = data.reset_index(drop = True)
      
    for i in range(1, len(data)):
        if ((data.Cycle_No_session.iloc[i] - data.Cycle_No_session.iloc[i-1]) > 0):
            data.Cycle_No_Chg_DChg.iloc[i] = data.Cycle_No_Chg_DChg.iloc[i-1] + 1;
        elif ((data.Cycle_No_session.iloc[i] - data.Cycle_No_session.iloc[i-1]) == 0):
            data.Cycle_No_Chg_DChg.iloc[i] = data.Cycle_No_Chg_DChg.iloc[i-1];
    
    data.Cycle_No_session = data.Cycle_No_Chg_DChg
    data = data.drop(columns=['Cycle_No_Chg_DChg'])
    
    fin_path=folder_path+'\\OTD_Merged_Summary_files'
    if not os.path.exists(fin_path):
        os.makedirs(fin_path)

    fin_file=fin_path+'\\OTD_Merged_Summary_file_'+f+'.csv' # if files are separated in folders
    # fin_file=fin_path+'\\OTD_Merged_Summary_file.csv'  # if files are not sepparated in folders
    data.to_csv(fin_file)
    return (fin_file)