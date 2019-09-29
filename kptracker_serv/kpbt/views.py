from django.shortcuts import render
from kpbt.models import *

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.template import loader

from django.contrib.auth.models import Group
from rest_framework import viewsets
from .serializers import cUserSerializer, GroupSerializer

from .forms import *

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



def update_profile(request):
	if request.method == 'POST':
		user_form = cUserCreationForm(request.POST, instance=request.user)
		profile_form = BowlerCreationForm(request.POST, instance=request.user.bowler)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, _('Profile successfully updated.'))
			return redirect('settings:profile')
		else:
			messages.error(request, _('Error.'))
	else:
		user_form = cUserCreationForm(instance=request.user)
		profile_form = BowlerCreationForm()
	return render(request, 'kpbt/bowler_profile.html', {
		'user_form': cUserCreationForm,
		'profile_form' : profile_form
	})

	
class BowlerList(generic.ListView):
		model = Bowler
	
class cUserViewSet(viewsets.ModelViewSet):
	queryset = cUser.objects.all().order_by('-username')
	serializer_class = cUserSerializer

class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer