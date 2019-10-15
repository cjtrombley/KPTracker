from django.db import models
from django.contrib.auth.models import User
import datetime

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='userprofile')
	first_name = models.CharField(max_length=64, blank=True)
	last_name = models.CharField(max_length=64, blank=True)
	email = models.EmailField(
		verbose_name='email address',
		max_length = 254,
		unique = False,
	)
	date_of_birth = models.DateField(default=datetime.date(1900, 1, 1), blank=True)
	
	
	is_bowler = models.BooleanField(default=False)
	is_league_secretary = models.BooleanField(default=False)
	is_center_manager = models.BooleanField(default=False)
	
	def __str__(self):
		return self.first_name + ' ' + self.last_name
	
	def set_center_manager(self, is_manager=False):
		self.is_center_manager = is_manager
	
class BowlerProfile(models.Model):
	HAND = (
		('R', 'Right'),
		('L', 'Left')
	)

	DESIGNATION = (
		('A', 'Adult'),
		('S', 'Senior'),
		('J', 'Junior')
	)
	
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	
	hand = models.CharField(max_length=1, choices=HAND)
	designation = models.CharField(max_length=1, choices=DESIGNATION)
	is_sanctioned = models.BooleanField(default=False, blank=False)
	last_date_sanctioned = models.DateField(default=datetime.date(1900,1,1), blank=True)
		
	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name		
		

