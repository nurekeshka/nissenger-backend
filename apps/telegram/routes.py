from .constants import MessageTexts
from telebot import types
from .utils import bot
from . import views


routepatterns = {
    'write-report': views.ReportCallbackAction,
}


@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    bot.reply_to(message=message, text=MessageTexts.menu.value,
                 markup=views.MenuMarkup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call: types.CallbackQuery):
    view: views.BaseCallbackAction = routepatterns[call.data]
    view.callback_action(call)


@bot.message_handler(content_types=['text'])
def message_handler(message: types.Message):
    if message.chat.id == int(bot.admin_chat_id):
        if message.reply_to_message:
            index = message.reply_to_message.text.index('REPORT_ID: ')
            reciever = message.reply_to_message.text[index +
                                                     len('REPORT_ID: '):]

            bot.send_message(chat_id=int(reciever), text=message.text)
    else:
        if message.reply_to_message.from_user.id == bot.get_me().id:
            bot.forward_to_admins(message.text)
