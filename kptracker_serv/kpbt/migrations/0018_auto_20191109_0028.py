# Generated by Django 2.2.5 on 2019-11-09 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kpbt', '0017_auto_20191109_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamroster',
            name='bowler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roster_record', to='kpbt.BowlerProfile'),
        ),
    ]