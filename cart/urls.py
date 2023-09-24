from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('get_available_dates/', views.get_available_dates, name='get_available_dates'),
    path('availabile_time_slots/', views.availabile_time_slots, name='availabile_time_slots'),
]
