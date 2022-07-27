from django.core.management.base import BaseCommand
from ...views import bot


class Command(BaseCommand):
    help = 'Это команда для запуска телеграм бота'

    def handle(self, *args, **kwargs):
        bot.polling()
