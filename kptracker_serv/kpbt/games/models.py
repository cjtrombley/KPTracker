from django.db import models
from kpbt.accounts.models import BowlerProfile
from kpbt.teams.models import Team
#from kpbt.leagues.models import League

from num2words import num2words


class Series(models.Model):
	bowler = models.ForeignKey(BowlerProfile, on_delete=models.SET_NULL, null=True)
	team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True)
	league = models.ForeignKey('League', on_delete=models.SET_NULL, null=True)

	
	series_date = models.DateField()
	week_number = models.PositiveSmallIntegerField()
	pair_number = models.PositiveSmallIntegerField()
	applied_average = models.PositiveSmallIntegerField()
	applied_handicap = models.PositiveSmallIntegerField()
	game_one_score = models.CharField(max_length=4)
	game_two_score = models.CharField(max_length=4)
	game_three_score = models.CharField(max_length=4)
	
	weekly_points_won = models.PositiveSmallIntegerField(default=0)
	weekly_points_lost = models.PositiveSmallIntegerField(default=0)
	
	
	
	def get_bowler_name(self):
		return self.bowler.get_name()
	
	def get_scratch_score(self):
		scratch_score = 0
		for score in [self.game_one_score, self.game_two_score, self.game_three_score]:
			if score[0] == 'A':
				pass
			else:
				scratch_score += int(score)
		return scratch_score
			
	def get_handicap_score(self):
		handicap_score = 0
		for score in [self.game_one_score, self.game_two_score, self.game_three_score]:
			if score[0] == 'A':
				pass
			else:
				handicap_score += int(score) + self.applied_handicap
		return handicap_score
	
	def set_points_won(self, points):
		self.weekly_points_won = points
		self.team.team_points_won += points
		
	def set_points_lost(self, points):
		self.weekly_points_lost = points
		self.team.team_points_lost += points
	
	@staticmethod	
	def calc_team_handicap_game_score(team, week_number, game_number, team_series):
		handicap_score = 0
		
		for game in team_series:
			gamefield = 'game_' + num2words(game_number) +'_score'
			handicap_score += int(getattr(game, gamefield)) + int(game.applied_handicap)
			#handicap_score += getattr(team_series, gamefield)  + team_series.applied_handicap
		
		return handicap_score
			
	@staticmethod
	def calc_team_scratch_game_score(team, week_number, game_number, team_series):
		scratch_score = 0
		
		for game in team_series:
			gamefield = 'game_' + num2words(game_number) +'_score'
			scratch_score += int(getattr(game, gamefield))
			
		return scratch_score