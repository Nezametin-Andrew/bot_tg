from rest_framework import serializers
from .models import *


class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id_tg', 'user_name']


class GetUserSerializer(serializers.Serializer):

    id_tg = serializers.IntegerField()
    user_name = serializers.CharField(max_length=50)
    #event = serializers.SlugRelatedField(many=True)

    def get_fields(self):
        ...


class TicketSerializer(serializers.ModelSerializer):

    #user_name = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user_name']