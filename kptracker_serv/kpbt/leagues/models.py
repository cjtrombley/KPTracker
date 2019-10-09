from django.db import models
from django.contrib.auth.models import User
from kpbt.centers.models import BowlingCenter
from django.core.exceptions import ObjectDoesNotExist


class League(models.Model):
	
	bowling_center = models.ForeignKey('BowlingCenter', on_delete=models.SET_NULL, null=True,
		related_name='leagues', verbose_name=('bowling center'))
	bowlers = models.ManyToManyField(User, through='LeagueBowler')
	rules = models.OneToOneField('LeagueRules', on_delete=models.CASCADE, default=1)
	
	name = models.CharField(max_length=32)
	
	def __str__(self):
		return self.bowling_center.name + ", " + self.name
		
	def set_center(self, center_name):
		try:
			center = BowlingCenter.objects.get(name=center_name)
		except ObjectDoesNotExist:
			print("Whoa")
		else:
			self.bowling_center = center
	
	def set_name(self, name):
		self.name = name

class LeagueRules(models.Model):
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
	bowler = models.ForeignKey(User, on_delete=models.CASCADE)
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