import asyncio

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from states.profile_state import UserDataState
from states.games_state import GameState
from utils.request import request
from keyboards.default import start_menu
from keyboards.inline import main_menu
from keyboards.inline.control_menu.my_profile import call_data_for_profile
from keyboards.inline.control_menu.control_main_menu import control_main_menu, level_menu
from keyboards.inline.control_menu.all_games import callback_for_ticket, buy_ticket


@dp.message_handler(CommandStart(), state='*')
async def bot_start(msg: types.Message, state: FSMContext):
    data = {'user': msg.from_user.id}
    await state.finish()
    if request(model='user', method='get_user', data=data):
        await msg.answer(text="👇 Выберите нужный пункт 👇", reply_markup=main_menu.main_menu, parse_mode="HTML")
    else:
        new_msg = await msg.answer(
            text="🤷‍♂️ Мы не нашли вашего профиля, хотите зарегистрироваться?", reply_markup=start_menu.start_menu
        )
        await asyncio.sleep(15)
        await new_msg.delete()


@dp.callback_query_handler(main_menu.menu_callback.filter(), state='*')
async def click_btn(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=2)
    markup, text = await control_main_menu[callback_data['item']](
        user_id=call.from_user.id, call_data=callback_data['item'], state=state
    )
    await call.message.edit_text(text=text)
    await call.message.edit_reply_markup(markup)


@dp.callback_query_handler(main_menu.cancel_callback.filter(), state='*')
async def prev_step_menu(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    state_name = await state.get_state()
    if state_name is not None and state_name[:9] == "GameState":
        data_state = await state.get_data()
        data_state['level_game'] = 0
        await state.update_data(data_state)

    if callback_data['level'] == "0":
        data = main_menu.get_start_menu()
    else:
        btn, text = await level_menu[callback_data['level']](user_id=call.from_user.id, state=state)
        data = [text, btn]
    await call.message.edit_text(data[0])
    await call.message.edit_reply_markup(data[1])


@dp.callback_query_handler(call_data_for_profile.filter(), state='*')
async def my_profile(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    markup, text = await control_main_menu[callback_data['data']](user_id=call.from_user.id, state=state)
    if not text:
        await call.answer(text="🤷‍♂ На текущий момент у вас нет билетов", show_alert=True, cache_time=10)
    else:
        await call.message.edit_text(text)
        await call.message.edit_reply_markup(markup)


@dp.message_handler(state=UserDataState.up_balance)
async def up_balance(msg: types.Message, state: FSMContext):
    await control_main_menu['added_money'](state=state, sum=msg.text, user_id=msg.from_user.id)
    status = await state.get_data()
    if status['up_balance']['status']: text = "✔ Ваш баланс успешно пополнен"
    else: text = "❌ Произошла непредвиденная ошибка, повторите запрос позже"

    await msg.delete()
    new_msg = await msg.answer(text)
    await asyncio.sleep(5)
    await new_msg.delete()
    await state.finish()


@dp.message_handler(state=UserDataState.get_balance)
async def get_my_balance(msg: types.Message, state: FSMContext):
    await control_main_menu['get_my_balance'](state=state, sum=msg.text, user_id=msg.from_user.id)
    status = await state.get_data()
    if status['get_balance']['status']:
        text = "✔ Запрос на вывод средств успешно обработан"
        await state.finish()
    else:
        if answer_msg := status['get_balance'].get('msg'):
            text = f"❌ Произошла ошибка, {answer_msg}"
        else:
            text = "❌ Произошла непредвиденная ошибка, повторите запрос позже"

    await msg.delete()
    new_msg = await msg.answer(text)
    await asyncio.sleep(5)
    await new_msg.delete()


@dp.message_handler(text="🧾 Регистрация 🧾")
async def registration_user(msg: types.Message):
    data = {'id_tg': int(msg.from_user.id), 'user_name': msg.from_user.full_name}
    if answer := request(model='user', method='create_user', data=data):
        await msg.delete()
        new_msg = await msg.answer(text="✔ Вы успешно зарегистрировались", reply_markup=types.ReplyKeyboardRemove())
        await msg.answer(text="👇 Выберите нужный пункт 👇", reply_markup=main_menu.main_menu, parse_mode="HTML")
        await asyncio.sleep(5)
        await new_msg.delete()


@dp.message_handler(state="*")
async def delete_all_msg_set_state(msg: types.Message, state: FSMContext):
    await msg.delete()
    new_msg = await msg.answer("❌ Бот не отвечает на текстовые сообщения ❌")
    await asyncio.sleep(3)
    await new_msg.delete()


@dp.message_handler()
async def delete_all_msg(msg: types.Message):
    await msg.delete()
    new_msg = await msg.answer("❌ Бот не отвечает на текстовые сообщения ❌")
    await asyncio.sleep(3)
    await new_msg.delete()


@dp.callback_query_handler(callback_for_ticket.filter(), state=GameState)
async def next_or_prev_ticket(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    btn, text = await control_main_menu['surfing_game'](state=state, ticket_level=callback_data)
    await call.message.edit_text(text)
    await call.message.edit_reply_markup(btn)


@dp.callback_query_handler(buy_ticket.filter(), state=GameState)
async def get_ticket(call: types.CallbackQuery, callback_data: dict, state: FSMContext):

    result = await control_main_menu['buy_ticket'](
        index_ticket=callback_data['ticket'], state=state, user_id=call.from_user.id
    )
    if result.get("error") is not None:

        await call.answer(text=f"❌ {result.get('msg')}", show_alert=True, cache_time=5)
    else:
        btn, text = await control_main_menu['all_games'](state=state)
        msg = await call.message.answer(text="Вы успешно зарегестрированы в игре")
        await asyncio.sleep(3)
        await msg.delete()
        await call.message.edit_text(text)
        await call.message.edit_reply_markup(btn)
    await call.answer()

#🧾
#✔
#💰
#❤
#💸
#🔑











