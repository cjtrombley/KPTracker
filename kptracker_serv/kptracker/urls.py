"""kptracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework import routers
from rest_framework.authtoken import views as authviews
from kpbt import views

router = routers.DefaultRouter()
router.register(r'users', views.cUserViewSet)
router.register(r'groups', views.GroupViewSet)




urlpatterns = [
    path('admin/', admin.site.urls),
	
	#Use include() to add paths from the kpbt application
	path('kpbt/', include('kpbt.urls')),
	
	#Redirect base URL to our appen
	path('', RedirectView.as_view(url='/kpbt/', permanent=True)),	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 #Use static() to add url mappings to serve static files during development
 
#Add Django site authentication URLs
urlpatterns += [
	path('accounts/', include('django.contrib.auth.urls')),
] 



urlpatterns += [
	path('', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api-token-auth/', authviews.obtain_auth_token)
]