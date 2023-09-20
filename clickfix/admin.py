from django.contrib import admin
from .models import *


@admin.register(Profile)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff', 'is_superuser']
    list_display_links = ['id', 'username']

    fieldsets = [
        [
            ('Personal Details'),
            {'fields': ('first_name', 'last_name', 'username', 'email', 'password', 'bio', 'image', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')}
        ]
    ]



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
