# Generated by Django 3.2.13 on 2022-12-06 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookiesAPI', '0005_alter_command_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
    ]