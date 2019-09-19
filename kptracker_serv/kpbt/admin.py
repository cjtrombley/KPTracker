from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from kpbt.models import cUser
from .forms import cUserCreationForm, cUserChangeForm
# Register your models here.

"""
class UserCreationForm(forms.ModelForm):
	#Form for creating new users#
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
	
	class Meta:
		model = cUser
		fields = ('username', 'email')
		
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
			
class UserChangeForm(forms.ModelForm):
	$form for updating users$
	
	password = ReadOnlyPasswordHashField()
	
	class Meta:
		model = cUser
		fields = ('password', 'email', 'is_active', 'is_admin')
		
	def clean_password(self):
	
		return self.initial["password"]
		
"""

class UserAdmin(BaseUserAdmin):
	#the forms to add and change Users
	form = cUserChangeForm
	add_form = cUserCreationForm

	list_display = ('username', 'email', 'is_admin')
	list_filter = ('is_admin',)
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Permissions', {'fields': ('is_admin',)}),
	)
	
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')}
		),
	)
	search_fields= ('username', 'email',)
	ordering = ('username', 'email',)
	filter_horizontal = ()
	

admin.site.register(cUser, UserAdmin)


