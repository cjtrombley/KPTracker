from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from kpbt.teams.forms import CreateTeamForm, TeamRosterForm
from kpbt.teams.models import Team


def create_team(request):
	if request.method == 'POST':
		team_form = CreateTeamForm(request.POST)
		if team_form.is_valid():
			team_form.save()
			return redirect('index')
		
		
	else:
		team_form = CreateTeamForm()
	return render(request, 'teams/create_team.html', {'form' : team_form})


def view_team(request, league_name="", team_name=""):
	try:
		team = Team.objects.get(name=team_name)
	except:
		return redirect('index')
	else:
		bowlers = team.roster.all()
		return render(request, 'teams/view_team.html', {'team' : team, 'bowlers' : bowlers}) 
		
def create_roster(request, league_name="", team_name=""):
	if request.method == 'POST':
		roster = TeamRosterForm(request.POST)
		if roster.is_valid():
			roster.save()
			return redirect('index')
	
	
	else:
		roster = TeamRosterForm()
	
	return render(request, 'teams/create_roster.html', {'roster' : roster })
		