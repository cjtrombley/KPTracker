from django.shortcuts import redirect, render, get_object_or_404
from kpbt.games.forms import CreateSeriesForm
from django.contrib.auth.decorators import permission_required
from kpbt.games.models import Series
from kpbt.leagues.models import League, LeagueBowler
from kpbt.teams.models import Team, TeamRoster
from kpbt.accounts.models import BowlerProfile
from kpbt.games.forms import ImportScoresForm
from kptracker.settings import SCOREFILES_FOLDER as SCOREDIR


def import_scores(request, center_name = "", league_name=""):
	if request.method == 'POST':
		import_form = ImportScoresForm(request.POST)
		
		if import_form.is_valid():
			week_number = import_form.cleaned_data['week_number']
			league = get_object_or_404(League, name=league_name)
			
			if league and week_number:
				filename = str(league.id) + '_' + str(week_number)
				filedir = SCOREDIR + filename + '.txt'
				
				with open(filedir) as scores:
					for _ in range(2):
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
							
							
							new_series = Series.objects.create(league=league, team=team, bowler=bp, week_number=week_number, series_date="1900-1-1",
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
			return redirect('index')
								
							
	else:
		league = get_object_or_404(League, name=league_name)
		import_form = ImportScoresForm()
		return render(request, 'games/import_scores.html', {'league' : league, 'import_form' : import_form })
		
"""
def create_series(request):
	if request.method == 'POST':
		series_form = CreateSeriesForm(request.POST)
		if game_form.is_valid():
			game_form.save()
			return redirect('index')
	
	else:
		game_form = CreateGameForm()
	return render(request, 'games/create_game.html', {'game_form' : game_form })
	
def view_games_by_bowler(request, username=""):
	if username:
		games = Game.objects.filter(bowler__username =username)
		print(games)
		return render(request, 'games/view_game.html', {'games' : games })
	else:
		return redirect('index')
"""		