from django.shortcuts import render, redirect
from cart.models import *
from django.contrib import messages


def remove_coupon(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request, "Coupon Removed Successfully!")
    return redirect('cart:cart')