from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from kpbt.teams.forms import CreateTeamForm, TeamRosterForm
from kpbt.teams.models import Team
from kpbt.leagues.models import League
from kpbt.centers.models import BowlingCenter

def create_team(request):
	if request.method == 'POST':
		team_form = CreateTeamForm(request.POST)
		if team_form.is_valid():
			team_form.save()
			return redirect('index')
		
		
	else:
		team_form = CreateTeamForm()
	return render(request, 'teams/create_team.html', {'form' : team_form})


def view_team(request, center_name= "", league_name="", team_name=""):
	if center_name:
		center = get_object_or_404(BowlingCenter, name=center_name)
		if league_name:
			league= get_object_or_404(League, name=league_name)
			if league:
				if team_name:
					team = get_object_or_404(Team, league__bowling_center__name=center_name, league__name=league_name, name=team_name)
					bowlers = team.roster.all()
					return render(request, 'teams/view_team.html', {'team' : team, 'bowlers' : bowlers })
				else:
					teams = Teams.objects.filter(league__bowling_center_name=center_name, league__name=league_name)
					return render(request, 'leagues/league_home.html', {'teams' : teams, 'center' : center, 'leagues' : leagues})
	else:
		teams = Team.objects.all()
		return render(request, 'teams/team_home.html', {'teams' : teams})
	
	"""
	try:
		team = Team.objects.get(name=team_name)
	except:
		return redirect('index')
	else:
		bowlers = team.roster.all()
		return render(request, 'teams/view_team.html', {'team' : team, 'bowlers' : bowlers}) 
	"""
		
def create_roster(request, league_name="", team_name=""):
	if request.method == 'POST':
		roster = TeamRosterForm(request.POST)
		if roster.is_valid():
			roster.save()
			return redirect('index')
	
	
	else:
		roster = TeamRosterForm()
	
	return render(request, 'teams/create_roster.html', {'roster' : roster })
		