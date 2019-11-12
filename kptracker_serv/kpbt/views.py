from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, RedirectView


# Create your views here.

class IndexView(TemplateView):

	template_name = 'index.html'

class AboutView(TemplateView):
	
	template_name = 'about-us.html'