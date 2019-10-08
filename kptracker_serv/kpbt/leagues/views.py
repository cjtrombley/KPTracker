from django.shortcuts import redirect, render
from django.contrib.auth.decorators import permission_required
from kpbt.leagues.forms import LeagueCreationForm
from kpbt.leagues.models import League

def create_league(request):
	if request.method == 'POST':
		league_form = LeagueCreationForm(request.POST)
		if league_form.is_valid():
			league_form.save()
			return redirect('index')
	else:
		league_form = LeagueCreationForm()
	return render(request, 'leagues/create_league.html', {'form' : league_form })

def view_league(request, identifier=""):
	try:
		league = League.objects.get(name=identifier)
	except:
		return redirect('create-league')
	else:
		teams = league.teams.all()
		
	return render(request, 'leagues/view_league.html', {'league' : league, 'teams' : teams})
	