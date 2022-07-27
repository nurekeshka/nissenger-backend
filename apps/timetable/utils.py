from .constants import DAYS
from .models import Day


def initialize_days():
    Day.objects.all().delete()

    for day in DAYS:
        Day.objects.create(name=day)
