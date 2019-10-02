from django.urls import path
from kpbt.centers import views

urlpatterns =[
	path('create/', views.create_bowling_center, name='create-bowling-center')
]
	