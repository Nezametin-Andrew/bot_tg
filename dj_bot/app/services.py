from datetime import datetime
from django.db import transaction

from .models import *
from decimal import Decimal


def get_user(*args, **kwargs):
    return UserProfile.objects.filter(id_tg=kwargs['user'][0])


def create_user_profile(*args, **kwargs):
    UserProfile.objects.create(id_tg=int(kwargs['id_tg'][0]), user_name=kwargs['user_name'][0], purse=0)
    return UserProfile.objects.filter(id_tg=int(kwargs['id_tg'][0]))


def get_info_user(*args, **kwargs):
    us = UserProfile.objects.filter(id_tg=int(kwargs['user'][0]))
    return us


def up_balance(**kwargs):
    us_balance = UserProfile.objects.get(id_tg=int(kwargs['id_tg']))
    new_balance = us_balance.account_amount + Decimal(kwargs['sum'])
    try:
        if UserProfile.objects.filter(id_tg=int(kwargs['id_tg'])).update(account_amount=new_balance): return True
    except Exception as e:
        print(e)
        return False


@transaction.atomic
def get_balance(*args, **kwargs):
    user = UserProfile.objects.get(id_tg=kwargs['id_tg'])
    if Decimal(float(kwargs['sum'])) > user.account_amount: return False
    new_balance = user.account_amount - Decimal(float(kwargs['sum']))
    UserProfile.objects.filter(id_tg=int(kwargs['id_tg'])).update(account_amount=new_balance)
    Balance.objects.create(user=user, get_sum=Decimal(float(kwargs['sum'])), user_purse=user.purse)
    return True


def format_to_json(data):
    for item in data:
        for k, v in item.items():
            if isinstance(v, Decimal):
                item[k] = str(v)
            if isinstance(v, datetime):
                item[k] = str(v.strftime("%d-%m-%Y %H:%M"))
    return data


def get_all_games(*args, **kwarg):
    games = Event.objects.filter(count_tickets__gt=0).values(
        'id', 'price', 'count_tickets', 'busy_tickets', 'date', 'bank',
        #'ticket', 'ticket__user__user_name'
    )

    return format_to_json(games)


@transaction.atomic
def get_ticket(request):
    game_id, id_tg = request.get('id_game'), request.get('id_tg')
    user = UserProfile.objects.get(id_tg=int(id_tg))
    game = Event.objects.get(pk=game_id)

    if game.price > user.account_amount:
        return [{"error": "bad request", "msg": "Недостаточно средств для покупки"}]
    if not game.count_tickets:
        return [{"error": "bad request", "msg": "Количество участников ограничено"}]

    bank, user_amount, bs_ticket = game.bank + game.price, user.account_amount - game.price, game.busy_tickets + 1
    count_ticket = game.count_tickets - 1

    Ticket.objects.create(event=game, user=user)
    Event.objects.filter(pk=int(game_id)).update(busy_tickets=bs_ticket, bank=bank, count_tickets=count_ticket)
    UserProfile.objects.filter(id_tg=int(id_tg)).update(account_amount=user_amount)
    return [{"bank": str(bank), "qt_players": bs_ticket}]


func_for_request = {
    'get_user': get_user,
    'create_user': create_user_profile,
    'get_info_user': get_info_user,
    'up_balance': up_balance,
    'get_balance': get_balance,
    'get_all_games': get_all_games,
    'buy_ticket': get_ticket,
}


def check_user_model(request):
    return func_for_request[request.get('method')](**request)


def pass_qs_for_user():
    return UserProfile.objects.filter(id_tg=00000000)


def update_balance_user(request):
    sum, user, method = request.get('sum'), request.get('user_id'), request.get('method')
    if func_for_request[method](id_tg=user, sum=sum): return {"result": True}
    return {'result': False}


def process_game(request):
    return list(func_for_request[request.get('method')](request))


