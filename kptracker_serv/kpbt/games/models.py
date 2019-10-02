from django.db import models
from kpbt.accounts.models import BowlerProfile
from kpbt.teams.models import Team
from kpbt.leauges.models import League


class Game(models.Model):
	bowler = models.ForeignKey('BowlerProfile', on_delete=models.SET_NULL, null=True)
	team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True)
	league = models.ForeignKey('League', on_delete=models.SET_NULL, null=True)

	
	series_date = models.DateField()
	applied_average = models.PositiveSmallIntegerField()
	game_one_score = models.PositiveSmallIntegerField()
	game_two_score = models.PositiveSmallIntegerField()
	gamee_three_score = models.PositiveSmallIntegerField()