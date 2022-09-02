from datetime import timedelta
from datetime import date
from .constants import DAYS
from typing import Tuple
from .models import Day


def initialize_days():
    Day.objects.all().delete()

    for day in DAYS:
        Day.objects.create(name=day)


def get_current_weeks() -> Tuple[str]:
    today: date = date.today()
    weekday: int = today.weekday()
    
    firstday: date = today - timedelta(days=weekday)
    lastday: date = firstday + timedelta(days=6)

    return tuple( map( lambda day: day.strftime('%Y-%m-%d'), ( firstday, lastday ) ) )
