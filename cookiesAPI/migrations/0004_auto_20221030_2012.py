# Generated by Django 3.2.13 on 2022-10-30 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cookiesAPI', '0003_alter_commandcookie_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookie',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='commandcookie',
            name='command',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='command_cookies', to='cookiesAPI.command'),
        ),
    ]
