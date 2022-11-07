from apps.timetable.constants import CLASS_LESSONS_DATA
from apps.timetable.constants import CLASS_LESSONS_LINK
from apps.timetable.utils import get_current_weeks
from apps.timetable import models
import requests


def _load_class_lessons(class_id: str, firstday: str, lastday: str, domain: str) -> requests.Response:
    data = CLASS_LESSONS_DATA.copy()

    data['__args'][1]['datefrom'] = firstday
    data['__args'][1]['dateto'] = lastday
    data['__args'][1]['id'] = class_id

    return requests.post( url=CLASS_LESSONS_LINK.format(domain), data=CLASS_LESSONS_DATA )


def load_lessons(domain: str, classes: list, timetable: models.Timetable):
    firstday, lastday = get_current_weeks()

    for class_name in classes:
        response = _load_class_lessons(class_name, firstday, lastday)
        print(response)
