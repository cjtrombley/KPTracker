from django import forms
from kpbt.accounts.models import UserProfile, BowlerProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#class CreateUserProfileForm(forms.ModelForm):
	#class Meta:
		#model = UserProfile
		#fields = ('first_name', 'last_name', 'email', 'date_of_birth')
	
class RegisterForm(UserCreationForm):
	email = forms.EmailField()
	
	class Meta:
		model = User 
		fields = ('username', 'email', 'password1', 'password2', )
	
class CreateUserBowlerProfileForm(forms.ModelForm):
	
	class Meta:
		model = BowlerProfile
		fields = ('first_name', 'last_name', 'hand', 'designation', 'gender')
		
		
class UpdateUserBowlerProfileForm(forms.ModelForm):
		
	class Meta:
		model = BowlerProfile
		exclude = ['user', 'is_linked']
		fields = ('__all__')
		
'''		
class UpdateLeagueBowlerProfileForm(forms.ModelForm):
		
		
	class Meta:
		model = BowlerProfile
		exclude = ['user']
		fields = ('__all__')
		
		def has_changed(self):
			changed_data = super(UpdateLeagueBowlerProfileForm, self).has_changed()
			return bool(changed_data)
			
class UpdateLeagueBowlerProfileFormset(BaseModelFormSet):
	def clean(self):
		super(UpdateLeagueBowlerProfileFormset, self).clean()

'''

		
"""		
class DisplayProfile(forms.Form):
	first_name = forms.CharField(label='first name', max_length=64)
	last_name = forms.CharField(label='last name', max_length=64)
	date_of_birth = 
"""