from django.contrib import admin
from .models import *


@admin.register(Cart)
class CustomCart(admin.ModelAdmin):
    list_display = ['id', 'user', 'isPaid', 'cart_cost']
    list_display_links = ['id', 'user']
    search_fields = ['id', 'user']

@admin.register(CartItem)
class CustomCartItem(admin.ModelAdmin):
    list_display = ['id', 'sub_service', 'cart', 'quantity']
    list_display_links = ['id', 'sub_service']
    search_fields = ['id', 'sub_service', 'cart', 'quantity']
    list_filter = ['sub_service']
