from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)

# Create your models here.

class cUserManager(BaseUserManager):
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


class cUser(AbstractBaseUser):
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