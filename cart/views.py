from django.shortcuts import render
from django.http import JsonResponse
import json
from clickfix.models import SubServices
from .models import *


def cart(request):
    return render(request, 'cart.html')


def add_to_cart(request):
    data = json.loads(request.body)
    sub_service = SubServices.objects.get(id=data['sub_service_id'])

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, isPaid=False)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, sub_service=sub_service)
        cart_item.quantity += 1
        cart_item.save()
        cart.cart_cost += sub_service.sub_service_price
        cart.save()

    return JsonResponse("Its Working", safe=False)