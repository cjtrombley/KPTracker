from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.forms import modelformset_factory
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
	team = get_object_or_404(Team, league__bowling_center__name = center_name, league__name = league_name, name=team_name)
	existing_RosterFormSet = modelformset_factory(BowlerProfile, extra = 0, fields=('first_name', 'last_name', 'hand', 'designation', 'gender'))
	new_RosterFormSet = modelformset_factory(BowlerProfile, extra=4, fields=('first_name', 'last_name', 'hand', 'designation', 'gender'))
	
	team_rosters = TeamRoster.objects.filter(team_id=team.id)
	bowler_data = []
	for roster in team_rosters:
		id = roster.bowler.id
		bowler_data.append(id)
	bowlers = BowlerProfile.objects.filter(id__in=bowler_data, is_linked=False)
	
	if request.method == 'POST':
		print(request.POST)
		
		
		#formset = new_RosterFormSet(request.POST)
		
		#print(request.POST)
		formset = existing_RosterFormSet(request.POST)
		#print(existing_formset)
		#new_formset = new_RosterFormSet(request.POST)
		#print(new_formset)
		if formset.is_valid():
			print('is_valid')
			formset.save()
			
			for new in formset.new_objects:
				print('new_object')
			
			#Sprint(formset)
			'''for form in formset.forms:
				#first_name = form.cleaned_data.get('first_name')
				#last_name = form.cleaned_data.get('last_name')
				#hand = form.cleaned_data.get('hand')
				#designation = form.cleaned_data.get('designation')
				#gender = form.cleaned_data.get('gender')
				
				form.save(commit=False)
				print('got here')
				print(form.cleaned_data.get('first_name'))
				print(form.cleaned_data.get('last_name'))
				print(form.cleaned_data.get('hand'))
				print(form.cleaned_data.get('designation'))
				print(form.cleaned_data.get('gender'))
				
				profile, created = BowlerProfile.objects.update_or_create(pk = form.cleaned_data.get('id'),
					first_name=form.cleaned_data.get('first_name'), 
					last_name=form.cleaned_data.get('last_name'),
					hand=form.cleaned_data.get('hand'),
					designation=form.cleaned_data.get('designation'),
					gender=form.cleaned_data.get('gender'),)
					
				print(profile)
				print(created)
					
				#profile = BowlerProfile.objects.get(updated)
				#print(profile)
				#if created:
				#	print('new record')
				
				
			 #existing_formset.save()
			 #new_formset.save()
			'''	
		return redirect('update-roster', center_name, league_name, team_name)
	
	else:
		
		rosterset = existing_RosterFormSet(queryset=bowlers)
		new_formset = new_RosterFormSet(queryset=BowlerProfile.objects.none())
		
		return render(request, 'teams/manage/update_roster.html', {'team': team, 'rosterset' : rosterset, 'new_formset' : new_formset})		
	