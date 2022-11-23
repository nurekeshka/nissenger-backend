from telebot import types
from .utils import bot


class BaseInlineKeyboardMarkup(types.InlineKeyboardMarkup):
    buttons = []

    def __init__(self):
        super(BaseInlineKeyboardMarkup, self).__init__()
        self.interface()

    def interface(self):
        for button in self.buttons:
            self.add(button)


class BaseInlineKeyboardButton(types.InlineKeyboardButton):
    text = None
    callback_data = None

    def __init__(self):
        super(BaseInlineKeyboardButton, self).__init__(
            text=self.text,
            callback_data=self.callback_data
        )


class ReportButton(BaseInlineKeyboardButton):
    text = 'Написать в тех. поддержку 🤖'
    callback_data = 'write-report'


class MenuMarkup(BaseInlineKeyboardMarkup):
    buttons = [ReportButton()]


class BaseCallbackAction(object):
    def callback_action(self, bot, message: types.Message):
        pass


class ReportCallbackAction(BaseCallbackAction):
    text = 'В следующем сообщении опишите проблему. Оно будет перенаправлено в чат тех. поддержки'
    callback_text = 'Спасибо за обратную связь! Вы сделали нашу жизнь немного сложнее >:)'

    @classmethod
    def report(self, message: types.Message):
        return '\n'.join([f'Репорт от: {message.from_user.id}',
                          f'Имя пользователя: {message.from_user.username}',
                          f'Имя: {message.from_user.first_name}',
                          f'Фамилия: {message.from_user.last_name}',
                          '',
                          f'Текст:',
                          message.text]
                         )

    @classmethod
    def callback_action(self, call: types.CallbackQuery):
        bot.answer_callback_query(callback_query_id=call.id)
        bot.reply_to(call.message, self.text)

        bot.register_next_step_handler(
            message=call.message, callback=self.callbacks_handler)

    @classmethod
    def callbacks_handler(self, message: types.Message):
        bot.forward_to_admins(self.report(message))
        bot.reply_to(message=message, text=self.callback_text)
