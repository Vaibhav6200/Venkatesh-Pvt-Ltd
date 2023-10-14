from django.urls import path
from . import views

app_name = "clickfix"

urlpatterns = [
    path('', views.home, name='home'),
    path('service/<slug:service_name>/', views.individual_service, name='individual_service'),
    path('checkout/', views.checkout, name='checkout'),
    path('live_tracking/', views.live_tracking, name='live_tracking'),
    path('bookings/', views.bookings, name='bookings'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search_view, name='search'),
    path('book_rent_call/', views.book_rent_call, name='book_rent_call'),
    path('book_amc_call/', views.book_amc_call, name='book_amc_call'),
]
