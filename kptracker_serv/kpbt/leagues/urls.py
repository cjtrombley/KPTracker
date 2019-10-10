from django.urls import path
from kpbt.leagues import views

urlpatterns = [
	path('', views.view_league, name='league-home'),
	path('create-league', views.create_league, name='create-league'),
	path('view-league/', views.view_league, name='view-league-home'),
	path('view-league/<str:league_name>', views.view_league, name='view-league-by-name'),
	path('<str:league_name>', views.view_league, name='view-league-by-name'),
	path('<str:league_name>/view-schedule/', views.view_schedule, name='view-center-league-schedule'),
]