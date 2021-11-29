import time
from random import randint
from django.utils import timezone

from .models import *


def game(user):
    user_k_v = {}
    for i in range(len(user)): user_k_v[str(i + 1)] = user[i]
    random_num = randint(10, 20)
    winner = divmod(random_num, len(user))[1]
    if winner > len(user): winner = 1
    if winner == 0: winner = 1
    return random_num, user_k_v[str(winner)]


def get_user_for_game(players):
    user_list_for_game = [player['ticket__user__user_name'] for player in players]
    user_id_list = [player['ticket__user'] for player in players]
    return user_list_for_game, user_id_list


def run_game(**kwargs):
    time.sleep(3)
    if kwargs.get('slug') is not None:
        event = Event.objects.get(slug=kwargs.get('slug'))
        if event.date > timezone.now():
            time.sleep(int((event.date - timezone.now()).total_seconds()))
            players = Event.objects.filter(slug=kwargs.get('slug')).values(
                'bank', 'busy_tickets', 'ticket__user__user_name', 'ticket__user__id_tg',
                'ticket__user',

            )

            if players[0]['busy_tickets']:
                user_list_for_game, user_id_list = get_user_for_game(players)
                random_num, winner = game(user_list_for_game)
                archive = ArchiveGame.objects.create(
                    id_game=str(event), date_game=event.date, count_players=len(players),
                    bank=players[0]['bank'], winner=UserProfile.objects.get(user_name=winner), random_num=random_num
                )
                for user in players:

                    archive.players.add(UserProfile.objects.get(pk=user['ticket__user']))
                archive.save()
                event.delete()
            else:
                archive = ArchiveGame(
                 id_game=str(event.id), date_game=event.date, count_players=0, bank=event.bank, random_num=0
                )
                archive.save()
                event.delete()
