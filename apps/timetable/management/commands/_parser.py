from apps.timetable.constants import TimetableIndexes as indexes
from apps.timetable import constants as const
from apps.timetable import models
import requests


def load_main_db(domain: str) -> requests.Response:
    link = const.TIMETABLE_DATABASE_LINK.format(domain)
    return requests.post(url=link, json=const.TIMETABLE_DATABASE_DATA).json()


def load_teachers(teachers: list, timetable: models.Timetable):
    change = const.TEACHER_CHANGES
    changes = const.TEACHER_CHANGES.keys()

    for teacher in teachers:
        name = change[ teacher['short'] ] if teacher['short'] in changes else teacher['short']
        models.Teacher.objects.create( name=name.lower().title(), timetable=timetable )


def load_subjects(subjects: list, timetable: models.Timetable):
    change = const.SUBJECT_CHANGES
    changes = const.SUBJECT_CHANGES.keys()

    for subject in subjects:
        name = change[ subject['name'] ] if subject['name'] in changes else subject['name']
        models.Subject.objects.create( name=name, timetable=timetable )


def load_offices(offices: list, timetable: models.Timetable):
    change = const.OFFICE_CHANGES
    changes = const.OFFICE_CHANGES.keys()

    for office in offices:
        name = change[ office['short'] ] if office['short'] in changes else office['short']
        models.Office.objects.create( name=name, timetable=timetable )


def load_periods(periods: list, timetable: models.Timetable):
    for period in periods:
        models.Period.objects.create( number=period['period'], start=period['starttime'], end=period['endtime'], timetable=timetable )


def load_classes(class_names: list, timetable: models.Timetable):
    for class_name in class_names:
        grade = int(class_name['short'][:-1])
        letter = class_name['short'][-1]

        entity = models.Class.objects.create( grade=grade, letter=letter, timetable=timetable )

        for number in range(1, 3):
            group = models.Group.objects.create(name=f'{number} - группа: {entity}', timetable=timetable)
            group.classes.add(entity)


def load_entities(tables: dict) -> dict:
    timetable = models.Timetable.objects.create()

    load_teachers( tables[indexes.teachers.value]['data_rows'], timetable )
    load_subjects( tables[indexes.subjects.value]['data_rows'], timetable )
    load_offices( tables[indexes.classrooms.value]['data_rows'], timetable )
    load_periods( tables[indexes.periods.value]['data_rows'], timetable )
    load_classes( tables[indexes.classes.value]['data_rows'], timetable )
