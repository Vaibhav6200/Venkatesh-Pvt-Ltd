from django.urls import path
from . import views

app_name = "razorpay"

urlpatterns = [
    path('payment/', views.payment, name='payment'),
]
