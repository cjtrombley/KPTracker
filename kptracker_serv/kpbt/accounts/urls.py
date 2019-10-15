from django.urls import path, include, re_path

from kpbt.accounts import views

urlpatterns = [
	path('register/', views.register, name="register"),
	path('create_profile/', views.create_profile, name='create_profile'),
	path('view_profile/', views.view_profile, name='view-profile-home'),
	path('view_profile/<str:identifier>', views.view_profile, name='view-profile-by-username'),
	re_path(r'verify/(.*)', views.verify, name='verify'),
]