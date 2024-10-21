from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select the database and collection
db = client['Deliveries']  # Replace 'mydatabase' with your database name
url_collection = db['ImageLinks']  # Replace 'urlCollection' with your collection name
counters_collection = db['counters']  # Collection to store the counter

# Step 1: Initialize the counter (Run this once)
def initialize_counter():
    if counters_collection.count_documents({'_id': 'urlid'}) == 0:
        counters_collection.insert_one({
            '_id': 'urlid',
            'sequence_value': 0
        })

# Step 2: Function to get the next sequence value
def get_next_sequence_value(sequence_name):
    sequence_document = counters_collection.find_one_and_update(
        {'_id': sequence_name},
        {'$inc': {'sequence_value': 1}},
        return_document=True
    )
    return sequence_document['sequence_value']

# Step 3: Insert document with auto-incremented _id
def insert_url_document(url):
    new_id = get_next_sequence_value('urlid')  # Get the next sequence value
    doc = {
        '_id': new_id,
        'url': url
    }
    url_collection.insert_one(doc)  # Insert the document
    print(f"Inserted document: {doc}")
    return doc['_id']

# Initialize counter if not already present
initialize_counter()

# Example usage: Inserting a URL

