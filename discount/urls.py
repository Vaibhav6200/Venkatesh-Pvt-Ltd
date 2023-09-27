from django.urls import path
from . import views

app_name = "discount"

urlpatterns = [
    path('remove_coupon/<cart_id>/', views.remove_coupon, name="remove_coupon"),
]
