from django.urls import path, include
from kpbt import views


urlpatterns=[
	
	#Path that maps to site root
	path('', views.IndexView.as_view(), name="index"),
	
	#Paths that map to user account functions
	path('accounts/', include('kpbt.accounts.urls')),
	
	
	#Paths that map to bowling center functions
	path('centers/', include('kpbt.centers.urls')),
	
	#Paths that map to league functions
	path('leagues/', include('kpbt.leagues.urls')),
	
	#Paths that map to team functions
	path('teams/', include('kpbt.teams.urls')),
	
	#Paths that map to game functions
	path('games/', include('kpbt.games.urls')),
]