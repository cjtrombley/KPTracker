from django.urls import path
from kpbt.teams import views

urlpatterns = [
	path('create_team', views.create_team, name='create-team'),
]