# Generated by Django 2.2.5 on 2019-10-07 04:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kpbt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bowlingcenter',
            name='manager',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='center_managed', to=settings.AUTH_USER_MODEL, verbose_name='manager'),
        ),
        migrations.AlterField(
            model_name='league',
            name='name',
            field=models.CharField(max_length=32),
        ),
    ]
