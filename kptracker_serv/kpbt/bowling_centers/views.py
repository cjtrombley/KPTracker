from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def create_bowling_center(request):
	return render(request, 'bowling_centers/create.html', context={})