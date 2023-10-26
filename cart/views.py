from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from clickfix.models import SubServices
from .models import *
import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from razorpayAPI.models import Order, OrderItem
from discount.models import Coupon
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail


def getDate(date):
    current_date = datetime.now().date()
    start_date = datetime.strptime(date, '%Y-%m-%d').date()

    if start_date < current_date:
        start_date += relativedelta(months=1)

    date_range_start = current_date
    date_range_end = current_date + timedelta(days=6)

    if start_date >= date_range_start and start_date <= date_range_end:
        start_date = start_date.strftime("%Y-%m-%d")
        return start_date
    return None


def get_cart(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(session_id=request.session['nonuser'])
    except:
        cart = None
    return cart


# NOTE: we have to send cart object to all functions so that it could be rendered on top right cart icon
def cart(request):
    cart = get_cart(request)
    cart_items = None
    if cart:
        cart_items = cart.cartitems.all()

    if request.method == "POST":
        coupon_code = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__iexact=coupon_code)[0]

        if cart.coupon:
            messages.warning(request, "Coupon Already Exists.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart.get_cart_total() < coupon_obj.minimum_price:
            messages.warning(request, f"Amount Should be greater than {coupon_obj.minimum_price}.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj.is_expired:
            messages.danger(request, "Coupon Expired")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        cart.coupon = coupon_obj
        cart.save()
        messages.success(request, "Coupon Applied!")

    data = {}
    data['cart'] = cart
    data['cart_items'] = cart_items
    data['coupons'] = Coupon.objects.filter(is_expired=False)
    if cart:
        data['cart_total'] = cart.get_cart_total()

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
    num_of_items = cart.num_of_items

    return JsonResponse(num_of_items, safe=False)


def get_available_dates(request):
    date_disable_map = {}
    data = json.loads(request.body)
    today = datetime.now().date()
    available_dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    for date in available_dates:
        date_disable_map[date] = False


    booked_date_slots = OrderItem.objects.filter(sub_service=data['sub_service_id']).values('start_date').annotate(total_time_slots=Count('time_slot'))
    for slot in booked_date_slots:
        temp_date = slot['start_date'].strftime('%Y-%m-%d')
        total_slots = slot['total_time_slots']
        if total_slots == 4:
            date_disable_map[temp_date] = True

    return JsonResponse(date_disable_map, safe=False)


def get_available_time_slots(request):
    time_disable_map = {}
    data = json.loads(request.body)
    booked_time_slots = OrderItem.objects.filter(sub_service=data['sub_service_id'], start_date=data['date_slot'])

    time_slots = ["10am-12pm", "12pm-2pm", "2pm-4pm", "4pm-7pm"]
    for slot in time_slots:
        time_disable_map['slot'] = False

    for slot in booked_time_slots:
        time_disable_map[slot.time_slot] = True

    return JsonResponse(time_disable_map, safe=False)


def send_customer_mail(customer_email, customer_name, service_type):
    if len(service_type) == 1:
        service_type = service_type[0]
    else:
        service_type = "\n" + "\n".join([f"{i + 1}. {service}" for i, service in enumerate(service_type)])

    subject = "Booking Confirmation - Thank You for Choosing ClickFix!"
    body = f"Dear {customer_name},\nThank you for choosing ClickFix! Your booking is confirmed\nService Type: {service_type} \n\nIf you have any questions or need assistance, please reach out to our customer support team at support@clickfix.co.in or +91 8910434505. \n\nWarm regards, \nClickFix Customer Services"

    send_mail(
        subject=subject,
        message=body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[customer_email],
        fail_silently=True,
    )


@login_required()
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
        payment_method = request.POST.get('payment_method')

        billing_obj = BillingDetails.objects.create( first_name = first_name , last_name = last_name , email = email , phone = phone , address_line_1 = address_line_1 , address_line_2 = address_line_2 , city = city , state = state)

# ***************************************************************************************************************************************************************************************************
        current_user = None
        cart = None
        if request.user.is_authenticated:
            user = request.user
            cart = Cart.objects.get(user=user)
            current_user = user
        else:
            session_id = request.session['nonuser']
            cart = Cart.objects.get(session_id=session_id)
            current_user = session_id

        order_objects_list = []
        booked_services_names = []
        total_order_amount = cart.get_cart_total()
        for item in cart.cartitems.all():
            service_name = item.sub_service.sub_service_name
            booked_services_names.append(service_name)

            order_obj = Order(billing_details=billing_obj)
            if request.user.is_authenticated:
                order_obj.user = current_user
            else:
                order_obj.session_id = current_user
            order_obj.cart_id = cart.id
            order_obj.total_cost = cart.get_cart_total()
            order_obj.save()

            order_item_obj = OrderItem()
            order_item_obj.order = order_obj
            order_item_obj.sub_service = item.sub_service
            order_item_obj.quantity = item.quantity
            order_item_obj.start_date = item.start_date
            order_item_obj.time_slot = item.time_slot
            order_item_obj.save()

            if payment_method == "cash_on_delivery":
                order_obj.payment_mode = "cash_on_delivery"
                order_obj.save()
            order_objects_list.append(order_obj)


        if payment_method == "cash_on_delivery":
            Cart.objects.get(id=cart.id).delete()       # deleting our cart cause our order placed successfully
            send_customer_mail(email, first_name, booked_services_names)
            messages.success(request, "Order Placed Successfully")
            return redirect('clickfix:bookings')

        send_customer_mail(email, first_name, booked_services_names)
        return render(request, 'razorpay/start_payment.html', {'total_amount': total_order_amount, 'order_objects_list': order_objects_list})

# ***************************************************************************************************************************************************************************************************


        # order_obj = Order(billing_details=billing_obj)
        # if request.user.is_authenticated:
        #     user = request.user
        #     cart = Cart.objects.get(user=user)
        #     order_obj.user = user
        # else:
        #     session_id = request.session['nonuser']
        #     cart = Cart.objects.get(session_id=session_id)
        #     order_obj.session_id = session_id

        # order_obj.cart_id = cart.id
        # order_obj.total_cost = cart.get_cart_total()
        # order_obj.save()

        # # Shifting our Cart Items to Order Items
        # for item in cart.cartitems.all():
        #     order_item_obj = OrderItem()
        #     order_item_obj.order = order_obj
        #     order_item_obj.sub_service = item.sub_service
        #     order_item_obj.quantity = item.quantity
        #     order_item_obj.start_date = item.start_date
        #     order_item_obj.time_slot = item.time_slot
        #     order_item_obj.save()

        # if payment_method == "cash_on_delivery":
        #     order_obj.payment_mode = "cash_on_delivery"
        #     # Since Order Placed Successfully So remove all items from our cart
        #     cart_id = order_obj.cart_id
        #     Cart.objects.get(id=cart_id).delete()
        #     order_obj.save()
        #     return redirect('clickfix:bookings')
        # return render(request, 'razorpay/start_payment.html', {'amount': order_obj.total_cost, 'order_id': order_obj.id})


def remove_cart_item(request):
    data = {}
    if request.method == "POST":
        data = json.loads(request.body)
        CartItem.objects.get(id=data['cart_item_id']).delete()
        cart = Cart.objects.get(id=data['cart_id'])
        data['cart_cost'] = cart.get_cart_total()
        data['remove_coupon'] = False   # this is done to remove coupon from cart when its price is not proper
        if cart.coupon and int(cart.coupon.minimum_price) > cart.get_cart_total():
            cart.coupon = None
            cart.save()
            data['remove_coupon'] = True
        data['num_of_items'] = cart.num_of_items

    return JsonResponse(data, safe=False)
