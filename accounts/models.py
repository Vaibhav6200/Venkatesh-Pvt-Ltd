from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import password_validation


class Profile(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True, help_text="It should be a 10 digit number only")
    dob = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username
