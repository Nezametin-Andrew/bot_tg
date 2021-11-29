from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from tg_bot.utils import request

profile_keyboard = InlineKeyboardMarkup(

)


def get_user_info(*args, **kwargs):
    print(args)
    print(kwargs)
    #r = request.request(model='user', method='get_user_info', data={'user_id': kwargs['user_id']})

    return 1, 2