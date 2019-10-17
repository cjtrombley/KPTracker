from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from kpbt.leagues.forms import LeagueCreationForm, CreateScheduleForm
from kpbt.leagues.models import League
from kpbt.centers.models import BowlingCenter
from kpbt.teams.models import Team

def create_league(request, center_name=""):
	if request.method == 'POST':
		center = get_object_or_404(BowlingCenter, name=center_name)
		if center:
			schedule_form = CreateScheduleForm(request.POST)
			league_form = LeagueCreationForm(request.POST)
			if schedule_form.is_valid() and league_form.is_valid():
				league = League.objects.create(
					name=league_form.cleaned_data['league_name'], bowling_center=center,)
				league.save()
				
				#create and save league schedule
				schedule = schedule_form.save(commit=False)
				schedule.league = league
				schedule.calc_num_weeks()
				
				
				#create and save league rules
				leaguerules = league_form.save(commit=False)
				leaguerules.league = league
	
			
				#create base empty teams for league
				for i in range(1,league_form.cleaned_data['num_teams'] +1 ):
					teami = Team.create(league, i)
					teami.save()
			
				#save models
				schedule.save()
				leaguerules.save()
				return redirect('center-home', center_name=center_name)
	else:
		schedule_form = CreateScheduleForm()
		league_form = LeagueCreationForm()
	return render(request, 'leagues/create_league.html', {'schedule_form' : schedule_form, 'league_form' : league_form })

def view_league(request, center_name = "", league_name=""):
	if center_name:
		if league_name:
			league = get_object_or_404(League, bowling_center__name=center_name, name=league_name)
			rulesform = LeagueCreationForm(instance = league.leaguerules)
			scheduleform = CreateScheduleForm(instance = league.schedule)
			teams = league.teams.all()
			return render(request, 'leagues/view_league.html', {'league' : league, 'rules' : rulesform, 'schedule': scheduleform, 'teams' : teams })
		else:
			center = get_object_or_404(BowlingCenter, name=center_name)
			leagues = center.leagues.all()
			return render(request, 'centers/view_center.html', {'leagues' : leagues, 'center' : center })
	else:
		leagues = League.objects.all()
			
		return render(request, 'leagues/league_home.html', {'leagues' : leagues})


def view_schedule(request, center_name="", league_name=""):
	if center_name:
		if league_name:
			league = get_object_or_404(League, bowling_center__name=center_name, name=league_name)
			schedule = list(league.schedule.pairings())
			print(schedule)
			print(schedule[12][0])
			return render(request, 'leagues/view_schedule.html', {'schedule' : schedule })