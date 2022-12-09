from cookiesAPI.models import  User, Command, Cookie
from rest_framework import viewsets, mixins
from cookiesAPI.serializers import CommandWriteOnlySerializer, UserCreateSerializer, UserSerializer, CookieSerializer, CommandSerializer, UserUpdateSerializer
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    model_name = User

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action == "update":
            return UserUpdateSerializer
        return UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def create(self, serializer):
        user = User.objects.create_user(username=self.request.data["email"],
            email=self.request.data["email"],
            password=self.request.data["password"],
            first_name=self.request.data["first_name"],
            last_name=self.request.data["last_name"],
        )
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CookieViewSet(viewsets.ReadOnlyModelViewSet):
    model_name = Cookie
    serializer_class = CookieSerializer
    queryset = Cookie.objects.all()


class CommandViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    model_name = Command

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CommandSerializer
        return CommandWriteOnlySerializer
    
    def get_queryset(self):
        return Command.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)