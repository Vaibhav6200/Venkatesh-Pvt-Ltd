from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from clickfix.models import *


class Cart(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    isPaid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    # TAX_AMOUNT = 19.25

    # def price_ttc(self):
    #     return self.price_ht * (1 + TAX_AMOUNT/100.0)
