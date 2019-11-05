from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from kpbt.teams.forms import CreateTeamForm, TeamRosterForm, RosterFormSet
from kpbt.teams.models import Team
from kpbt.leagues.models import League
from kpbt.centers.models import BowlingCenter
from num2words import num2words

def create_team(request, center_name="", league_name="", team_number=""):
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
			if team_name:
				team = get_object_or_404(Team, league__bowling_center__name=center_name, league__name=league_name, name=team_name)
				bowlers = team.roster.all()
				return render(request, 'teams/view_team.html', {'team' : team, 'bowlers' : bowlers })
			else:
				teams = Team.objects.filter(league__bowling_center__name=center_name, league__name=league_name)
				return render(request, 'teams/team_home.html', {'teams' : teams })
	else:
		teams = Team.objects.all()
		return render(request, 'teams/team_home.html', {'teams' : teams})
	
#previously create_roster		
def update_roster(request, center_name= "", league_name="", team_name=""):
	if request.method == 'POST':
		if team_name:
			team = get_object_or_404(Team, league__name=league_name, name=team_name)
			formset = RosterFormSet(request.POST, extra = team.league.leaguerules.max_roster_size)
			if formset.is_valid():
				for roster in formset:
					new_roster = roster.save(commit=False)
					new_roster.team = team
					new_roster.save()
			return redirect('team-home')
	
	
	else:
		
		team = get_object_or_404(Team, league__name=league_name, name=team_name)
		rosterset = RosterFormSet(request.GET or None)
		roster_size = range(1, team.league.leaguerules.max_roster_size)
	
	return render(request, 'teams/create_roster.html', {'team': team, 'rosterset' : rosterset, 'size' : roster_size })
	
"""
def update_roster(request, center_name="", league_name="", team_name=""):
	if request.method == 'POST':	
		if center_name, league_name, team_name:
			team = get_object_or_404(Team, league__bowling_center__name=center_name, league__name=league_name, name=team_name)
			new_roster = TeamRoster(request.user, team)
"""			