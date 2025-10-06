# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 10:45:35 2022

@author: IITM
"""

import pandas as pd
import glob

#%%
folders=glob.glob("D:\\Benisha\\2.8kWh_Charging Algorithm\\Pack_5\\22_08_19\\Pack5Data18-08-2022\\*")


#%%
for f1 in folders:
    files=glob.glob(f1+"\\*.*_modified.xlsx")
    if len(files)!=0:
        df=pd.DataFrame()
        for f in files:
            d1=pd.read_excel(f)
            try:
                df=pd.merge(how='right',left=df,right=d1,on='DateTime',right_index=True)
            except KeyError:
                df=pd.concat([df,d1])
        
#%%
        if 'charging' in f.rsplit('\\',1)[1].lower():
            df['Session_Type']='Charging'
            state='Charging'
        elif 'battery' in f.rsplit('\\',1)[1].lower():
            df['Session_Type']='Discharging'
            state='Driving'
            
#%%
        df=df.sort_values(by='DateTime', ascending=True)
        df=df.dropna(how='all',axis=1)
        df=df.dropna(subset=['C0'])
        df=df.fillna(method='ffill')
        
        df=df.fillna(method='bfill')
        
#%%
        df.to_csv(f.rsplit('.',2)[0].rsplit('\\',1)[0]+'\\'+state+'_complete_graph_data.csv')
    else:
        continue