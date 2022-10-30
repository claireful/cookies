from rest_framework import serializers
from cookiesAPI.models import User, Command, CommandCookie, Cookie


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CookieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cookie
        exclude = ["available"]


class CommandCookieSerializer(serializers.ModelSerializer):
    total_cost = serializers.IntegerField(read_only=True)

    class Meta:
        model = CommandCookie
        exclude = ('id', 'command',)
        extra_fields = ("total_cost",)


class CommandSerializer(serializers.ModelSerializer):
    command_cookies = CommandCookieSerializer(many=True,)
    total_cost_command = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        command_cookies = validated_data.pop("command_cookies")
        obj = super(CommandSerializer, self).create(validated_data)
        for command_cookie in command_cookies:
            CommandCookie.objects.create(**command_cookie, command=obj)
        return obj

    class Meta:
        model = Command
        exclude = ("cookies", "user")
        extra_fields = ("total_cost_command",)


