import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from MongoDBFunctions import *
import configparser

# MongoDB connection parameters
mongo_collection = 'sensorData'


config = configparser.ConfigParser()
config.read('Keys.cfg')
cfgW = config['WEATHER']
cfgM = config['MONGODB']


    
client = connectToDB(cfgM['username'], cfgM['password'])
db = client[cfgM['database_name']]
collection = db[mongo_collection]


# Get most recent image
#download_image_from_mongodb(client, "", db, "", "images/image.jpg")

# Fetch data from MongoDB
data = list(collection.find().sort([("timestamp", pymongo.ASCENDING)]))

# Convert data to pandas DataFrame
df = pd.DataFrame(data)

# Convert timestamp to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Define devices and colors
devices = ['pico00001', 'pico00002', 'pico00003']
colors = ['blue', 'orange', 'green']

# Define sensor readings
sensor_readings = ['pressure', 'temperature', 'humidity', 'gas', 'moisture', 'moisture_raw']

# Plotting
plt.figure(figsize=(8, 8))

for i, reading in enumerate(sensor_readings):
    plt.subplot(2, 3, i + 1)
    for j, device in enumerate(devices):
        device_df = df[df['device_id'] == device]
        plt.plot(device_df['timestamp'], device_df[reading], label=f'{device} - {reading.capitalize()}', color=colors[j])

    plt.xlabel('Timestamp')
    plt.ylabel(reading.capitalize())
    plt.title(f'{reading.capitalize()} Data Visualization')
    plt.legend()

plt.tight_layout()
plt.show()