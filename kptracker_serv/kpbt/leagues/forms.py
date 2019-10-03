from django import forms
from kpbt.leagues.models import League

class LeagueCreationForm(forms.ModelForm):
	class Meta:
		model = League
		fields = ('bowling_center', 'bowlers', 'name', 'num_teams', 'designation', 'gender', 
			'min_roster_size', 'max_roster_size', 'is_handicap', 'handicap_scratch', 'allow_substitutes',
			'bye_team_point_threshold', 'absentee_score', 'game_point_value', 'series_point_value')