from rest_framework import serializers
from cookiesAPI.models import User, Command, CommandCookie, Cookie


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "address_line", "postal_code", "city", "country"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "password", "username")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "country", "city", "postal_code", "address_line")


class CookieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cookie
        fields = "__all__"


class CommandCookieSerializer(serializers.ModelSerializer):
    total_cost = serializers.IntegerField(read_only=True)

    class Meta:
        model = CommandCookie
        exclude = ('id', 'command',)
        extra_fields = ("total_cost",)


class CommandSerializer(serializers.ModelSerializer):
    command_cookies = CommandCookieSerializer(many=True,)
    total_cost_command = serializers.IntegerField(read_only=True)

    class Meta:
        model = Command
        exclude = ("cookies", "user")
        extra_fields = ("total_cost_command")

class CommandWriteOnlySerializer(serializers.ModelSerializer):
    command_cookies = CommandCookieSerializer(many=True,)

    def create(self, validated_data):
        command_cookies = validated_data.pop("command_cookies")
        obj = super(CommandWriteOnlySerializer, self).create(validated_data)
        for command_cookie in command_cookies:
            CommandCookie.objects.create(command=obj, cookie=command_cookie["cookie"], quantity=command_cookie["quantity"])
        return obj

    class Meta:
        model = Command
        fields = ["command_cookies"]
