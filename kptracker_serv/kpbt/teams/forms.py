from django import forms
from kpbt.teams.models import Team, TeamRoster
from kpbt.accounts.models import BowlerProfile
from django.contrib.auth.models import User

class CreateTeamForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ('league', 'number', 'name')
		
		
class TeamRosterForm(forms.ModelForm):
	class Meta:
		model = TeamRoster
		fields = ('bowler', 'team', 'is_substitute')
		
#class TeamRosterForm(forms.Form):
#	team = forms.ModelChoiceField(queryset=Team.objects.all())
#	bowlers = forms.ModelChoiceField(queryset=User.objects.all())