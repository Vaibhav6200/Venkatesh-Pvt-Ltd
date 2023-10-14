from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models import Q


class Services(models.Model):
    class Meta:
        verbose_name_plural = 'Services'

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    price = models.CharField(max_length=10)
    card_image = models.ImageField(upload_to='service_cards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # New Fields
    enable_contact = models.BooleanField(default=False)
    is_contact_rent = models.BooleanField(default=True, help_text="Tick if you want to show Contact Form for Rent")

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
    sub_service_price = models.FloatField(default=0, null=True, blank=True)
    price_details = RichTextField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)
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
    is_answered = models.BooleanField(default=False, help_text="Tick it if you have replied to the customers query")
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


class deals_and_discount(models.Model):
    class Meta:
        verbose_name_plural = 'Deals & Discount'
    image = models.ImageField(upload_to='deals_and_discount_banners')
    heading = models.CharField(max_length=255, null=True, blank=True)
    percent_off = models.CharField(max_length=3, null=True, blank=True, help_text="write here only percentage i.e. (10, 20, 30 etc)")
    description = models.CharField(max_length=255, null=True, blank=True, help_text="it can be at max 256 of characters long")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class BookCall(models.Model):
    class Meta:
        verbose_name_plural = "Calls Booked"
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=13)
    quantity = models.CharField(max_length=3, null=True, blank=True)
    duration = models.CharField(max_length=3, null=True, blank=True)
    description = models.TextField()
    is_amc_call = models.BooleanField(default=False)
    is_rent_call = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)