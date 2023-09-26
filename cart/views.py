from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from clickfix.models import SubServices
from .models import *
import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.urls import reverse
import requests
from django.http import HttpResponseRedirect
from razorpayAPI.models import Order, OrderItem


def getDate(day):
    current_date = datetime.now()
    start_date = current_date.replace(day=int(day))
    if start_date < current_date:
        start_date += relativedelta(months=1)

    date_range_start = current_date
    date_range_end = current_date + timedelta(days=6)

    if start_date >= date_range_start and start_date <= date_range_end:
        start_date = start_date.strftime("%Y-%m-%d")
        return start_date
    return None


# NOTE: we have to send cart object to all functions so that it could be rendered on top right cart icon
def cart(request):
    cart = None
    cart_items = []
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(session_id=request.session['nonuser'])
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
    day = data['date_slot']
    date_slot = getDate(day)
    time_slot = id=data['time_slot']

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)

    else:
        if "nonuser" in request.session:
            session_id = request.session['nonuser']
        else:
            session_id = str(uuid.uuid4())
            request.session['nonuser'] = session_id
        cart, created = Cart.objects.get_or_create(session_id=session_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, start_date=date_slot, time_slot=time_slot, sub_service=sub_service)
    cart_item.quantity += 1
    cart_item.save()
    cart.cart_cost += sub_service.sub_service_price
    cart.save()
    num_of_items = cart.num_of_items

    return JsonResponse(num_of_items, safe=False)


def get_available_dates(request):
    date_disable_map = {}
    data = json.loads(request.body)
    today = datetime.now().date()
    available_dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    for date in available_dates:
        date_disable_map[date] = False


    booked_date_slots = CartItem.objects.filter(sub_service=data['sub_service_id']).values('start_date').annotate(total_time_slots=Count('time_slot'))
    for slot in booked_date_slots:
        temp_date = slot['start_date'].strftime('%Y-%m-%d')
        total_slots = slot['total_time_slots']
        if total_slots == 4:
            date_disable_map[temp_date] = True

    return JsonResponse(date_disable_map, safe=False)


def get_available_time_slots(request):
    time_disable_map = {}
    data = json.loads(request.body)
    booked_time_slots = CartItem.objects.filter(sub_service=data['sub_service_id'], start_date=data['date_slot'])

    time_slots = ["10am-12pm", "12pm-2pm", "2pm-4pm", "4pm-7pm"]
    for slot in time_slots:
        time_disable_map['slot'] = False

    for slot in booked_time_slots:
        time_disable_map[slot.time_slot] = True

    return JsonResponse(time_disable_map, safe=False)



def billing(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')

        billing_obj = BillingDetails.objects.create( first_name = first_name , last_name = last_name , email = email , phone = phone , address_line_1 = address_line_1 , address_line_2 = address_line_2 , city = city , state = state)

        order_obj = Order(billing_details=billing_obj)
        if request.user.is_authenticated:
            user = request.user
            cart = Cart.objects.get(user=user)
            order_obj.user = user
        else:
            session_id = request.session['nonuser']
            cart = Cart.objects.get(session_id=session_id)
            order_obj.session_id = session_id
        order_obj.cart_id = cart.id
        order_obj.total_cost = cart.cart_cost
        order_obj.save()

        # Shifting our Cart Items to Order Items
        for item in cart.cartitems.all():
            order_item_obj = OrderItem()
            order_item_obj.order = order_obj
            order_item_obj.sub_service = item.sub_service
            order_item_obj.quantity = item.quantity
            order_item_obj.start_date = item.start_date
            order_item_obj.time_slot = item.time_slot
            order_item_obj.save()



        return render(request, 'razorpay/start_payment.html', {'amount': order_obj.total_cost, 'order_id': order_obj.id})



