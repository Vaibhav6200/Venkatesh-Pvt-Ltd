from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify



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


class Handyman(models.Model):
    class Meta:
        verbose_name_plural = 'Service Provider'
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=10, help_text="It should be 10 digit number")
    image = models.ImageField(upload_to='handyman', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
