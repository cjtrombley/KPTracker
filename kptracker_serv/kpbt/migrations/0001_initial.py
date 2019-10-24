# Generated by Django 2.2.5 on 2019-10-24 01:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BowlerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=64)),
                ('last_name', models.CharField(blank=True, max_length=64)),
                ('date_of_birth', models.DateField(blank=True, default=datetime.date(1900, 1, 1))),
                ('hand', models.CharField(choices=[('R', 'Right'), ('L', 'Left')], max_length=1)),
                ('designation', models.CharField(choices=[('A', 'Adult'), ('S', 'Senior'), ('J', 'Junior')], max_length=1)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('is_sanctioned', models.BooleanField(default=False)),
                ('last_date_sanctioned', models.DateField(blank=True, default=datetime.date(1900, 1, 1))),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BowlingCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('num_lanes', models.IntegerField(default=0)),
                ('manager', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='center_managed', to=settings.AUTH_USER_MODEL, verbose_name='manager')),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField()),
                ('name', models.CharField(default='', max_length=32)),
                ('total_pinfall', models.PositiveSmallIntegerField(default=0)),
                ('total_handicap_pins', models.PositiveIntegerField(default=0)),
                ('total_scratch_pins', models.PositiveIntegerField(default=0)),
                ('team_points', models.PositiveSmallIntegerField(default=0)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='kpbt.League', verbose_name='league')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('is_bowler', models.BooleanField(default=False)),
                ('is_league_secretary', models.BooleanField(default=False)),
                ('is_center_manager', models.BooleanField(default=False)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamRoster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games_with_team', models.PositiveSmallIntegerField(default=0)),
                ('is_substitute', models.BooleanField(default=False)),
                ('bowler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kpbt.Team')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='roster',
            field=models.ManyToManyField(through='kpbt.TeamRoster', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series_date', models.DateField()),
                ('applied_average', models.PositiveSmallIntegerField()),
                ('game_one_score', models.PositiveSmallIntegerField()),
                ('game_two_score', models.PositiveSmallIntegerField()),
                ('game_three_score', models.PositiveSmallIntegerField()),
                ('bowler', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kpbt.BowlerProfile')),
                ('league', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kpbt.League')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kpbt.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_starting', models.DateField()),
                ('date_ending', models.DateField()),
                ('num_weeks', models.PositiveSmallIntegerField(default=0)),
                ('start_time', models.TimeField()),
                ('current_week', models.PositiveSmallIntegerField(default=1)),
                ('league', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kpbt.League')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_teams', models.PositiveSmallIntegerField()),
                ('designation', models.CharField(choices=[('A', 'Adult'), ('S', 'Senior'), ('J', 'Junior')], max_length=1)),
                ('gender', models.CharField(choices=[('M', 'Men'), ('W', 'Women'), ('X', 'Mixed')], max_length=1)),
                ('min_roster_size', models.PositiveSmallIntegerField()),
                ('max_roster_size', models.PositiveSmallIntegerField()),
                ('is_handicap', models.BooleanField(default=False)),
                ('handicap_scratch', models.PositiveSmallIntegerField()),
                ('allow_substitutes', models.BooleanField(default=False)),
                ('bye_team_point_threshold', models.PositiveSmallIntegerField()),
                ('absentee_score', models.PositiveSmallIntegerField()),
                ('game_point_value', models.PositiveSmallIntegerField()),
                ('series_point_value', models.PositiveSmallIntegerField()),
                ('league', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kpbt.League')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueBowler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league_average', models.PositiveSmallIntegerField()),
                ('league_high_game', models.PositiveSmallIntegerField()),
                ('league_high_series', models.PositiveSmallIntegerField()),
                ('league_total_scratch', models.PositiveSmallIntegerField()),
                ('league_total_handicap', models.PositiveSmallIntegerField()),
                ('bowler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kpbt.BowlerProfile')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kpbt.League')),
            ],
        ),
        migrations.AddField(
            model_name='league',
            name='bowlers',
            field=models.ManyToManyField(through='kpbt.LeagueBowler', to='kpbt.BowlerProfile'),
        ),
        migrations.AddField(
            model_name='league',
            name='bowling_center',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leagues', to='kpbt.BowlingCenter', verbose_name='bowling center'),
        ),
    ]
