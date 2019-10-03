from django.db import models
from django.contrib.auth.models import User

class BowlingCenter(models.Model):
	center_name = models.CharField(max_length = 64)
	num_lanes = models.IntegerField(default=0)
	
	manager= models.OneToOneField(User, on_delete=models.SET_NULL, null=True,
		related_name='center_managed', verbose_name=('managed by'))
	
	def set_manager(self, user):
		self.manager = user