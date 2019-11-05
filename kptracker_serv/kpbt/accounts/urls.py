from django.urls import path
from kpbt.accounts import views

urlpatterns = [
	path('register', views.register, name="register"),
	path('create-profile', views.kpbt_user_create_profile, name='create-profile'),
	path('update-profile/<str:username>', views.kpbt_user_update_profile, name='update-profile-by-username'),
	#path('profile/', views.view_profile, name='view-profile-home'),
	path('profile/<str:username>', views.view_kpbt_user_bowler_profile, name='view-profile-by-username'),
]