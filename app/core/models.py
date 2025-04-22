"""
# app/core/models.py
Models for Django application
"""

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    """Manager for User model."""

    def create_user(self, email, password=None, **extra_field):
        """Create, save and return a new user."""
        # Self.model call `class: User` and inputs the attr
        if not email:
            raise ValueError("Email was not provided.")
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create's a User a superuser"""
        user = self.create_user(email, password)
        # Adding superuser functionality
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Creates User in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Create the user
    objects = UserManager()

    REQUIRED_FIELDS = []

    # Overriding in system to use `email` instead of
    # username when Authenticating.
    USERNAME_FIELD = "email"


class Flavour(models.Model):
    """Create Flavour DB in the system."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField("Tag")

    def __str__(self):
        """Returns strings representation of the class."""
        return self.title


class Tag(models.Model):
    """Create Tag DB Schema."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        """Returns string representation of Tag."""
        return self.name
