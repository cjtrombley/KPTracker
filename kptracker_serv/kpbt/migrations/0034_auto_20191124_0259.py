# Generated by Django 2.2.5 on 2019-11-24 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpbt', '0033_merge_20191124_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaguerules',
            name='designation',
            field=models.CharField(choices=[('A', 'Adult'), ('S', 'Senior'), ('J', 'Junior'), ('N', 'Any')], max_length=1),
        ),
    ]
