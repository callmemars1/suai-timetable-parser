from bs4 import BeautifulSoup as bs
import requests
import logging
import json
import re


class RaspBodyParser:
    def __init__(self, url):
        self.url = url
        self.request = self.get_request()
        self.soup = bs(self.request.text, "html.parser")
        self.class_result = self.soup.find('div', class_='result')
        # self.group = re.search(r'\d+', self.class_result.find('h2').text).group(0)
        self.group = self.class_result.find('h2').text

    def get_request(self):
        try:
            request = requests.get(self.url)
            if request.status_code == 200:
                return request
        except:
            print("Connection error")

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
        rasp = {'Группа': self.group}
        for day in days:
            day_name = day[0]
            day_lessons = {}
            lesson_time = 'Ошибка определения времени'
            time_lessons = []
            for string in day[1:]:
                if 'пара (' in string or 'вне сетки' in string:
                    time_lessons = []
                    lesson_time = string
                else:
                    time_lessons.append(self.expand_lesson(string) if isinstance(string, str) else string)
                    day_lessons[f'{lesson_time}'] = time_lessons
            rasp[f'{day_name}'] = day_lessons
        return rasp

    @staticmethod
    def expand_lesson(lesson: str) -> dict:
        match = re.search(r'(.*)(Л|ПР|ЛР|КР)\W*(.*)  \W*(.*), ауд. (.*)(Преподаватель: |на базе кафедры )(.*)(Группы: '
                          r'|Группа: )(.*)', lesson)

        if match.group(1) == '':
            week_type = 'верхняя и нижняя'
        elif match.group(1) == '▲ ':
            week_type = 'верхняя'
        elif match.group(1) == '▼ ':
            week_type = 'нижняя'
        else:
            week_type = 'неопределено'
        # week_type = match.group(1)
        lesson_type = match.group(2)
        lesson_name = match.group(3)
        building = match.group(4)
        class_room = match.group(5)
        teacher = match.group(7)
        groups = re.findall(r'\d+', match.group(9))

        expanded_lesson = {
            'week_type': week_type,
            'lesson_type': lesson_type,
            'lesson_name': lesson_name,
            'building': building,
            'class_room': class_room,
            'teacher': teacher,
            'groups': groups,
        }
        return expanded_lesson


if __name__ == '__main__':
    TEST_URL = 'https://rasp.guap.ru/?g=315'
    TABLE_PATH = 'result.json'
    rasp_5038 = RaspBodyParser(TEST_URL)

    with open(TABLE_PATH, 'w', encoding='utf8') as file:
        json.dump(rasp_5038.crt_dict(), file, indent=2, ensure_ascii=False)
