from django.db import models
from django.contrib.auth.models import User
from kpbt.teams.models import Team
from kpbt.leagues.models import League


class Game(models.Model):
	bowler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True)
	league = models.ForeignKey('League', on_delete=models.SET_NULL, null=True)

	
	series_date = models.DateField()
	applied_average = models.PositiveSmallIntegerField()
	game_one_score = models.PositiveSmallIntegerField()
	game_two_score = models.PositiveSmallIntegerField()
	game_three_score = models.PositiveSmallIntegerField()