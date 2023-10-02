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

    path('order_sms/', views.Order_SMS, name='order_sms'),
    path('order_email/', views.Order_Email, name='order_email'),
]
