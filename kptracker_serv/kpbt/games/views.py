from django.shortcuts import redirect, render, get_object_or_404
#from kpbt.games.forms import CreateSeriesForm
from django.contrib.auth.decorators import permission_required
from kpbt.games.models import Series
from kpbt.leagues.models import League, LeagueBowler
from kpbt.teams.models import Team, TeamRoster
from kpbt.accounts.models import BowlerProfile
from kpbt.games.forms import ImportScoresForm, FilterScoresChartForm
from kptracker.settings import SCOREFILES_FOLDER as SCOREDIR
from django.http import JsonResponse, HttpResponse

import json
from datetime import datetime
		
def view_scores(request, center_name="", league_name="", week_number=""):
	league = get_object_or_404(League, bowling_center__name=center_name, name=league_name)
	
	if week_number:
		#scores =[]
		
		#teams = league.teams.all()
		#for team in teams:
		scores = Series.objects.filter(league=league, week_number=int(week_number)).order_by('team')
		return render(request, 'games/view_scores_by_week.html', {'week_number' : week_number, 'scores' : scores})
	else:
		scores = Series.objects.filter(league=league).order_by('-week_number')
		return render(request, 'games/view_scores.html', {'week_number': week_number, 'scores' : scores})
	
def view_all_stats(request, center_name="", league_name=""):
		return redirect('index')
	
'''
def stats_chart_data(request):
	if request.method == 'POST' or request.is_ajax():
		print(request.POST)
		
		linked_profiles = BowlerProfile.objects.filter(user__username=request.user.username)
		filter = request.POST.get('filter')
		
		if filter == "average":
			chart_title = "Weekly/League Average"
			y_axis_title = "Score"
			
			
			scores = Series.objects.filter(bowler__in=linked_profiles)
			
			series_data = []
			averages_data = []
			for score in enumerate(scores, start=1):
				series_data.append({ 'x': 'score.series_date', 'y': 'score.scratch_score' })
				averages_data.append({ 'x': 'score.series_date', 'y': 'score.applied_average'})
			print(series_data)
			print(averages_data)
	
	
	
			return render(request, 'accounts/view_stats.html', {'form' : form, 'chart_title' : chart_title, 'y_axis_title' : y_axis_title, 'series_data' : series_data, 'averages_data': averages_data})
			
		print(filter)
		return HttpResponse(
			json.dumps({}),
			content_type="application/json",
		)
	else:
		form = FilterScoresChartForm()
		
		chart_title = "Weekly/League Average"
		y_axis_title = "Score"
		suffix = "Pins"
			
		linked_profiles = BowlerProfile.objects.filter(user__username=request.user.username)	
		scores = Series.objects.filter(bowler__in=linked_profiles)
		
		series_data = []
		averages_data = []
		for score in enumerate(scores, start=1):
			series_data.append({score[0] : score[1].scratch_score})
			averages_data.append({score[0] : score[1].applied_average})
		print(series_data)
		print(averages_data)
		
		return render(request, 'accounts/view_stats.html', {'form' : form, 'chart_title' : chart_title, 'y_axis_title' : y_axis_title, 'series_data' : series_data, 'averages_data': averages_data, 'suffix' : suffix})
	'''	