from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('get_available_dates/', views.get_available_dates, name='get_available_dates'),
    path('get_available_time_slots/', views.get_available_time_slots, name='get_available_time_slots'),
    path('billing/', views.billing, name='billing'),
    path('remove_cart_item/', views.remove_cart_item, name='remove_cart_item'),
]
