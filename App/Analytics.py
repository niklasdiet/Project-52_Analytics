from pymongo import ASCENDING
import pandas as pd
import matplotlib.pyplot as plt
from MongoDBFunctions import *
import configparser
import time


def getTimeframe(collection, start, end = (time.time()*1000)):
    query = {"timestamp": {"$gte": start, "$lte": end}}
    data = list(collection.find(query).sort([("timestamp", ASCENDING)]).allow_disk_use(True))
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp']/1000, unit='s')
    return df



def mainPlotter(devices, sensor_readings, df):
    colors = ['blue', 'red', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'black', 'gray']

    plt.figure(figsize=(8, 8))

    for i, reading in enumerate(sensor_readings):
        plt.subplot(2, 2, i + 1)
        for j, device in enumerate(devices):
            device_df = df[df['device_id'] == device]

            # Check if the DataFrame is not empty before plotting
            if not device_df.empty:
                plt.plot(device_df['timestamp'], device_df[reading], label=f'{device} - {reading.capitalize()}', color=colors[j])
            else:
                print(f"No data available for {device} - {reading.capitalize()}")

        plt.xlabel('Timestamp')
        plt.ylabel(reading.capitalize())
        plt.title(f'{reading.capitalize()} Data Visualization')
        plt.legend()

    plt.tight_layout()
    plt.show()


config = configparser.ConfigParser()
config.read('Keys.cfg')
cfgM = config['MONGODB']
cfgMA = config['MONGODBANALYTICS']
    
client = connectToDB(cfgM['username'], cfgM['password'])
collection1 = getCollection(client, cfgM['database_name'], 'sensorData')
collection2 = getCollection(client, cfgMA['database_name'], 'sensorData')


# Define devices and colors
devices = ['hub0001', 'pico00001', 'pico00002', 'pico00003']

# Define sensor readings
sensor_readings = ['pressure', 'temperature', 'humidity', 'moisture']
data = getTimeframe(collection1, 1708453690000)#1701542714000)
mainPlotter(devices, sensor_readings, data)


