# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 13:16:41 2022

@author: IITM
"""
"""
DESCRIPTION:

[OPTIONAL STEP] 

If the file of the same cell are separated into different files due to the size concern, run this code to combine the summary files into one **BEFORE** manipulating the SoH data to smoothen it

The input to this code is the SoH smoothened summary files from the SoH_data_manipulation code
Put all the files needed to be concatenated in a single folder, and you get the output saved automatically in the same folder

THINGS TO NOTE:
--------Change the filename in the last "df.to_csv" line as required------
If you want the files to be concatenated in a particular order, then rename and save them accordingly in the folder, before running this code
This code is to merge the csv files of the same type of cell, last step before training/testing data using NN

"""


import pandas as pd
import glob

#%%
files=glob.glob("D:\\Benisha\\SoH_NN\\Data\\BRD\\SoH Summary Files\\*.csv")
df=pd.DataFrame()

for f in files:
    d1=pd.read_csv(f)
    df=pd.concat([df,d1])
    
# df.to_csv(files[0].rsplit('\\',1)[0]+'\\'+f.split('\\',7)[6]+'_AllCycles_Timestates_added_soh_summary.csv')
df.to_csv(files[0].rsplit('\\',1)[0]+'\\BRD_AllCells_AllCycles_Timestates_added_soh_summary.csv')