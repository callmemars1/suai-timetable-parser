import json
import re
from parser_class import Parser


class RaspBodyParser(Parser):
    """Loads the timetable body"""
    def __init__(self, url):
        super().__init__(url)
        self.class_result = self.soup.find('div', class_='result')
        self.group = re.search(r'(\w+) - (.*)', self.class_result.find('h2').text).group(2)

    def divide_by_days(self):
        days = []
        h3_tags = self.class_result.find_all('h3')
        for index, h3 in enumerate(h3_tags):
            day = [h3_tags[index].text]
            if index + 1 < len(h3_tags):
                while h3.find_next_sibling() != h3_tags[index + 1]:
                    nex_el = h3.find_next_sibling()
                    h3 = nex_el
                    day.append(nex_el.text)
            else:
                while h3.find_next_sibling() is not None:
                    nex_el = h3.find_next_sibling()
                    h3 = nex_el
                    day.append(nex_el.text)
            days.append(day)
        return days

    def crt_dict(self):
        days = self.divide_by_days()
        lessons = []

        for day in days:
            day_name = day[0]
            start_time = ''
            end_time = ''
            lesson_number = ''
            for string in day[1:]:
                if 'пара (' in string:
                    match = re.search(r'(.*) пара \((.*)–(.*)\)', string)
                    lesson_number = match.group(1)
                    start_time = match.group(2)
                    end_time = match.group(3)
                elif 'вне сетки' in string:
                    start_time = ''
                    end_time = ''
                    lesson_number = 'Вне сетки расписания'
                else:
                    time_lessons = self.expand_lesson(string) if isinstance(string, str) else string
                    lesson = {
                        'week_day': day_name,
                        'start_time': start_time,
                        'end_time': end_time,
                        'lesson_number': lesson_number
                    }
                    lesson.update(time_lessons)
                    lessons.append(lesson)
        return lessons

    @staticmethod
    def expand_lesson(lesson: str) -> dict:
        match = re.search(r'(.*)(ЛР|Л|ПР|КР|КП)\W*(.*)  \W*(.*), ауд. (.*)(Группы: |Группа: )(.*)', lesson)

        if match.group(1) == '':
            week_type = ['верхняя', 'нижняя']
        elif match.group(1) == '▲ ':
            week_type = ['верхняя']
        elif match.group(1) == '▼ ':
            week_type = ['нижняя']
        else:
            week_type = ['неопределено']
        lesson_type = match.group(2)
        lesson_name = match.group(3)
        building = match.group(4)
        class_room_and_teacher = match.group(5)
        if ':' in class_room_and_teacher:
            match2 = re.search(r'(.*)(Преподаватель: |на базе кафедры |Преподаватели: )(.*)', class_room_and_teacher)
            class_room = [room.strip() for room in match2.group(1).split(sep=';')]
            teachers = [teacher.strip() for teacher in match2.group(3).split(sep=';')]
        else:
            class_room = [room.strip() for room in match.group(5).split(sep=';')]
            teachers = ['']
        groups = re.findall(r'\w+', match.group(7))

        expanded_lesson = {
            'week_types': week_type,
            'lesson_type': lesson_type,
            'lesson_name': lesson_name,
            'building': building,
            'class_rooms': class_room,
            'teachers': teachers,
            'groups': groups,
        }
        return expanded_lesson


if __name__ == '__main__':
    TEST_URL = 'https://rasp.guap.ru/?g=456'
    TABLE_PATH = 'result.json'
    rasp_5038 = RaspBodyParser(TEST_URL)

    with open(TABLE_PATH, 'w', encoding='utf8') as file:
        json.dump(rasp_5038.crt_dict(), file, indent=2, ensure_ascii=False)
