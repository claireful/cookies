from django.db import models
import fernet_fields
import uuid
from django.contrib.auth.models import AbstractUser


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(UUIDModel, AbstractUser):
    first_name = fernet_fields.EncryptedCharField(max_length=30)
    last_name = fernet_fields.EncryptedCharField(max_length=150)
    email = fernet_fields.EncryptedEmailField()
    address_line = fernet_fields.EncryptedCharField(max_length=1000, blank=True)
    postal_code = fernet_fields.EncryptedCharField(max_length=12, blank=True)
    city = fernet_fields.EncryptedCharField(max_length=12, blank=True)
    country = fernet_fields.EncryptedCharField(max_length=12, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Cookie(UUIDModel):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000, blank=True, null=True)
    price = models.FloatField()
    photo_main_page = models.ImageField(upload_to="images/")
    photo_detail = models.ImageField(upload_to="images/")
    

class Command(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    cookies = models.ManyToManyField(Cookie, related_name="commands", through="CommandCookie")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commands")

    @property
    def total_cost_command(self):
        return sum([cc.total_cost for cc in self.command_cookies.all()])

    class Meta:
        ordering = ["-created_at"]


class CommandCookie(UUIDModel):
    cookie = models.ForeignKey(Cookie, on_delete=models.DO_NOTHING, related_name="command_cookies")
    command = models.ForeignKey(Command, on_delete=models.CASCADE, related_name="command_cookies")
    quantity = models.SmallIntegerField()

    @property
    def total_cost(self):
        return self.quantity * self.cookie.price