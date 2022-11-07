from django.conf import settings
from enum import Enum


class TimetableIndexes(Enum):
    teachers = 0
    subjects = 1
    classrooms = 2
    classes = 3
    periods = 4


DAYS = (
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
)
