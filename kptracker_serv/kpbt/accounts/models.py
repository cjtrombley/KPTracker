from django.db import models
from django.contrib.auth.models import User
from kpbt.teams.models import Team

import datetime


"""
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)
		BowlerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.userprofile.save()
	instance.bowlerprofile.save()
"""

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	first_name = models.CharField(max_length=64, blank=True)
	last_name = models.CharField(max_length=64, blank=True)
	email = models.EmailField(
		verbose_name='email address',
		max_length = 254,
		unique = False,
	)
	
	is_league_secretary = models.BooleanField(default=False)
	is_bowlingcenter_manager = models.BooleanField(default=False)
	
	def __str__(self):
		return self.first_name + ' ' + self.last_name
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
		return self.first_name + ' ' + self.last_name
