from pymongo import MongoClient


class RaspMongoClient:
    def __init__(self, connection_string: str, database: str, collection: str):
        self.client = MongoClient(connection_string)
        self.collection = self.client[database][collection]

    def disconnect(self):
        self.client.close()

    @staticmethod
    def insert_document(collection, data):
        return collection.insert_one(data)

    def add_lessons(self, lessons: list):
        self.collection.insert_many(lessons)

    def add_lesson(self, lesson: dict):
        self.collection.insert_one(lesson)
