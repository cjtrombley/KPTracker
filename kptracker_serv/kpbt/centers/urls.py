from django.urls import path
from kpbt.centers import views

urlpatterns =[
	path('create', views.create_bowling_center, name='create-bowling-center'),
    path('locations', views.center_locations, name='center_locations'),
	path('', views.view_center_home, name='center-home'),
	path('<str:center_name>', views.view_center_home, name='view-center-by-name'),
]
	