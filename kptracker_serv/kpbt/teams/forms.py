from django import forms
from kpbt.teams.models import Team

class CreateTeamForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ('league', 'number', 'name')