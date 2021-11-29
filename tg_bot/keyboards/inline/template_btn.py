from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


cancel_callback = CallbackData('step', 'level')


def get_template_btn(row_width):
    return InlineKeyboardMarkup(row_width=row_width)


def get_cancel_btn(level=0):
    return InlineKeyboardButton(text="⏮ Назад", callback_data=cancel_callback.new(level=level))


def get_returned_btn():
    return InlineKeyboardMarkup(text="🚪 Вернуться в начало",  callback_data=cancel_callback.new(level=0))


def get_cancel_markup():
    markup = get_template_btn(row_width=1)
    markup.add(get_cancel_btn())
    return markup

