from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views 
from .views import *
from kpbt.leagues import views as league_views

urlpatterns = [ 
	
	#Path that maps to site root
	path('', views.IndexView.as_view(), name="index"),
	
	#Paths that map to user account functions
	path('signup/', views.signup, name="signup"),
	path('create_profile/', views.create_profile, name='create_profile'),
	path('view_profile/', views.view_profile, name='view_profile'),
	
	#Paths that map to bowling center functions
	path('bowling_centers/', include('kpbt.bowling_centers.urls'))
]