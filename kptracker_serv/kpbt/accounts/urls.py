from django.urls import path
from kpbt.accounts import views

urlpatterns = [
	path('register/', views.register, name="register"),
	path('create-profile/', views.create_profile, name='create_profile'),
	path('view-profile/', views.view_profile, name='view-profile-home'),
	path('view-profile/<str:identifier>', views.view_profile, name='view-profile-by-username'),
]