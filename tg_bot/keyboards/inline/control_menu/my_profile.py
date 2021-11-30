from decimal import Decimal

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.template_btn import get_template_btn, get_cancel_btn, get_returned_btn

call_data_for_profile = CallbackData('profile', 'data')


def get_my_balance_btn(*args, **kwargs):
    if Decimal(float(args[0][0]['account_amount'])) > Decimal(0):
        return InlineKeyboardButton(
            text="💵  Запросить выплату", callback_data=call_data_for_profile.new('get_my_balance')
        )
    return False


def get_markup_for_profile(*args, **kwargs):

    btn_list = [
        InlineKeyboardButton(text='💸 Мои билеты', callback_data=call_data_for_profile.new(data='my_tickets')),
        InlineKeyboardButton(text='💰 Пополнить баланс', callback_data=call_data_for_profile.new(data='added_money'))
    ]
    markup = get_template_btn(row_width=1)
    if btn := get_my_balance_btn(*args, **kwargs):
        btn_list.append(btn)

    for btn in btn_list: markup.add(btn)
    markup.add(get_cancel_btn())
    return markup


def get_markup_for_my_ticket(*args, **kwargs):
    markup = get_template_btn(row_width=1)
    markup.add(get_cancel_btn(level=kwargs['level']))
    markup.add(get_returned_btn())
    return markup





