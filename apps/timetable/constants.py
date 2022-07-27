from enum import Enum


TIMETABLE_DATABASE_LINK = 'https://{}.edupage.org/rpr/server/maindbi.js?__func=mainDBIAccessor'
TIMETABLE_DATABASE_DATA = {
    "__args": [
        None,
        2021,
        {},
        {
            "op": "fetch",
            "needed_part": {
                "teachers": [
                    "short"
                ],
                "classes": [
                    "short"
                ],
                "classrooms": [
                    "short"
                ],
                "subjects": [
                    "name"
                ],
                "periods": [
                    "period",
                    "starttime",
                    "endtime"
                ],
                "dayparts": [
                    "starttime",
                    "endtime"
                ]
            },
            "needed_combos": {}
        }
    ],
    "__gsh": "00000000"
}


class TimetableIndexes(Enum):
    teachers = 0
    subjects = 1
    classrooms = 2
    classes = 3
    periods = 4
    dayparts = 5


TEACHER_CHANGES = {
    '?міртай Э. Т.': 'Әміртай Э. Т.',
    'С?лтан Р. М.': 'Сұлтан Р. М.',
    'У?лихан А.': 'Уәлихан А.',
    'К': 'Куратор',
    'У': 'Учитель',
}

SUBJECT_CHANGES = {
    "Русский язык и литература": "Русский",
    "Русская литература": "Русская литература",
    "Русский язык": "Русский",
    "Казахский язык": "Казахский",
    "Казахская литература": "Казахская литература",
    "Казахский язык и литература": "Казахский",
    "Английский язык": "Английский",
    "Мат PISA": "Математика PISA",
    "Каз PISA": "Казахский PISA",
    "Рус PISA": "Русский PISA",
    "Физика ВСО/PISA": "Физика ВСО",
    "Казахский язык ВСО": "Казахский ВСО",
    "Информатика ВСО/PISA": "Информатика ВСО",
    "Химия ВСО/PISA": "Химия ВСО",
    "Биология ВСО/PISA": "Биология ВСО",
    "Русский язык ВСО": "Русский ВСО",
    "Химия(Углубленная)": "Химия",
    "Биология(Углубленная)": "Биология",
    "Информатика(Углубленная)": "Информатика",
    "Физика(Углубленная)": "Физика",
    "География(Стандартная)": "География",
    "Экономика(Стандартная)": "Экономика",
    "Графика и проектирование(Стандартная)": "ГИП",
    "Математика(7)": "Математика",
    "Математика(10)": "Математика (10)",
    "Програм.": "Программирование",
    "История Казахстана (Казахстан в современном мире)": "КСМ",
    "Физика Доп.": "Физика Доп",
    "Физическая культура": "Физ-ра",
    "Глобальные перспективы и проектные работы": "GPPW",
    "Начальная военная и технологическая подготовка": "НВП",
    "Человек. Общество. Право (Основы права)": "Основы Права",
}

OFFICE_CHANGES = {
    'МСЗ': 'Малый Спорт Зал',
    'СЗ': 'Спорт Зал'
}
