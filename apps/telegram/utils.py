from django.conf import settings
from telebot import TeleBot
from telebot import types


bot = TeleBot(token=settings.TELEGRAM, threaded=True)


def reply(message: types.Message, text: str):
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode='html'
    )
