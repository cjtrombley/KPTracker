from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from kpbt.leagues.forms import LeagueCreationForm, CreateScheduleForm
from kpbt.leagues.models import League
from kpbt.centers.models import BowlingCenter

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
				schedule = schedule_form.save(commit=False)
				schedule.league = league
				schedule.calc_num_weeks()
				schedule.save()
				
				leaguerules = league_form.save(commit=False)
				leaguerules.league = league
			
				leaguerules.save()
			
				return redirect('view-center-by-name', center_name=center_name)
	else:
		schedule_form = CreateScheduleForm()
		league_form = LeagueCreationForm()
	return render(request, 'leagues/create_league.html', {'schedule_form' : schedule_form, 'league_form' : league_form })

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


def view_schedule(request, center_name="", league_name=""):
	if center_name:
		if league_name:
			league = get_object_or_404(League, bowling_center__name=center_name, name=league_name)
			schedule = league.schedule.pairings()
			return render(request, 'leagues/view_schedule.html', {'schedule' : schedule })