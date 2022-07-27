from .constants import Messages
from telebot import types
from .utils import bot
from . import utils


@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    utils.reply(message, '\n\n'.join(Messages.start_command.value))
