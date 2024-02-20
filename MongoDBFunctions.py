from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import os
from gridfs import GridFS


def round_to_5_minutes(dt):
    # Round the minutes to the nearest 5
    rounded_minutes = (dt.minute // 5) * 5
    # Set seconds to 0
    dt = dt.replace(minute=rounded_minutes, second=0, microsecond=0)
    return dt



def uploadData(device, client, dbName, collection_name, d1, d2 = {}, d3 = {}):
    # Get the current time
    current_time = datetime.now()

    # Round to the nearest 5 minutes
    rounded_time = round_to_5_minutes(current_time)

    d4 = {"device": device, "time": rounded_time}
    data = d1 | d2 | d3 | d4
    
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


def upload_image_to_mongodb(client, image_path, db_name, collection_name, device_info):
    current_time = datetime.now()

    # Round to the nearest 5 minutes
    rounded_time = round_to_5_minutes(current_time)

    # Connect to the specified database
    db = client[db_name]
    
    # Initialize GridFS
    fs = GridFS(db, collection=collection_name)
    
    # Open the image file
    with open(image_path, 'rb') as image_file:
        # Create a document with additional metadata
        metadata = {
            'timestamp': rounded_time,
            'device_info': device_info
        }
        
        # Store the image and metadata in GridFS
        file_id = fs.put(image_file, filename=image_path, metadata=metadata)
    

    
    print(f"Image uploaded to MongoDB with file ID: {file_id}")
    os.remove(image_path)

    #return file_id

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

