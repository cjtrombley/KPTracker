from django.shortcuts import render
from kpbt.models import cUser

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.template import loader

from .forms import cUserCreationForm

# Create your views here.

class SignUp(CreateView):
	form_class = cUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'registration/register.html'
	
def login(request):
	context = { }
	return render(request, 'registration/login.html', context)
	

def index(request):
	"""View function for home page of site."""
	
	context = { }
	
	return render(request, 'index.html', context=context)