from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from clickfix.models import *


class Cart(models.Model):
    class Meta:
        verbose_name_plural = 'Cart'
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cart_cost = models.FloatField(default=0.0)
    isPaid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    class Meta:
        verbose_name_plural = 'Cart Items'
    sub_service = models.ForeignKey(SubServices, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    # TAX_AMOUNT = 19.25

    # def price_ttc(self):
    #     return self.price_ht * (1 + TAX_AMOUNT/100.0)
