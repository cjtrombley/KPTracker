from django.db import models
from django.contrib.auth.models import User
from kpbt.teams.models import Team
from django.dispatch import receiver
from django.db.models.signals import post_save
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
	
	is_league_secretary = models.BooleanField(default=False)
	is_center_manager = models.BooleanField(default=False)
	
	def __str__(self):
		return self.first_name + ' ' + self.last_name
		
	
	def set_is_center_manager(self):
		return
	
	
	"""
	USER_TYPE_CHOICES = (
		(1, 'bowler'),
		(2, 'league_secretary'),
		(3, 'bowlingcenter_manager'),
		(4, 'admin'),
	)
	
	
	user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
	
	is_default = models.BooleanField(default=True, blank=False)
	
	def void_default(self):
		self.is_default = False
	"""

	
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
	team = models.ForeignKey('Team', null=True, on_delete=models.SET_NULL,
		related_name='teams', verbose_name='teams')
	
	date_of_birth = models.DateField(default=datetime.date(1900,1,1), blank=True)
	hand = models.CharField(max_length=1, choices=HAND)
	designation = models.CharField(max_length=1, choices=DESIGNATION)
	is_sanctioned = models.BooleanField(default=False, blank=False)
	last_date_sanctioned = models.DateField(default=datetime.date(1900,1,1), blank=True)
		
	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name



@receiver(post_save, sender=UserProfile)
def perms_update(sender, instance, **kwargs):
	if instance.is_center_manager:
		user = instance.user
		user.user_permissions.add('kpbt.add_bowlingcenter')