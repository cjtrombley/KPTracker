# Generated by Django 2.2.5 on 2019-09-25 20:54

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpbt', '0002_auto_20190925_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_name',
            field=models.CharField(default=models.IntegerField(default=builtins.id), max_length=32),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_number',
            field=models.IntegerField(default=builtins.id),
        ),
    ]
