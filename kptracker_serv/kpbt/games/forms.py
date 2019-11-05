from django import forms
from kpbt.accounts.models import BowlerProfile
from kpbt.games.models import Series
#from kpbt.leagues.models import Legaue, LeagueSchedule

class CreateSeriesForm(forms.ModelForm):
	class Meta:
		model = Series
		fields = ('bowler', 'league', 'team', 'series_date', 'applied_average', 'game_one_score', 'game_two_score', 'game_three_score')
