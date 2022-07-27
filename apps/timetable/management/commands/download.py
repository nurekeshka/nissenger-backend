from django.core.management.base import BaseCommand
from . import _parser as parser


class Command(BaseCommand):
    help = 'Это команда для загрузки расписания с серверов показа расписания'

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str)

    def handle(self, *args, **kwargs):
        response = parser.load_main_db(kwargs['domain'])
