from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import DESCENDING
from datetime import datetime, timedelta
from gridfs import GridFS
import pandas as pd
import pymongo

def uploadData(client, dbName, collection_name, data):
    db = client[dbName]

    # Get the reference to the collection and upload the data
    collection_ref = db[collection_name]
    id = collection_ref.insert_one(data)
    print(f"Data uploaded with id: {id}")
    return id


def connectToDB(username, password):
    connection_string = f"mongodb+srv://{username}:{password}@cluster0.qgruyjo.mongodb.net/?retryWrites=true&w=majority"
    
    # Create a new client and connect to the server
    client = MongoClient(connection_string, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)


def download_image_from_mongodb(client, file_id, db_name, collection_name, output_path):
    # Connect to the specified database
    db = client[db_name]
    
    # Initialize GridFS
    fs = GridFS(db, collection=collection_name)
    
    # Find the file by its ID
    file_data = fs.get(file_id)
    
    # Write the file data to the specified output path
    with open(output_path, 'wb') as output_file:
        output_file.write(file_data.read())
    
    print(f"Image downloaded from MongoDB and saved to: {output_path}")


def get_data_last_24_hours(client, db_name, collection_name):
    # Set up your MongoDB connection
    db = client[db_name]
    collection = db[collection_name]

    # Calculate the timestamp for 24 hours ago
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)

    # Query the database to retrieve data created or modified in the last 24 hours
    query = {"timestamp": {"$gte": twenty_four_hours_ago}}
    
    # Execute the query and fetch the results
    result = list(collection.find(query))

    # Process and return the result as needed
    return result


def get_latest_timestamp(client, analyze_db_name, clean_data_collection):
    analyze_db = client[analyze_db_name]
    clean_data_col = analyze_db[clean_data_collection]
    
    # Find the document with the latest timestamp
    latest_data = clean_data_col.find_one(sort=[("timestamp", DESCENDING)])
    
    if latest_data:
        return latest_data["timestamp"]
    else:
        # If no data is found, return a default timestamp (you may adjust this based on your requirements)
        return datetime(2000, 1, 1)


def round_timestamp_to_whole_number(timestamp):
    return int(timestamp.timestamp())

def get_data_last_hour(client, db_name, collection_name):
    db = client[db_name]
    collection = db[collection_name]

    one_hour_ago = datetime.utcnow() - timedelta(hours=1)


    # Round the timestamp to remove the decimal part
    rounded_timestamp = round_timestamp_to_whole_number(one_hour_ago)
    data = list(collection.find().sort([("timestamp", pymongo.ASCENDING)]))

    # Convert data to pandas DataFrame
    df = pd.DataFrame(data)
    # Query for documents with timestamps greater than or equal to the rounded timestamp
    cursor = collection.find({"timestamp": {"$gte": rounded_timestamp}})

    # Convert cursor data to Pandas DataFrame
    #df = pd.DataFrame(list(cursor))

    # Print or process the DataFrame as needed
    print(df)
