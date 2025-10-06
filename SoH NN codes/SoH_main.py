# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 15:43:34 2021

@author: IITM
"""

#%% Importing necessary libraries
import time
import glob
import pandas as pd
import os
import sys
from SoH_Add_Timestates_where import timestates
from SoH_Delete_Duplicated_data import timecheck
from SoH_Combine_Pack_data import combinedata

#%%
start1=time.time()

#%% Path to files are added
sys.path.append("D:\\Benisha\\SoH_NN\\Codes") # add the path to the code files here

l1=[]; l2=[]; l0=[]
files1= glob.glob("D:\\Benisha\\SoH_NN\\Data\\iitm\\*")
files2= glob.glob("D:\\Benisha\\SoH_NN\\Data\\iitm\\*")

Chg_file_path='\\'.join(files1[0].split('\\')[0:-1])
DChg_file_path='\\'.join(files2[0].split('\\')[0:-1])

#%% 
Chg_times_path='\\'.join(files1[0].split('\\')[0:-2])+'\\Charging_Files_Added Timestates'
Dchg_times_path='\\'.join(files1[0].split('\\')[0:-2])+'\\Discharging_Files_Added Timestates'
Chg_summary_path='\\'.join(files1[0].split('\\')[0:-2])+'\\Charging_Files_Session Summary'
Dchg_summary_path='\\'.join(files1[0].split('\\')[0:-2])+'\\Discharging_Files_Session Summary'
Combined_summary_path='\\'.join(files1[0].split('\\')[0:-2])+'\\Combined_Summary'

#%%
for i in range(0, len(files1)):
    f1=files1[i].split('\\')
    l1.append(f1[-1])

for i in range(0, len(files2)):
    f2=files2[i].split('\\')
    l2.append(f2[-1])
    
for i in l1:
    if (i in l2):
        l0.append(i)

#%% Create new folders to save the files separately
if not os.path.exists(Chg_times_path):
    os.makedirs(Chg_times_path)
if not os.path.exists(Dchg_times_path):
    os.makedirs(Dchg_times_path)
if not os.path.exists(Chg_summary_path):
    os.makedirs(Chg_summary_path)
if not os.path.exists(Dchg_summary_path):
    os.makedirs(Dchg_summary_path)
if not os.path.exists(Combined_summary_path):
    os.makedirs(Combined_summary_path)
    
#%% 
for i in l0:
    Chg_path=glob.glob(Chg_file_path+"\\"+i+"\\charging_*.tsv")
    DChg_path=glob.glob(DChg_file_path+"\\"+i+"\\driving_*.tsv")
    
    Chg_file_s=[pd.read_csv(f,header=0,sep='\t',index_col=False,error_bad_lines=False) for f in Chg_path if os.path.getsize(f)>0]
    DChg_file_s=[pd.read_csv(f,header=0,sep='\t',error_bad_lines=False,index_col=False) for f in DChg_path if os.path.getsize(f)>0]
    
#%%       
    try:
        Chg_file=pd.concat(Chg_file_s,ignore_index=True)
        DChg_file=pd.concat(DChg_file_s,ignore_index=True) 
    #%%
        Chg_file['voltage']=Chg_file['voltage'].shift(-1)
        Chg_file['current']=Chg_file['current'].shift(-1)
#%%       
        Chg_file=Chg_file.dropna(subset=['C0'])
        Chg_file=Chg_file.reset_index(drop=True)
        
        DChg_file=DChg_file.dropna(subset=['C0'])
        DChg_file=DChg_file.reset_index(drop=True)
        
        if (len(Chg_file)==0 or len(DChg_file)==0):
            pass
        else: 
            times_chg=timestates(Chg_file,Chg_times_path,Chg_summary_path,i)
            times_dchg=timestates(DChg_file,Dchg_times_path,Dchg_summary_path,i)
        
            timecheck_chg=timecheck(times_chg,Chg_summary_path,i)
            timecheck_dchg=timecheck(times_dchg,Dchg_summary_path,i)
            
            combinedata(timecheck_chg, timecheck_dchg,Combined_summary_path)

    except ValueError:
        pass


print('-----------%s seconds---------' % (time.time()-start1))