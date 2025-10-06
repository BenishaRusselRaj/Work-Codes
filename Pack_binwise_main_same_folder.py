# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 10:16:51 2020

@author: IITM
"""

"""
Use this when chg and dchg files are in same folder separated bin-wise
Change 'bin' in timestates code!!!

"""
import time
start1=time.time()
import glob
import pandas as pd
import os
import sys
sys.path.append('D:\\Benisha\\Code files') # add the path to the code files here
from Pack_Timestates_binwise import timestates
from Pack_del_duplicated_DChg import timecheck
from Combined_pack_data import combinedata

l1=[]
files1= glob.glob("D:\\Benisha\\Battery DCA\\IITM data\\iitm_driving_charging_data\\iitm\\*")

file_path='\\'.join(files1[0].split('\\')[0:-1])
folder_path='\\'.join(files1[0].split('\\')[0:-2])

Chg_folder_path=folder_path+'\\Charging_timestates_files'
DChg_folder_path=folder_path+'\\Discharging_timestates_files'
Chg_summary_path=folder_path+'\\Charging_Summary_files'
DChg_summary_path=folder_path+'\\Discharging_Summary_files'
Combined_summary_path=folder_path+'\\Combined_Summary_files'

#%%
folders=[Chg_folder_path,DChg_folder_path,Chg_summary_path,DChg_summary_path,Combined_summary_path]
for x in folders:
    if not os.path.exists(x):
        os.makedirs(x)


#%%
for i in range(0, len(files1)):
    f1=files1[i].split('\\')
    l1.append(f1[-1])


#%%

for j in l1:
    
    Chg_path=glob.glob(file_path+"\\"+j+"\\charging*.*.*.tsv")
    DChg_path=glob.glob(file_path+"\\"+j+"\\driving*.*.*.tsv")

    
#%%
    
    Chg_file_s=[pd.read_csv(f,header=0,sep='\t',index_col=False,error_bad_lines=False) for f in Chg_path if os.path.getsize(f)>0]
    DChg_file_s=[pd.read_csv(f,header=0,sep='\t',error_bad_lines=False,index_col=False) for f in DChg_path if os.path.getsize(f)>0]
    
    
#%%
    try:
        Chg_file=pd.concat(Chg_file_s, ignore_index=True)
        DChg_file=pd.concat(DChg_file_s,ignore_index=True)
        times_chg=timestates(Chg_file,file_path+"\\"+j,'Charging',Chg_folder_path,Chg_summary_path)
        times_dchg=timestates(DChg_file,file_path+"\\"+j,'Driving',DChg_folder_path,DChg_summary_path)
        
#%%   
        if ((times_chg=='Stop') or (times_dchg=='Stop')):
            del Chg_file,DChg_file
            pass
        else:
            timecheck_chg=timecheck(times_chg)
            timecheck_dchg=timecheck(times_dchg)
            
            combinedata(timecheck_chg, timecheck_dchg, Combined_summary_path, j)
            del Chg_file,DChg_file
    except ValueError:
        pass
      



print('-----------%s seconds---------' % (time.time()-start1))