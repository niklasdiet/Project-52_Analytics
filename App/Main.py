from MongoDBFunctions import *
import configparser
import threading
import time

MAX_THREADS = 4

def getInfoEveryFiveMinutes():
    print('Test')


def timer_thread():
    print("Starting Threads...")
    thread_number = 1
    while True:
        if threading.active_count() - 1 < MAX_THREADS:  # Subtract 1 to exclude the timer thread
            current_time = time.localtime()
            current_minutes = current_time.tm_min

            # Check if the current minutes is at the end of 5 or 0
            if current_minutes % 5 == 0:
                threading.Thread(target=getInfoEveryFiveMinutes).start()
                thread_number += 1

        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    print("Starting App...")
    # get keys
    config = configparser.ConfigParser()
    config.read('Keys.cfg')
    cfgM = config['MONGODB']
    client = connectToDB(cfgM['username'], cfgM['password'])
    #get_data_last_hour(client, "Project52", "sensorData")

    #threading.Thread(target=timer_thread).start()
    from bson import ObjectId
    from datetime import datetime

    # Connect to MongoDB
    db = client["Project52"]
    collection = db["sensorData"]

    threshold_timestamp = 1700000000

    # Iterate through every document in the collection
    for document in collection.find({"timestamp": {"$lt": threshold_timestamp}}):
        # Get the ObjectId from the document
        object_id = document["_id"]

        # Extract the timestamp from the ObjectId
        timestamp = ObjectId(object_id).generation_time.timestamp()

        # Update the "timestamp" field in the document
        collection.update_one({"_id": object_id}, {"$set": {"timestamp": timestamp}})


    print("Timestamps updated successfully.")