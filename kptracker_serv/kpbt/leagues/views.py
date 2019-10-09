from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from kpbt.leagues.forms import LeagueCreationForm
from kpbt.leagues.models import League
from kpbt.centers.models import BowlingCenter

def create_league(request, center_name=""):
	if request.method == 'POST':
		league_form = LeagueCreationForm(request.POST)
		if league_form.is_valid():
			league_form.save()
			return redirect('index')
	else:
		league_form = LeagueCreationForm()
	return render(request, 'leagues/create_league.html', {'form' : league_form })

def view_league(request, center_name = "", league_name=""):
	if center_name:
		if league_name:
			league = get_object_or_404(League, bowling_center__name=center_name, name=league_name)
			teams = league.teams.all()
			return render(request, 'leagues/view_league.html', {'league' : league, 'teams' : teams })
		else:
			center = get_object_or_404(BowlingCenter, name=center_name)
			leagues = center.leagues.all()
			return render(request, 'leagues/league_home.html', {'leagues' : leagues, 'center' : center })
	else:
		return redirect('index')
	"""
	try:
		league = League.objects.get(name=identifier)
	except:
		return redirect('create-league')
	else:
		teams = league.teams.all()
		
	return render(request, 'leagues/view_league.html', {'league' : league, 'teams' : teams})
	"""