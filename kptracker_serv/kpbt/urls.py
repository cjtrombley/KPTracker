from django.urls import path, include
from kpbt import views


urlpatterns=[
	
	#Path that maps to site root
	path('', views.IndexView.as_view(), name="index"),
	
	#Paths that map to user account functions
	path('accounts/', include('kpbt.accounts.urls')),
	
	
	#Paths that map to bowling center functions
	path('bowling_centers/', include('kpbt.centers.urls')),
]