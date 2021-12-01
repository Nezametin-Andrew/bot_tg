from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.template_btn import get_template_btn, get_returned_btn


callback_for_ticket = CallbackData('ticket', 'prev', 'next')
buy_ticket = CallbackData('buy_ticket', 'ticket')

info_ticket = """
🎲 <b>Игра №:</b>  {play}                                                
📅 <b>Начало:</b>   {datetime}                             
📋 <b>Количество участников:</b>    {qt_players}                  
💰 <b>Разыгрывается сумма:</b>    {sum_bank}                             
💵 <b>Стоимость билета:</b>    {sum_ticket}

"""


async def get_btn_for_all_game(*args, **kwargs):
    markup = None
    data = await args[0].get_data()
    if data.get('level_game') is None:
        data.update({'level_game': 0})
        await args[0].update_data(data)

    markup = get_template_btn(row_width=1)

    if not data['level_game'] and len(data['game_data']) > 1:
        markup.add(InlineKeyboardButton(text="⏭ Далее", callback_data=callback_for_ticket.new(prev=0, next=1)))

    if data['level_game'] and len(data['game_data']) == (data['level_game'] + 1):
        markup.add(InlineKeyboardButton(text="⏮ Назад", callback_data=callback_for_ticket.new(prev=1, next=0)))

    if data['level_game'] and len(data['game_data']) != (data['level_game'] + 1):
        markup = InlineKeyboardMarkup(
            row_width=2,
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="⏮ Назад", callback_data=callback_for_ticket.new(prev=1, next=0)),
                    InlineKeyboardButton(text="⏭ Далее", callback_data=callback_for_ticket.new(prev=0, next=1))
                ]
            ]
        )

    if markup is not None:
        markup.add(InlineKeyboardButton(text="💸 Купить", callback_data=buy_ticket.new(ticket=data['level_game'])))
        markup.add(get_returned_btn())

    level_game, data = data['level_game'], data['game_data']

    return markup, info_ticket.format(
        play=data[level_game]['id'], datetime=data[level_game]['date'],
        qt_players=data[level_game]['busy_tickets'],
        sum_bank=data[level_game]['bank'], sum_ticket=data[level_game]['price']
    )

