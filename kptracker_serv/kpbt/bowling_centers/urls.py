from django.urls import path
from . import views

urlpatterns =[
	path('create/', views.create_bowling_center, name='create-bowling-center')
]
	