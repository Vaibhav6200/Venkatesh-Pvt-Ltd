from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import password_validation
from ckeditor.fields import RichTextField
from django.utils.text import slugify



class Profile(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(validators=[password_validation.validate_password], max_length=128)
    bio = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username



class Services(models.Model):
    class Meta:
        verbose_name_plural = 'Our Services'

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    price = models.CharField(max_length=10)
    card_image = models.ImageField(upload_to='service_cards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubServices(models.Model):
    class Meta:
        verbose_name_plural = 'Sub Services'
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    sub_service_name = models.CharField(max_length=255)
    sub_service_card_image = models.ImageField(upload_to='service_cards', help_text='Small card image on left')
    sub_service_main_image = models.ImageField(upload_to='service_cards', help_text='Big card image on Right, which we scroll')
    sub_service_price = models.FloatField(default=0)
    price_details = RichTextField(blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sub_service_name


class Testimonials(models.Model):
    class Meta:
        verbose_name_plural = 'Testimonials'

    image = models.ImageField(upload_to='testimonial_images')
    title = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Contact(models.Model):
    class Meta:
        verbose_name_plural = 'Customer Queries'

    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=150)
    mobile_number = models.CharField(max_length=20)
    service_needed = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

