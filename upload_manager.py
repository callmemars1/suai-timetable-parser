from rasp_mongo_client import RaspMongoClient


class UploadManager:
    @staticmethod
    def upload_to_the_mangodb(DB_USER, DB_PASS, DB_HOST, DB_NAME, collection_name, file):
        bd = RaspMongoClient(f'mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}/',
                             f'{DB_NAME}',
                             f'{collection_name}')
        bd.add_lessons(file)
        bd.disconnect()
