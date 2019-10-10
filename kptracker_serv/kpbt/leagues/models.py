from django.db import models
from django.contrib.auth.models import User
from kpbt.centers.models import BowlingCenter
from kpbt.teams.models import Team
from django.core.exceptions import ObjectDoesNotExist

from collections import deque
from itertools import islice
from dateutil import rrule
import datetime


class League(models.Model):
	
	bowling_center = models.ForeignKey('BowlingCenter', on_delete=models.SET_NULL, null=True,
		related_name='leagues', verbose_name=('bowling center'))
	bowlers = models.ManyToManyField(User, through='LeagueBowler')
	
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
	league = models.OneToOneField(League, on_delete=models.CASCADE)
	
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
	league = models.ForeignKey(League, on_delete=models.CASCADE)
	
	league_average = models.PositiveSmallIntegerField()
	league_high_game = models.PositiveSmallIntegerField()
	league_high_series = models.PositiveSmallIntegerField()
	league_total_scratch = models.PositiveSmallIntegerField()
	league_total_handicap = models.PositiveSmallIntegerField()
	

class Schedule(models.Model):
	league = models.OneToOneField(League, on_delete=models.CASCADE)

	date_starting = models.DateField()
	date_ending = models.DateField()
	num_weeks = models.PositiveSmallIntegerField(default=0)
	start_time = models.TimeField()
	
	current_week = models.PositiveSmallIntegerField(default=1)
	
	def calc_num_weeks(self):
		weeks = rrule.rrule(rrule.WEEKLY, dtstart=self.date_starting, until=self.date_ending)
		self.num_weeks = weeks.count()
		
	
	def advance_week(self):
		current_week += 1
	
	
	def pairings(self):
		this_league = self.league
		
		teams = this_league.teams.all()
		
		if len(teams) % 2:
			teams.append('Bye')
		
		mid = len(teams) // 2
		dq1 = deque(islice(teams, None, mid))
		dq2 = deque(islice(teams, mid, None))
		
		week_range = self.num_weeks - 1
		
		for _ in range(week_range):
			yield list(zip(dq1, dq2))
			start = dq1.popleft()
			dq1.appendleft(dq2.popleft())
			dq2.append(dq1.pop())
			dq1.appendleft(start)
		