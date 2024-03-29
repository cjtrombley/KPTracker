# Generated by Django 2.2.5 on 2019-11-26 06:33

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
                ('hand', models.CharField(blank=True, choices=[('R', 'Right'), ('L', 'Left')], max_length=1)),
                ('designation', models.CharField(blank=True, choices=[('A', 'Adult'), ('S', 'Senior'), ('J', 'Junior')], max_length=1)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('is_linked', models.BooleanField(default=False)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BowlingCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('num_lanes', models.IntegerField(default=0, verbose_name='number of lanes')),
                ('manager', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='center_managed', to=settings.AUTH_USER_MODEL, verbose_name='manager')),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('current_week', models.PositiveSmallIntegerField(default=1)),
                ('week_pointer', models.PositiveSmallIntegerField(default=1)),
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
                ('team_points_won', models.PositiveSmallIntegerField(default=0)),
                ('team_points_lost', models.PositiveIntegerField(default=0)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='kpbt.League', verbose_name='league')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_number', models.PositiveSmallIntegerField(default=0)),
                ('lane_pair', models.PositiveSmallIntegerField(default=0)),
                ('average', models.PositiveSmallIntegerField(default=0)),
                ('handicap', models.PositiveSmallIntegerField(default=0)),
                ('g1', models.PositiveSmallIntegerField(default=0)),
                ('g2', models.PositiveSmallIntegerField(default=0)),
                ('g3', models.PositiveSmallIntegerField(default=0)),
                ('series', models.PositiveSmallIntegerField(default=0)),
                ('points_won', models.PositiveSmallIntegerField(default=0)),
                ('points_lost', models.PositiveSmallIntegerField(default=0)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='kpbt.League')),
                ('opponent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opponent', to='kpbt.Team')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kpbt.Team')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyPairings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_number', models.PositiveSmallIntegerField(default=0)),
                ('lane_pair', models.PositiveSmallIntegerField(default=0)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pairings', to='kpbt.League')),
                ('team_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_pair', to='kpbt.Team')),
                ('team_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_pair', to='kpbt.Team')),
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
                ('is_active', models.BooleanField(default=True)),
                ('lineup_position', models.PositiveSmallIntegerField(default=0)),
                ('bowler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roster_record', to='kpbt.BowlerProfile')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roster_record', to='kpbt.Team')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='roster',
            field=models.ManyToManyField(through='kpbt.TeamRoster', to='kpbt.BowlerProfile'),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series_date', models.DateField(default='1900-01-01')),
                ('week_number', models.PositiveSmallIntegerField(default=0)),
                ('pair_number', models.PositiveSmallIntegerField(default=0)),
                ('applied_average', models.PositiveSmallIntegerField(default=0)),
                ('applied_handicap', models.PositiveSmallIntegerField(default=0)),
                ('game_one_score', models.CharField(blank=True, max_length=4)),
                ('game_two_score', models.CharField(blank=True, max_length=4)),
                ('game_three_score', models.CharField(blank=True, max_length=4)),
                ('scratch_score', models.IntegerField(default=0)),
                ('handicap_score', models.IntegerField(default=0)),
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
                ('day_of_week', models.CharField(choices=[('MO', 'Monday'), ('TU', 'Tuesday'), ('WE', 'Wednesday'), ('TH', 'Thursday'), ('FR', 'Friday'), ('SA', 'Saturday'), ('SU', 'Sunday')], max_length=2)),
                ('league', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kpbt.League')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_teams', models.PositiveSmallIntegerField()),
                ('designation', models.CharField(choices=[('A', 'Adult'), ('S', 'Senior'), ('J', 'Junior'), ('N', 'Any')], max_length=1)),
                ('gender', models.CharField(choices=[('M', 'Men'), ('W', 'Women'), ('X', 'Mixed')], max_length=1)),
                ('playing_strength', models.PositiveSmallIntegerField(default=1)),
                ('max_roster_size', models.PositiveSmallIntegerField(default=9)),
                ('entering_average', models.PositiveSmallIntegerField(default=0)),
                ('is_handicap', models.BooleanField(default=False)),
                ('handicap_scratch', models.PositiveSmallIntegerField(default=0)),
                ('handicap_percentage', models.PositiveSmallIntegerField(default=0)),
                ('bye_team_point_threshold', models.PositiveSmallIntegerField(default=0)),
                ('absentee_score', models.PositiveSmallIntegerField(default=0)),
                ('game_point_value', models.PositiveSmallIntegerField(default=0)),
                ('series_point_value', models.PositiveSmallIntegerField(default=0)),
                ('league', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kpbt.League')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueBowler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games_bowled', models.PositiveSmallIntegerField(default=0)),
                ('league_average', models.PositiveSmallIntegerField(default=0)),
                ('league_high_scratch_game', models.PositiveSmallIntegerField(default=0)),
                ('league_high_handicap_game', models.PositiveSmallIntegerField(default=0)),
                ('league_high_scratch_series', models.PositiveSmallIntegerField(default=0)),
                ('league_high_handicap_series', models.PositiveSmallIntegerField(default=0)),
                ('league_total_scratch', models.PositiveSmallIntegerField(default=0)),
                ('league_total_handicap', models.PositiveSmallIntegerField(default=0)),
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
        migrations.AddField(
            model_name='league',
            name='secretary',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CenterAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_addr', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Conneticut'), ('DE', 'Deleware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HA', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virgina'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2)),
                ('zip_code', models.CharField(max_length=10)),
                ('bowling_center', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='kpbt.BowlingCenter')),
            ],
        ),
    ]
