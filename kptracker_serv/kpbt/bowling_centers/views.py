from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from kpbt import models

def create_bowling_center(request):
	return render(request, 'bowling_centers/create.html', context={})