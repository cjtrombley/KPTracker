from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from kpbt.centers.forms import BowlingCenterForm
from kpbt.leagues.forms import LeagueCreationForm
from kpbt.centers.models import BowlingCenter
from kpbt.accounts.models import UserProfile
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

@permission_required('kpbt.add_bowlingcenter')
def create_bowling_center(request):
	if request.method == 'POST':
		form = BowlingCenterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('center-home')
	else:
		form = BowlingCenterForm()
	return render(request, 'centers/create_center.html', {'form': form})
	
@permission_required('kpbt.view_bowlingcenter')
def view_center_home(request, identifier=""):
	try:
		center = request.user.center_managed
		manager = request.user
		return render(request, 'centers/view_center.html', {'center' : center, 'manager' : manager})
	except ObjectDoesNotExist:
		return render(request, 'centers/create_center.html', {'form' : BowlingCenterForm()})
		
	