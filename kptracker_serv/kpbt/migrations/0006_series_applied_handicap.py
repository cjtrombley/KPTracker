# Generated by Django 2.2.5 on 2019-10-30 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpbt', '0005_teamroster_lineup_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='applied_handicap',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]