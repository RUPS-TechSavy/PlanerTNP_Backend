import os

from pymongo import MongoClient
from pymongo.server_api import ServerApi


class DB:
    def __init__(self):
        # MongoDB connection
        connection_uri = "mongodb+srv://haracicervin:G8wWnGS6zos139B9@cluster0.x7x9i.mongodb.net/?retryWrites=true&w=majority&appName=planerTNP"
        #connection_uri = os.getenv('DATABASE_URL')
        client = MongoClient(connection_uri, server_api=ServerApi('1'))
        self.db = client.dsml

        # Ping MongoDB to check connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as ex:
            print(f"Could not connect to MongoDB: {ex}")
        
db=DB().db