from django.db import models
from kpbt.leagues.models import League

class Team(models.Model):
	
	league = models.ForeignKey('League', on_delete=models.CASCADE, 
		related_name='teams', verbose_name=('league'))
	
	number = models.PositiveSmallIntegerField(default=id)
	name = models.CharField(max_length=32, default="")
	total_pinfall = models.PositiveSmallIntegerField()
	total_handicap_pins = models.PositiveIntegerField()
	total_scratch_pins = models.PositiveIntegerField()
	team_points = models.PositiveSmallIntegerField()
