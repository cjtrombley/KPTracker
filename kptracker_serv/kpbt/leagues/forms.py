from django import forms
from kpbt.leagues.models import League, LeagueRules, Schedule
from kpbt.centers.models import BowlingCenter

class LeagueCreationForm(forms.ModelForm):
	
	league_name = forms.CharField(max_length=32)
	#bowling_center = ModelChoiceField(queryset=BowlingCenter
	
	class Meta:
		model = LeagueRules
		fields = ('league_name', 'num_teams', 'designation', 'gender', 
			'playing_strength', 'max_roster_size', 'is_handicap', 'handicap_scratch', 'allow_substitutes',
			'bye_team_point_threshold', 'absentee_score', 'game_point_value', 'series_point_value')
			
class CreateScheduleForm(forms.ModelForm):
	
	class Meta:
		model = Schedule
		fields = ('date_starting', 'date_ending', 'start_time')
		
class UpdateLeagueSecretaryForm(forms.ModelForm):
	class Meta:
		model = League
		fields = ('secretary',)