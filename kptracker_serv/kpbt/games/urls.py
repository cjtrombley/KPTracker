from django.urls import path
from kpbt.games import views


urlpatterns = [
	path('', views.view_scores, name='scores-home'),
	path('import', views.import_scores, name='import-scores-select'),
	
	#path('create-game', views.create_game, name='create-game'),
	#path('<str:username>', views.view_games_by_bowler, name='view-games-by-bowler'),
]

