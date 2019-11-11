from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from kpbt.leagues.forms import LeagueCreationForm, CreateScheduleForm, UpdateLeagueSecretaryForm
from kpbt.accounts.models import BowlerProfile
from kpbt.leagues.models import League, LeagueBowler, WeeklyPairings
from kpbt.centers.models import BowlingCenter
from kpbt.teams.models import Team, TeamRoster
from kpbt.games.models import Series
from kptracker.settings import ROSTEREXPORT_FOLDER as ROSTERS_DIR
from kpbt.games.forms import CreateSeriesForm, ImportScoresForm
from kptracker.settings import SCOREFILES_FOLDER as SCOREDIR
import math

def create_league(request, center_name=""):
	if request.method == 'POST':
		center = get_object_or_404(BowlingCenter, name=center_name)
		
		schedule_form = CreateScheduleForm(request.POST)
		league_form = LeagueCreationForm(request.POST)
		if schedule_form.is_valid() and league_form.is_valid():
			new_league = League.objects.create(
				name=league_form.cleaned_data['league_name'], bowling_center=center,)
			new_league.save()
			
			
			#create and save league schedule
			schedule = schedule_form.save(commit=False)
			schedule.league = new_league
			schedule.calc_num_weeks()
			
		
			
			#create and save league rules
			leaguerules = league_form.save(commit=False)
			leaguerules.league = new_league
		
			#create base empty teams with empty rosters for league
			roster_size = leaguerules.playing_strength
			for i in range(1,league_form.cleaned_data['num_teams'] +1 ):
				teami = Team.create_team(new_league, i)
				teami.save()
			
				for _ in range(roster_size):
					empty_bowler = get_object_or_404(BowlerProfile, id=0)
					#empty_bowler.save()
					team_roster_record = TeamRoster.create_roster_record(teami, empty_bowler)
					#empty_bowler.save()
					team_roster_record.save()
				
					league_bowler = LeagueBowler.objects.create(bowler=empty_bowler, league=new_league)
					league_bowler.save()
			
			
			
			#generate weekly lane pairings
			new_league.create_pairings()
			
			
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
			#pairings = list(league.schedule.pairings())
			weekly_pairings = WeeklyPairings.objects.filter(league=league, week_number = league.current_week)
			teams = league.teams.all().order_by('-team_points_won')
			league_bowlers = LeagueBowler.objects.filter(league__name=league_name).exclude(bowler__id=0)
			last_week_scores = []
			'''
			if league.schedule.current_week > 1:
				
				for pairing in weekly_pairings:
					teams = pairing.strip().split('-')
					for team in teams:
				
				
						scores = Series.objects.filter(league__name=league_name, team__number = team, week_number=league.schedule.current_week -1)
						if scores:
							last_week_scores.append(scores)
			'''
			last_week_scores=[]
			return render(request, 'leagues/view_league.html', 
				{'league' : league, 'rules' : rulesform, 'schedule': scheduleform, 'teams' : teams, 'weekly_pairings' : weekly_pairings, 'bowlers' : league_bowlers, 'last_week' : last_week_scores})
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
			
			weekly_schedule = []
			
			
			schedule = WeeklyPairings.objects.filter(league=league).order_by('week_number')
			#print(weekly_schedule)
			
			for i in range(1, league.schedule.num_weeks):
				week_pairs = WeeklyPairings.objects.filter(league=league, week_number=i)
				
				if week_pairs:
					week_list = []
					for pair in week_pairs:
						teams = str(pair)
						week_list.append(teams)
					print(week_list)
					weekly_schedule.append(week_list)
			
			
			return render(request, 'leagues/view_schedule.html', {'schedule' : weekly_schedule })
			


def view_weekly_tasks(request, center_name="", league_name=""):
	league = get_object_or_404(League, bowling_center__name=center_name, name=league_name)
	
	return render(request, 'leagues/weekly/weekly_tasks.html', {'league' : league})
	

			
def export_rosters(request, center_name="", league_name=""):
	league = get_object_or_404(League, bowling_center__name=center_name, name=league_name)
	week_number = league.schedule.current_week
	
	
	export_filename = str(league.id) + '_' + str(week_number) +'.txt'
	rosterFile = open(ROSTERS_DIR + export_filename, 'w')
	
	weekly_pairs_list = league.schedule.pairings(week_number)[0]
	team_numbers = []
	for pair in weekly_pairs_list:
		pairs = pair.strip().split('-')
		
		team_numbers.append(pairs[0])
		team_numbers.append(pairs[1])
	
	print(team_numbers)
	
	for i in team_numbers:
		team = get_object_or_404(Team, league__bowling_center__name=center_name, league__name=league_name, number=i)
		rosters = TeamRoster.objects.filter(team=team, is_active=True).order_by('lineup_position')
		
		rosterFile.write(str(team.number) + '\n')
		for roster in rosters:
			league_record = get_object_or_404(LeagueBowler, league=league, bowler=roster.bowler)
			bowler_name = roster.bowler.get_name()
			
			line = str(roster.bowler.id) + ',' + bowler_name + ',' + str(league_record.league_average)
			
			print(line)
			rosterFile.write(line + '\n')
	rosterFile.close()	
	return render(request, 'leagues/view_league.html')
		
		
		
def import_scores(request, center_name = "", league_name=""):
	if request.method == 'POST':
		#import_form = ImportScoresForm(request.POST)
		
		#if import_form.is_valid():
			#week_number = import_form.cleaned_data['week_number']
		league = get_object_or_404(League, name=league_name)
		week_number = league.schedule.current_week
			
		if league and week_number:
			filename = str(league.id) + '_' + str(week_number)
			filedir = SCOREDIR + filename + '.txt'
			
			with open(filedir) as scores:
				for i in range(1, 5):  # only importing 4 teams until scores file has been updated to include a leagues worth of scores
					pair_number = int(math.ceil(i / 2))
					team_id = scores.readline().strip()
					team = get_object_or_404(Team, id=team_id, league__name=league_name)
					game_scores = []
					for t in range(league.leaguerules.playing_strength):
						raw_series_data = scores.readline().strip()
						
						series_data = raw_series_data.split(',')
					
						#[0] BowlerProfile.id
						#[1] AppliedAverage
						#[2] AppliedHandicap
						#[3] GameOneScore
						#[4] GameTwoScore
						#[5] GameThreeScore
						
						bp = get_object_or_404(BowlerProfile, id=series_data[0])
						app_avg = series_data[1]
						app_handi = series_data[2]
						game_one = series_data[3]
						game_two = series_data[4]
						game_three = series_data[5]
						
						
						new_series = Series.objects.create(league=league, team=team, bowler=bp, week_number=week_number, pair_number=pair_number, series_date="1900-1-1",
							applied_average = app_avg, applied_handicap = app_handi,
							game_one_score = game_one, game_two_score = game_two, game_three_score = game_three)
							
							
						game_scores = [new_series.game_one_score, new_series.game_two_score, new_series.game_three_score]
						new_series.save()
						
						#Update team pinfall statistics
						team.update_pinfall(app_handi, game_scores)
						
						#Many-to-Many fields that require updating when scores are imported
						#Update league_bowler record
						league_bowler_record = get_object_or_404(LeagueBowler, league=league, bowler=bp)
						league_bowler_record.update(app_avg, app_handi, game_scores)
						league_bowler_record.save()
						
						#Update team_roster record
						team_roster_record, created = TeamRoster.objects.get_or_create(bowler=bp, team=team)
						team_roster_record.update_games(game_scores)
						team_roster_record.save()
						
			league.score_week(week_number)				
		return redirect('view_league', center_name, league_name )
								
							
	else:
		league = get_object_or_404(League, name=league_name)
		import_form = ImportScoresForm()
		return render(request, 'games/import_scores.html', {'league' : league, 'import_form' : import_form })



def manage_league(request, center_name="", league_name=""):
	league = get_object_or_404(League, bowling_center__name=center_name, name=league_name)
	
	return render(request, 'leagues/manage/manage_league.html', {'league' : league })
		
def manage_league_secretary(request, center_name="", league_name=""):
	league = get_object_or_404(League, bowling_center__name = center_name, name=league_name)
	
	if request.method == 'POST':
		
		form = UpdateLeagueSecretaryForm(request.POST)
		if form.is_valid():
			new_secretary = form.cleaned_data['secretary']
			
			old_secretary = league.secretary
			
			league.set_secretary(new_secretary)
			new_secretary.userprofile.set_league_secretary(True)
			new_secretary.userprofile.save()
			
			
			if old_secretary:
				
				other_leagues = League.objects.filter(secretary__id=old_secretary.id)
				if not other_leagues:
					old_secretary.userprofile.set_league_secretary(False)
					old_secretary.userprofile.save()
			
			
		return redirect('manage-league', league.bowling_center.name, league.name)
	else:
		form = UpdateLeagueSecretaryForm()
		return render(request, 'leagues/manage/update_league_secretary.html', {'form': form })