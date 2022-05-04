import re


def expand_lesson(lesson: str):
    """
    ▲ Л – Социология  – Гастелло 15, ауд. 32-02Преподаватель: Плотникова В.А. - старший преподавательГруппы: 5031; 5036; 5037; 5038
    ПР – Иностранный язык  – Гастелло 15, ауд. 34-04Преподаватель: Карпова О.П. - старший преподавательГруппа: 5038
    "КР – Технологии программирования  – , ауд. на базе кафедры КАФЕДРА 53Группа: 5038"
    """
    match = re.search(
        r'(.*)(Л|ПР|ЛР|КР)\W*(.*)  \W*(.*), ауд. (.*)(Преподаватель: |на базе кафедры )(.*)(Группы: |Группа: )(.*)',
        lesson)

    week_type = match.group(1)
    lesson_type = match.group(2)
    lesson_name = match.group(3)
    building = match.group(4)
    class_room = match.group(5)
    teacher = match.group(7)
    groups = re.findall(r'\d+', match.group(9))

    print(f'{week_type=}\n'
          f'{lesson_type=}\n'
          f'{lesson_name=}\n'
          f'{building=}\n'
          f'{class_room=}\n'
          f'{teacher=}\n'
          f'{groups=}\n')


expand_lesson(
    "▲ Л – Социология  – Гастелло 15, ауд. 32-02Преподаватель: Плотникова В.А. - старший преподавательГруппы: 5031; 5036; 5037; 5038")
