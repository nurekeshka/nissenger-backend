from telebot import types


class BaseInlineKeyboardMarkup(types.InlineKeyboardMarkup):
    buttons = []

    def __init__(self):
        super(BaseInlineKeyboardMarkup, self).__init__()
        self.interface()

    def interface():
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
    callback_data = 'report'


class MenuMarkup(BaseInlineKeyboardMarkup):
    buttons = [ReportButton()]
