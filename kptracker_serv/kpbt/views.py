from django.shortcuts import render
from kpbt.models import *

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.template import loader

from django.contrib.auth.models import Group
from rest_framework import viewsets
from .serializers import cUserSerializer, GroupSerializer

from .forms import cUserCreationForm

from django.views import generic

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

"""
@login_required
def update_profile(request):
	if request.method == 'POST':
		user_form = cUserCreationForm(request.POST, instance=request.user)
		profile_form = Bowler(request.POST, instance=request.user.bowler)
"""
	
class BowlerList(generic.ListView):
		model = Bowler
	
class cUserViewSet(viewsets.ModelViewSet):
	queryset = cUser.objects.all().order_by('-username')
	serializer_class = cUserSerializer

class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer