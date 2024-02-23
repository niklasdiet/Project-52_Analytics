import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from MongoDBFunctions import *
import configparser
from datetime import datetime, timedelta

# MongoDB connection parameters
mongo_collection = 'sensorData'

config = configparser.ConfigParser()
config.read('Keys.cfg')
cfgM = config['MONGODB']

client = connectToDB(cfgM['username'], cfgM['password'])
db = client[cfgM['database_name']]
collection = db[mongo_collection]

# Get data with timestamp greater than 1700000000
query = {"timestamp": {"$gt": 1700000000}}
data = list(collection.find(query).sort([("timestamp", pymongo.ASCENDING)]))

# Convert data to pandas DataFrame
df = pd.DataFrame(data)

# Convert timestamp to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# Define devices and colors
devices = ['hub0001', 'pico00001', 'pico00002', 'pico00003']
colors = ['black', 'blue', 'orange', 'green']

# Define sensor readings
sensor_readings = ['pressure', 'temperature', 'humidity', 'gas', 'moisture', 'moisture_raw']

# Plotting
plt.figure(figsize=(8, 8))

for i, reading in enumerate(sensor_readings):
    plt.subplot(2, 3, i + 1)
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