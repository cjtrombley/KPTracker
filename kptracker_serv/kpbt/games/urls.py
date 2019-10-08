from django.urls import path
from kpbt.games import views

urlpatterns = [
	path('create_game', views.create_game, name='create-game'),
	path('view_games/<str:username>', views.view_games_by_bowler, name='view-games-by-bowler'),
]