from django.shortcuts import render
from kpbt.models import cUser


# Create your views here.

def index(request):
	"""View function for home page of site."""
	
	context = { }
	
	return render(request, 'index.html', context=context)