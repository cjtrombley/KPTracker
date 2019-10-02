from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, login
from .forms import CreateUserProfileForm, CreateBowlerProfileForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

class IndexView(TemplateView):

	template_name = 'index.html'


def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('create_profile')
	else:
		form = UserCreationForm()
	return render(request, 'registration/signup.html', {'form': form})

@login_required
def create_profile(request):
	try:
		has_profile = request.user.userprofile
	except ObjectDoesNotExist:
		if request.method == 'POST':
		
			userprofile_form = CreateUserProfileForm(request.POST)
			bowlerprofile_form = CreateBowlerProfileForm(request.POST)
			if userprofile_form.is_valid() and bowlerprofile_form.is_valid():
				up = userprofile_form.save(commit=False)
				bp = bowlerprofile_form.save(commit=False)
			
				#up.void_default()
				request.user.userprofile = up
				request.user.bowlerprofile = bp
			
				request.user.userprofile.save()
				request.user.bowlerprofile.save()
			
				return redirect('index')
		else:
			userprofile_form = CreateUserProfileForm()
			bowlerprofile_form = CreateBowlerProfileForm()
		return render(request, 'registration/create_profile.html', {
		'userprofile': userprofile_form, 'bowlerprofile': bowlerprofile_form})
	else:
		return redirect('view_profile')

@login_required			
def view_profile(request):
	if request.method == 'POST':
		pass
	else:
		try: 
			userprofile = UserProfile.objects.get(pk=request.user.userprofile.id)
			bowlerprofile = BowlerProfile.objects.get(pk=request.user.bowlerprofile.id)
		except ObjectDoesNotExist:
			return redirect('create_profile')
		else:
			up_form = CreateUserProfileForm(instance=userprofile)
			bp_form = CreateBowlerProfileForm(instance=bowlerprofile)
		return render(
			request, 'registration/view_profile.html', {
			'up_form': up_form,
			'bp_form': bp_form,
		})
		return render(request, 'registration/profile', context={})