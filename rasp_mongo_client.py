import loguru
from pymongo import MongoClient


class RaspMongoClient:
    def __init__(self, connection_string: str, database: str):
        try:
            self.client = MongoClient(connection_string)
        except Exception as _ex:
            loguru.logger.warning('connection with mangoDB failed')
            loguru.logger.warning(_ex)

        self.database = self.client[database]

    def disconnect(self):
        self.client.close()

    def insert_document(self, data: dict, collection):
        collection = self.database[collection]
        collection.insert_one(data)

    def insert_documents(self, data: list, collection):
        collection = self.database[collection]
        collection.insert_many(data)

    def drop_collection(self, collection):
        collection = self.database[collection]
        collection.drop()
