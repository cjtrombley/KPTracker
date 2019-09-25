from django.contrib.auth.models import Group
from .models import cUser
from rest_framework import serializers

#Define serializers here

class cUserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = cUser
		fields = ['url', 'username', 'first_name', 'last_name', 'email', 'groups']
		
class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = cUser
		fields = ['url', 'first_name']
		
