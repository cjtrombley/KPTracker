from django.urls import path
from kpbt.accounts import views

urlpatterns = [
	path('register', views.register, name="register"),
	path('create-profile', views.create_or_update_profile, name='create-profile'),
	path('update-profile/<str:username>', views.create_or_update_profile, name='update-profile-by-username'),
	path('profile/', views.view_profile, name='view-profile-home'),
	path('profile/<str:username>', views.view_profile, name='view-profile-by-username'),
]