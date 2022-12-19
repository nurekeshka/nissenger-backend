from django.conf import settings
from django.db import models
from telebot import TeleBot


class TelegramBot(TeleBot):
    token = settings.TELEGRAM_API_TOKEN
    parse_mode = 'html'
    admin_chat = settings.TELEGRAM_ADMIN_CHAT
    parser_chat = settings.TELEGRAM_PARSER_CHAT

    def __init__(self):
        super(TelegramBot, self).__init__(
            token=self.token,
            parse_mode=self.parse_mode,
            threaded=True,
        )

    def send_to_parser(self, text: str):
        self.send_message(
            chat_id=self.parser_chat,
            text=text,
        )

    def send_to_admins(self, text: str):
        self.send_message(
            chat_id=self.admin_chat,
            text=text,
        )


bot = TelegramBot()
