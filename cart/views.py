from django.shortcuts import render
from django.http import JsonResponse
import json
from clickfix.models import SubServices
from .models import *
import uuid


# NOTE: we have to send cart object to all functions so that it could be rendered on top right cart icon
def cart(request):
    cart = None
    cart_items = []
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user, isPaid=False)
        else:
            cart = Cart.objects.get(session_id=request.session['nonuser'], isPaid=False)
        cart_items = cart.cartitems.all()
    except:
        cart = {'num_of_items': 0}

    data = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', data)


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
        num_of_items = cart.num_of_items
    else:
        if "nonuser" in request.session:
            session_id = request.session['nonuser']
        else:
            session_id = str(uuid.uuid4())
            request.session['nonuser'] = session_id

        cart, created = Cart.objects.get_or_create(session_id=session_id, isPaid=False)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, sub_service=sub_service)
        cart_item.quantity += 1
        cart_item.save()
        cart.cart_cost += sub_service.sub_service_price
        cart.save()
        num_of_items = cart.num_of_items

    return JsonResponse(num_of_items, safe=False)