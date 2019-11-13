from django import forms
from kpbt.teams.models import Team, TeamRoster
from kpbt.accounts.models import BowlerProfile
from django.contrib.auth.models import User
from django.forms import formset_factory
from kpbt.accounts.forms import CreateUserBowlerProfileForm, UpdateUserBowlerProfileForm

class CreateTeamForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ('league', 'number', 'name')
		
		
class TeamRosterForm(forms.ModelForm): #extends BowlerProfile?
	
	class Meta:
		model = BowlerProfile
		fields = ('__all__')
	
class ViewRosterForm(forms.ModelForm):

	league_average = forms.IntegerField()

	class Meta:
		model = BowlerProfile
		fields = ('first_name', 'last_name', 'league_average')

class DeleteRosterForm(forms.ModelForm):
	
	delete_roster = forms.BooleanField()
	
	class Meta:
		model = TeamRoster
		fields = ('bowler',)



	
#class TeamRosterForm(forms.Form):
#	team = forms.ModelChoiceField(queryset=Team.objects.all())
#	bowlers = forms.ModelChoiceField(queryset=User.objects.all())