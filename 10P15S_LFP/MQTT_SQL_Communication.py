# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 09:52:45 2023

@author: IITM
"""

#%% Pre-existing(modified) code

import paho.mqtt.client as mqtt
import mysql.connector

broker_address = "192.168.1.3"
topic="Bpack1/#"
# topic="/$SYS/#"

#%%

mydb=mysql.connector.connect(host='localhost',user='root',password='root')
db_cursor=mydb.cursor()

try:
    db_cursor.execute("CREATE DATABASE testdatabase")
except:
    pass

db_cursor.execute('USE testdatabase;')
mydb.commit() # for real time updation of values in tables in database (tables are created realtime without commit; but value assignment needs commit to view changes in real time-changes are made, but they will not be visible immediately without the commit statement)

#%%

# db_cursor.execute('CREATE TABLE test2(col2 varchar(255), col3 float);')
# mydb.commit()

# #%%
# db_cursor.execute('CREATE TABLE %s(%s %s, %s %s);' % ('test4','col1','varchar(255)','col2','int')) # also works
# mydb.commit()
# #%%
# db_cursor.execute('INSERT INTO test2 (%s,%s) VALUES (%s,%s)' % ('col2','col3','hello',1.2))
# mydb.commit()
# #%% Passing Mean values to the database
# # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))

#     # Subscribing in on_connect() means that if we lose the connection and
#     # reconnect then subscriptions will be renewed.
#     client.subscribe(topic)
# global name
# name='cell_V'

# bus=''
# columns=''

# # The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     global name,bus,columns
#     payload=[float(i) for i in msg.payload.decode().split(',')]
#     mean=sum(payload)/len(payload)
#     try:
#         db_cursor.execute('CREATE TABLE %s(ID int NOT NULL PRIMARY KEY AUTO_INCREMENT);' % (msg.topic.split('/')[1]))
#     except:
#         pass
#     try:
#         db_cursor.execute('ALTER TABLE %s ADD %s varchar(255);' % (msg.topic.split('/')[1],msg.topic.split('/')[2]))
#     except:
#         pass
#     if msg.topic.split('/')[1]==name:
#         bus=bus+','+str(mean)
#         columns=columns+','+str(msg.topic.split('/')[2])
#         # voltage_bus.append(msg.payload.decode().split(','))
#     else:
#         print('INSERT INTO {}({}) VALUES ({})'.format(name,columns[1:],bus[1:])) # to see the actual command being executed
#         db_cursor.execute('INSERT INTO {}({}) VALUES ({})'.format(name,columns[1:],bus[1:])) # last value msg.payload.decode().split(',')[-1]
#         bus=''
#         columns=''
#         bus=bus+','+str(mean)
#         columns=columns+','+str(msg.topic.split('/')[2])        
#     # elif msg.topic.split('/')[1]=='temp':
#     #     temp_bus.append(msg.payload.decode().split(','))
#     # elif msg.topic.split('/')[1]=='States':
#     #     state_bus.append()
#     # db_cursor.execute('INSERT INTO %s (%s) VALUES (%s)' % (msg.topic.split('/')[1],msg.topic.split('/')[2],msg.payload.decode().split(',')[-1]))
#     # mean=sum(msg.payload.decode().split(','))/len(msg.payload.decode().split(','))
#     # db_cursor.execute('INSERT INTO %s (%s) VALUES (%s)' % (msg.topic.split('/')[1],msg.topic.split('/')[2],mean)) # last value msg.payload.decode().split(',')[-1]
#     # print(msg.topic.split('/')[2])
#     # print(len(msg.payload.decode().split(','))) # len() works
#     print(msg.topic+" "+str(msg.payload.decode()))
#     print('-----')
#     name=msg.topic.split('/')[1]

# client = mqtt.Client("Python Client")
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect(broker_address)
# # client.loop_start()

# # Blocking call that processes network traffic, dispatches callbacks and
# # handles reconnecting.
# # Other loop*() functions are available that give a threaded interface and a
# # manual interface.
# # client.loop_stop()
# client.loop_forever()

#%% Passing complete values to the database
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)
global name
name='cell_V'

bus=''
columns=''

# The callback for when a PUBLISH message is received from the server.
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
        # voltage_bus.append(msg.payload.decode().split(','))
    else:
        print('INSERT INTO {}({}) VALUES ({})'.format(name,columns[1:],bus[1:])) # to see the actual command being executed
        db_cursor.execute('INSERT INTO {}({}) VALUES ({})'.format(name,columns[1:],bus[1:])) # last value msg.payload.decode().split(',')[-1]
        bus=''
        columns=''
        bus=bus+','+'"'+msg.payload.decode()+'"'
        columns=columns+','+str(msg.topic.split('/')[2])        
    # elif msg.topic.split('/')[1]=='temp':
    #     temp_bus.append(msg.payload.decode().split(','))
    # elif msg.topic.split('/')[1]=='States':
    #     state_bus.append()
    # db_cursor.execute('INSERT INTO %s (%s) VALUES (%s)' % (msg.topic.split('/')[1],msg.topic.split('/')[2],msg.payload.decode().split(',')[-1]))
    # mean=sum(msg.payload.decode().split(','))/len(msg.payload.decode().split(','))
    # db_cursor.execute('INSERT INTO %s (%s) VALUES (%s)' % (msg.topic.split('/')[1],msg.topic.split('/')[2],mean)) # last value msg.payload.decode().split(',')[-1]
    # print(msg.topic.split('/')[2])
    # print(len(msg.payload.decode().split(','))) # len() works
    print(msg.topic+" "+str(msg.payload.decode()))
    print('-----')
    name=msg.topic.split('/')[1]

client = mqtt.Client("Python Client")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address)
# client.loop_start()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_stop()
client.loop_forever()
#%% Read data from database
import pandas as pd
import sqlalchemy

engine=sqlalchemy.create_engine("mysql+mysqlconnector://root:root@localhost/testdatabase")

V=pd.read_sql_table(table_name='cell_v',con=engine)
T=pd.read_sql_table(table_name='temp',con=engine)
S=pd.read_sql_table(table_name='states',con=engine)

#%%
V=V.drop(columns='ID')
T=T.drop(columns='ID')
S=S.drop(columns='ID')
#%%
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
#%% create sql database Own code-testing
# import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",password="root" 
#     )

# mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE testdatabase")

#%% GPT solution
# import mysql.connector
# import paho.mqtt.client as mqtt

# # MQTT Settings
# broker_address = "192.168.1.3"
# topic = "Bpack1/#"

# # MySQL Database Connection
# db_connection = mysql.connector.connect(
#   host="localhost",
#   user="root",password="root" 
#     )

# db_cursor = db_connection.cursor()

# # Create a table to store the received data if it doesn't exist
# db_cursor.execute('USE testdatabase;')
# db_connection.commit()

# # Callback function when MQTT message is received
# def on_message(client, userdata, message):
#     # print(f"Received message: {message.payload.decode()}")
#     print(message.topic+" "+str(message.payload.decode()))
#     # Store received message in the MySQL database
#     # db_cursor.execute('''
#     #     INSERT INTO sensor_data (topic, message)
#     #     VALUES (%s, %s)
#     # ''', (message.topic, message.payload.decode()))
#     # db_connection.commit()

# # MQTT Client Setup
# client = mqtt.Client("Python_Client")
# client.on_message = on_message

# # Connect to MQTT broker
# client.connect(broker_address)
# client.subscribe(topic)

# # Start the MQTT loop
# client.loop_forever()

# #%% SO

# import mysql.connector
# import paho.mqtt.client as mqtt
# import ssl

# mysql_connection = mysql.connector.connect(user='root', password='root', database='testdatabase')
# cursor = mysql_connection.cursor()

# # MQTT Settings 
# MQTT_Broker = "mqtt.eclipse.org"
# MQTT_Port = 1883
# Keep_Alive_Interval = 60
# MQTT_Topic = "Bpack1/#" #Bpack1/States


# # Subscribe
# def on_connect(client, userdata, flags, rc):
#   mqttc.subscribe(MQTT_Topic) #,0

# def on_message(mosq, obj, msg):
#   # Prepare Data, separate columns and values
#   msg_clear = msg.payload.translate(None, '{}""').split(", ")
#   msg_dict =    {}
#   for i in range(0, len(msg_clear)):
#     msg_dict[msg_clear[i].split(": ")[0]] = msg_clear[i].split(": ")[1]

#   # Prepare dynamic sql-statement
#   placeholders = ', '.join(['%s'] * len(msg_dict))
#   columns = ', '.join(msg_dict.keys())
#   sql = "INSERT INTO pws ( %s ) VALUES ( %s )" % (columns, placeholders)

#   # Save Data into DB Table
#   try:
#       cursor.execute(sql, msg_dict.values())
#   except mysql.connector.Error as error:
#       print("Error: {}".format(error))
#   mysql.connector_connection.commit()

# def on_subscribe(mosq, obj, mid, granted_qos):
#   pass

# mqttc = mqtt.Client()

# # Assign event callbacks
# mqttc.on_message = on_message
# mqttc.on_connect = on_connect
# mqttc.on_subscribe = on_subscribe

# # Connect
# # mqttc.tls_set(ca_certs="ca.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
# mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

# # Continue the network loop & close db-connection
# mqttc.loop_forever()
# mysql_connection.close()