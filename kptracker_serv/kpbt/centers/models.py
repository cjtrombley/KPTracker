from django.db import models
from django.contrib.auth.models import User

class BowlingCenter(models.Model):
	center_name = models.CharField(max_length = 64)
	num_lanes = models.IntegerField(default=0)
	
	manager= models.ForeignKey(User, on_delete=models.CASCADE, null=True,
		related_name= 'centers_managed', verbose_name=('managed by'))
	
	def set_manager(self, user):
		self.manager = user