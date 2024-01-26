# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 09:40:56 2024

@author: School Account
"""

import requests
'''print(requests.__version__)'''
import json
import pandas as pd
from datetime import datetime
import datetime as dt
from time import sleep
import pytz
import mysql.connector
import pathlib

'''
NPS = requests.get('https://sv-api.nps100.com/api/v1/wtg1536/', headers={'Authorization':'Token f8641c4daea06763ca6cdf46dbaeea40ee250dec'})
print(NPS)
data = json.loads(NPS.content)
print(data)

tmpdf = pd.json_normalize(data, meta=['timestamp','wind_speed','power','energy','yaw_position','yaw_delta','temp_amb','turbine_state','dispatch_enable','env_condition'])
print(tmpdf)
'''
#Normalize time
italyTime = pytz.timezone("CET") 
oldMin = -1
i = 0
j=0
saveFrequency = 120
uploadFrequency = 5
histWindData = pd.DataFrame()
newWindData = pd.DataFrame()
saveFileName = 'na'
continueLoop = True
currentTime = datetime.now(italyTime)
print(currentTime)
currentMin = currentTime.strftime('%M')
currentMin = int(currentMin)
oldMin = currentMin

while continueLoop:
    italyTime = pytz.timezone("CET")  
    currentTime = datetime.now(italyTime)
    time_change = dt.timedelta(seconds=15) 
    currentTime = currentTime + time_change
    currentMin = currentTime.strftime('%M')
    currentMin = int(currentMin)

    if not (currentMin == oldMin):
        i = i+1
        j=j+1
        oldMin = currentMin
        try:
            NPS = requests.get('https://sv-api.nps100.com/api/v1/wtg1536/', headers={'Authorization':'Token f8641c4daea06763ca6cdf46dbaeea40ee250dec'})
            #print(NPS)
        except: 
            print("data not collected")
            pass
        data = json.loads(NPS.content)

        tmpdf = pd.json_normalize(data, meta=['timestamp','wind_speed','power','energy','yaw_position','yaw_delta','temp_amb','turbine_state','dispatch_enable','env_condition'])
        print(tmpdf)
        histWindData = pd.concat([histWindData, tmpdf])
        newWindData = pd.concat([newWindData, tmpdf])

    if (i==saveFrequency):
        print('Saving dataframe')
        tmpTime = currentTime.strftime('%y-%m-%d-%H-%M')
        tmpTime = str(tmpTime)
        saveFileName = (r"M:\\MLEPS\\windDashboard\\" + tmpTime + '.csv')
        #print(saveFileName)
        try:  
            histWindData.to_csv(saveFileName)
            print("Saved")
        except:
            print('Data not written')
        i=0
         
    if (j==uploadFrequency):
        print("Uploading")
        database = mysql.connector.connect(
            username = 'root',
            password = 'WartN52206.!.',
            host =  'localhost',
            )
        mycursor = database.cursor()
        
        #windDict = windData.to_dict(orient='list')
        
        for idx, row in newWindData.iterrows():
            sql = "INSERT INTO wind_data.wind_table(timestamp, wind_speed, power, energy, yaw_position, yaw_delta, temp_amb, turbine_state, dispatch_enable, env_condition) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = [row['timestamp'], row['wind_speed'], row['power'], row['energy'], row['yaw_position'], row['yaw_delta'], row['temp_amb'], row['turbine_state'], row['dispatch_enable'], row['env_condition']]
            mycursor.execute(sql,val)
        database.commit()
        database.close()
        newWindData = pd.DataFrame()
        j=0
        
        
    sleep(5)
#https://www.youtube.com/watch?v=9VtkwH6iLL0