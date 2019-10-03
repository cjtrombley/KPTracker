from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from kpbt.centers.forms import BowlingCenterForm
from kpbt.leagues.forms import LeagueCreationForm
from kpbt.centers.models import BowlingCenter

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
	
	
	return render(request, 'centers/view_center.html', {})
	