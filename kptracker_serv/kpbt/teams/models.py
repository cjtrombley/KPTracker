from django.db import models
#from kpbt.leagues.models import League
from kpbt.accounts.models import BowlerProfile
from django.contrib.auth.models import User

from num2words import num2words

class Team(models.Model):
	
	league = models.ForeignKey('League', on_delete=models.CASCADE,
		related_name = 'teams', verbose_name = 'league')
	
	number = models.PositiveSmallIntegerField()
	name = models.CharField(max_length=32, default="")
	total_pinfall = models.PositiveSmallIntegerField(default=0)
	total_handicap_pins = models.PositiveIntegerField(default=0)
	total_scratch_pins = models.PositiveIntegerField(default=0)
	team_points_won = models.PositiveSmallIntegerField(default=0)
	team_points_lost = models.PositiveIntegerField(default=0)
	
	roster = models.ManyToManyField(BowlerProfile, through='TeamRoster')
	
	def update_points(self, points_won, points_lost):
		self.team_points_won += points_won
		self.team_points_lost += points_lost
	
	def update_pinfall(self, handicap, game_scores):
		scratch_score = 0
		handicap_score = 0
		
		for score in game_scores:
			if score[0] == 'A':
				scratch_score += int(score[1:])
			else:
				scratch_score += int(score)
				handicap_score += scratch_score + int(handicap)
				
		self.total_scratch_pins += scratch_score
		self.total_handicap_pins += handicap_score
		self.save()
		self.total_pinfall += scratch_score + handicap_score
		
	def create_team(league, number):
		new_team = Team(league=league, number=number,
			name='Team' + num2words(number))
		#new_team.save(commit=False)
		
		#new_team.league = league
		#new_team.number = number
		#new_team.name = 'Team' + num2words(new_team.number)
		
	
		'''
		roster_size = league.leaguerules.playing_strength
		for _ in range(roster_size):
			empty_bowler = BowlerProfile().save(commit=False)
			team_roster = TeamRoster(team=new_team, bowler= empty_bowler)
			team_roster.save(commit=False)
			new_team.save()
		'''	
		return new_team
	
	#def create_roster_record(team, bowler):
	#	empty_bowler = BowlerProfile()
	#	roster_record = TeamRoster(team=team, bowler= empty_bowler)
		
	#	return roster_record
		
	def __str__(self):
		return self.name
		
class TeamRoster(models.Model):
	bowler = models.ForeignKey('BowlerProfile', on_delete=models.CASCADE, related_name='roster_record')
	team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='roster_record')
	games_with_team = models.PositiveSmallIntegerField(default=0)
	
	is_substitute = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	lineup_position = models.PositiveSmallIntegerField(default=0)
	
	
	def __str__(self):
		return self.bowler.first_name + " " + self.bowler.last_name + ", " + self.team.name
	
	def get_bowler(self):
		return self.bowler
	
	def create_roster_record(team, bowler):
		roster_record = TeamRoster(bowler=bowler, team=team)
		return roster_record
	
	def swap_roster_spots(self, roster_record):
		if self.team is roster_record.team:
			swap = roster_record.lineup_position
			roster_record.lineup_position = self.lineup_position
			self.lineup_position = swap
	
	def set_lineup_position(self, position):
		self.lineup_position = position
	
	def update_games(self, game_scores):
		counter = 0
		for score in game_scores:
			if score[0] is 'A':
				pass
			else:
				counter += 1
		self.games_with_team += counter
		