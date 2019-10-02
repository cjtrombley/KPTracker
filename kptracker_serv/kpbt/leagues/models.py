from django.db import models
from kpbt.centers.models import BowlingCenter


class League(models.Model):
	DESIGNATION = (
		('A', 'Adult'),
		('S', 'Senior'),
		('J', 'Junior')
	)
	
	GENDER = (
		('M', 'Men'),
		('W', 'Women'),
		('X', 'Mixed'),
	)

	bowling_center = models.ForeignKey('BowlingCenter', on_delete=models.CASCADE,
		related_name='bowling_center', verbose_name=('bowling center'))
	bowlers = models.ManyToManyField('BowlerProfile', through='LeagueBowler')
	
	name = models.CharField(max_length=32, default=id)
	num_teams = models.PositiveSmallIntegerField()
	designation = models.CharField(max_length=1, choices=DESIGNATION)
	gender = models.CharField(max_length=1, choices=GENDER)
	min_roster_size = models.PositiveSmallIntegerField()
	max_roster_size = models.PositiveSmallIntegerField()
	is_handicap = models.BooleanField(default=False)
	handicap_scratch = models.PositiveSmallIntegerField()
	allow_substitutes = models.BooleanField(default=False)
	bye_team_point_threshold = models.PositiveSmallIntegerField()
	absentee_score = models.PositiveSmallIntegerField()
	game_point_value = models.PositiveSmallIntegerField()
	series_point_value = models.PositiveSmallIntegerField()
	

class LeagueBowler(models.Model):
	bowler = models.ForeignKey('BowlerProfile', on_delete=models.CASCADE)
	league = models.ForeignKey('League', on_delete=models.CASCADE)
	
	league_average = models.PositiveSmallIntegerField()
	league_high_game = models.PositiveSmallIntegerField()
	league_high_series = models.PositiveSmallIntegerField()
	league_total_scratch = models.PositiveSmallIntegerField()
	league_total_handicap = models.PositiveSmallIntegerField()
	

class LeagueSchedule(models.Model):
	league = models.OneToOneField('LeagueSchedule', on_delete=models.SET_NULL, null=True)
	
	date_started = models.DateField()
	date_ending = models.DateField()
	num_weeks = models.PositiveSmallIntegerField()
	start_time = models.TimeField()



class WeeklyPairing(models.Model):
	league = models.ForeignKey('League', on_delete=models.SET_NULL, null=True,
		related_name='league', verbose_name=('weekly_pairing'))