from django.urls import path
from kpbt.leagues import views

urlpatterns = [
	path('create_league', views.create_league, name='create-league'),
	path('view_league/<str:identifier>', views.view_league, name='view-league'),
]