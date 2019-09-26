from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import *

class cUserCreationForm(forms.ModelForm):
	"""Form for creating new users"""
	firstname = forms.CharField(label="First Name", widget=forms.TextInput)
	lastname = forms.CharField(label="Last Name", widget=forms.TextInput)
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
	
	class Meta:
		model = cUser
		fields = ('username', 'first_name', 'last_name', 'email')
		
		def clean_password2(self):
			#check password entries match
			password1 = self.cleaned_data.get("password1")
			password2 = self.cleaned_data.get("password2")
			if password1 and password2 and password1 != password2:
				raise forms.ValidataionError("Passwords don't match!")
			return password2
		
		def save(self, commit=True):
			#save the provided password in a hashed format
			user = super().save(commit=Fale)
			user.set_password(self.cleaned_data["password1"])
			if commit:
				user.save()
			return user
			
class cUserChangeForm(forms.ModelForm):
	"""form for updating users"""
	
	password = ReadOnlyPasswordHashField()
	
	class Meta:
		model = cUser
		fields = ('password', 'email', 'is_active', 'is_admin')
		
	def clean_password(self):
	
		return self.initial["password"]
		

class BowlerCreationForm(forms.ModelForm):
	class Meta:
		fields = ('date_of_birth', 'is_sanctioned', 'hand', 'team')
		model = Bowler