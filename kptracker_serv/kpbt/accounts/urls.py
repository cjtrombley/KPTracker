from django.urls import path
from kpbt.accounts import views

urlpatterns = [
	path('signup/', views.signup, name="signup"),
	path('create_profile/', views.create_profile, name='create_profile'),
	path('view_profile/', views.view_profile, name='view_profile'),
]