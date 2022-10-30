from django.contrib import admin

from .models import Command, Cookie, User
# TODO: créer des "adminUser" ?

admin.site.register([Command, Cookie, User])

