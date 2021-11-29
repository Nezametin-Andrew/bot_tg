from aiogram.dispatcher.filters.state import State, StatesGroup


class GameState(StatesGroup):
    game_data = State()
