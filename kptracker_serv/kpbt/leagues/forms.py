from django import forms
from kpbt.leagues.models import League, LeagueRules, Schedule
from kpbt.centers.models import BowlingCenter



class LeagueCreationForm(forms.ModelForm):
	
	league_name = forms.CharField(max_length=32, widget= forms.TextInput(attrs={'placeholder':'League name'}))
	#bowling_center = ModelChoiceField(queryset=BowlingCenter
	
	num_teams = forms.IntegerField(widget = forms.NumberInput(attrs={'placeholder':'Number of teams'}))
	#designation = forms.ChoiceField(widget = forms.RadioSelect())
	
	playing_strength = forms.IntegerField(widget = forms.NumberInput(attrs={'placeholder':'Playing strength'}))
	max_roster_size = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Maximum roster size'}))
	entering_average = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Entering average'}))
	handicap_scratch = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Scratch figure'}))
	handicap_percentage = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Handicap percentage'}))
	bye_team_point_threshold = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Bye-Team point diff'}))
	absentee_score = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Blind score'}))
	game_point_value = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Game point value'}))
	series_point_value = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Series point value'}))
	
	class Meta:
		model = LeagueRules
		fields = ('league_name', 'num_teams', 'designation', 'gender', 
			'playing_strength', 'max_roster_size', 'is_handicap', 'handicap_scratch', 'handicap_percentage',
			'bye_team_point_threshold', 'absentee_score', 'game_point_value', 'series_point_value')
	
	
	
class UpdateLeagueRulesForm(forms.ModelForm):
	class Meta:
		model = LeagueRules
		fields = ('designation', 'gender', 'max_roster_size', 'handicap_scratch', 'handicap_percentage', 
			'bye_team_point_threshold', 'absentee_score', 'game_point_value', 'series_point_value')
			
class RenameLeagueForm(forms.ModelForm):
	class Meta:
		model = League
		fields = ('name',)
		
class CreateScheduleForm(forms.ModelForm):
	
	date_starting = forms.DateField(widget= forms.DateInput(attrs={'placeholder':'Start date'}))
	date_ending = forms.DateField(widget=forms.DateInput(attrs={'placeholder':'End date'}))
	start_time = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder':'Starting time'}))
	
	class Meta:
		model = Schedule
		fields = ('date_starting', 'date_ending', 'day_of_week', 'start_time')
		
class UpdateScheduleForm(forms.ModelForm):
	class Meta:
		model = Schedule
		fields = ('date_starting', 'date_ending', 'day_of_week', 'start_time')
		
class UpdateLeagueSecretaryForm(forms.ModelForm):
	class Meta:
		model = League
		fields = ('secretary',)
		
class MoveLeagueForm(forms.ModelForm):
	class Meta:
		model = League
		fields=('bowling_center',)
		
class SetWeekForm(forms.Form):
	week_pointer = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Set Week Number'}))
	current_week = forms.IntegerField(widget=forms.HiddenInput())
	
	def clean(self):
		cleaned_data = super().clean()
		
		week_pointer = cleaned_data.get('week_pointer')
		current_week = cleaned_data.get('current_week')
		
		if (week_pointer <=0):
			raise forms.ValidationError(
				"Week must be greater than 0."
			)
		elif (week_pointer > current_week):
			raise forms.ValidationError(
				"Week must be less than current week number"
				)
		