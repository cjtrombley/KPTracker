from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from kpbt.leagues.forms import LeagueCreationForm, CreateScheduleForm
from kpbt.accounts.models import BowlerProfile
from kpbt.leagues.models import League, LeagueBowler
from kpbt.centers.models import BowlingCenter
from kpbt.teams.models import Team, TeamRoster
from kpbt.games.models import Series

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
	
			
				#create base empty teams with empty rosters for league
				roster_size = leaguerules.playing_strength
				for i in range(1,league_form.cleaned_data['num_teams'] +1 ):
					teami = Team.create_team(league, i)
					teami.save()
				
					for _ in range(roster_size):
						empty_bowler = get_object_or_404(BowlerProfile, id=0)
						#empty_bowler.save()
						team_roster_record = TeamRoster.create_roster_record(teami, empty_bowler)
						#empty_bowler.save()
						team_roster_record.save()
					
						league_bowler = LeagueBowler.objects.create(bowler=empty_bowler, league=league)
						league_bowler.save()
			
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
			
			
			#standings = Series.objects.filter(league__name=league_name).order_by('-team__team_points_won')
			rulesform = LeagueCreationForm(instance = league.leaguerules)
			scheduleform = CreateScheduleForm(instance = league.schedule)
			pairings = list(league.schedule.pairings())
			weekly_pairings = pairings[league.current_week()]
			teams = league.teams.all().order_by('-team_points_won')
			league_bowlers = LeagueBowler.objects.filter(league__name=league_name).exclude(bowler__id=0)
			last_week_scores = []
			
			if league.schedule.current_week > 1:
				
				for pairing in weekly_pairings:
					teams = pairing.trim().split('-')
					for team in teams:
				
				
						scores = Series.objects.filter(league__name=league_name, team__number = team, week=current_week)
						last_week_scores.append(scores)
			
			return render(request, 'leagues/view_league.html', 
				{'league' : league, 'rules' : rulesform, 'schedule': scheduleform, 'teams' : teams, 'pairings' : pairings,
				'weekly_pairing' : weekly_pairings, 'bowlers' : league_bowlers, 'last_week' : last_week_scores})
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
			schedule = schedule[1:] #shift schedule indices left one space to maintain 1:1 alignment with current week
			
			return render(request, 'leagues/view_schedule.html', {'schedule' : schedule })