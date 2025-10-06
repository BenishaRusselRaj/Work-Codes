# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 12:20:13 2021

@author: IITM
"""

import pickle
import glob
import time
start=time.time()
files=glob.glob("D:\\Benisha\\SoH_NN\\Data\\PHY\\OCV_StatesOnly_Phy\\*.pkl")
for f1 in files:
    path=f1.rsplit('.',1)[0]
    with open(f1,'rb') as f:
        data = pickle.load(f)
        data.to_csv(path+".csv")

print('--------------%s seconds------------' % (time.time()-start))      