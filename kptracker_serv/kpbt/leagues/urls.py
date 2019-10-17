from django.urls import path, include
from kpbt.leagues import views
from kpbt.teams import views as team_views

team_patterns = [
	path('teams', team_views.view_team, name='teams-home'),
	path('teams/', include('kpbt.teams.urls')),
	path('<str:team_name>', team_views.view_team, name='view-center-league-team-by-name'),
	path('<str:team_name>/', include('kpbt.teams.urls')),
]



urlpatterns = [
	path('', views.view_league, name='league-home'),
	path('create-league', views.create_league, name='create-league'),
	path('view-league/', views.view_league, name='view-league-home'),
	path('view-schedule', views.view_schedule, name='view-center-league-schedule'),
	#path('view-league/<str:league_name>', views.view_league, name='view-league-by-name'),
	#path('<str:league_name>', views.view_league, name='view-league-by-name'),
	path('', include(team_patterns)),
]

