from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧾 Регистрация 🧾")
        ]
    ],
    resize_keyboard=True
)

show_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Показать главное меню")
        ]
    ],
    resize_keyboard=True
)

