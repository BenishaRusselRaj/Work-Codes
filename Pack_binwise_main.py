# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 18:59:52 2020

@author: IITM
"""
"""
Use this when chg and dchg files are in separate folders having bin numbers of their own

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

l1=[]; l2=[]
files1= glob.glob("D:\\Benisha\\Battery DCA\\Zomato\\zomato_charging_data\\zomato\\*")
files2= glob.glob("D:\\Benisha\\Battery DCA\\Zomato\\Zomato Driving\\Zomato\\*")

Chg_file_path='\\'.join(files1[0].split('\\')[0:-1])
DChg_file_path='\\'.join(files2[0].split('\\')[0:-1])

#%%
for i in range(0, len(files1)):
    f1=files1[i].split('\\')
    l1.append(f1[-1])


for i in range(0, len(files2)):
    f2=files2[i].split('\\')
    l2.append(f2[-1])

#%%

for i in l1:
    if (i in l2):
        Chg_path=glob.glob(Chg_file_path+"\\"+i+"\\*.*.*.tsv")
        DChg_path=glob.glob(DChg_file_path+"\\"+i+"\\*.*.*.tsv")

        Chg_file_s=[pd.read_csv(f,header=0,sep='\t',index_col=False,error_bad_lines=False) for f in Chg_path if os.path.getsize(f)>0]
        DChg_file_s=[pd.read_csv(f,header=0,sep='\t',error_bad_lines=False,index_col=False) for f in DChg_path if os.path.getsize(f)>0]
        
        try:
            Chg_file=pd.concat(Chg_file_s, ignore_index=True)
            DChg_file=pd.concat(DChg_file_s,ignore_index=True)
        except ValueError:
            pass
        
        times_chg=timestates(Chg_file,Chg_file_path+"\\"+i)
        times_dchg=timestates(DChg_file,DChg_file_path+"\\"+i)
        
        if ((times_chg=='Stop') or (times_dchg=='Stop')):
            pass
        else:
            timecheck_chg=timecheck(times_chg)
            timecheck_dchg=timecheck(times_dchg)
            
            combinedata(timecheck_chg, timecheck_dchg)
    else:
        pass
print('-----------%s seconds---------' % (time.time()-start1))