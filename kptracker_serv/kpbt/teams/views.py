from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.forms.formsets import formset_factory
from kpbt.teams.forms import CreateTeamForm, TeamRosterForm #RosterFormSet
from kpbt.teams.models import Team, TeamRoster
from kpbt.leagues.models import League
from kpbt.centers.models import BowlingCenter
from kpbt.accounts.models import BowlerProfile
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
				bowlers = team.roster.filter(teamroster__is_active=True)
				#bp = request.user.bowlerprofile
				#bowlers = bp.teamroster_set.all()
				#print(bowlers)
				#for roster in bowlers:
				#	print(roster)
				return render(request, 'teams/view_team.html', {'team' : team, 'bowlers' : bowlers })
			else:
				teams = Team.objects.filter(league__bowling_center__name=center_name, league__name=league_name)
				return render(request, 'teams/team_home.html', {'teams' : teams })
	else:
		teams = Team.objects.all()
		return render(request, 'teams/team_home.html', {'teams' : teams})
	
#previously create_roster		
def update_roster(request, center_name= "", league_name="", team_name=""):
	team = get_object_or_404(Team, league__bowling_center__name = center_name, league__name = league_name, name=team_name)
	
	RosterFormSet = formset_factory(TeamRosterForm, extra=0)	
	
	team_rosters = TeamRoster.objects.filter(team_id=team.id)
	roster_data = [{'bowler' : roster.bowler} for roster in team_rosters]
	
	if request.method == 'POST':
		formset = RosterFormSet(request.POST)
		if formset.is_valid():
			for roster in formset:
				if roster.has_changed():
					print(roster.changed_data)
					new_roster = roster.save(commit=False)
					new_roster.team = team
					new_roster.save()
		return redirect('update-roster', center_name, league_name, team_name)
	
	else:
		
		rosterset = RosterFormSet(initial=roster_data)
		#roster_size = range(1, team.league.leaguerules.max_roster_size)
	
	return render(request, 'teams/update_roster.html', {'team': team, 'rosterset' : rosterset})
	
"""
def update_roster(request, center_name="", league_name="", team_name=""):
	if request.method == 'POST':	
		if center_name, league_name, team_name:
			team = get_object_or_404(Team, league__bowling_center__name=center_name, league__name=league_name, name=team_name)
			new_roster = TeamRoster(request.user, team)
"""			