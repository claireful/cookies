from cookiesAPI.models import User, Command, CommandCookie, Cookie
from rest_framework import viewsets, mixins
from cookiesAPI.serializers import UserSerializer, CookieSerializer, CommandSerializer


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    model_name = User
    serializer_class = UserSerializer


class CookieViewSet(viewsets.ModelViewSet):
    model_name = Cookie
    serializer_class = CookieSerializer
    queryset = Cookie.objects.all()


class CommandViewSet(viewsets.ModelViewSet):
    model_name = Command
    serializer_class = CommandSerializer

    def get_queryset(self):
        return Command.objects.get_for_user(self.request.user)



