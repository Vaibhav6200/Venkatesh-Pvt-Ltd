from django.contrib import admin
from .models import *


@admin.register(Order)
class CustomOrder(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_id', 'total_cost', 'payment_status', 'booking_status', 'tracking_status', 'service_provider', 'created_at']
    list_display_links = ['id', 'user', 'session_id']
    search_fields = ['id', 'user', 'session_id', 'payment_status', 'created_at']
    list_filter = ['payment_status']


@admin.register(OrderItem)
class CustomOrderItem(admin.ModelAdmin):
    list_display = ['id', 'order', 'sub_service', 'quantity', 'start_date', 'time_slot', 'created_at']
    list_display_links = ['id', 'order', 'sub_service']
    search_fields = ['id', 'order', 'sub_service', 'start_date', 'time_slot', 'created_at']
    list_filter = ['time_slot']
