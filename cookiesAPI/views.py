from cookiesAPI.models import  User, Command, Cookie
from rest_framework import viewsets, mixins
from cookiesAPI.serializers import UserSerializer, CookieSerializer, CommandSerializer
from rest_framework import permissions


class AuthorizedUser(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.has_read_perm(request.user)
        return obj.has_write_perm(request.user)


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (AuthorizedUser,)
    model_name = User
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)
    

class CookieViewSet(viewsets.ReadOnlyModelViewSet):
    model_name = Cookie
    serializer_class = CookieSerializer
    queryset = Cookie.objects.filter(available=True)


class CommandViewSet(viewsets.ModelViewSet):
    # permission_classes = (AuthorizedUser,)
    model_name = Command
    serializer_class = CommandSerializer
    
    def get_queryset(self):
        
        return Command.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        print("fheizophfiozafhioza", self.request.user)

        return serializer.save(user=self.request.user)