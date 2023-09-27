from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import password_validation


class Profile(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    bio = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username
