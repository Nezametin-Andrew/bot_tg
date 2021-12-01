from decimal import Decimal

from keyboards.inline.control_menu.all_games import get_btn_for_all_game
from utils.request import request
from data.msg import callback_msg
from keyboards.inline.template_btn import get_cancel_markup
from keyboards.inline.control_menu.my_profile import get_markup_for_profile, get_markup_for_my_ticket
from states.profile_state import UserDataState
from states.games_state import GameState



def create_msg_for_view_profile(*args, **kwargs):
    qt = 0 if args[0][0]['ticket__event__price'] is None else str(len(args[0]))
    result_msg = f"""
❤ <b>Пользователь:</b>    {args[0][0]['user_name']}
🔑 <b>ID:</b>   {args[0][0]['id_tg']}
💸 <b>Количество билетов:</b>   {qt}
💰 <b>Ваш баланс:</b>   {args[0][0]['account_amount']}
    
"""
    return result_msg


template_view_for_tickets = """
🎲 <b>Игра №:</b>  {play}                                                
📅 <b>Начало:</b>   {datetime}                             
📋 <b>Количество участников:</b>    {qt_players}                  
💰 <b>Разыгрывается сумма:</b>    {sum_bank}                             
💸 <b>Мой билет №:</b>    {my_ticket}                                    

"""

msg_for_up_balance = """
❗ Это фейковая реализация пополнения баланса ❗

Введите сумму на которую хотите пополнить баланс
и отправьте обычным текстовым сообщением,
например: 100
 
"Сообщение не должно содержать символы и спец. символы,
сообщение должно состоять из цифр без пробелов" 
"""

get_my_balance_msg = """
❗ Это фейковая реализация для вывода средств ❗

Введите сумму которую хотите вывести
и отправьте обычным текстовым сообщением,
например: 100
 
"Сообщение не должно содержать символы и спец. символы,
сообщение должно состоять из цифр без пробелов" 

Вам доступно для вывода: {user_balance}

"""


def create_msg_for_my_tickets(*args, **kwargs):
    if args[0][0]['ticket__event__price'] is None: return False
    result_msg = f"""

"""
    for item in args[0]:
        result_msg += template_view_for_tickets.format(
            play=item['ticket__event__pk'], datetime=item['ticket__event__date'],
            qt_players=str(int(float(item['ticket__event__bank']) / float(item['ticket__event__price']))),
            sum_bank=item['ticket__event__bank'], my_ticket=item['ticket']
        )

    return result_msg


async def get_data_for_user(*args, **kwargs):
    state = kwargs['state']
    state_name = await state.get_state()

    if state_name is not None and state_name[:13] != "UserDataState":
        await state.finish()

    if await state.get_state() == 'UserDataState:up_balance':
        await state.finish()

    if not await state.get_data():
        await UserDataState.user_data.set()
        user_info = request(model='', method='get_user', data={'user': kwargs['user_id']})
        new_user_info = []

        for item in user_info['data']:
            if int(item['id_tg']) == int(kwargs['user_id']):
                new_user_info.append(item)

        if not new_user_info:
            user_info = user_info['data']
        else:
            user_info = new_user_info

        await state.update_data(user_data=user_info)
    else:
        user_info = await state.get_data()
        user_info = user_info['user_data']
    return user_info


async def get_info_user(*args, **kwargs):
    user_info = await get_data_for_user(*args, **kwargs)
    return get_markup_for_profile(user_info), create_msg_for_view_profile(user_info)


async def get_my_tickets(*args, **kwargs):
    user_info = await get_data_for_user(*args, **kwargs)
    return get_markup_for_my_ticket(level=1), create_msg_for_my_tickets(user_info)


async def top_up_balance(*args, **kwargs):
    state = await kwargs['state'].get_state()
    if state == 'UserDataState:up_balance':
        money_sum, user_id = kwargs['sum'], kwargs['user_id']
        if float(money_sum) > float(999):
            msg = "❌ Сумма не может быть больше 999"
            await kwargs['state'].update_data(up_balance={'status': False, "msg": msg})
            return
        req = request(model='balance', method='up_balance', data={'sum': money_sum, 'user_id': user_id})
        if req['result']:
            await kwargs['state'].update_data(up_balance={'status': True})
    else:
        await UserDataState.up_balance.set()
    return get_markup_for_my_ticket(level=1), msg_for_up_balance


async def get_my_balance(*args, **kwargs):
    user_info = await get_data_for_user(*args, **kwargs)
    if await kwargs['state'].get_state() == "UserDataState:get_balance":
        money_sum, user_id = kwargs['sum'], kwargs['user_id']
        if Decimal(float(money_sum)) > Decimal(float(user_info[0]['account_amount'])):
            await kwargs['state'].update_data(
                get_balance={'status': False, 'msg': "Запрошеная сумма не может быть выведена"}
            )
        else:
            response = request(model='balance', method='get_balance', data={'sum': money_sum, 'user_id': user_id})
            if response['result']:
                await kwargs['state'].update_data(get_balance={'status': True})
            else:
                await kwargs['state'].update_data(get_balance={'status': False, 'msg': response['error']})
    else:
        await UserDataState.get_balance.set()
    return get_markup_for_my_ticket(level=1), get_my_balance_msg.format(user_balance=user_info[0]['account_amount'])


async def all_games(*args, **kwargs):
    state = await kwargs['state'].get_state()
    if state is None or state[:9] != "GameState":
        response = request(model='game', method='get_all_games', data={})
        if not response['game_data']:
            return False, False
        else:
            await kwargs['state'].finish()
            await GameState.game_data.set()
            await kwargs['state'].update_data(response)

    return await get_btn_for_all_game(kwargs['state'])


async def surfing_game(*args, **kwargs):
    data = await kwargs['state'].get_data()
    if int(kwargs['ticket_level']['next']): data['level_game'] += 1
    else: data['level_game'] -= 1

    await kwargs['state'].update_data(data)

    return await get_btn_for_all_game(kwargs['state'])


async def buy_ticket(*args, **kwargs):
    state_data = await kwargs['state'].get_data()
    id_game, id_user, = state_data['game_data'][int(kwargs['index_ticket'])]['id'], kwargs['user_id']
    response = request(model='game', method='buy_ticket', data={'id_game': id_game, 'id_tg': id_user})

    if response['game_data'][0].get("error") is None:
        state_data['game_data'][int(kwargs['index_ticket'])]['busy_tickets'] = response['game_data'][0]['qt_players']
        state_data['game_data'][int(kwargs['index_ticket'])]['bank'] = response['game_data'][0]['bank']
        await kwargs['state'].update_data(state_data)

    return response['game_data'][0]


async def get_regulations_game(*args, **kwargs):
    return get_cancel_markup(), callback_msg[kwargs['call_data']]


control_main_menu = {
    'all_games': all_games,
    'my_profile': get_info_user,
    'regulations_game': get_regulations_game,
    'added_money': top_up_balance,
    'get_my_balance': get_my_balance,
    'my_tickets': get_my_tickets,
    'surfing_game': surfing_game,
    'buy_ticket': buy_ticket,
}


level_menu ={
    '1': control_main_menu['my_profile']
}
