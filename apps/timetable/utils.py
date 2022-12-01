from rest_framework.parsers import JSONParser
from django.db.models import Count
from typing import List

from .constants import DAYS
from . import exceptions
from . import models
import io


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


def json(function):
    def wrapper(self, request, *args, **kwargs):
        stream = io.BytesIO(request.body)
        json = JSONParser().parse(stream)

        return function(self, request, json, *args, **kwargs)

    return wrapper


def timetable(function):
    def wrapper(self, request, json, *args, **kwargs):
        try:
            try:
                city = models.City.objects.get(name=json['school']['city'])
            except models.City.DoesNotExist:
                raise exceptions.CityNotFoundExceptionHandler()

            try:
                school = models.School.objects.get(
                    name=json['school']['name'], city=city)
            except models.School.DoesNotExist:
                raise exceptions.SchoolNotFoundExceptionHandler()

            try:
                timetable = models.Timetable.objects.get(
                    school=school, active=True)
            except models.Timetable.DoesNotExist:
                raise exceptions.TimetableNotFoundException()

            return function(self, request, json, timetable, *args, **kwargs)
        except KeyError:
            raise exceptions.KeyErrorExceptionHandler(
                'Timetable\'s school or city was not provided.')

    return wrapper
