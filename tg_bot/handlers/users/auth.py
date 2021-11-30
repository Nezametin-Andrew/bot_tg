from aiogram import types

from keyboards.inline import main_menu
from loader import dp
from utils.request import request


@dp.message_handler(text="🧾 Регистрация 🧾")
async def registration_user(msg: types.Message):
    data = {'id_tg': int(msg.from_user.id), 'user_name': msg.from_user.full_name}
    if answer := request(model='user', method='create_user', data=data):
        await msg.answer(text="✔ Вы успешно зарегистрировались", reply_markup=types.ReplyKeyboardRemove())
        await msg.answer(text="👇 Выберите нужный пункт 👇", reply_markup=main_menu.main_menu, parse_mode="HTML")

#reply_markup=types.ReplyKeyboardRemove()