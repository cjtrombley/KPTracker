from django.db import models
#from kpbt.leagues.models import League
#from kpbt.accounts.models import BowlerProfile
from django.contrib.auth.models import User

class Team(models.Model):
	
	league = models.ForeignKey('League', on_delete=models.CASCADE,
		related_name = 'teams', verbose_name = 'league')
	
	number = models.PositiveSmallIntegerField()
	name = models.CharField(max_length=32, default="")
	total_pinfall = models.PositiveSmallIntegerField(default=0)
	total_handicap_pins = models.PositiveIntegerField(default=0)
	total_scratch_pins = models.PositiveIntegerField(default=0)
	team_points = models.PositiveSmallIntegerField(default=0)
	
	roster = models.ManyToManyField(User, through='TeamRoster')
		
	def __str__(self):
		return self.name
		
class TeamRoster(models.Model):

	bowler = models.ForeignKey(User, on_delete=models.CASCADE)
	team = models.ForeignKey('Team', on_delete=models.CASCADE)
	games_with_team = models.PositiveSmallIntegerField(default=0)
	is_substitute = models.BooleanField(default=False)
	
	def __str__(self):
		return self.bowler.first_name + " " + self.bowler.last_name + ", " + self.team.name
		
	
