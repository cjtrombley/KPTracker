from django.urls import path
from kpbt.leagues import views

urlpatterns = [
	path('', views.view_league, name='league-home'),
	path('create_league', views.create_league, name='create-league'),
	path('view_league/', views.view_league, name='view-league-home'),
	path('view_league/<str:identifier>', views.view_league, name='view-league-by-name'),
]