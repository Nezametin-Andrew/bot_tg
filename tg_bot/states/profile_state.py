from aiogram.dispatcher.filters.state import State, StatesGroup


class UserDataState(StatesGroup):
    user_data = State()
    up_balance = State()
    get_balance = State()
