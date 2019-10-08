from django import forms
from django.contrib.auth.models import User
from kpbt.games.models import Game
#from kpbt.leagues.models import Legaue, LeagueSchedule

class CreateGameForm(forms.ModelForm):
	class Meta:
		model = Game
		fields = ('bowler', 'league', 'team', 'series_date', 'applied_average', 'game_one_score', 'game_two_score', 'game_three_score')
