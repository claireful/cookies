from django.db import models
import fernet_fields
import uuid


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(UUIDModel): # TODO: voir tout ce qui est authentification !! + password 
    first_name = fernet_fields.EncryptedCharField(max_length=30)
    last_name = fernet_fields.EncryptedCharField(max_length=150)
    email = fernet_fields.EncryptedEmailField()
    created_at = models.DateTimeField(auto_now=True)
    address_line = fernet_fields.EncryptedCharField(max_length=1000)
    postal_code = fernet_fields.EncryptedCharField(max_length=12)
    city = fernet_fields.EncryptedCharField(max_length=12)
    country = fernet_fields.EncryptedCharField(max_length=12)
    phone_number = fernet_fields.EncryptedCharField(max_length=20)
    is_admin = models.BooleanField()


class Cookie(UUIDModel):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000, blank=True, null=True)
    price = models.FloatField()
    photo = models.ImageField(upload_to="images/")


class CommandManager(models.Manager):
    def get_for_user(self, user):
        if user.is_admin: 
            return self.objects.all()
        return self.filter(user=user)


class Command(UUIDModel):
    objects = CommandManager()
    created_at = models.DateTimeField(auto_now=True)
    cookies = models.ManyToManyField(Cookie, related_name="commands", through="CommandCookie")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commands")

    @property
    def total_cost_command(self):
        return sum(self.command_cookies.values_list(("total_cost"), flat=True))


class CommandCookie(UUIDModel):
    cookie = models.ForeignKey(Cookie, on_delete=models.DO_NOTHING, related_name="command_cookies")
    command = models.ForeignKey(Command, on_delete=models.DO_NOTHING, related_name="command_cookies")
    quantity = models.IntegerField()

    @property
    def total_cost(self):
        return self.quantity * self.cookie.price



