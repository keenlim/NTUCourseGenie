import os
from azure.cosmos import CosmosClient
from uuid import uuid4
from functions.models.feedback import Feedback
from dotenv import load_dotenv 

load_dotenv(override=True)


class Database_Client:
    def __init__(self, database_name, container_name, partition_key):
        self.cosmos_uri = os.environ['ACCOUNT_URI']
        self.primary_key = os.environ['ACCOUNT_KEY']
        self.client = CosmosClient(self.cosmos_uri, self.primary_key)
        self.partition_key = partition_key

        self.database_name = database_name
        self.container_name = container_name

        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def insert_item(self, items: Feedback):
        try:
            items['partitionKey'] = self.partition_key
            self.container.upsert_item(items)
            return True
        except Exception as e:
            print(e)
