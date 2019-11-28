from django.urls import path, include
from kpbt.teams import views

#team_management_patterns = [
	#path('', views.manage_team, name='manage-team'),


urlpatterns = [
	path('', views.view_team),
	path('home', views.view_team, name='team-home'),
	#path('create-team', views.create_team, name='create-team'),
	path('view-team/<str:team_name>', views.view_team, name='view-team'),
	#path('create-roster', views.create_roster, name='create-roster'),
	#path('update-roster', views.update_roster, name='update-roster'),
	path('manage/', views.manage_team, name='manage-team'),
]