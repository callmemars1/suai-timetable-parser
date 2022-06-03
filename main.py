from take_rasp_body import RaspBodyParser
from take_params import RaspParamParser
from datetime import datetime
from config import lesson_collection_name, actualWeekType_collection_name
from loguru import logger
from rasp_mongo_client import RaspMongoClient
import os
from dotenv import load_dotenv
import sched, time

TABLE_PATH = 'full_result.json'


def main():
    logger.info('!suai-timetable-parser START work!')

    try:
        load_dotenv('.env')
        logger.info('use .env')
    except Exception:
        pass

    logger.info('started connecting with mangoDB')

    # bd = RaspMongoClient(f'mongodb://localhost:27017/',
    #                      f'suai_timetable_test')

    bd = RaspMongoClient(f'mongodb://{os.environ["DB_USER"]}:{os.environ["DB_PASS"]}@{os.environ["DB_HOST"]}/',
                         f'{os.environ["DB_NAME"]}')

    logger.info('mangoDB successfully joined')

    logger.info('RaspParamParser started its work')
    start_time = datetime.now()
    params_parser = RaspParamParser('https://rasp.guap.ru/')
    logger.info('RaspParamParser finished its work')
    g_params = params_parser.g_param_table

    lessons = []
    logger.info('RaspBodyParser started its work(its take ~2min)')
    for group in g_params:
        g = group['value']
        ref = f'https://rasp.guap.ru/?g={g}'
        rasp = RaspBodyParser(ref)
        for lesson in rasp.crt_dict():
            if lesson not in lessons:
                lessons.append(lesson)
    logger.info('RaspBodyParser finished its work')

    logger.info(f'Parsing time: {datetime.now() - start_time}')

    logger.info('start to upload to mangoDB')

    bd.drop_collection(lesson_collection_name)
    bd.drop_collection(actualWeekType_collection_name)
    bd.insert_documents(lessons, lesson_collection_name)
    bd.insert_document({'actualWeekType': params_parser.actual_week}, actualWeekType_collection_name)
    bd.disconnect()

    logger.info('uploaded to mangoDB')
    logger.info('!suai-timetable-parser END work!')


if __name__ == '__main__':

    try:
        load_dotenv('.env')
        logger.info('use .env')
    except Exception:
        pass

    logger.add('debug.log', format="{time} {level} {message}", level='DEBUG', rotation='10 KB')
    logger.info('start first parsing')
    main()

    period_in_sec = float(os.environ["TIME_SPAN"])
    logger.info(f'timer set on:{period_in_sec}sec.')
    s = sched.scheduler(time.time, time.sleep)

    def do_something(sc):
        logger.info(f"its time to parsing, next parsing in {period_in_sec} seconds ")
        main()
        sc.enter(period_in_sec, 1, do_something, (sc,))

    s.enter(period_in_sec, 1, do_something, (s,))
    s.run()
