from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from kpbt.centers.forms import BowlingCenterForm

@login_required
def create_bowling_center(request):
	if request.method == 'POST':
		form = BowlingCenterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('index')
	else:
		form = BowlingCenterForm()
	return render(request, 'centers/create_center.html', {'form': form})