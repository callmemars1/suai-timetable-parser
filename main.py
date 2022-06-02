import json
from take_rasp_body import RaspBodyParser
from take_params import RaspParamParser
from upload_manager import UploadManager
from datetime import datetime
from config import DB_USER, DB_NAME, DB_HOST, DB_PASS
from loguru import logger

TABLE_PATH = 'full_result.json'


def main():
    UploadManager.check_connection(DB_USER, DB_PASS, DB_HOST, DB_NAME, 'lessons')

    start_time = datetime.now()
    logger.info('RaspParamParser started its work')
    params_parser = RaspParamParser('https://rasp.guap.ru/')
    logger.info('RaspParamParser finished its work')
    g_params = params_parser.g_param_table

    lessons = []
    logger.info('RaspBodyParser started its work')
    for group in g_params:
        g = group['value']
        ref = f'https://rasp.guap.ru/?g={g}'
        rasp = RaspBodyParser(ref)
        for lesson in rasp.crt_dict():
            if lesson not in lessons:
                lessons.append(lesson)
    logger.info('RaspBodyParser started its work')

    logger.info(f'Parsing time: {datetime.now() - start_time}')

    # with open(TABLE_PATH, 'w', encoding='utf8') as file:
    #     json.dump(lessons, file, indent=2, ensure_ascii=False)

    logger.info('start to upload to mangoDB')
    UploadManager.upload_to_the_mangodb(DB_USER, DB_PASS, DB_HOST, DB_NAME, 'lessons', lessons)
    logger.info('uploaded to mangoDB')


if __name__ == '__main__':
    main()
