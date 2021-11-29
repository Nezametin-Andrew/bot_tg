from django.http import JsonResponse
from threading import Thread

from .tasks import run_game

class ProcessGetBalance:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception) -> JsonResponse:
        if request.path == '/api/v1/balance':
            return JsonResponse({"error": str(exception), "result": False})


class GetTicket:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        return self._get_response(request)

    def process_exception(self, request, exception) -> JsonResponse:
        if request.path == "/api/v1/game":
            return JsonResponse({'game_data':[{"error": str(exception), "result": False}]})


class RunGame:

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if request.path == "/admin/app/event/add/":
            if request.method == "POST":
                thread = Thread(target=run_game, kwargs={'slug': request.POST.get('slug')})
                thread.start()
        return self._get_response(request)
