from django.db import models
from django.contrib.auth.models import User, AbstractUser, UserManager
import datetime


# definitions relating to signals
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group

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


class Team(models.Model):
	
	league = models.ForeignKey('League', on_delete=models.CASCADE, 
		related_name='teams', verbose_name=('league'))
	
	number = models.PositiveSmallIntegerField(default=id)
	name = models.CharField(max_length=32, default="")
	total_pinfall = models.PositiveSmallIntegerField()
	total_handicap_pins = models.PositiveIntegerField()
	total_scratch_pins = models.PositiveIntegerField()
	team_points = models.PositiveSmallIntegerField()
	
	
class BowlingCenter(models.Model):
	center_name = models.CharField(max_length = 64)
	num_lanes = models.IntegerField(default=0)
	
	manager= models.ForeignKey(User, on_delete=models.CASCADE, null=True,
		verbose_name=('manager'))
	
	def set_manager(self, user):
		self.manager = user

class League(models.Model):
	DESIGNATION = (
		('A', 'Adult'),
		('S', 'Senior'),
		('J', 'Junior')
	)
	
	GENDER = (
		('M', 'Men'),
		('W', 'Women'),
		('X', 'Mixed'),
	)

	bowling_center = models.ForeignKey('BowlingCenter', on_delete=models.CASCADE,
		related_name='bowling_center', verbose_name=('bowling center'))
	bowlers = models.ManyToManyField('BowlerProfile', through='LeagueBowler')
	
	name = models.CharField(max_length=32, default=id)
	num_teams = models.PositiveSmallIntegerField()
	designation = models.CharField(max_length=1, choices=DESIGNATION)
	gender = models.CharField(max_length=1, choices=GENDER)
	min_roster_size = models.PositiveSmallIntegerField()
	max_roster_size = models.PositiveSmallIntegerField()
	is_handicap = models.BooleanField(default=False)
	handicap_scratch = models.PositiveSmallIntegerField()
	allow_substitutes = models.BooleanField(default=False)
	bye_team_point_threshold = models.PositiveSmallIntegerField()
	absentee_score = models.PositiveSmallIntegerField()
	game_point_value = models.PositiveSmallIntegerField()
	series_point_value = models.PositiveSmallIntegerField()
	
	
class LeagueBowler(models.Model):
	bowler = models.ForeignKey('BowlerProfile', on_delete=models.CASCADE)
	league = models.ForeignKey('League', on_delete=models.CASCADE)
	
	league_average = models.PositiveSmallIntegerField()
	league_high_game = models.PositiveSmallIntegerField()
	league_high_series = models.PositiveSmallIntegerField()
	league_total_scratch = models.PositiveSmallIntegerField()
	league_total_handicap = models.PositiveSmallIntegerField()


class LeagueGame(models.Model):
	bowler = models.ForeignKey('BowlerProfile', on_delete=models.SET_NULL, null=True)
	team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True)
	league = models.ForeignKey('League', on_delete=models.SET_NULL, null=True)

	
	series_date = models.DateField()
	applied_average = models.PositiveSmallIntegerField()
	game_one_score = models.PositiveSmallIntegerField()
	game_two_score = models.PositiveSmallIntegerField()
	gamee_three_score = models.PositiveSmallIntegerField()
	
	
class LeagueSchedule(models.Model):
	league = models.OneToOneField('LeagueSchedule', on_delete=models.SET_NULL, null=True)
	
	date_started = models.DateField()
	date_ending = models.DateField()
	num_weeks = models.PositiveSmallIntegerField()
	start_time = models.TimeField()


class WeeklyPairing(models.Model):
	league = models.ForeignKey('League', on_delete=models.SET_NULL, null=True,
		related_name='league', verbose_name=('league'))
		
