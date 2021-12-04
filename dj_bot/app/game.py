import time

from dotenv import dotenv_values
import requests

from django.utils import timezone
from django.db import transaction

from dj_bot.dj_bot.settings import PATH_ENV
from .models import *
from .parse.main import DataGame


def get_event(slug):
    try:
        if slug is not None:
            return {"event": Event.objects.get(slug=slug)}
        return {"error": "Not found slug"}
    except Exception as e:
        return {"error": str(e)}


def check_datetime_event(event_date):
    if event_date > timezone.now():
        return True
    return False


def get_data_from_us(field_name, users):
    return [item[field_name] for item in users]


def game(users, random_num):
    winner = divmod(random_num, len(users))[1]
    if winner > len(users): winner = 1
    if winner == 0: winner = 1
    return users[str(winner)]


def get_num_lst_users(users):
    user_num = {}
    for user in range(len(users)): user_num[str(user + 1)] = users[user]
    return user_num


@transaction.atomic
def update_balance_winner(balance_up, winner):
    balance = UserProfile.objects.get(id=winner)
    balance = balance_up + balance.account_amount
    UserProfile.objects.filter(pk=winner).update(account_amount=balance)


@transaction.atomic
def added_game_in_archive(event, users, data_game, winner):
    archive = ArchiveGame.objects.create(
        id_game=str(event.id), date_game=event.date, count_players=len(users),
        bank=event.bank, winner=winner['user'], random_num=int(data_game['random_num']),
        link=data_game['link']
    )

    for user in users: archive.players.add(user['user'])
    archive.save()
    event.delete()


token_tg = dotenv_values(PATH_ENV)['TOKEN_TG']
template_link = "https://api.telegram.org/bot{token}/sendMessage?chat_id={id_tg}&text={msg}"
template_msg = """
Результыт игры: № {id_game} 
Выйграл участник: {user_name}
Суммы выйгрыша: {bank}
Список участников:

"""


def generate_msg(users, winner, event_id, data_game, bank):
    msg = template_msg.format(id_game=str(event_id), user_name=winner['user__user_name'], bank=str(bank))
    for user in users:
        msg += user['user__user_name'] + " \n"
    return msg + f"Ссылка на случайное число: {data_game['link']}"


def send_msg_tg(lst_id_tg, msg):
    for user in lst_id_tg:
        requests.get(
            url=template_link.format(token=token_tg, id_tg=str(user), text=msg)
        )
    time.sleep(1)


def run_game(**kwargs):
    time.sleep(3)
    event = get_event(slug=kwargs.get('slug'))
    if event.get('error') is None and check_datetime_event(event['event'].date):
        time.sleep(int((event['event'].date - timezone.now()).total_seconds()))
        users = Ticket.objects.filter(event=event['event'].id).values(
            'user', 'user__user_name', 'user__id_tg', 'user__account_amount'
        )
        if users:
            obj_game = DataGame()
            data_game = obj_game.get_data_for_game()
            user_num_lst = get_num_lst_users(users)
            winner = game(user_num_lst, int(data_game['random_num']))
            id_tg_lst = get_data_from_us('user__id_tg', users)
            event = Event.objects.get(pk=event['event'].id)
            event_id = event.id
            bank = event.bank
            update_balance_winner(event.bank, winner['user'])
            added_game_in_archive(event, users, data_game, winner)
            send_msg_tg(id_tg_lst, generate_msg(users, winner, event_id, data_game, bank))
        else:
            archive = ArchiveGame(
                id_game=str(event['event'].id), date_game=event['event'].date,
                count_players=0, bank=event['event'].bank, random_num=0
            )
            archive.save()
            event.delete()
