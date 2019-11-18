from django import forms
from kpbt.accounts.models import BowlerProfile
from kpbt.games.models import Series
#from kpbt.leagues.models import Legaue, LeagueSchedule

class ImportScoresForm(forms.Form):
	week_number = forms.IntegerField(min_value=1, max_value=52)
	
	def clean(self):
		cleaned_data = super().clean()

'''
class CreateSeriesForm(forms.ModelForm):
	class Meta:
		model = Series
		fields = ('bowler', 'league', 'team', 'series_date', 'applied_average', 'game_one_score', 'game_two_score', 'game_three_score')
'''

class EditScoresForm(forms.ModelForm):
	
	#bowler_id = forms.IntegerField()
	#bowler_first_name = forms.CharField(max_length=32, disabled=True)
	
	bowler = forms.ChoiceField(disabled=True)
	
	class Meta:
		model = Series
		fields = ('bowler', 'applied_average', 'game_one_score', 'game_two_score', 'game_three_score')