# -*- coding: utf-8 -*-
"""
Created on Fri Dec 1 09:23:20 2023

@author: IITM
"""
#%% Read data from database
import pandas as pd
import sqlalchemy

engine=sqlalchemy.create_engine("mysql+mysqlconnector://root:root@localhost/testdatabase")
# Sqlalchemy format for mysql engine: "mysql+mysqlconnector://<password>:<user>@<host_name>/<database_name>"
# Pandas library supports sqlalchemy for dealing with mysql data, so sqlalchemy was selected.

V=pd.read_sql_table(table_name='cell_v',con=engine)
T=pd.read_sql_table(table_name='temp',con=engine)
S=pd.read_sql_table(table_name='states',con=engine)

#%% ID columns are not useful in providing any information; Also their format is different from the other columns; 
# Hence they are dropped
V=V.drop(columns='ID')
T=T.drop(columns='ID')
S=S.drop(columns='ID')
#%% Separating the comma separated values into individual entries
# In the database, the data is stored in sucha way that each entry has 10 values
# These values are separated by commas
# In this section, we separate them and include them in a new dataframe file as individual row entries

l=[]
for n in V.columns:
    l.append(','.join(str(i) for i in V[n])) 

V_data=pd.DataFrame(index=range(len(l[0].split(','))))

for i,n in enumerate(V.columns):
    V_data[n]=l[i].split(',')
    
#%%
l=[]
for n in T.columns:
    l.append(','.join(str(i) for i in T[n])) 

T_data=pd.DataFrame(index=range(len(l[0].split(','))))

for i,n in enumerate(T.columns):
    T_data[n]=l[i].split(',')

#%%
l=[]
for n in S.columns:
    l.append(','.join(str(i) for i in S[n])) 

S_data=pd.DataFrame(index=range(len(l[0].split(','))))

for i,n in enumerate(S.columns):
    S_data[n]=l[i].split(',')
