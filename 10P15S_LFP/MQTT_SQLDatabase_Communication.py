# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 09:52:45 2023

@author: IITM
"""

#%% Pre-existing(modified) code

import paho.mqtt.client as mqtt
import mysql.connector

broker_address = "192.168.1.3" #IP addr.
topic="Bpack1/#" # Topic name; Visible in the mqtt broker interface

#%%

mydb=mysql.connector.connect(host='localhost',user='root',password='root') # Establishing a connection
db_cursor=mydb.cursor() # cursor is needed to pass any commands to the mysql interface

try:
    db_cursor.execute("CREATE DATABASE Bpack_database") # creates a database if not already present
except:
    pass

db_cursor.execute('USE Bpack_database;') # selecting the database
mydb.commit() # for real time updation of values in tables in database (tables are created realtime without commit; but value assignment needs commit to view changes in real time-changes are made, but they will not be visible immediately without the commit statement)


#%% Passing complete values to the database
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe(topic)
global name
name='cell_V'

bus=''
columns=''

def on_message(client, userdata, msg):
    global name,bus,columns
    try:
        db_cursor.execute('CREATE TABLE %s(ID int NOT NULL PRIMARY KEY AUTO_INCREMENT);' % (msg.topic.split('/')[1]))
    except:
        pass
    try:
        db_cursor.execute('ALTER TABLE %s ADD %s varchar(255);' % (msg.topic.split('/')[1],msg.topic.split('/')[2]))
    except:
        pass
    if msg.topic.split('/')[1]==name:
        bus=bus+','+'"'+msg.payload.decode()+'"'
        columns=columns+','+str(msg.topic.split('/')[2])
    else:
        print('INSERT INTO {}({}) VALUES ({})'.format(name,columns[1:],bus[1:])) # to see the actual command being executed
        db_cursor.execute('INSERT INTO {}({}) VALUES ({})'.format(name,columns[1:],bus[1:]))
        bus=''
        columns=''
        bus=bus+','+'"'+msg.payload.decode()+'"'
        columns=columns+','+str(msg.topic.split('/')[2])        
    print(msg.topic+" "+str(msg.payload.decode()))
    print('-----')
    name=msg.topic.split('/')[1]

client = mqtt.Client("Python Client")
client.on_connect = on_connect # calls back to on_connect function
client.on_message = on_message # calls back to on_message function

client.connect(broker_address)
client.loop_forever()
