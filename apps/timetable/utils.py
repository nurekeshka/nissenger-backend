from django.db.models import Count
from .constants import DAYS
from typing import List
from . import models


def initialize_days():
    models.Day.objects.all().delete()

    for day in DAYS:
        models.Day.objects.create(name=day)


def search_for_group(name: str, classes: List[models.Class], timetable: models.Timetable) -> List[models.Group]:
    group = models.Group.objects.annotate(
        count=Count('classes')).filter(classes=classes[0], name=name, timetable=timetable)

    for __class in classes[1:]:
        group = group.filter(classes=__class)

    group = group.filter(count=len(classes))
    return group


def sort_lessons_by_day_and_period(lessons_queryset: List[models.Lesson]) -> List[models.Lesson]:
    days_to_lessons_dictionary = {day.name: list()
                                  for day in models.Day.objects.all()}

    for lesson in lessons_queryset:
        days_to_lessons_dictionary[lesson.day.name].append(lesson)

    output = list()

    for day, lessons in days_to_lessons_dictionary.items():
        output.extend(sorted(lessons, key=lambda lesson: lesson.period.number))

    return output
