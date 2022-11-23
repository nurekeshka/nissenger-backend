from django.conf import settings
from telebot import TeleBot
from telebot import types


class TelegramBot(TeleBot):
    token = settings.TELEGRAM
    threaded = True
    parse_mode = 'html'

    def __init__(self):
        super(TelegramBot, self).__init__(
            token=self.token,
            parse_mode=self.parse_mode,
            threaded=self.threaded,
        )

    def reply_to(self, message: types.Message, text: str, markup: types.InlineKeyboardMarkup = None):
        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=markup,
        )

    def edit(self, message: types.Message, text: str, markup: types.InlineKeyboardButton = None):
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=text,
            reply_markup=markup,
        )


bot = TelegramBot()
