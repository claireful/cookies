from django.db import models
from django.db.models import Sum
import fernet_fields
import uuid
from django.contrib.auth.models import AbstractUser


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

# TODO: on veut que les admins puissent voir tous les users ? Comment est le panel d'administration ?
class User(UUIDModel, AbstractUser): # TODO: voir tout ce qui est authentification !! + password 
    first_name = fernet_fields.EncryptedCharField(max_length=30, blank=True)
    last_name = fernet_fields.EncryptedCharField(max_length=150, blank=True)
    email = fernet_fields.EncryptedEmailField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    address_line = fernet_fields.EncryptedCharField(max_length=1000, blank=True)
    postal_code = fernet_fields.EncryptedCharField(max_length=12, blank=True)
    city = fernet_fields.EncryptedCharField(max_length=12, blank=True)
    country = fernet_fields.EncryptedCharField(max_length=12, blank=True)
    phone_number = fernet_fields.EncryptedCharField(max_length=20, blank=True) # TODO: attention, voir fernet_key...

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_read_perm(self, user):
        return user.id == self.id
    
    def has_write_perm(self, user):
        return self.has_read_perm(user)


class Cookie(UUIDModel):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000, blank=True, null=True)
    price = models.FloatField()
    photo = models.ImageField(upload_to="images/")
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def has_read_perm(self, user):
        return True
    
    def has_write_perm(self, user):
        return user.is_staff
    

class Command(UUIDModel):
    created_at = models.DateTimeField(auto_now=True)
    cookies = models.ManyToManyField(Cookie, related_name="commands", through="CommandCookie")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commands")

    @property
    def total_cost_command(self):
        return sum([cc.total_cost for cc in self.command_cookies.all()])

    def has_read_perm(self, user):
        return user.id == self.id or user.is_staff()
    
    def has_write_perm(self, user):
        return user.is_staff()



class CommandCookie(UUIDModel):
    cookie = models.ForeignKey(Cookie, on_delete=models.DO_NOTHING, related_name="command_cookies")
    command = models.ForeignKey(Command, on_delete=models.CASCADE, related_name="command_cookies")
    quantity = models.SmallIntegerField()

    @property
    def total_cost(self):
        return self.quantity * self.cookie.price

    def has_read_perm(self, user):
        return user.id == self.id
    
    def has_write_perm(self, user):
        return user.is_staff()

