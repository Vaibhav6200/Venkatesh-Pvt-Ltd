from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from clickfix.models import *
from accounts.models import *
from discount.models import *


class Cart(models.Model):
    class Meta:
        verbose_name_plural = 'Cart'

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_cart_total(self):
        cart_items = self.cartitems.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.sub_service.sub_service_price)

        if self.coupon:
            if self.coupon.minimum_price < sum(price):
                return sum(price) - self.coupon.discount_price
        return sum(price)

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return "Guest"

    @property
    def num_of_items(self):
        cartitems = self.cartitems.all()
        quantity =  sum([item.quantity for item in cartitems])
        return quantity


class CartItem(models.Model):
    class Meta:
        verbose_name_plural = 'Cart Items'

    TIME_SLOTS = (
        ("10am-12pm", "10am-12pm"),
        ("12pm-2pm", "12pm-2pm"),
        ("2pm-4pm", "2pm-4pm"),
        ("4pm-7pm", "4pm-7pm"),
    )
    sub_service = models.ForeignKey(SubServices, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems")
    quantity = models.IntegerField(default=0)
    start_date = models.DateField(null=True)
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS, default=1)

    def __str__(self):
        return self.sub_service.sub_service_name

    @property
    def price(self):
        new_price = self.sub_service.sub_service_price * self.quantity
        return new_price



class BillingDetails(models.Model):
    class Meta:
        verbose_name_plural = 'Billing Details'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=15)
    address_line_1 = models.TextField()
    address_line_2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"Billing Id - {self.id}"