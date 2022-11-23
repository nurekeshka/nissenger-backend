from .constants import MessageTexts
from telebot import types
from .utils import bot
from . import views


routepatterns = {
    'write-report': views.ReportCallbackAction,
    'forward_to_admins': views.ForwardToAdminChatCallbackAction,
}


@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    bot.reply_to(message=message, text=MessageTexts.menu.value,
                 markup=views.MenuMarkup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call: types.CallbackQuery):
    view: views.BaseCallbackAction = routepatterns[call.data]()
    view.callback_action(bot, call.message)
