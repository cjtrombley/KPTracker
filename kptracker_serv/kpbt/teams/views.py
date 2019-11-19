from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.forms import modelformset_factory
from kpbt.teams.forms import CreateTeamForm, TeamRosterForm, ExistingBowlerForm #RosterFormSet
from kpbt.teams.models import Team, TeamRoster
from kpbt.leagues.models import League, LeagueBowler
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
	return render(request, 'teams/manage/create_team.html', {'form' : team_form})

def view_team(request, center_name= "", league_name="", team_name=""):
	if center_name:
		center = get_object_or_404(BowlingCenter, name=center_name)
		if league_name:
			league= get_object_or_404(League, name=league_name)
			if team_name:
				team = get_object_or_404(Team, league__bowling_center__name=center_name, league__name=league_name, name=team_name)
				bowlers = team.roster.filter(roster_record__is_active=True)
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
		teams = Team.objects.all().order_by('-league__bowling_center__name', 'league__name', 'number')
		print(teams)
		return render(request, 'teams/team_home.html', {'teams' : teams})
	
#previously create_roster		
def update_roster(request, center_name= "", league_name="", team_name=""):
	league = get_object_or_404(League, bowling_center__name= center_name, name=league_name)
	team = get_object_or_404(Team, league=league, name=team_name)
	existing_RosterFormSet = modelformset_factory(BowlerProfile, extra = 0, fields=('first_name', 'last_name', 'hand', 'designation', 'gender'))
	new_RosterFormSet = modelformset_factory(BowlerProfile, extra=4, fields=('first_name', 'last_name', 'hand', 'designation', 'gender'))
	
	team_rosters = TeamRoster.objects.filter(team_id=team.id, is_active=True)
	bowler_data = []
	for roster in team_rosters:
		id = roster.bowler.id
		bowler_data.append(id)
	bowlers = BowlerProfile.objects.filter(id__in=bowler_data, is_linked=False)
	
	if request.method == 'POST':
		formset = existing_RosterFormSet(request.POST)
		existing = ExistingBowlerForm(request.POST)
		
		if request.POST.get("add_existing", ""):
			lb = get_object_or_404(LeagueBowler, id=request.POST.get("bowler"))
			bp = lb.bowler
			team_roster_record, created = TeamRoster.objects.get_or_create(bowler=bp, team=team)
			team_roster_record.is_active=True
			team_roster_record.save()
			
		elif request.POST.get("remov_existing", ""):
			print(request.POST.get("bowler"))
			lb = get_object_or_404(LeagueBowler, bowler=request.POST.get("bowler"))
			print(lb)
			bp = lb.bowler
			print(bp)
			tr_record = TeamRoster.objects.get(team=team, bowler=bp)
			tr_record.is_active=False
			tr_record.save()
			
		else:
			formset = existing_RosterFormSet(request.POST)
			if formset.is_valid():
			
				formset.save()
				for new in formset.new_objects:
					TeamRoster.objects.create(bowler=new, team=team, is_active=True)
					LeagueBowler.objects.create(league=league, bowler=new)
				#create new team roster record here
				
		
			
		return redirect('update-roster', center_name, league_name, team_name)
	
	else:
		rosterset = existing_RosterFormSet(queryset=bowlers)
		new_formset = new_RosterFormSet(queryset=BowlerProfile.objects.none())
		
		#get league bowlers not already on a team roster in this league
		league_team_rosters = TeamRoster.objects.filter(team__league__name = league_name, is_active=False)
		
		bowler_ids = []
		for roster in league_team_rosters:
			bowler_ids.append(roster.bowler.id)
		inactive_bowlers = LeagueBowler.objects.filter(bowler__id__in=bowler_ids)
		
		eadd_form = ExistingBowlerForm()
		eadd_form.fields['bowler'].queryset = inactive_bowlers
		
		eremov_form = ExistingBowlerForm()
		eremov_form.fields['bowler'].queryset = bowlers
		
		return render(request, 'teams/manage/update_roster.html', {'team': team, 'rosterset' : rosterset, 'new_formset' : new_formset, 'eadd_form' : eadd_form, 'eremov_form' : eremov_form})		
	