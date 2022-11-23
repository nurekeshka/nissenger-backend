from .constants import MessageTexts
from telebot import types
from .utils import bot
from . import views


@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    bot.reply_to(message=message, text=MessageTexts.menu.value,
                 markup=views.MenuMarkup())
