# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 10:23:27 2022

@author: IITM
"""

import pandas as pd
import os
import time
start=time.time()

#%%
f="D:\\Benisha\\SoH_NN\\Data\\BRD\\Sample 3.2\\BRD_3.2_25Deg_AllCycles_AllCycles_raw.csv"
data=pd.read_csv(f)

data=data.reset_index(drop=True)

#%%
a=len(data)//2
i=a//2
j=a+((len(data)-a)//2)
print('1/3............')
#%%
d1=data[:i]
d2=data[i:a]
d3=data[a:j]
d4=data[j:]

print('2/3............')
#%%
fin_path=f.rsplit('\\',1)[0]+'\\'+f.rsplit('\\',1)[1].rsplit('_',4)[0]
if not os.path.exists(fin_path):
    os.makedirs(fin_path)
    

filename=f.rsplit('\\',1)[1].rsplit('.',1)[0]

print('3/3............')
#%%
d1.to_csv(fin_path+'\\'+filename+'_1.csv')
d2.to_csv(fin_path+'\\'+filename+'_2.csv')
d3.to_csv(fin_path+'\\'+filename+'_3.csv')
d4.to_csv(fin_path+'\\'+filename+'_4.csv')

print('---------------%s seconds---------------' %(time.time()-start))