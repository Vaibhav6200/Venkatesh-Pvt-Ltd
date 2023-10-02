from django.contrib import admin
from .models import *


@admin.register(Services)
class CustomServices(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'slug']
    list_display_links = ['id', 'name']
    exclude = ('slug',)


@admin.register(SubServices)
class CustomSubServices(admin.ModelAdmin):
    list_display = ['id', 'sub_service_name', 'service', 'sub_service_price']
    list_display_links = ['id', 'service', 'sub_service_name']
    search_fields = ['sub_service_name', 'service']
    list_filter = ['service']


@admin.register(Testimonials)
class CustomTestimonials(admin.ModelAdmin):
    list_display = ['id', 'title', 'state']
    list_display_links = ['id', 'title']


@admin.register(Handyman)
class CustomHandyman(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'mobile_number']
    list_display_links = ['id', 'full_name']


@admin.register(Contact)
class CustomContact(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'mobile_number', 'service_needed', 'is_answered']
    list_display_links = ['id', 'full_name']
    list_filter = ['is_answered']


@admin.register(deals_and_discount)
class CustomDeals(admin.ModelAdmin):
    list_display = ['id', 'heading', 'percent_off']
    list_display_links = ['id', 'heading', 'percent_off']
    list_filter = ['percent_off']
    search_fields = ['heading', 'percent_off']

