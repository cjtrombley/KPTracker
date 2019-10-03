from django import forms
from kpbt.accounts.models import UserProfile, BowlerProfile

class CreateUserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('first_name', 'last_name', 'email')
		
class CreateBowlerProfileForm(forms.ModelForm):
	class Meta:
		model = BowlerProfile
		fields = ('date_of_birth', 'hand', 'designation', 'is_sanctioned')
"""		
class DisplayProfile(forms.Form):
	first_name = forms.CharField(label='first name', max_length=64)
	last_name = forms.CharField(label='last name', max_length=64)
	date_of_birth = 
"""