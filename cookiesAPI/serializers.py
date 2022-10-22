from rest_framework import serializers
from cookiesAPI.models import User, Command, CommandCookie, Cookie


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CookieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cookie
        fields = '__all__'


class CommandCookieSerializer(serializers.ModelSerializer):
    total_cost = serializers.IntegerField()

    class Meta:
        model = CommandCookie
        exclude = ('id', 'command',)
        extra_fields = ("total_cost",)


class CommandSerializer(serializers.ModelSerializer):
    command_cookies = CommandCookieSerializer(many=True)
    total_cost_command = serializers.IntegerField()

    class Meta:
        model = Command
        exclude = ("cookies", "user")
        extra_fields = ("total_cost_command",)

