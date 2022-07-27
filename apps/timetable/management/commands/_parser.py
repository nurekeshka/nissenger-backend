from ...constants import TimetableIndexes as indexes
from ... import constants as const
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


def load_entities(tables: dict) -> dict:
    timetable = models.Timetable.objects.create()

    load_teachers(tables[indexes.teachers.value]['data_rows'], timetable)
    load_subjects(tables[indexes.subjects.value]['data_rows'], timetable)
