# Generated by Django 2.2.5 on 2019-11-07 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpbt', '0014_auto_20191105_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='pair_number',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
