from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from kpbt.accounts.models import BowlerProfile
from kpbt.centers.models import BowlingCenter
from kpbt.teams.models import Team, TeamRoster
from kpbt.games.models import Series
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.files import File
from kptracker.settings import SCHEDULEFILES_FOLDER as SCHEDULEDIR
from kptracker.settings import BACKUPS_FOLDER as BACKUPSDIR


from collections import deque
from itertools import islice
from dateutil import rrule
import datetime
import itertools
from num2words import num2words

import math, json

class League(models.Model):
	
	bowling_center = models.ForeignKey('BowlingCenter', on_delete=models.SET_NULL, null=True,
		related_name='leagues', verbose_name=('bowling center'))
	bowlers = models.ManyToManyField('BowlerProfile', through='LeagueBowler')
	
	secretary = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
	
	name = models.CharField(max_length=32)
	current_week = models.PositiveSmallIntegerField(default=1)
	week_pointer = models.PositiveSmallIntegerField(default=1)
	
	
	def __str__(self):
		return self.bowling_center.name + ", " + self.name
		
	def set_center(self, center_name):
		center = get_object_or_404(BowlingCenter, name=center_name)
		self.bowling_center = center
	
	def set_name(self, name):
		self.name = name
		
	def set_secretary(self, user):
		self.secretary = user
		self.save()
		
	#def current_week(self):
		#return self.schedule.current_week
		
	def create_pairings(self):
		num_teams = self.leaguerules.num_teams
		num_weeks = self.schedule.num_weeks # // 2
		
		if num_teams % 2:
			num_teams += 1
			
		filename = str(num_teams) + 'teams'
		filedir = SCHEDULEDIR + filename + '.csv'
		
		pairings = [None] * num_weeks
		with open(filedir) as schedule:
			
			schedule.readline() #skip first line to allow week number to align with list index
			
			raw_weekly_pairings = schedule.readlines()
			week_number_counter=1
			for raw_pairings in raw_weekly_pairings:

				weekly_pairing_list = raw_pairings.strip('\n').split(',')
				
				pair_counter = 1
				for pair in weekly_pairing_list:
					
					teams = pair.split('-')
					team_one = Team.objects.get(league=self, number=teams[0])
					team_two = Team.objects.get(league=self, number=teams[1])
					new_pairing = WeeklyPairings.objects.create(league=self, team_one=team_one, team_two=team_two, week_number=week_number_counter, lane_pair = math.ceil(pair_counter))
					
					new_pairing.save()
					pair_counter +=1
				
				week_number_counter += 1
		
	def score_week(self, week_number): #needs to be updated to include handicap stuff
		
		#weekly_pairs = self.schedule.pairings()
		
		#this_week = weekly_pairs[week_number]
		
		this_week = WeeklyPairings.objects.filter(league=self, week_number=week_number)
		
		for pair in this_week:
			#teams = pair.split('-')
			
			#team_one = get_object_or_404(Team, league=self, number=teams[0])
			#team_two = get_object_or_404(Team, league=self, number=teams[1])
			team_one = pair.team_one
			team_two = pair.team_two
			
			team_one_series = Series.objects.filter(league=self, team=team_one, week_number=week_number)
			team_two_series = Series.objects.filter(league=self, team=team_two, week_number=week_number)
			
			game_points = self.leaguerules.game_point_value
			series_points = self.leaguerules.series_point_value
			weekly_points = self.leaguerules.total_weekly_points()
			
			team_one_total_series = 0
			team_two_total_series = 0
			
			team_one_points = 0
			team_two_points = 0
			
			for i in range(1, 4): #Games number 1-3
				
				t1_hc_score = Series.calc_team_handicap_game_score(team_one, week_number, i, team_one_series)
				team_one_total_series += t1_hc_score
				t2_hc_score = Series.calc_team_handicap_game_score(team_two, week_number, i, team_two_series)
				team_two_total_series += t2_hc_score
				
				if t1_hc_score > t2_hc_score:
					#team_one.team_points_won += game_points
					team_one_points += game_points
					#team_two.team_points_lost += game_points
					
				elif t1_hc_score < t2_hc_score:
					#team_one.team_points_lost += game_points
					#team_two.team_points_won += game_points
					team_two_points += game_points
				else:
					team_one_points += game_points / 2
					team_two_points += game_points / 2
					#team_one.team_points_won += game_points / 2
					#team_one.team_points_lost += game_points / 2
					#team_two.team_points_won += game_points / 2
					#team_two.team_points_lost += game_points / 2
			
			if team_one_total_series > team_two_total_series:
				team_one_points += series_points
				#team_one.team_points_won += series_points
				#team_two.team_points_lost += series_points
			elif team_one_total_series < team_two_total_series:
				team_two_points += series_points
				#team_one.team_points_lost += series_points
				#team_two.team_points_won += series_points
			#else:
				#team_one.team_points_lost += series_points
				#team_two.team_points_lost += series_points
			
			
			
			#team_one_series = Series.objects.filter(league=self, team=team_one, week_number=week_number)
			#team_two_series = Series.objects.filter(league=self, team=team_two, week_number=week_number)
			
			for series_one in team_one_series:
				series_one.set_points_won(team_one_points)
				series_one.set_points_lost(weekly_points - team_one_points)
				series_one.save()
				
				
			
			for series_two in team_two_series:
				series_two.set_points_won(team_two_points)
				series_two.set_points_lost(weekly_points - team_two_points)
				series_two.save()
			
			team_one.update_points(team_one_points, weekly_points - team_one_points)
			team_two.update_points(team_two_points, weekly_points - team_two_points)
			team_one.save()
			team_two.save()

	def create_weekly_score_backup(self):
		week_number = self.current_week
		backup_filename= str(self.id) + '_' + str(week_number) + '.json'
		
		backup = open(BACKUPSDIR + backup_filename, 'w') 
		backup_dict = {}
		
		
		#Backups file header information
		header_dict = { "league_name": self.name , "current_week" : str(week_number) } 
		backup_dict.update( {"header" : header_dict})
		
		
		#Teams Backup Info
		teams_set = self.teams.all()
		teams = {}
		for team in teams_set:
			team_dict = {team.id :  {"total_scratch_pins" : team.total_scratch_pins, "total_handicap_pins": team.total_handicap_pins, "total_pinfall" : team.total_pinfall, "team_points_won" : team.team_points_won, "team_points_lost" : team.team_points_lost}}
		
			teams.update(team_dict)
		backup_dict.update({"teams" : teams})
		
		
		
		'''
		backup.write('TEAMS'+ '\n')
		for team in teams:
			backup.write(str(team.number) + ': ' + team.name + '\n')
			
			pinfalls_list = []
			pinfalls_list.append('total_scratch_pins : ' + str(team.total_scratch_pins) + '\n')
			pinfalls_list.append('total_handicap_pins : ' + str(team.total_handicap_pins) + '\n')
			pinfalls_list.append('total_pinfall : ' + str(team.total_pinfall) + '\n')
			
			backup.write(''.join(pinfalls_list))
		
			points_list = []
			points_list.append('team_points_won : ' + str(team.team_points_won) + '\n')
			points_list.append('team_points_lost : ' + str(team.team_points_lost) + '\n')
			
			backup.write(''.join(points_list))
		'''
		
		#LeagueBowler/TeamRoster Backups
		lb_records = LeagueBowler.objects.filter(league=self)
		tr_records = TeamRoster.objects.filter(id__in=teams)
		
		team_rosters_dict = {}
		lb_records_dict = {}
		
		for lb in lb_records:
			lb_dict = {lb.id : {"league_average" : lb.league_average, "games_bowled" : lb.games_bowled, "league_total_scratch" : lb.league_total_scratch, "league_total_handicap" : lb.league_total_handicap, "league_high_scratch_game" : lb.league_high_scratch_game, "league_high_handicap_game" : lb.league_high_handicap_game, "league_high_scratch_series" : lb.league_high_scratch_series, "league_high_handicap_series" : lb.league_high_handicap_series} }
			lb_records_dict.update(lb_dict)
		backup_dict.update({"league_bowler_records" : lb_records_dict})
		
		
		for tr in tr_records:
			tr_dict = {tr.id : { "games_with_team" : tr.games_with_team }}
			team_rosters_dict.update(tr_dict)
		backup_dict.update({"team_roster_records" : team_rosters_dict})
		
		json.dump(backup_dict, backup, indent=4)
		
		with open(BACKUPSDIR + backup_filename) as backup:
			data = json.load(backup)
		
		#print(teams)
		
		''' 
		Example for how to access lists of backup items
		
		for items in data['teams'].items():
			for key, value in items[1].items():
				print(key, ',', value)
		'''	
		
		
		#print(data['teams']['1'])
		#for team in data['teams']:
			#rint(team.id['total_scratch_pins'])
		#print(data['header']['league_name'])
	
		
		backup.close()
		
	def advance_week(self):
		self.current_week += 1
		
	def set_week_pointer(self, week_selection):
		self.week_pointer = week_selection
		
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
	#allow_substitutes = models.BooleanField(default=False)
	bye_team_point_threshold = models.PositiveSmallIntegerField(default=0)
	absentee_score = models.PositiveSmallIntegerField(default=0)
	game_point_value = models.PositiveSmallIntegerField(default=0)
	series_point_value = models.PositiveSmallIntegerField(default=0)

	def total_weekly_points(self):
		return (3 * self.game_point_value) + self.series_point_value

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
	WEEKDAY = (
		('MO', 'Monday'),
		('TU', 'Tuesday'),
		('WE', 'Wednesday'),
		('TH', 'Thursday'),
		('FR', 'Friday'),
		('SA', 'Saturday'),
		('SU', 'Sunday'),
	)
	
	league = models.OneToOneField(League, on_delete=models.CASCADE)

	date_starting = models.DateField()
	date_ending = models.DateField()
	num_weeks = models.PositiveSmallIntegerField(default=0)
	start_time = models.TimeField()
	
	day_of_week = models.CharField(max_length=2, choices=WEEKDAY)
	
	#current_week = models.PositiveSmallIntegerField(default=1)
	
	def calc_num_weeks(self):
		weeks = rrule.rrule(rrule.WEEKLY, dtstart=self.date_starting, until=self.date_ending)
		self.num_weeks = weeks.count()
		
	
			
class WeeklyPairings(models.Model):
	league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='pairings')
	
	team_one = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='first_pair')
	team_two = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='second_pair')
	
	week_number = models.PositiveSmallIntegerField(default=0)
	lane_pair = models.PositiveSmallIntegerField(default=0)
	
	def __str__(self):
		return str(self.team_one.number) + " - " + str(self.team_two.number)
		
		
	def get_lanes_by_pairnumber(self):
		return str(self.lane_pair *2 - 1) + ' - ' + str(self.lane_pair*2)
