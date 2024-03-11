from MongoDBFunctions import *
import configparser
import threading
import time

MAX_THREADS = 4

def getInfoEveryFiveMinutes():
    from bson import ObjectId
    print("Start")
    collection = getCollection(client, cfgM['database_name'], "sensorData")

    threshold_timestamp = 1704107514000

    # Iterate through every document in the collection
    for document in collection.find({"timestamp": {"$lt": threshold_timestamp}}):

        # Get the ObjectId from the document
        object_id = document["_id"]

        # Extract the timestamp from the ObjectId
        timestamp = ObjectId(object_id).generation_time.timestamp()
        ts_new = int(timestamp)
        if int(timestamp) <= 2000000000:
            ts_new = timestamp * 1000
        print(ts_new)
        collection.update_one({"_id": object_id}, {"$set": {"timestamp": ts_new}})


    print("Timestamps updated successfully.")



def timer_thread():
    print("Starting Threads...")
    thread_number = 1
    while True:
        print(threading.active_count() - 1)
        if threading.active_count() - 1 < MAX_THREADS:  # Subtract 1 to exclude the timer thread
            threading.Thread(target=getInfoEveryFiveMinutes).start()
            thread_number += 1

        time.sleep(10000)  # Check every minute


if __name__ == "__main__":
    print("Starting App...")
    # get keys
    config = configparser.ConfigParser()
    config.read('Keys.cfg')
    cfgM = config['MONGODB']
    client = connectToDB(cfgM['username'], cfgM['password'])
    #get_data_last_hour(client, "Project52", "sensorData")
    #getInfoEveryFiveMinutes()
    threading.Thread(target=timer_thread).start()





# prepare data 

# reduze data points and move it over to other db
    
# get further info 
    
