# Generated by Django 2.2.5 on 2019-10-27 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpbt', '0004_teamroster_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamroster',
            name='lineup_position',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
