from django.conf import settings
from telebot import TeleBot
from telebot import types


class TelegramBot(TeleBot):
    token = settings.TELEGRAM
    threaded = True
    parse_mode = 'html'
    admin_chat_id = settings.TELEGRAM_ADMIN_CHAT

    def __init__(self):
        super(TelegramBot, self).__init__(
            token=self.token,
            parse_mode=self.parse_mode,
            threaded=self.threaded,
        )

    def reply_to(self, message: types.Message, text: str, markup: types.InlineKeyboardMarkup = None):
        self.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=markup,
        )

    def edit(self, message: types.Message, text: str, markup: types.InlineKeyboardButton = None):
        self.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=text,
            reply_markup=markup,
        )

    def forward_to(self, chat_id: int, text: str):
        self.send_message(
            chat_id=chat_id,
            text=text,
        )


bot = TelegramBot()
