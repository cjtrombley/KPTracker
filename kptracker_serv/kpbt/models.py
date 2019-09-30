from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.contrib.auth.models import PermissionsMixin

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import datetime

# Create your models here.

# Manager class for custom user
class cUserManager(BaseUserManager):
	use_in_migrations=True

	def create_user(self, username, email, first_name, last_name, password=None):
		"""
		Creates and saves a user with given username, email, and password.
		"""
		if not username:
			raise ValueError('Users must have a User Name.')
		
		if not email:
			raise ValueError('Users must have a valid email address.')
			
		user = self.model(
			username = username,
			email = self.normalize_email(email),
			first_name = first_name,
			last_name = last_name
		)
		
		user.set_password(password)
		user.save(using=self._db)
		
		
		@receiver(post_save, sender=settings.AUTH_USER_MODEL)
		def create_auth_token(sender, instance=None, created=False, **kwargs):
			if created:
				Token.objects.create(user=instance)

		
		return user
	
	def create_superuser(self, username, first_name, last_name, email, password):
		"""
		Creates and saves a superuser.
		"""
		user = self.create_user(
			username = username,
			email = email,
			password = password,
			first_name = first_name,
			last_name = last_name
		)
		
		user.is_admin = True
		user.save(using=self._db)
		return user

# Defines a custom user class
class cUser(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=32, unique=True)
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)
	first_name = models.CharField(max_length=32, default="")
	last_name = models.CharField(max_length=32, default = "")
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	
	objects = cUserManager()
	
	REQUIRED_FIELDS = ['first_name', 'last_name','email']
	USERNAME_FIELD = 'username'
	
	def __str__(self):
		return self.username + ", " + self.email
	
	
	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		return True
	
	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app 'app_label'?"
		return True
	
	@property
	def is_staff(self):
		"Is the user a member of the staff?"
		return self.is_admin

# Defines the Bowler class
class Bowler(models.Model):
	HAND = (
		('R', 'Right'),
		('L', 'Left'),
	)
	
	GENDER = (
		('M', 'Male'), 
		('F', 'Female'),
		('B', 'Boy'),
		('G', 'Girl'),
	)
	
	DESIGNATION = (
		('A', 'Adult'),
		('S', 'Senior'),
		('J', 'Junior'),
	)
	
	cUser = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	
	date_of_birth = models.DateField(default=datetime.date(1900,1,1))
	designation = models.CharField(max_length=1, choices=DESIGNATION)
	is_sanctioned = models.BooleanField(default=False)
	hand = models.CharField(max_length=1, choices=HAND)
	team = models.ForeignKey(
		'Team',
		null=True,
		on_delete=models.SET_NULL)
	
	def __str__(self):
		return self.first_name + " " + self.last_name
		
	@receiver(post_save, sender=cUser)
	def create_user_bowler(sender, instance, created, **kwargs):
		if created:
			Bowler.objects.create(settings.AUTH_USER_MODEL.instance)
	
	@receiver(post_save, sender=cUser)
	def save_user_bowler(sender, instance, **kwargs):
		instance.profile.save()
		
class Team(models.Model):
	team_number = models.IntegerField(default=id)
	team_name = models.CharField(max_length=32, default="")
