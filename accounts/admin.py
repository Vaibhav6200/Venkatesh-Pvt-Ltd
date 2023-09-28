from django.contrib import admin
from .models import *


@admin.register(Profile)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff', 'is_superuser']
    list_display_links = ['id', 'username']

    fieldsets = [
        [
            ('Personal Details'),
            {'fields': ('full_name', 'email', 'phone', 'dob', 'image', 'bio', 'billing_address', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')}
        ]
    ]