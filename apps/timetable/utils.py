from .models import Day, Group, Class
from django.db.models import Count
from .constants import DAYS
from typing import List


def initialize_days():
    Day.objects.all().delete()

    for day in DAYS:
        Day.objects.create(name=day)


def search_for_group(name: str, classes: List[Class]) -> List[Group]:
    group = Group.objects.annotate(
        count=Count('classes')).filter(classes=classes[0], name=name)

    for __class in classes[1:]:
        group = group.filter(classes=__class)

    group = group.filter(count=len(classes))
    return group
