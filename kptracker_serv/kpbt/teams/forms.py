from django import forms
from kpbt.teams.models import Team, TeamRoster
from kpbt.accounts.models import BowlerProfile
from django.contrib.auth.models import User
from django.forms import formset_factory

class CreateTeamForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ('league', 'number', 'name')
		
		
class TeamRosterForm(forms.ModelForm):
	class Meta:
		model = TeamRoster
		fields = ('bowler', 'is_substitute')
	
RosterFormSet = formset_factory(TeamRosterForm, extra = 4)	
#class TeamRosterForm(forms.Form):
#	team = forms.ModelChoiceField(queryset=Team.objects.all())
#	bowlers = forms.ModelChoiceField(queryset=User.objects.all())