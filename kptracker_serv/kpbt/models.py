from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)

# Create your models here.

class cUserManager(BaseUserManager):
	def create_user(self, identifier, email, password=None):
		"""
		Creates and saves a user with given username, email, and password.
		"""
		if not identifier:
			raise ValueError('Users must have a User Name.')
		
		if not email:
			raise ValueError('Users must have a valid email address.')
			
		user = self.model(
			identifier = identifier,
			email = self.normalize_email(email),
		)
		
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_superuser(self, identifier, email, password):
		"""
		Creates and saves a superuser.
		"""
		user = self.create_user(
			identifier=identifier,
			email=email,
			password=password
		)
		user.is_admin = True
		user.save(using=self._db)
		return user


class cUser(AbstractBaseUser):
	identifier = models.CharField(max_length=255, unique=True)
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	
	objects = cUserManager()
	
	REQUIRED_FIELDS = ['email']
	USERNAME_FIELD = 'identifier'
	
	def __str__(self):
		return self.identifier + ", " + self.email
	
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