from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib.auth.forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from kpbt.accounts.forms import RegisterForm, CreateProfileForm, UpdateBowlerProfileForm #, CreateUserProfileForm
from kpbt.accounts.models import UserProfile, BowlerProfile
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist



def register(request):
	if request.method == 'POST':
		new_user_form = RegisterForm(request.POST)
		if new_user_form.is_valid():
			new_user = new_user_form.save()
			
			
			
			user_email = new_user_form.cleaned_data['email']
			user_profile = UserProfile.objects.create(user= new_user, email= user_email)
			#user_profile.user = new_user
		
			#new_user.save()
			user_profile.save()
			
			#new_user.userprofile = user_profile
			
			username = new_user_form.cleaned_data.get('username')
			raw_password = new_user_form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('create-profile')
	else:
		new_user_form = RegisterForm()
	return render(request, 'registration/register.html', {'form': new_user_form})



@login_required
def create_or_update_profile(request, username=""):
	'''
	try:
		#Check to see if request.user has an associated UserProfile. If so, we want to make sure it is not
		#overwritten during the update process
		
		has_profile = request.user.userprofile #Exception occurs if no profile is found
	'''	
	if request.method == 'POST':
		bowler_profile_form = UpdateBowlerProfileForm(request.POST)
		
		if bowler_profile_form.is_valid():
			updated_profile = bowler_profile_form.save(commit=False)
			request.user.bowlerprofile = updated_profile
			request.user.bowlerprofile.save()
			return redirect('view-profile-by-username', request.user.username)
	else:
		user = get_object_or_404(User, username=username)
		bowler_profile_form = UpdateBowlerProfileForm(instance=user.bowlerprofile)
	return render(request, 'accounts/update_profile.html', {'profile_form' : bowler_profile_form})
	
	'''
	except ObjectDoesNotExist: #User does not have associated UserProfile
	
		if request.method == 'POST':
			profile_form = CreateProfileForm(request.POST)
			
			if profile_form.is_valid():
				userprofile = UserProfile.objects.create(email = profile_form.cleaned_data['email'])
				bowlerprofile = profile_form.save(commit=False)
				
				request.user.userprofile = userprofile
				request.user.bowlerprofile = bowlerprofile
				
				request.user.userprofile.save()
				request.user.bowlerprofile.save()

		else:
			new_profile_form = CreateProfileForm()
		return render(request, 'accounts/create_profile.html', {'profile_form' : new_profile_form})

	'''
	'''
	try:
		has_profile = request.user.userprofile
	except ObjectDoesNotExist:
		if request.method == 'POST':
		
			userprofile_form = CreateUserProfileForm(request.POST)
			bowlerprofile_form = CreateBowlerProfileForm(request.POST)
			if userprofile_form.is_valid() and bowlerprofile_form.is_valid():
				up = userprofile_form.save(commit=False)
				bp = bowlerprofile_form.save(commit=False)
			
				request.user.userprofile = up
				request.user.bowlerprofile = bp
			
				request.user.userprofile.save()
				request.user.bowlerprofile.save()
			
				return redirect('view-profile-by-username', identifier=request.user.username)
		else:
			userprofile_form = CreateUserProfileForm()
			bowlerprofile_form = CreateBowlerProfileForm()
		return render(request, 'accounts/create_profile.html', {
		'userprofile': userprofile_form, 'bowlerprofile': bowlerprofile_form})
	else:
		return redirect('view-profile-home')
'''

@login_required			
def view_profile(request, username= ""):
	if username:
		try:
			bp = BowlerProfile.objects.get(user__username=username)
		except ObjectDoesNotExist:
			return redirect('create-profile')
		else:
			bp_form = CreateProfileForm(instance=bp)
		return render(request, 'accounts/view_profile.html', {'bp_form' : bp_form})
	'''
	try:
		if identifier:
			user = User.objects.get(username = identifier)
			userprofile = UserProfile.objects.get(user__username=identifier)
			bowlerprofile = BowlerProfile.objects.get(user__username=identifier)
		else:
			userprofile = UserProfile.objects.get(pk=request.user.userprofile.id)
			bowlerprofile = BowlerProfile.objects.get(pk=request.user.bowlerprofile.id)
	except ObjectDoesNotExist:
		return redirect('create-profile')
	else:
		#up_form = CreateUserProfileForm(instance=userprofile)
		bp_form = CreateProfileForm(instance=bowlerprofile)
	return render(
		request, 'accounts/view_profile.html', {
		'up_form': up_form,
		'bp_form': bp_form,
	})	
'''