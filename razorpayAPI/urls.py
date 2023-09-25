from django.urls import path
from . import views

app_name = "razorpay"

urlpatterns = [
    path('payment/', views.payment, name='payment'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('success/', views.paymentsuccess, name='paymentsuccess'),
    path('failure/', views.paymentfailure, name='paymentfailure'),
]
