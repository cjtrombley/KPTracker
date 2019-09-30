from django.urls import path
from .views import SignUp as SignUpView
from django.contrib.auth import views as auth_views
from . import views 
from .views import *

urlpatterns = [ 

	#Paths that map to login and register functions
	path('', views.index, name="index"),
	path('login/', auth_views.LoginView.as_view(template_name='kpbt/registration/login.html'), name='login'),
	path('register/', SignUpView.as_view(), name='register'),
	path('bowlers/', BowlerList.as_view(), name='bowlers'),
	path('bowlers/profile', views.view_user_profile, name='user_profile'),
]