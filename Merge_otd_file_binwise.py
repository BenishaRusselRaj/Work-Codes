# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 18:06:53 2020

@author: IITM
"""



import pandas as pd
import os

def mergefile(filepath, otdfilepath):


    df1=pd.read_csv(filepath) # Sessions summary
    df2=pd.read_csv(otdfilepath, sep='\t') # OTD
    

    folder_path='\\'.join(otdfilepath.split('\\')[0:-1])
    
    #%%
#    f=df1['bin'].iloc[0]
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
    fin_path=folder_path+'\\OTD_Merged_Summary_files'
    if not os.path.exists(fin_path):
        os.makedirs(fin_path)
        
#    fin_file=fin_path+'\\OTD_Merged_Summary_file_'+f+'.csv' # if files are separated in folders
    fin_file=fin_path+'\\OTD_Merged_Summary_file.csv'  # if files are not sepparated in folders
    data.to_csv(fin_file)
    return (fin_file)