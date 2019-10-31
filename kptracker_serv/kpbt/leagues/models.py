from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from kpbt.accounts.models import BowlerProfile
from kpbt.centers.models import BowlingCenter
from kpbt.teams.models import Team
from kpbt.games.models import Series
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from kptracker.settings import SCHEDULEFILES_FOLDER as SCHEDULEDIR


from collections import deque
from itertools import islice
from dateutil import rrule
import datetime
import itertools
from num2words import num2words

class League(models.Model):
	
	bowling_center = models.ForeignKey('BowlingCenter', on_delete=models.SET_NULL, null=True,
		related_name='leagues', verbose_name=('bowling center'))
	bowlers = models.ManyToManyField('BowlerProfile', through='LeagueBowler')
	
	name = models.CharField(max_length=32)
	
	def __str__(self):
		return self.bowling_center.name + ", " + self.name
		
	def set_center(self, center_name):
		center = get_object_or_404(BowlingCenter, name=center_name)
		self.bowling_center = center
	
	def set_name(self, name):
		self.name = name
		
	def current_week(self):
		return self.schedule.current_week
		
		
		
	def score_week(self, week_number):
		
		weekly_pairs = self.schedule.pairings()
		
		this_week = weekly_pairs[week_number]
		
		for pair in this_week:
			teams = pair.split('-')
			
			team_one = get_object_or_404(Team, league=self, number=teams[0])
			team_two = get_object_or_404(Team, league=self, number=teams[1])
			
			game_points = self.leaguerules.game_point_value
			series_points = self.leaguerules.series_point_value
			weekly_points = self.leaguerules.total_weekly_points
			
			team_one_total_series = 0
			team_two_total_series = 0
			
			for i in range(1, 4):
				
				t1_hc_score = Series.calc_team_handicap_game_score(team_one, week_number, i)
				team_one_total_series += t1_hc_score
				t2_hc_score = Series.calc_team_handicap_game_score(team_two, week_number, i)
				team_two_total_series += t2_hc_score
				
				if t1_hc_score > t2_hc_score:
					team_one.team_points_won += game_points
					team_two.team_points_lost += game_points
				elif t1_hc_score < t2_hc_score:
					team_one.team_points_lost += game_points
					team_two.team_points_won += game_points
				else:
					team_one.team_points_won += game_points / 2
					team_one.team_points_lost += game_points / 2
					team_two.team_points_won += game_points / 2
					team_two.team_points_lost += game_points / 2
			
			if team_one_total_series > team_two_total_series:
				team_one.team_points_won += series_points
				team_two.team_points_lost += series_points
			elif team_one_total_series < team_two_total_series:
				team_one.team_points_lost += series_points
				team_two.team_points_won += series_points
			else:
				team_one.team_points_lost += series_points
				team_two.team_points_lost += series_points
			
			team_one.save()
			team_two.save()

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
	playing_strength = models.PositiveSmallIntegerField(default=1)
	max_roster_size = models.PositiveSmallIntegerField(default=9)
	is_handicap = models.BooleanField(default=False)
	handicap_scratch = models.PositiveSmallIntegerField(default=0)
	handicap_percentage = models.PositiveSmallIntegerField(default=0)
	allow_substitutes = models.BooleanField(default=False)
	bye_team_point_threshold = models.PositiveSmallIntegerField(default=0)
	absentee_score = models.PositiveSmallIntegerField(default=0)
	game_point_value = models.PositiveSmallIntegerField(default=0)
	series_point_value = models.PositiveSmallIntegerField(default=0)

	def total_weekly_points(self):
		return (3 * game_point_value) + series_point_value

class LeagueBowler(models.Model):
	bowler = models.ForeignKey(BowlerProfile, on_delete=models.CASCADE)
	league = models.ForeignKey(League, on_delete=models.CASCADE)
	
	games_bowled = models.PositiveSmallIntegerField(default=0)
	league_average = models.PositiveSmallIntegerField(default=0)
	league_high_scratch_game = models.PositiveSmallIntegerField(default=0)
	league_high_handicap_game = models.PositiveSmallIntegerField(default=0)
	league_high_scratch_series = models.PositiveSmallIntegerField(default=0)
	league_high_handicap_series = models.PositiveSmallIntegerField(default=0)
	league_total_scratch = models.PositiveSmallIntegerField(default=0)
	league_total_handicap = models.PositiveSmallIntegerField(default=0)
	
	
	def update(self, average, handicap, scores):
		series_scratch_score = 0
		series_handicap_score = 0
		games_played_counter = 0
		
		for score in scores:
			if score[0] == 'A':
				#Bowler was absent for this game, does not count toward league stats
				pass
			else:
				games_played_counter += 1
				series_scratch_score += int(score)
				if int(score) > self.league_high_scratch_game: #Update highest scratch score
					self.league_high_scratch_game = int(score)
				
				
				game_handicap_score = int(score) + int(handicap)
				series_handicap_score += game_handicap_score
				if game_handicap_score > self.league_high_handicap_game: #Update highest handicap game score
					self.league_high_handicap_game = game_handicap_score

		self.games_bowled += games_played_counter
		
		self.league_total_scratch += series_scratch_score
		if series_scratch_score > self.league_high_scratch_series:
			self.league_high_scratch_series = series_scratch_score
			
		self.league_total_handicap += series_handicap_score
		if series_handicap_score > self.league_high_handicap_series:
			self.league_high_handicap_series = series_handicap_score
	

		self.update_average()
	
	def update_average(self):
		self.league_average = self.league_total_scratch / self.games_bowled
		
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
	
	
	def pairings(self, current_week=""):
		num_teams = self.league.leaguerules.num_teams
		num_weeks = self.num_weeks // 2
		
		if num_teams % 2:
			num_teams += 1
			
		filename = str(num_teams) + 'teams'
		filedir = SCHEDULEDIR + filename + '.csv'
		
		pairings = [None] * num_weeks
		with open(filedir) as schedule:
			
			schedule.readline() #skip first line to allow week number to align with list index
			for i in range(1, num_weeks):
				weekly_pairings = schedule.readline()
				
				weekly_pairing_list = weekly_pairings.strip('\n').split(',')
				pairings[i] = weekly_pairing_list
			
		if current_week:
			return [pairings[current_week]]
		else:
			return pairings
				
			