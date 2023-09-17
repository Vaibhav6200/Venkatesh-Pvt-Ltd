from django.urls import path
from . import views

app_name = "clickfix"

urlpatterns = [
    path('', views.index, name='home'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('individual_service/', views.individual_service, name='individual_service'),
    path('checkout/', views.checkout, name='checkout'),
    path('live_tracking/', views.live_tracking, name='live_tracking'),
    path('bookings/', views.bookings, name='bookings'),
]
