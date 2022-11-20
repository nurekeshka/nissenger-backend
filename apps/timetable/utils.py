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
