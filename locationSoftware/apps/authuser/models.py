from enum import unique

from apps.core.models import BaseModel
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(UserManager):
    def _create_user(self, name, email, password):
        if not email:
            raise ValueError("Votre adresse email n'est pas valide")

        email = self.normalize_email(email)
        user = self.model()
        user.name = name
        user.email = email
        user.set_password(password)
        user.save()

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_lessor", False)
        extra_fields.setdefault("is_locator", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, name, username, email=None, password=None):
        # extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_locator', True)
        # extra_fields.setdefault('is_lessor', True)
        user = self._create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(blank=False, default="", unique=True)
    name = models.CharField(max_length=50, blank=False, default="", unique=True)
    phone = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=False)
    username = models.CharField(max_length=50, blank=False, default="")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_lessor = models.BooleanField(default=False)
    is_locator = models.BooleanField(default=False)

    date_joined = models.DateField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "name"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username", "email"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split("@")[0]
