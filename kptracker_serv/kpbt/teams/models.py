from django.db import models
from kpbt.leagues.models import League

class Team(models.Model):
	
	league = models.ForeignKey('League', on_delete=models.CASCADE, 
		related_name='teams', verbose_name=('league'))
	
	number = models.PositiveSmallIntegerField()
	name = models.CharField(max_length=32, default="")
	total_pinfall = models.PositiveSmallIntegerField(default=0)
	total_handicap_pins = models.PositiveIntegerField(default=0)
	total_scratch_pins = models.PositiveIntegerField(default=0)
	team_points = models.PositiveSmallIntegerField(default=0)
	
	def __str__(self):
		return self.name
