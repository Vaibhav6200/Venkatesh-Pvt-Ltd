from django.contrib import admin
from .models import *


@admin.register(Coupon)
class CustomCoupon(admin.ModelAdmin):
    list_display = ['id', 'coupon_code', 'is_expired', 'discount_price', 'minimum_price']
    list_display_links = ['id', 'coupon_code']
    search_fields = ['id', 'coupon_code']
    list_filter = ['is_expired']


