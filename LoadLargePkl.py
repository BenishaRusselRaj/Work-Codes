import time
start=time.time()
import pickle
import pandas as pd
#with open("D:\\New folder (2)\\PHY\\PHY_4.1_25Deg_AllCycles_1147Cycles_processed_1.pkl",'rb') as f:
#    d1=pickle.load(f)
#with open("D:\\New folder (2)\\PHY\\PHY_4.1_25Deg_AllCycles_1147Cycles_processed_2.pkl",'rb') as f:
#    d2=pickle.load(f)
with open("D:\\New folder (2)\\PHY_6.1_25Deg_AllCycles_1092Cycles_OCV_StatesOnly_1.pkl",'rb') as f:
    d3=pickle.load(f)
with open("D:\\New folder (2)\\PHY_6.1_25Deg_AllCycles_1092Cycles_OCV_StatesOnly_2.pkl",'rb') as f:
    d4=pickle.load(f)
with open("D:\\New folder (2)\\PHY_6.1_25Deg_AllCycles_1092Cycles_OCV_StatesOnly_3.pkl",'rb') as f:
    d5=pickle.load(f)
d3=pd.concat([d3,d4,d5])
del d5
del d4
d3.to_pickle('PHY_6.1_25Deg_AllCycles_1092Cycles_OCV_StatesOnly.pkl')
print('------------%s seconds---------------' % (time.time()-start))
