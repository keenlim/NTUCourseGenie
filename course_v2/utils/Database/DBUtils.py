import os
import sys
from random import randint
import pymongo 
from dotenv import load_dotenv

load_dotenv(override=True)
CONNECTION_STRING = os.environ.get("MONGODB_HOST")

DB_NAME = "coursegenie"
COLLECTION_NAME = "users"

client = pymongo.MongoClient(CONNECTION_STRING)

# Check if the database exists with list_database_names method. If the database doesn't exist, use the create database extension command to create it with a specified provisioned throughput

# Create database if it doesn't exist
db = client[DB_NAME]
if DB_NAME not in client.list_database_names():
    # Create a database with 400 RU throughput that can be shared across
    # the DB's collections
    db.command({"customAction": "CreateDatabase", "offerThroughput": 400})
    print("Created db '{}' with shared throughput.\n".format(DB_NAME))
else:
    print("Using database: '{}'.\n".format(DB_NAME))

# Create Collection if it doesn't exist
collection = db[COLLECTION_NAME]
if COLLECTION_NAME not in db.list_collection_names():
    # Creates a unsharded collection that uses the DBs shared throughput
    db.command(
        {"customAction": "CreateCollection", "collection": COLLECTION_NAME}
    )
    print("Created collection '{}'.\n".format(COLLECTION_NAME))
else:
    print("Using collection: '{}'.\n".format(COLLECTION_NAME))


# Create an index
indexes = [
    {"key": {"_id": 1}, "name": "_id_1"},
    {"key": {"name": 2}, "name": "_id_2"}
]
db.command(
    {
        "customAction": "UpdateCollection",
        "collection": COLLECTION_NAME,
        "indexes": indexes,
    }
)
print("Indexes are: {}\n".format(sorted(collection.index_information())))

"""Create new document and upsert (create or replace) to collection"""
# user = {
#    "userId": "234",
#    "name": "#LIM KE EN#",
#    "email": "ABC@e.ntu.edu.sg",
#    "last_updated": {"degree": "CSC", "cohort": "2021", "degree_key": "CSC", "career": ["AI"], "year_standing": "year1"},
#    "coursedata": {"2021": ["SC1003"]},
#    "career_path": "AI"
# }
# result = collection.update_one(
#     {"_id": user["userId"]}, {"$set": user}, upsert=True
# )
# print("Upserted document with _id {}\n".format(result))

doc = collection.find_one({"_id": "dfd4ed12-16a9-443f-b19f-dc2b8cd90b9e"})
# print("Found a document with _id {}: {}\n".format(result.upserted_id, doc))

print(doc)