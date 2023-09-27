from django.contrib import admin
from .models import *


@admin.register(Cart)
class CustomCart(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_display_links = ['id', 'user']
    search_fields = ['id', 'user']

@admin.register(CartItem)
class CustomCartItem(admin.ModelAdmin):
    list_display = ['id', 'sub_service', 'cart', 'quantity', 'start_date', 'time_slot']
    list_display_links = ['id', 'sub_service']
    search_fields = ['id', 'sub_service', 'cart', 'quantity']
    list_filter = ['sub_service']

@admin.register(BillingDetails)
class CustomBillingDetails(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', "phone", 'city', 'state']
    list_display_links = ['id', 'first_name', 'last_name']
    search_fields = ['id', 'first_name', 'last_name', 'email', "phone", 'city', 'state']
