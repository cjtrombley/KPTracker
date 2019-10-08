from django.urls import path
from kpbt.teams import views

urlpatterns = [
	path('create-team', views.create_team, name='create-team'),
	path('view-team/<str:team_name>', views.view_team, name='view-team'),
	path('create-roster', views.create_roster, name='create-roster'),
]