from django.shortcuts import redirect, render
from kpbt.games.forms import CreateGameForm
from django.contrib.auth.decorators import permission_required
from kpbt.games.models import Game

def create_game(request):
	if request.method == 'POST':
		game_form = CreateGameForm(request.POST)
		if game_form.is_valid():
			game_form.save()
			return redirect('index')
	
	else:
		game_form = CreateGameForm()
	return render(request, 'games/create_game.html', {'game_form' : game_form })
	
def view_games_by_bowler(request, username=""):
	if username:
		games = Game.objects.filter(bowler__username =username)
		print(games)
		return render(request, 'games/view_game.html', {'games' : games })
	else:
		return redirect('index')
		