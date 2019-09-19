from django.urls import path
from .views import SignUp as SignUpView
from . import views

urlpatterns = [ 

	path('', views.index, name="index"),
	path('register/', SignUpView.as_view(), name='register'),
	path('login', views.login, name='login')
]