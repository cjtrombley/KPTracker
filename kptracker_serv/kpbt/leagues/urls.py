from django.urls import path
from kpbt.leagues import views

urlpatterns = [
	path('', views.view_league, name='league-home'),
	path('create-league', views.create_league, name='create-league'),
	path('view-league/', views.view_league, name='view-league-home'),
	path('view-league/<str:identifier>', views.view_league, name='view-league-by-name'),
]