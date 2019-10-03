from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from kpbt.centers.forms import BowlingCenterForm
from kpbt.leagues.forms import LeagueCreationForm
from kpbt.centers.models import BowlingCenter
from kpbt.accounts.models import UserProfile
from django.forms import ModelForm
from django.forms.models import model_to_dict

@permission_required('kpbt.add_bowlingcenter')
def create_bowling_center(request):
	if request.method == 'POST':
		form = BowlingCenterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('index')
	else:
		form = BowlingCenterForm()
	return render(request, 'centers/create_center.html', {'form': form})
	
@permission_required('kpbt.view_bowlingcenter')
def view_center_home(request):
	center = request.user.centers_managed.first()
	if center:
		form = BowlingCenterForm(instance=center)
		return render(request, 'centers/view_center.html', {'form' : form})
	else:
		return render(request, 'centers/create_center.html', {})
		
	