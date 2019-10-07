from django.urls import path
from kpbt.teams import views

urlpatterns = [
	path('create_team', views.create_team, name='create-team'),
	path('view_team/<str:team_name>', views.view_team, name='view-team'),
]