from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('api/v1/user', include(router.urls)),
    path('api/v1/', TestView.as_view()),
    path('api/v1/balance', BalanceView.as_view()),
    path('api/v1/game', GameView.as_view()),
]
