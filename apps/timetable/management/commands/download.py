from apps.timetable.constants import TimetableIndexes as indexes
from django.core.management.base import BaseCommand
from apps.timetable.models import Timetable
from . import _parser as parser
from . import _lessons as lessons


class Command(BaseCommand):
    help = 'Это команда для загрузки расписания с серверов показа расписания'

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str)

    def handle(self, *args, **kwargs):
        data = parser.load_main_db(kwargs['domain'])

        timetable = Timetable.objects.create()
        # parser.load_entities(data['r']['tables'], timetable)
        lessons.load_lessons(
            domain=kwargs['domain'],
            classes=data['r']['tables'][indexes.classes.value]['data_rows'],
            timetable=timetable,
        )
