from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
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
			manager = form.cleaned_data['manager']
			manager.userprofile.set_center_manager(True)
			manager.userprofile.save()
			form.save()
			return redirect('center-home')
	else:
		form = BowlingCenterForm()
	return render(request, 'centers/create_center.html', {'form': form})


def view_center_home(request, center_name=""):
	if center_name:	
		center = get_object_or_404(BowlingCenter, name=center_name)
		leagues = center.leagues.all()
		return render(request, 'centers/view_center.html', {'center' : center, 'leagues' : leagues})
	else:
		centers = BowlingCenter.objects.all()
		return render(request, 'centers/center_home.html', {'centers' : centers })
		
		#try:
		#	center = BowlingCenter.objects.get(name=identifier)
		#except:
		#	ObjectDoesNotExist
def center_locations(request):
    return render(request, 'centers/center_locations.html')
	
"""	
@permission_required('kpbt.view_bowlingcenter')

def view_center_home(request, identifier=""):
	try:
		center = request.user.center_managed
		manager = request.user
		return render(request, 'centers/view_center.html', {'center' : center, 'manager' : manager})
	except ObjectDoesNotExist:
		return render(request, 'centers/create_center.html', {'form' : BowlingCenterForm()})
"""		
	