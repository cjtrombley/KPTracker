from django.urls import path, include
from kpbt.centers import views

center_management_patterns = [
	path('', views.center_management_home, name='center-management-home'),
	path('update_manager', views.update_manager, name='update-center-manager'),
]

urlpatterns =[
	path('create', views.create_bowling_center, name='create-bowling-center'),
	path('locations', views.center_locations, name='center_locations'),
	path('', views.view_center_home, name='center-home'),
	path('create', views.create_bowling_center, name='create-bowling-center'),
	path('center_management/', include(center_management_patterns)),

	
	#path('<str:center_name>', views.view_center_home, name='view-center-by-name'),
	path('center-management/', include(center_management_patterns)),
	
]
	