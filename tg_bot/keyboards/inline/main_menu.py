from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


menu_callback = CallbackData("main_menu", "item")
cancel_callback = CallbackData('step', 'level')


main_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🎲 Ближайшие игры",
                callback_data=menu_callback.new(item='all_games')
            )
        ],
        [
            InlineKeyboardButton(
                text="🧑‍🔧  Мой профиль",
                callback_data=menu_callback.new(item='my_profile'),
                parse_mode="HTML"
            )
        ],
        [
            InlineKeyboardButton(
                text="🧾 Правила игры",
                callback_data=menu_callback.new(item='regulations_game'),
                parse_mode="HTML"
            )
        ]
    ]
)

cancel = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⏮ Назад",
                callback_data=cancel_callback.new(level=1)
            )
        ]
    ]
)

full_game = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [

        ]
    ]
)


def get_full_game():
    ...


def get_start_menu():
    return ["👇 Выберите нужный пункт 👇", main_menu]
