from django.urls import path
from .views import SignUp as SignUpView
from . import views 
from .views import *

urlpatterns = [ 

	#Paths that map to login and register functions
	path('', views.index, name="index"),
	path('login/', views.login, name='login'),
	path('register/', SignUpView.as_view(), name='register'),
	path('bowlers/', BowlerList.as_view(), name='bowlers'),
	
]