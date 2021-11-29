from tg_bot.keyboards.inline.main_menu import cancel
from tg_bot.keyboards.inline.user_profile import get_user_info

callback_msg = {
    'full_game': '🎲 Ближайшие игры 🎲',
    'my_profile': '',
    'regulations_game': '''
📜 Здесь описаны правила игры,
это сообщение может быть каких
угодно размеров и оформлено как пожелаешь
''',
}

callback_keyboard = {
    'regulations_game': cancel,

}

level_menu = {
    '0'
}

