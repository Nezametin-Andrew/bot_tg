from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.views import APIView
from .models import *
from .serializers import *
import json

from . import services


class UserViewSet(viewsets.ModelViewSet):

    queryset = None

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            self.queryset = services.check_user_model(request.GET)
        return super().dispatch(request, *args, **kwargs)

    if queryset is None: queryset = services.pass_qs_for_user()

    serializer_class = TestSerializer


class TestView(APIView):

    def get(self, request):
        qs = [
            self.serialize_decimal(items)
            for items in UserProfile.objects.values(
                'id_tg', 'user_name', 'account_amount', 'ticket__event__price',
                'ticket__event__pk', 'ticket__event__date',
                'ticket', 'ticket__event__bank'
            )
            ]
        return JsonResponse({'data':qs})

    def serialize_decimal(self, *args):
        if args[0]['ticket__event__date']:
            args[0]['ticket__event__date'] = str(args[0]['ticket__event__date'].strftime('%d-%m-%Y %H:%M'))

        if args[0]['ticket__event__price']:
            args[0]['ticket__event__price'] = str(args[0]['ticket__event__price'])

        if args[0]['account_amount']:
            args[0]['account_amount'] = str(args[0]['account_amount'])

        return args[0]


class BalanceView(APIView):

    def get(self, request, *args, **kwargs):
        result = services.update_balance_user(request.GET)
        return JsonResponse(result)


class GameView(APIView):

    def get(self, request, *args, **kwargs):
        return JsonResponse({"game_data": services.process_game(request.GET)})

