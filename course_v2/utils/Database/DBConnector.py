from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(override=True)

class DBConnector:
    def __init__(self, DB_HOST):
        # Azure CosmosDB MongoDB RU
        self.connection = MongoClient(DB_HOST)
    
    # Get DB based on the DB_NAME
    def get_db(self, db_name):
        return self.connection[db_name]
    