from rasp_mongo_client import RaspMongoClient
import loguru


class UploadManager:
    @staticmethod
    def check_connection(DB_USER, DB_PASS, DB_HOST, DB_NAME, collection_name):
        try:
            bd = RaspMongoClient(f'mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}/',
                                 f'{DB_NAME}',
                                 f'{collection_name}')
            bd.disconnect()
        except Exception as _ex:
            loguru.logger.warning('cant connect to mangodb')
            loguru.logger.warning(_ex)

    @staticmethod
    def upload_to_the_mangodb(DB_USER, DB_PASS, DB_HOST, DB_NAME, collection_name, file):
        bd = RaspMongoClient(f'mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}/',
                             f'{DB_NAME}',
                             f'{collection_name}')
        bd.add_lessons(file)
        bd.disconnect()
